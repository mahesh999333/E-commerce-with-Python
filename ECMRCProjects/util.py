from datetime import datetime
import json

from django.http import JsonResponse
from django.utils import timezone

from model2 import (
    FinoramicLogin,
    BankStatementApi,
    BankStatementLog,
    BankStatementAuditHistory,
    SourceAudit,
    FinoramicDataEntityV2,
)
from constants import BankStatementStatus, GenericStatusz


def formatted_date(date):
    return date.strftime('%d/%m/%Y %H:%M:%S.%f')


def create_finormic_login(user_id, status):
    now = timezone.now()
    return FinoramicLogin.objects.create(
        created_date=now,
        updated_date=now,
        user_id=user_id,
        status=status,
        mono_status=GenericStatus.PENDING.value
    )


def update_finoramic_login_ts(finoramic_login):
    now = timezone.now()
    # finoramic_login.created_date = now
    finoramic_login.updated_date = now
    finoramic_login.mono_status = GenericStatus.PENDING.value
    finoramic_login.save()
    return finoramic_login


def update_finormic_login(finormic_login, status):
    finormic_login.updated_date = timezone.now()
    finormic_login.status = status
    finormic_login.save()


def create_bank_statement_api(api_name, source):
    now = timezone.now()
    return BankStatementApi.objects.create(
        name=api_name,
        count=1,
        status=BankStatementStatus.PENDING.value,
        source=source,
        invocation_datetime=formatted_date(now)
    )


def update_bank_statement_api(api, response):
    api.status = BankStatementStatus.DONE.value
    api.response = response
    api.received_datetime = formatted_date(timezone.now())
    api.save()


def create_bank_statement_log(borrower_id, loan_id):
    now = timezone.now()
    return BankStatementLog.objects.create(
        borrower_id=borrower_id,
        loan_id=loan_id,
        status=BankStatementStatus.PENDING.value,
        created_datetime=formatted_date(now)
    )


def update_mono_status_on_bank_statement_log(log, api, service_name):
    recvd_ts = formatted_date(timezone.now())
    api.received_datetime = recvd_ts
    api.save()
    log.update_datetime = recvd_ts
    log.save()


def update_bank_statement_log(log, api):
    recvd_ts = formatted_date(timezone.now())
    api.received_datetime = recvd_ts
    api.status = BankStatementStatus.UPDATED.value
    api.save()
    log.update_datetime = recvd_ts
    log.save()


def create_audit(log_id, api):
    now = timezone.now()
    return BankStatementAuditHistory.objects.create(
        api_name=api.name,
        bank_statement_id=log_id,
        invocation_datetime=formatted_date(now),
        source=api.source,
        response=api.response
    )


def create_source_audit(source_name, api):
    now = timezone.now()
    return SourceAudit.objects.create(
        created_datetime=formatted_date(now),
        source_name=source_name,
        status=BankStatementStatus.PENDING.value
    )


def update_source_audit(audit, response):
    audit.response = response
    audit.update_datetime = formatted_date(timezone.now())
    audit.save()


def prepare_fixed_response(data, status, message):
    return {
        'data': data if data is not None else {},
        'status': status,
        'message': message
    }


def create_finoramic_data(client_user_id, status):
    now = timezone.now()
    return FinoramicDataEntityV2.objects.create(
        created_date=now,
        updated_date=now,
        last_callback_date=now,
        status=status,
        client_user_id=client_user_id,
        download_count=0,
        is_data_synced_with_mono=False
    )


def update_finoramic_data(finoramic_data):
    now = timezone.now()
    finoramic_data.last_callback_date = now
    finoramic_data.updated_date = now
    finoramic_data.download_count += 1
    finoramic_data.save()


def prepare_response(media_type, message, code, data):
    response_data = {
        'message': message,
        'code': code,
        'data': data
    }
    return JsonResponse(response_data, status=200, content_type=media_type)


def prepare_request(request_body):
    json_data = json.dumps(request_body)
    return json_data


def convert_map_to_json(data):
    return json.dumps(data)
