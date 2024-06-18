import requests
import json


class PayPingSandBox:
    
    _payment_url = "https://api.payping.ir/v2/pay"
    _return_url = ""
    _payment_approval = ""
    
    def __init__ (self,api_key="j7EcjwpHw3U2D3o4rbzVCkzAE3ql8HLDaBnkBERYESE"):        
        self.api = api_key
    
    def request_payment(self,amount,payerIdentity=None,payerName=None,description=None):
        
        payload = {
            
        }
        auth = self.api
        headers = {"authorization": f"Bearer {auth}"}
        pass