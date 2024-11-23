from django.core.mail import send_mail
from django.template import Template, Context
from apps.core.models import EmailTemplate


def send_dynamic_email(template_name, to_email, context_data):
    try:
        template = EmailTemplate.objects.get(name=template_name)
    except EmailTemplate.DoesNotExist:
        raise ValueError(f"Template with name '{template_name}' does not exist.")
    subject = Template(template.subject).render(Context(context_data))
    body = Template(template.body).render(Context(context_data))
    send_mail(subject, body, 'your_email@shuttle.com', [to_email])
