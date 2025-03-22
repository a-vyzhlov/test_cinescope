from models.user_data_model import RegisterUserResponse

class TestUser:

    def test_create_user(self, super_admin, registration_user_data):
        response = super_admin.api.user_api.create_user(registration_user_data)
        creation_user_response = RegisterUserResponse(**response.json())

        assert creation_user_response.email == registration_user_data.email
        assert creation_user_response.fullName == registration_user_data.fullName
        assert creation_user_response.roles == registration_user_data.roles
        assert  creation_user_response.verified is True

    def test_get_user_by_locator(self, super_admin, registration_user_data):
        creation_user_response = super_admin.api.user_api.create_user(registration_user_data)
        for_id_response = super_admin.api.user_api.get_user(creation_user_response.id)
        for_email_response = super_admin.api.user_api.get_user(creation_user_response.email)
        get_for_id_user_response = RegisterUserResponse(**for_id_response.json())
        get_for_email_user_response = RegisterUserResponse(**for_email_response.json())

        assert get_for_id_user_response == get_for_email_user_response, "Содержание ответов должно быть идентичным"
        assert get_for_id_user_response.verified is True

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)