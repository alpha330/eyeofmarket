import requests
import json
from django.conf import settings

class ParsPaySandBox:
    _payment_request_url = "https://sandbox.api.parspal.com/v1/payment/request"
    _payment_verify_url = "https://sandbox.api.parspal.com/v1/payment/verify"
    _payment_page_url = "https://sandbox.api.parspal.com/v1/payment/redirect"
    _return_url = "http://127.0.0.1:8000/payment/verify/parspay"

    def __init__(self, api_key="00000000aaaabbbbcccc000000000000"):
        self.api_key = api_key

    def payment_request(self, amount, description="پرداختی کاربر از پارس پی", reserve_id=None, order_id=None):
        data = {
            'amount': amount,
            'return_url': self._return_url,
            'description': description,
            'currency': "IRT",
            'reserve_id': reserve_id,
            'order_id': order_id,
        }
        headers = {
            'APIKEY': self.api_key,
            'Content-Type': 'application/json'
        }
        response = requests.post(self._payment_request_url, data=json.dumps(data), headers=headers)
        
        return response.json()

    def payment_verify(self, receipt_number, amount, currency=None):
        payload = {
            "amount": amount,
            "receipt_number": receipt_number,
            "currency": currency,
        }
        headers = {
            'Content-Type': 'application/json',
            'APIKEY': self.api_key
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=json.dumps(payload))
        result = response.json()

        if response.status_code != 200 or result.get('status') != 'SUCCESSFUL':
            error_message = result.get('message', 'Unknown error')
            raise Exception(f"Error in payment verification: {error_message}")

        return result

    def generate_payment_url(self, payment_id):
        return self._payment_page_url + payment_id

# Test the class
if __name__ == "__main__":
    api_key = "00000000aaaabbbbcccc000000000000"
    parspay = ParsPaySandBox(api_key)

    try:
        response = parspay.payment_request(15000.890)
        print(response)
        payment_url = response["link"]
        print(f"Payment URL: {payment_url}")

        input("Proceed to payment and press enter to verify...")

        verification_response = parspay.payment_verify(str(response["payment_id"]), 15000)
        print(verification_response)

    except Exception as e:
        print(f"An error occurred: {e}")
