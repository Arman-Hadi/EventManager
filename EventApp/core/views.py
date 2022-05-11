from datetime import timedelta

from django.db.transaction import atomic, non_atomic_requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone

from core.models import WebHookMessage, Ticket


@csrf_exempt
@require_POST
@non_atomic_requests
def webhook(request):
    WebHookMessage.objects.filter(
        recieved_at__lte=timezone.now() - timedelta(days=2)
    ).delete()
    try:
        payload = request.POST.copy()
        WebHookMessage.objects.create(
            received_at=timezone.now(),
            payload=payload,
        )
        process_webhook_payload(payload)
    except Exception as e:
        print('---------------error:')
        print(str(e))
        print(request.POST)
    finally:
        return HttpResponse("Message received okay.", content_type="text/plain")


@atomic
def process_webhook_payload(payload):
    print(payload)
    t = Ticket().from_evand(payload)
    print(t)
