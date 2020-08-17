from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from crm.views import *

app_name = 'crm'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('users/<int:pk>', UsersListView.as_view(), name='users'),
    path('profile/<int:pk>', MyProfileView.as_view(), name='profile'),
    path('change-password-confirm/', ChangePasswordLinkView.as_view(), name='change-password-confirm'),
    path('change-pass/<str:data>', ChangePasswordView.as_view(), name='change-pass'),
    path('confirm-user/<str:data>', UserRegisterView.as_view(), name='confirm-user'),
    path('invite-new-user/', InviteNewUserView.as_view(), name='invite-new-user'),
    path('generate-link/', GenerateLinkView.as_view(), name='generate-link'),
    path('contractors/', ContractorsListView.as_view(), name='contractor'),
    path('contractors/<int:pk>', ContractorsListView.as_view(), name='contractor-pk'),
    path('postformats/', PostFormatListView.as_view(), name='contractor-post-formats'),
    path('postformats/<int:pk>', PostFormatListView.as_view(), name='contractor-post-formats-pk'),
    path('email-registered/<str:email>', CheckEmailRegisteredView.as_view(), name='email-registered'),
    path('change-group/<int:user_id>', ChangeGroupView.as_view(), name='change-group'),
    path('hashtags/', HashtagsListView.as_view(), name='hashtags'),
    path('burst-news/', BurstNewsView.as_view(), name='burst-news'),
    path('news-waves/', NewsWaveView.as_view(), name="get-post-news-wave"),
    path('news-waves/<int:pk>', NewsWaveView.as_view(), name="update-delete-news-wave"),
    path('news-emails/', NewsEmailListView.as_view(), name="news-emails"),
    path('news-emails/<int:pk>', NewsEmailListView.as_view(), name="put-news-emails"),
    path('newsprojects/', NewsProjectListView.as_view(), name="newsprojects"),
    path('newsprojects/<int:pk>', NewsProjectListView.as_view(), name="newsprojects"),
    path('news-fileupload/', NewsFileUploadView.as_view(), name='upload-news-file'),
    path('news-fileupload/<int:pk>', NewsFileUploadView.as_view(), name='upload-news-file'),
    path('wave-formation-fileupload/', WaveFormationUploadView.as_view(), name='wave-formation-upload-files'),
    path('wave-formation-fileupload/<int:pk>', WaveFormationUploadView.as_view(), name='wave-formation-upload-files'),
    path('clients/', ClientView.as_view(), name='clients'),
    path('clients/<int:pk>', ClientView.as_view(), name='update-clients')

]
