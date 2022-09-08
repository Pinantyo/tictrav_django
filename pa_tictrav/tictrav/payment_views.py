from tictrav import models, forms
from django.shortcuts import render, redirect


# Get settings
from django.conf import settings

# Midtrans payment
import midtransclient



def payment(request):
	# Create Snap API instance
	snap = midtransclient.Snap(
	    # Set to true if you want Production Environment (accept real transaction).
	    is_production=False,
	    server_key=settings.MIDTRANS_SERVER
	)
	# Build API parameter
	param = {
	    "transaction_details": {
	        "order_id": "test-transaction-123",
	        "gross_amount": 200000
	    }, "credit_card":{
	        "secure" : True
	    }, "customer_details":{
	        "first_name": "budi",
	        "last_name": "pratama",
	        "email": "budi.pra@example.com",
	        "phone": "08111222333"
	    }
	}
	 
	transaction = snap.create_transaction(param)
	 
	transaction_token = transaction['token']

	client_key = settings.CLIENT_KEY

	return render(request, 'pemesanan.html',{'transaction_token':transaction_token,'client_key':client_key})