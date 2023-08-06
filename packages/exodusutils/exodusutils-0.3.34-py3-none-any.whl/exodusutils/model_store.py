import base64
import pickle
import warnings
from typing import Any, Dict, List, Tuple
from io import BytesIO
from minio import Minio
from exodusutils.constants import PREDICTION_COLNAME
from exodusutils.configuration import MongoInstance, identify
from exodusutils.exceptions import ExodusNotFound

from exodusutils.schemas.model import SingleModel
from pydantic.main import BaseModel
from pymongo.collection import Collection

warnings.simplefilter("ignore", FutureWarning)

MINIO_BUCKET_NAME = "models"

def save_stuff_to_minio(uri: str, content: bytes, minio: Minio) -> str:
    """
    Stores stuff to Minio.

    Parameters
    ----------
    stuff : Any
        Whatever you want to store.

    Returns
    -------
    str
        The stringified id of the stuff you just stored.
    """
    # FIXME Be extra careful when storing sklearn stuff: there is virtually no backwards compatibility if you pickle
    # scikit-learn pipelines!
    # Reference: https://scikit-learn.org/stable/modules/model_persistence.html#security-maintainability-limitations
    # Either use ONNX, PMML (this requires Java), or try to dump your model to a bytearray!
    # content = pickle.dumps(stuff)
    minio.put_object(MINIO_BUCKET_NAME, uri, BytesIO(content), len(content))

def load_stuff_from_minio(uri: str, minio: Minio) -> bytes:
    """
    Loads stuff back from Minio.

    Parameters
    ----------
    stuff_id : str
        The stringified id of the stuff you just stored.

    Returns
    -------
    Any
        Whatever you just stored during training.
    """
    content = minio.get_object(MINIO_BUCKET_NAME, uri)
    if not content:
        raise RuntimeError(f"Item with id = {uri} not found")
    return content.read()

# FIXME there are probably better ways to do this!
def dump_to_base64(stuff: Any) -> bytes:
    """
    Dumps the thing to pickle format, then encodes the result with `b64encode`.
    """
    return base64.b64encode(pickle.dumps(stuff))

class ModelStore(BaseModel):
    """
    We define connector here.
    """
    name: str
    minio: Minio
    mongo: MongoInstance
    db_collection: Collection

    class Config:
        arbitrary_types_allowed = True

    def pickle_and_save(
        self,
        model_id: str,
        model_info: SingleModel,
        model: Any = None,
        additions_stuff: Dict[str, Any] = {},
    ):
        return self.save(model_id=model_id,
                         model_info=model_info,
                         model_bytes=pickle.dumps(model),
                         additions_stuff={key: pickle.dumps(additions_stuff[key]) for key in additions_stuff },
                         )

    def save(
        self,
        model_id: str,
        model_info: SingleModel,
        model_bytes: bytes = None,
        additions_stuff: Dict[str, bytes] = {},
    ) -> str:
        """
        Creates a `ModelInfo` instance and saves it. Will store the `model` and `encoders` into `minio`.
        """
        # Some algos. number of models base on timegroup (ex. arima, theta)
        if model_bytes:
            save_stuff_to_minio(
                f"{model_info.experiment}/{self.name}_{model_id}", model_bytes, self.minio
            )
        # Also save other stuff
        for stuff_id in additions_stuff:
            save_stuff_to_minio(
                f"{model_info.experiment}/{self.name}_{model_info.options.get(stuff_id)}",
                additions_stuff[stuff_id],
                self.minio,
            )

        doc = model_info.dict(by_alias=True)
        doc["_id"] = identify(model_id=model_id).get("_id")
        return str(self.db_collection.insert_one(doc).inserted_id)
    
    def load_and_unpickle(
        self, model_id: str
    ) -> Tuple[SingleModel, bytes, Dict[str, bytes]]:
        meta, model_bytes, stuff = self.load(self, model_id=model_id)
        return meta, pickle.loads(model_bytes), {key: stuff[key] for key in stuff}

    def load(
        self, model_id: str
    ) -> Tuple[SingleModel, bytes, Dict[str, bytes]]:
        """
        Loads `SingleModel, Model, training_df, label_encoders` from MongoDB and Minio.

        MongoDB handles decryption automatically, so no extra step is required here.
        """
        obj = self.db_collection.find_one(filter=identify(model_id))
        if not obj:
            raise ExodusNotFound(f"No model found with id = {model_id}")
        model_info = SingleModel.parse_obj(obj)

        minio_path_prefix = f"{model_info.experiment}/{self.name}_"
        model_bytes: Any = load_stuff_from_minio(minio_path_prefix + model_id, self.minio)

        # load other stuff from model_info.options
        addition_stuff = {}
        for id in model_info.options:
            addition_stuff[id] = load_stuff_from_minio(
                minio_path_prefix + model_info.options.get(id), self.minio
            )
        return (model_info, model_bytes, addition_stuff)

    def to_prediction_header(
        self, has_target: bool, keep_columns: List[str]
    ) -> List[str]:
        """
        Returns the appropriate header for the predicted results.

        Parameters
        ----------
        has_target : bool
            Whether the target column exists in the prediction's input dataframe.
        keep_columns : List[str]
            A list of column names that the user wants to preserve in the response.

        Returns
        -------
        List[str]
            The column names of the response dataframe.
        """
        return (
            [self.date_column_name]
            + self.time_groups
            + [PREDICTION_COLNAME]
            + ([self.target.name] if has_target else [])
            + keep_columns
        )

    def to_downloadable(self) -> Dict[str, Any]:
        """
        Convert the `ModelInfo` instance to a downloadable dictionary.

        The actual `LGBMRegressor` models are going to be in pickled form.

        Parameters
        ----------
        minio : Minio
            The `Minio` instance that contains the `LGBMRegressor`s.

        Returns
        -------
        Dict[str, Any]
            This `ModelInfo` as a donwloadable dictionary.
        """
        doc = self.dict()

        doc["model"] = str(self.model)
        doc["training_df"] = str(self.training_df)
        doc["label_encoders"] = str(self.label_encoders)

        return doc

    @classmethod
    def delete(cls, model_id: str, collection: Collection, minio: Minio) -> None:
        """
        Deletes the `ModelInfo` and the underlying `ThetaForecaster` models associated with the
        given `model_id`.

        Parameters
        ----------
        model_id : str
            The stringified `ObjectId` for the target `ModelInfo`.
        collection : Collection
            The `Collection` containing the `ModelInfo`.
        minio : Minio
            The `Minio` instance containing the `ThetaForecaster` models.
        """
        model_info = cls.load(model_id, collection, minio)
        minio.remove_object(MINIO_BUCKET_NAME, model_info.model_id)
        minio.remove_object(MINIO_BUCKET_NAME, model_info.training_df)
        minio.remove_object(MINIO_BUCKET_NAME, model_info.label_encoders)
        collection.delete_one(identify(model_id))
