from enum import Enum


class BaseML3Enum(str, Enum):
    """
    Base class for all enums in the ML3 Platform SDK
    """

    def __str__(self):
        return self.value


class TaskType(BaseML3Enum):
    """
    **Fields:**

        - REGRESSION
        - CLASSIFICATION_BINARY
        - CLASSIFICATION_MULTICLASS
        - CLASSIFICATION_MULTILABEL
        - RAG
    """

    REGRESSION = "regression"
    CLASSIFICATION_BINARY = "classification_binary"
    CLASSIFICATION_MULTICLASS = "classification_multiclass"
    CLASSIFICATION_MULTILABEL = "classification_multilabel"
    RAG = "rag"
    OBJECT_DETECTION = "object_detection"


class MonitoringStatus(BaseML3Enum):
    """
    **Fields:**

        - OK
        - WARNING
        - DRIFT
    """

    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"


class KPIStatus(BaseML3Enum):
    """
    **Fields:**

        - NOT_INITIALIZED
        - OK
        - WARNING
        - DRIFT
    """

    NOT_INITIALIZED = "not_initialized"
    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"


class DataStructure(BaseML3Enum):
    """
    Represents the typology of the data to send

    **Fields:**

        - TABULAR
        - IMAGE
        - TEXT
        - EMBEDDING
    """

    TABULAR = "tabular"
    IMAGE = "image"
    TEXT = "text"
    EMBEDDING = "embedding"


class StoringDataType(BaseML3Enum):
    """
    **Fields:**

        - HISTORICAL
        - REFERENCE
        - PRODUCTION
    """

    HISTORICAL = "historical"
    PRODUCTION = "production"
    TASK_TARGET = "task_target"
    KPI = "kpi"


class FileType(BaseML3Enum):
    """
    **Fields:**

        - CSV
        - JSON
    """

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    PNG = "png"
    JPG = "jpg"
    NPY = "npy"


class FolderType(BaseML3Enum):
    """
    Type of folder

    **Fields**

        - UNCOMPRESSED
        - TAR
        - ZIP
    """

    UNCOMPRESSED = "uncompressed"
    TAR = "tar"
    ZIP = "zip"


class JobStatus(BaseML3Enum):
    """
    **Fields:**

        - IDLE
        - STARTING
        - RUNNING
        - COMPLETED
        - ERROR
    """

    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    ROLLBACK_COMPLETE = "rollback_complete"


class UserCompanyRole(BaseML3Enum):
    """
    **Fields:**

        - COMPANY_OWNER
        - COMPANY_ADMIN
        - COMPANY_USER
        - COMPANY_NONE
    """

    COMPANY_OWNER = "COMPANY_OWNER"
    COMPANY_ADMIN = "COMPANY_ADMIN"
    COMPANY_USER = "COMPANY_USER"
    COMPANY_NONE = "COMPANY_NONE"


class UserProjectRole(BaseML3Enum):
    """
    **Fields:**

        - PROJECT_ADMIN
        - PROJECT_USER
        - PROJECT_VIEW
    """

    PROJECT_ADMIN = "PROJECT_ADMIN"
    PROJECT_USER = "PROJECT_USER"
    PROJECT_VIEW = "PROJECT_VIEW"


class DetectionEventSeverity(BaseML3Enum):
    """
    **Fields:**

        - LOW
        - MEDIUM
        - HIGH
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class DetectionEventType(BaseML3Enum):
    """
    **Fields:**

        - DRIFT
    """

    WARNING_OFF = "warning_off"
    WARNING_ON = "warning_on"
    DRIFT_ON = "drift_on"
    DRIFT_OFF = "drift_off"


class MonitoringTarget(BaseML3Enum):
    """
    **Fields:**

        - ERROR
        - INPUT
        - CONCEPT
        - PREDICTION
        - USER_INPUT
        - USER_INPUT_RETRIEVED_CONTEXT
        - RETRIEVED_CONTEXT
        - USER_INPUT_MODEL_OUTPUT
        - MODEL_OUTPUT_RETRIEVED_CONTEXT
    """

    ERROR = "error"
    INPUT = "input"
    CONCEPT = "concept"
    PREDICTION = "prediction"
    INPUT_PREDICTION = "input_prediction"
    USER_INPUT = "user_input"
    RETRIEVED_CONTEXT = "retrieved_context"
    USER_INPUT_RETRIEVED_CONTEXT = "user_input_retrieved_context"
    USER_INPUT_MODEL_OUTPUT = "user_input_model_output"
    MODEL_OUTPUT_RETRIEVED_CONTEXT = "model_output_retrieved_context"


class MonitoringMetric(BaseML3Enum):
    """
    **Fields:**

        - FEATURE
        - TEXT_TOXICITY
        - TEXT_EMOTION
        - TEXT_SENTIMENT
        - MODEL_PERPLEXITY

    """

    FEATURE = "feature"
    TEXT_TOXICITY = "text_toxicity"
    TEXT_EMOTION = "text_emotion"
    TEXT_SENTIMENT = "text_sentiment"
    TEXT_LENGTH = "text_length"
    MODEL_PERPLEXITY = "model_perplexity"
    IMAGE_BRIGHTNESS = "image_brightness"
    IMAGE_CONTRAST = "image_contrast"
    BBOXES_QUANTITY = "bboxes_quantity"
    BBOXES_AREA = "bboxes_area"


class DetectionEventActionType(BaseML3Enum):
    """
    **Fields:**

        - DISCORD_NOTIFICATION
        - SLACK_NOTIFICATION
        - EMAIL_NOTIFICATION
        - TEAMS_NOTIFICATION
        - MQTT_NOTIFICATION
        - RETRAIN
    """

    DISCORD_NOTIFICATION = "discord_notification"
    SLACK_NOTIFICATION = "slack_notification"
    EMAIL_NOTIFICATION = "email_notification"
    TEAMS_NOTIFICATION = "teams_notification"
    MQTT_NOTIFICATION = "mqtt_notification"
    RETRAIN = "retrain"


class ModelMetricName(BaseML3Enum):
    """
    Name of the model metrics that is associated with the model

    **Fields:**
        - RMSE
        - RSQUARE
    """

    RMSE = "rmse"
    RSQUARE = "rsquare"
    ACCURACY = "accuracy"
    AVERAGE_PRECISION = "average_precision"


class SuggestionType(BaseML3Enum):
    """
    Enum to specify the preferred
    type of suggestion

    **Fields:**
        - SAMPLE_WEIGHTS
        - RESAMPLED_DATASET
    """

    SAMPLE_WEIGHTS = "sample_weights"
    RESAMPLED_DATASET = "resampled_dataset"


class ApiKeyExpirationTime(BaseML3Enum):
    """
    **Fields:**

        - ONE_MONTH
        - THREE_MONTHS
        - SIX_MONTHS
        - ONE_YEAR
        - NEVER

    """

    ONE_MONTH = "one_month"
    THREE_MONTHS = "three_months"
    SIX_MONTHS = "six_months"
    ONE_YEAR = "one_year"
    NEVER = "never"


class ExternalIntegration(BaseML3Enum):
    """
    An integration with a 3rd party service provider

    **Fields:**
        - AWS
        - GCP
        - AZURE
        - AWS_COMPATIBLE
    """

    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    AWS_COMPATIBLE = "aws_compatible"


class StoragePolicy(BaseML3Enum):
    """
    Enumeration that specifies the storage policy for the data sent to
    ML cube Platform

    **Fields:**
        - MLCUBE: data are copied and stored into the ML cube Platform
            cloud
        - CUSTOMER: data are kept only in your cloud and ML cube
            Platform will access to this storage source every time
            it needs to read data
    """

    MLCUBE = "mlcube"
    CUSTOMER = "customer"


class RetrainTriggerType(BaseML3Enum):
    """
    Enumeration of the possible retrain triggers
    """

    AWS_EVENT_BRIDGE = "aws_event_bridge"
    GCP_PUBSUB = "gcp_pubsub"
    AZURE_EVENT_GRID = "azure_event_grid"


class Currency(BaseML3Enum):
    """
    Currency of to use for the Task
    """

    EURO = "euro"
    DOLLAR = "dollar"


class DataType(BaseML3Enum):
    """
    Data type enum
    Describe data type of input
    """

    FLOAT = "float"
    STRING = "string"
    CATEGORICAL = "categorical"

    # array can have multiple dimensions each of them with n elemens
    # for instance, an image is an array with c channels, hence it is
    # an array_3 with [h, w, c] where h is the number of pixels over
    # the height axis, w over the width axis and c is the number of
    # channels (3 for RGB images).

    # array [h]  # noqa
    ARRAY_1 = "array_1"
    # array [h, w]  # noqa
    ARRAY_2 = "array_2"
    # array [h, w, c]  # noqa
    ARRAY_3 = "array_3"


class ColumnRole(BaseML3Enum):
    """
    Column role enum
    Describe the role of a column
    """

    INPUT = "input"
    INPUT_MASK = "input_mask"
    PREDICTION = "prediction"
    TARGET = "target"
    ERROR = "error"
    ID = "id"
    TIME_ID = "time_id"
    KPI = "kpi"
    INPUT_ADDITIONAL_EMBEDDING = "input_additional_embedding"
    TARGET_ADDITIONAL_EMBEDDING = "target_additional_embedding"
    PREDICTION_ADDITIONAL_EMBEDDING = "prediction_additional_embedding"
    USER_INPUT = "user_input"
    RETRIEVED_CONTEXT = "retrieved_context"


class ColumnSubRole(BaseML3Enum):
    """
    Column subrole enum
    Describe the subrole of a column
    """

    RAG_USER_INPUT = "user_input"
    RAG_RETRIEVED_CONTEXT = "retrieved_context"
    MODEL_PROBABILITY = "model_probability"
    OBJECT_DETECTION_LABEL_TARGET = "object_detection_label_target"
    OBJECT_DETECTION_LABEL_PREDICTION = "object_detection_label_prediction"


class TextLanguage(BaseML3Enum):
    """Enumeration of text language used in nlp tasks.

    Fields
    ------

    ITALIAN
    ENGLISH
    MULTILANGUAGE
    """

    ITALIAN = "italian"
    ENGLISH = "english"
    MULTILANGUAGE = "multilanguage"


class ImageMode(BaseML3Enum):
    """
    Image mode enumeration

    Fields
    ------
    RGB: Red, Green, Blue
    RGBA: Red, Green, Blue, Alpha
    GRAYSCALE: Grayscale
    """

    RGB = "rgb"
    RGBA = "rgba"
    GRAYSCALE = "grayscale"


class SubscriptionType(BaseML3Enum):
    """Type of subscription plan of a company

    Fields
    ------
    CLOUD: subscription plan for web app or sdk access
    EDGE: subscription plan for edge deployment
    """

    CLOUD = "cloud"
    EDGE = "edge"


class ProductKeyStatus(BaseML3Enum):
    """Status of a product key

    Fields
    ------
    NEW = generated but not yet used product key
    VALIDATING = validation requested from client
    IN_USE = validated product key, client activated
    """

    NEW = "new"
    VALIDATING = "validating"
    IN_USE = "in use"
