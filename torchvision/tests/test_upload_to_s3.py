import unittest
from unittest.mock import patch, call
from src.upload_to_s3 import upload_to_s3

AWS_ACCESS_KEY_ID = "mock_access_key"
AWS_SECRET_ACCESS_KEY = "mock_secret_key"

class TestS3Upload(unittest.TestCase):
    @patch('src.upload_to_s3.boto3.client')
    def test_upload_to_s3_success(self, mock_boto_client):
        bucket_name = 'my-test-bucket-for-unittesting'
        file_path = 'path/to/test_file.txt'
        object_name = 'test_file.txt'
        mock_s3_client = mock_boto_client.return_value
        with patch('src.upload_to_s3.os.remove') as mock_os_remove:
            upload_to_s3(bucket_name, file_path, object_name)

            mock_s3_client.upload_file.assert_called_once_with(file_path, bucket_name, object_name)
            mock_os_remove.assert_called_once_with(file_path)

    @patch('src.upload_to_s3.boto3.client')
    @patch('builtins.print')
    def test_upload_to_s3_exception(self, mock_print, mock_boto_client):
        bucket_name = 'my-test-bucket-for-unittesting'
        file_path = 'path/to/test_file.txt'
        object_name = 'test_file.txt'

        mock_s3_client = mock_boto_client.return_value
        mock_s3_client.upload_file.side_effect = Exception("Mock exception")

        upload_to_s3(bucket_name, file_path, object_name)

        failure_message_call = call(f"Failed to upload {file_path} to {bucket_name}/{object_name}.")
        exception_message_call = call(mock_s3_client.upload_file.side_effect)

        self.assertIn(failure_message_call, mock_print.call_args_list, "The failure message was not printed as expected.")
        self.assertIn(exception_message_call, mock_print.call_args_list, "The exception message was not printed as expected.")


if __name__ == '__main__':
    unittest.main()
