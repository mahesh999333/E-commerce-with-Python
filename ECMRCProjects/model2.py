from mongoengine import Document, DateTimeField, StringField, LongField, \
    BooleanField, IntField, EmbeddedDocumentField, DynamicField


class SourceAudit(Document):
    api_id = StringField(unique=True)
    created_date_time = StringField()
    update_date_time = StringField()
    api_name = StringField()
    source_name = StringField()
    response = StringField()
    third_party_source = StringField()
    status = StringField()

    meta = {
        'collection': 'source_audit'
    }


class PirimidInitiationEntity(Document):
    initiationDate = DateTimeField()
    updatedDate = DateTimeField()
    vuaId = StringField()
    status = StringField()
    trackingId = LongField()
    mobileNumber = StringField()
    response = StringField()
    source = StringField()
    referenceId = StringField()

    meta = {
        'collection': 'pirimidInitiationDetails'
    }


class PirimidData(Document):
    id = StringField(primary_key=True)
    createdDate = DateTimeField()
    updatedDate = DateTimeField()
    isJsonDataSentToMono = BooleanField()
    isExcelDataSentToMono = BooleanField()
    trackingId = StringField()
    referenceId = StringField()
    data = StringField()  # Change the field type as per your requirement
    webhookFailureNotification = BooleanField(default=False)

    meta = {
        'collection': 'pirimidData'
    }


class PirimidCallBackLog(Document):
    notificationType = StringField()
    status = StringField()
    trackingId = StringField()
    referenceId = StringField()
    dataDetails = StringField()  # Change the field type as per your requirement
    date = DateTimeField()

    meta = {
        'collection': 'pirimidCallBackLogger'
    }


class PirimidAuditLogEntity(Document):
    id = StringField(primary_key=True)
    createdDate = DateTimeField()
    request = StringField()
    response = StringField()
    data = StringField()
    event = StringField()
    trackingId = LongField()
    mobileNumber = StringField()

    meta = {
        'collection': 'pirimidAuditLog'
    }


class BankStatementApi(Document):
    name = StringField()
    source = StringField()
    status = StringField()
    invocationDateTime = StringField()
    receivedDateTime = StringField()
    count = IntField()
    response = StringField()
    s3Url = StringField()


class BankStatementLog(Document):
    createdDateTime = StringField()
    updateDateTime = StringField()
    borrowerId = StringField()
    loanId = StringField()
    status = StringField()
    responseSource = StringField()
    latestAuditId = StringField()
    glibWorkorderId = StringField()
    monoId = StringField()
    bankStatementApis = EmbeddedDocumentField(BankStatementApi)

    meta = {
        'collection': 'glib_data'
    }


class FipDataEntity(Document):
    id = StringField(primary_key=True)
    name = StringField()
    code = StringField()
    isActive = BooleanField(default=True)
    bankNameMono = StringField()

    meta = {
        'collection': 'fipData'
    }

class FinoramicLogin(Document):
    userId = StringField()
    status = StringField()
    code = StringField()
    error = StringField()
    createdDate = StringField()
    updatedDate = StringField()
    monoStatus = StringField()
    monoUpdateDate = StringField()
    hasConsent = StringField()
    refreshCallResponse = StringField()

    meta = {
        'collection': 'finormicLogin'
    }
    
    
class FinoramicDataEntityV2(Document):
    id = StringField(primary_key=True)
    status = IntField()
    clientUserId = StringField()
    createdDate = DateTimeField()
    updatedDate = DateTimeField()
    lastCallBackDate = DateTimeField()
    response = DynamicField()
    downloadStatus = StringField()
    downloadCount = IntField()
    isDataSyncedWithMono = BooleanField()
    refreshInvocationDate = DateTimeField()
    refreshCallBackDate = DateTimeField()
    refreshInSyncWithMono = BooleanField()

    meta = {
        'collection': 'finoramicDataV2'
    }


class FinoramicCallBack(Document):
    status = IntField()
    clientUserId = StringField()
    dataAvailable = StringField()
    finalProcessingDone = BooleanField()
    creationDateTime = StringField()
    dataRefreshed = BooleanField()

    meta = {
        'collection': 'finoramicCallbackLogger'
    }