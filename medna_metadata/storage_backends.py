from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import get_storage_class


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION
    file_overwrite = True
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = True
    default_acl = 'public-read'


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False


class PrivateSequencingStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_SEQUENCING_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class PrivateBackupStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_BACKUP_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


# https://stackoverflow.com/questions/59437637/django-use-private-s3-storage-only-in-production-environment
def select_private_media_storage():
    private_storage_class = get_storage_class(settings.PRIVATE_FILE_STORAGE)
    return private_storage_class()  # instantiate the storage


def select_private_sequencing_storage():
    private_storage_class = get_storage_class(settings.PRIVATE_SEQUENCING_FILE_STORAGE)
    return private_storage_class()  # instantiate the storage


def select_public_media_storage():
    public_storage_class = get_storage_class(settings.DEFAULT_FILE_STORAGE)
    return public_storage_class()
