import requests
import json
from django.conf import settings

class ParsPaySandBox:
    _payment_request_url = "https://sandbox.api.parspal.com/v1/payment/request"
    _payment_verify_url = "https://sandbox.api.parspal.com/v1/payment/verify"
    _payment_inquery_url = "https://sandbox.api.parspal.com/v1/payment/inquiry"
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

    def payment_verify(self, id, amount, currency=None):
        payload = {
            "amount": amount,
            "receipt_number": id,
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

    def payment_inquery(self,amount,payment_id):
        payload = {
            "payment_id": payment_id,
            "amount": amount
        }
        
        headers ={
            'Content-Type': 'application/json',
            'APIKEY': self.api_key
        }
        response = requests.post(self._payment_inquery_url,headers=headers,data=json.dumps(payload))
        result = response.json()
        return result
    
    
# Test the class
if __name__ == "__main__":
    api_key = "00000000aaaabbbbcccc000000000000"
    parspay = ParsPaySandBox(api_key)

    try:
        response = parspay.payment_request(15000.890)
        response_inquery = parspay.payment_inquery(amount=15000.890,payment_id=response["payment_id"])
        print(response)
        print(response_inquery)
        payment_url = response["link"]
        payment_id = response["payment_id"]
        print(f"Payment URL: {payment_url} and payment id :{payment_id}")

        input("Proceed to payment and press enter to verify...")
        
        if response_inquery["is_paymented"] is not True:
            status = response_inquery["status"]
            print (f"payment status is {status} and not payed without recipt number")
        else:
           verification_response = parspay.payment_verify(amount=response["amount"],currency=response["currency"],id=response_inquery["receipt_number"])
           print(verification_response)

    except Exception as e:
        print(f"An error occurred: {e}")
