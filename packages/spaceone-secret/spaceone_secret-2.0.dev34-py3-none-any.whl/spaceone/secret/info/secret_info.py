import logging
import functools
from spaceone.api.secret.v1 import secret_pb2
from spaceone.core.pygrpc.message_type import *
from spaceone.core import utils
from spaceone.secret.model.secret_model import Secret

__all__ = ["SecretInfo", "SecretsInfo", "SecretDataInfo"]
_LOGGER = logging.getLogger(__name__)


def SecretDataInfo(secret_data):
    info = {
        "encrypted": secret_data.get("encrypted", False),
        "encrypt_options": change_struct_type(secret_data.get("encrypt_options", {})),
        "data": change_struct_type(secret_data["data"]),
    }

    return secret_pb2.SecretDataInfo(**info)


def SecretInfo(secret_vo: Secret, minimal=False):
    info = {
        "secret_id": secret_vo.secret_id,
        "name": secret_vo.name,
        "schema_id": secret_vo.schema_id,
        "provider": secret_vo.provider,
    }

    if minimal is False:
        info.update(
            {
                "tags": change_struct_type(secret_vo.tags),
                "trusted_secret_id": secret_vo.trusted_secret_id,
                "service_account_id": secret_vo.service_account_id,
                "resource_group": secret_vo.resource_group,
                "project_id": secret_vo.project_id,
                "workspace_id": secret_vo.workspace_id,
                "domain_id": secret_vo.domain_id,
                "created_at": utils.datetime_to_iso8601(secret_vo.created_at),
            }
        )

    return secret_pb2.SecretInfo(**info)


def SecretsInfo(secret_vos, total_count, **kwargs):
    results = list(map(functools.partial(SecretInfo, **kwargs), secret_vos))

    return secret_pb2.SecretsInfo(results=results, total_count=total_count)
