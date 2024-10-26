from spaceone.core.error import *


class ERROR_DEFINE_SECRET_BACKEND(ERROR_BASE):
    _message = "Secret Backend is not defined. {backend}"


class ERROR_WRONG_ENCRYPT_ALGORITHM(ERROR_HANDLER_CONFIGURATION):
    _message = "EncryptAlgorithm({encrypt_algorithm}) is not supported."


class ERROR_NOT_EXIST_TRUST_SERVICE_ACCOUNT(ERROR_BASE):
    _message = "Trust type service account is not exist"


class ERROR_EXIST_RELATED_SECRET(ERROR_BASE):
    _message = "Related Secret is exist. (secret_id={secret_id})"


class ERROR_DIFF_SECRET_AND_TRUSTED_SECRET_ENCRYPTED(ERROR_BASE):
    _message = "The encryption algorithm of Secret and Trusted Secret are different."
