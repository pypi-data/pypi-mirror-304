from cbr_shared.aws.s3.S3_DB_Base import S3_DB_Base
from osbot_utils.utils.Status import status_warning


class S3_DB_Base__Disabled(S3_DB_Base):

    def s3(self):
        return None

    def s3_bucket(self):
        return None

    def s3_bucket__temp_data(self):
        return None

    def s3_file_bytes(self, s3_key):
        return None

    def s3_file_contents(self, s3_key):
        return None

    def s3_file_contents_json(self, s3_key):
        return None

    def s3_file_data(self, s3_key):
        return None

    def s3_file_delete(self, s3_key):
        return False

    def s3_file_exists(self, s3_key):
        return False

    def s3_file_info(self, s3_key):
        return {}

    def s3_file_metadata(self, s3_key):
        return {}

    def s3_file_set_metadata(self, s3_key, metadata):
        return False

    def s3_folder_contents(self, folder, return_full_path=False):
        return []

    def s3_folder_files(self, folder='', return_full_path=False, include_sub_folders=False):
        return []

    def s3_folder_list(self, folder='', return_full_path=False):
        return []

    def s3_save_data(self, data, s3_key, metadata=None):
        return False

    def s3_temp_folder__pre_signed_urls_for_object(self, source='NA', reason='NA', who='NA', expiration=3600):
        return {}

    def s3_temp_folder__pre_signed_url(self, s3_bucket, s3_key, operation, expiration=3600):
        return None

    def s3_temp_folder__download_string(self, pre_signed_url):
        return None

    def s3_temp_folder__upload_string(self, pre_signed_url, file_contents):
        return False

    def s3_folder_odin_data(self):
        return None

    def s3_folder_users_metadata(self):
        return None

    def s3_folder_temp_file_uploads(self):
        return None

    # setup and restore

    def bucket_delete(self):
        return False

    def bucket_delete_all_files(self):
        return False

    def bucket_exists(self):
        return False

    def setup(self):
        return self

    def using_minio(self):
        return False
