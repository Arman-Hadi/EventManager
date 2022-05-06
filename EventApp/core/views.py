from datetime import timedelta
from json import loads

from django.conf import settings
from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone

from core.models import WebHookMessage


@csrf_exempt
@require_POST
@non_atomic_requests
def acme_webhook(request):
    WebHookMessage.objects.filter(
        received_at__lte=timezone.now() - timedelta(days=2)
    ).delete()
    payload = loads(request.body)
    WebHookMessage.objects.create(
        received_at=timezone.now(),
        payload=payload,
    )
    process_webhook_payload(payload)
    return HttpResponse("Message received okay.", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    print(payload)
