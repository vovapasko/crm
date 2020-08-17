import io
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from crm.models import User
from crm.views.profile.can_change_permission import CanChangePermission
from crm.tests.base_test_case import BaseTestCase
from .test_data.test_data import *


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = io.BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class ProfileTestCase(BaseTestCase):
    url = '/profile/'
    permission_error_message_dict = CanChangePermission.message
    # because this dict may contain only one key
    permission_error_message_dict_key = list(permission_error_message_dict.keys())[0]
    unauthorised_error_key = "detail"

    @classmethod
    def setUpTestData(cls: object) -> None:
        super().setUpTestData()
        cls.user = super().get_test_user()
        cls.users = User.objects.all()

    @classmethod
    def tearDownClass(cls):
        cls.user.avatar.delete()
        super().tearDownClass()

    def test_put_other_profile_authorised(self) -> None:
        # trying to get id of non requesting user
        client, not_user_request_id = self.get_auth_client_and_model_last_id(user=self.user, par_model=self.users)
        response = client.put(
            # change other's user profile
            path=self.generate_url(self.url, not_user_request_id),
            data=correct_profile_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        json_content = self.get_json_content_from_response(response)
        self.check_keys_in_dict(json_content, self.permission_error_message_dict.keys())
        self.check_values(self.permission_error_message_dict, json_content, self.permission_error_message_dict_key)

    # todo think how to delete mock avatar from S3 after test executing
    def test_put_users_profile_with_avatar_authorised(self) -> None:
        client = self.get_api_client(user=self.user)
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        correct_profile_data.update({"avatar": avatar_file})
        response = client.put(
            path=self.generate_url(self.url, self.user.id),
            data=correct_profile_data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # todo think how to provide correct formatting of Image in the next line
        # self.compare_data(correct_profile_data, self.get_json_content_from_response(response))

    def test_put_users_profile_without_avatar_authorised(self) -> None:
        client = self.get_api_client(user=self.user)
        response = client.put(
            path=self.generate_url(self.url, self.user.id),
            data={
                "first_name": "Test First Name",
                "last_name": "Test Last Name",
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.compare_data(correct_profile_data, self.get_json_content_from_response(response))

    def test_put_users_profile_wrong_avatar_authorised(self):
        client = self.get_api_client(user=self.user)
        response = client.put(
            path=self.generate_url(self.url, self.user.id),
            data=incorrect_profile_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            member="avatar",
            container=self.get_json_content_from_response(response)
        )

    def test_put_profile_unauthorised(self) -> None:
        client = self.get_api_client(authenticated=False)
        response = client.put(
            path=self.generate_url(self.url, self.user.id),
            data=correct_profile_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(
            member=self.unauthorised_error_key,
            container=self.get_json_content_from_response(response)
        )
