from enum import Enum

class APIResponseMessages(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING"


class BankStatementStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    UPDATED = "UPDATED"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"
    DONE = "DONE"
    
    
class CallBackServices(Enum):
    FINORAMIC = "finoramic"
    GLIB = "glib"
    PIRIMID = "pirimid"
    
    
class FinoramicConstants(Enum):
    SUCCESS = "success"
    ERROR = "error"
    

class GenericStatus(Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"
    DONE = "DONE"
    
    
class Pirimid:
    class Events(Enum):
        EXCEL_DATA_DOWNLOAD = 'EXCEL_DATA_DOWNLOAD'
        JSON_DATA_DOWNLOAD = 'JSON_DATA_DOWNLOAD'
        JSON_DATA_DOWNLOAD_FAILED = 'JSON_DATA_DOWNLOAD_FAILED'
        EXCEL_DATA_DOWNLOAD_FAILED = 'EXCEL_DATA_DOWNLOAD_FAILED'
        JSON_NOTIFICATION_TO_MONO = 'JSON_NOTIFICATION_TO_MONO'
        EXCEL_NOTIFICATION_TO_MONO = 'EXCEL_NOTIFICATION_TO_MONO'
        JSON_NOTIFICATION_TO_MONO_FAILED = 'JSON_NOTIFICATION_TO_MONO_FAILED'
        EXCEL_NOTIFICATION_TO_MONO_FAILED = 'EXCEL_NOTIFICATION_TO_MONO_FAILED'
        INITIATION = 'INITIATION'
        CONSENT_CREATED = 'CONSENT_CREATED'
        CONSENT_REJECTED = 'CONSENT_REJECTED'
        CONSENT_STATUS_CHANGE = 'CONSENT_STATUS_CHANGE'
        CONSENT_ACTIVE = 'CONSENT_ACTIVE'
        ANALYTICS_COMPLETE = 'ANALYTICS_COMPLETE'
        DATA_FETCH_SUCCESS = 'DATA_FETCH_SUCCESS'
        FI_REQUEST_CREATION_FAILED = 'FI_REQUEST_CREATION_FAILED'
        DECRYPTION = 'DECRYPTION'
        DECRYPTION_FAILED = 'DECRYPTION_FAILED'
        FETCH_VUAID = 'FETCH_VUAID'
        CONSENT_NOTIFICATION_TO_MONO_FAILED = 'CONSENT_NOTIFICATION_TO_MONO_FAILED'
        CONSENT_NOTIFICATION_TO_MONO_SUCCESS = 'CONSENT_NOTIFICATION_TO_MONO_SUCCESS'


class PirimidNotificationType(Enum):
    CONSENT_CREATED = "CONSENT_CREATED"
    CONSENT_STATUS_CHANGE = "CONSENT_STATUS_CHANGE"
    ANALYTICS_COMPLETE = "ANALYTICS_COMPLETE"
    FI_REQUEST_CREATION_FAILED = "FI_REQUEST_CREATION_FAILED"
    CONSENT_ACTIVE = "CONSENT_ACTIVE"
    DATA_FETCH_SUCCESS = "DATA_FETCH_SUCCESS"


class PirimidSources(Enum):
    WEB = "WEB"
    APP = "APP"
    
    
class PirimidTemplateType(Enum):
    UNDERWRITING = "UNDERWRITING"
    INITIATED = "INITIATED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"