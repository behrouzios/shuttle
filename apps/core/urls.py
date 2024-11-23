from django.urls import path
from apps.core.VIEWS.user_view import RegisterUserAPIView, UserProfileAPIView, LoginAPIView
from apps.core.VIEWS.file_upload_view import FileUploadAPIView
from apps.core.VIEWS.email_template_view import EmailTemplateListCreateAPIView, EmailTemplateDetailAPIView, BulkEmailToAllUsersAPIView, BulkEmailControlAPIView, bulk_email_progress

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register/', RegisterUserAPIView.as_view(), name='register'),
    path('api/profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('upload-file/', FileUploadAPIView.as_view(), name='upload_file'),
    path('email-templates/', EmailTemplateListCreateAPIView.as_view(), name='email_template_list_create'),
    path('email-templates/<int:pk>/', EmailTemplateDetailAPIView.as_view(), name='email_template_detail'),
    path('send-bulk-emails/', BulkEmailToAllUsersAPIView.as_view(), name='email_template_detail'),
    path("bulk-email-control/", BulkEmailControlAPIView.as_view(), name="bulk_email_control"),
    path('bulk-email-progress/<str:task_id>/', bulk_email_progress, name='bulk_email_progress'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]


