from rest_framework import generics
from apps.core.models import EmailTemplate, BulkEmailTask, CustomUser, EmailLog
from apps.core.API.serializers import EmailTemplateSerializer
from apps.core.MODEL_HANDLER.permission import IsStaffUser
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from apps.core.models import BulkEmailTask
from apps.core.tasks import send_email_task

CustomUser = get_user_model()


class EmailTemplateListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsStaffUser]


class EmailTemplateDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [IsStaffUser]


class BulkEmailToAllUsersAPIView(APIView):
    permission_classes = [IsStaffUser]

    def post(self, request):
        template_name = request.data.get('template_name')
        context_data = request.data.get('context_data', {})

        if not template_name:
            return Response({"error": "template_name is required."}, status=status.HTTP_400_BAD_REQUEST)
        users = CustomUser.objects.filter(is_active=True)
        if not users.exists():
            return Response({"error": "No active users found."}, status=status.HTTP_404_NOT_FOUND)
        for user in users:
            personalized_context = context_data.copy()
            personalized_context['name'] = user.first_name or "User"
            send_email_task.delay(template_name, user.email, personalized_context)

        return Response({"message": "Bulk email tasks submitted successfully."}, status=status.HTTP_200_OK)


class BulkEmailControlAPIView(APIView):
    def post(self, request):
        action = request.data.get("action")
        template_name = request.data.get("template_name")
        task_id = request.data.get("task_id")

        if not action:
            return Response({"error": "Action is required."}, status=status.HTTP_400_BAD_REQUEST)

        if action not in ["start", "pause", "resume", "cancel"]:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        if action == "start" and not template_name:
            return Response({"error": "Template name is required for starting emails."},
                            status=status.HTTP_400_BAD_REQUEST)

        if action in ["pause", "resume", "cancel"] and not task_id:
            return Response({"error": "Task ID is required for this action."}, status=status.HTTP_400_BAD_REQUEST)

        if action == "start":
            # Start a new task
            task = send_email_task.apply_async(args=[template_name])
            BulkEmailTask.objects.create(task_id=task.id, template_name=template_name, status="active")
            return Response({"message": "Task started successfully.", "task_id": task.id}, status=status.HTTP_200_OK)

        try:
            bulk_task = BulkEmailTask.objects.get(task_id=task_id)
        except BulkEmailTask.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        if action == "pause":
            if bulk_task.status != "active":
                return Response({"error": "Only active tasks can be paused."}, status=status.HTTP_400_BAD_REQUEST)
            bulk_task.status = "paused"
            bulk_task.save()
            return Response({"message": "Task paused successfully."}, status=status.HTTP_200_OK)

        if action == "resume":
            if bulk_task.status != "paused":
                return Response({"error": "Only paused tasks can be resumed."}, status=status.HTTP_400_BAD_REQUEST)
            bulk_task.status = "active"
            bulk_task.save()
            return Response({"message": "Task resumed successfully."}, status=status.HTTP_200_OK)

        if action == "cancel":
            if bulk_task.status == "canceled":
                return Response({"error": "Task is already canceled."}, status=status.HTTP_400_BAD_REQUEST)
            AsyncResult(task_id).revoke(terminate=True)
            bulk_task.status = "canceled"
            bulk_task.save()
            return Response({"message": "Task canceled successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


def bulk_email_progress(request, task_id):
    try:
        total_emails = CustomUser.objects.filter(is_active=True).count()
        if total_emails == 0:
            return JsonResponse({"progress": 100})

        sent_emails = EmailLog.objects.filter(task_id=task_id, status="success").count()
        progress = int((sent_emails / total_emails) * 100)

        return JsonResponse({"progress": progress})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
