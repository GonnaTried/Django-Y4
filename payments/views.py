# payments/views.py
import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt # Use csrf_exempt just for the webhook for testing, but better to use proper Webhook handling

stripe.api_key = settings.STRIPE_SECRET_KEY

def set_amount_view(request):
    return render(request, 'payments/amount_form.html')

# 2. Modified View: Reads the amount from the form submission
def create_checkout_session(request):
    if request.method != 'POST':
        # Safety check: should only be accessed via POST from the form
        return HttpResponse('Invalid request method. Please set the amount first.', status=405)

    try:
        # Get the amount from the form submission and convert to float
        amount_usd = float(request.POST.get('amount'))
        
        # Stripe requires the amount in CENTS (or the smallest currency unit)
        # 10.00 USD * 100 = 1000 Cents
        unit_amount_cents = int(amount_usd * 100)
        
        if unit_amount_cents <= 50: # Enforce a minimum amount (Stripe minimum is often 50 cents)
             return HttpResponse('Amount must be greater than $0.50.', status=400)


        YOUR_DOMAIN = "http://127.0.0.1:8000"
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Assignment Fee for ${amount_usd:.2f}', # Dynamic Product Name
                        },
                        'unit_amount': unit_amount_cents, 
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment/success/',
            cancel_url=YOUR_DOMAIN + '/payment/cancel/',
            # Note: Success/Cancel URLs must be fully qualified (including /payment/ if you used it in the main urls.py)
        )
        return redirect(checkout_session.url, code=303)
        
    except ValueError:
        return HttpResponse('Invalid amount entered.', status=400)
    except Exception as e:
        # Catch any Stripe/other errors
        return render(request, 'payments/error.html', {'error': str(e)}) 

def payment_success_view(request):
    # Your logic to mark the task/order as paid goes here
    return render(request, 'payments/success.html')

def payment_cancel_view(request):
    # Your logic for a cancelled payment
    return render(request, 'payments/cancel.html')