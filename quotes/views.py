from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import QuoteRequest

class SubmitQuoteView(APIView):
    def post(self, request):
        data = request.data

        # Validate required fields
        required = ['full_name', 'email']
        for field in required:
            if not data.get(field):
                return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Save to database
        quote = QuoteRequest.objects.create(
            full_name=data.get('full_name', ''),
            company=data.get('company', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            country=data.get('country', ''),
            product_lines=data.get('product_lines', []),
            message=data.get('message', ''),
        )

        # Send notification email to sales team
        try:
            subject = f'New Quote Request — {quote.full_name} ({quote.company})'
            body = f"""
New quote request received on vantumsurgical.com

━━━━━━━━━━━━━━━━━━━━━━━━
CONTACT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━
Name:     {quote.full_name}
Company:  {quote.company or '—'}
Email:    {quote.email}
Phone:    {quote.phone or '—'}
Country:  {quote.country or '—'}

━━━━━━━━━━━━━━━━━━━━━━━━
PRODUCT INTEREST
━━━━━━━━━━━━━━━━━━━━━━━━
{', '.join(quote.product_lines) if quote.product_lines else '—'}

━━━━━━━━━━━━━━━━━━━━━━━━
MESSAGE
━━━━━━━━━━━━━━━━━━━━━━━━
{quote.message or '—'}

━━━━━━━━━━━━━━━━━━━━━━━━
View in admin: https://vantum-backend.railway.app/admin/quotes/quoterequest/{quote.id}/change/
            """
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.QUOTE_NOTIFICATION_EMAIL],
                fail_silently=True,
            )

            # Send confirmation email to customer
            send_mail(
                subject='We received your quote request — Vantum Surgical',
                message=f"""Dear {quote.full_name},

Thank you for reaching out to Vantum Surgical.

We have received your quote request and our team will get back to you within 24 hours with pricing and lead times.

If you need to reach us urgently:
📞 USA: +1 (917) 939-5371
💬 WhatsApp: +92 (327) 997-4498
📧 sales@vantumsurgical.com

Best regards,
Vantum Surgical Team
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[quote.email],
                fail_silently=True,
            )
        except Exception:
            pass  # Don't fail if email fails

        return Response({'success': True, 'id': quote.id}, status=status.HTTP_201_CREATED)
