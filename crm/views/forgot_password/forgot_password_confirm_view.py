from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from crm.library.helpers.views import unconvert_uid
from crm.models import User
from crm.views.base_view import BaseView
from crm.serializers.security import ConfirmPasswordSerializer


class ForgotPasswordConfirmView(BaseView):
    serializer_class = ConfirmPasswordSerializer

    password_param = 'password'
    uid_param = 'uid'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get(self.password_param)
            converted_uid = serializer.data.get(self.uid_param)
            uid = unconvert_uid(converted_uid)
            user = User.objects.get(id=uid)
            user.set_password(password)
            user.save()
            return self.json_success_response(message={"Success": "Password is changed!"})
        return self.json_failed_response(errors=serializer.errors)
