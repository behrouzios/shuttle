from celery import shared_task
from apps.core.models import EmailLog, CustomUser, BulkEmailTask
import time
from celery import shared_task
from apps.core.models import BulkEmailTask, CustomUser
from apps.core.UTILS.send_dynamic_email import send_dynamic_email


# @shared_task(bind=True)
# def send_bulk_emails_task(self, template_name):
#     try:
#         bulk_task = BulkEmailTask.objects.get(task_id=self.request.id)
#         users = CustomUser.objects.filter(is_active=True)
#
#         for user in users:
#             bulk_task.refresh_from_db()
#             if bulk_task.status == "paused":
#                 break
#             if bulk_task.status == "canceled":
#                 return "Task canceled."
#             send_dynamic_email(template_name, user.email, {"name": user.first_name or "User"})
#         bulk_task.status = "completed"
#         bulk_task.save()
#         return "Bulk email task completed successfully."
#
#     except Exception as e:
#         bulk_task.status = "failed"
#         bulk_task.save()
#         raise e
from celery import shared_task
from apps.core.models import BulkEmailTask, CustomUser, EmailLog
from apps.core.UTILS.send_dynamic_email import send_dynamic_email
import time

@shared_task(bind=True)
def send_email_task(self, template_name, batch_size=10):
    try:
        task_id = self.request.id
        bulk_task = BulkEmailTask.objects.get(task_id=task_id)
        users = CustomUser.objects.filter(is_active=True)
        user_count = users.count()

        for start in range(0, user_count, batch_size):
            bulk_task.refresh_from_db()
            if bulk_task.status == "paused":
                while bulk_task.status == "paused":
                    time.sleep(1)
                    bulk_task.refresh_from_db()

            if bulk_task.status == "canceled":
                return "Task was canceled."

            # Process batch
            batch = users[start:start + batch_size]
            for user in batch:
                try:
                    send_dynamic_email(
                        template_name,
                        user.email,
                        {"name": user.first_name or "User"}
                    )
                    EmailLog.objects.create(
                        template_name=template_name,
                        to_email=user.email,
                        status="success",
                        task_id=task_id
                    )
                except Exception:
                    EmailLog.objects.create(
                        template_name=template_name,
                        to_email=user.email,
                        status="failed",
                        task_id=task_id
                    )

            progress = int((start + batch_size) / user_count * 100)
            bulk_task.progress = min(progress, 100)
            bulk_task.save()
            time.sleep(1)

        bulk_task.status = "completed"
        bulk_task.progress = 100
        bulk_task.save()
        return "Emails sent successfully."
    except Exception as e:
        bulk_task.status = "failed"
        bulk_task.save()
        raise e
