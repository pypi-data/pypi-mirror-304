import os
import json
import uuid
import aiohttp

BASE_URL = 'http://gateway.arifpay.net/api/'
MakePayment_url = 'checkout/session'

class ArifPay:
    
    def __init__(self, API_key, expireDate):
        self.API_key = API_key
        self.expireDate = expireDate
        self.requiredFields = [
            "cancelUrl",
            "phone",
            "successUrl",
            "errorUrl",
            "notifyUrl",
            "paymentMethods",
            "items",
        ]

    def validatePaymentInfo(self, payment_info):
        beneficiariesAmount = sum(item['quantity'] * item['price'] for item in payment_info['items'])

        if 'beneficiaries' not in payment_info:
            payment_info['beneficiaries'] = [
                {
                    "accountNumber": "01320811436100",
                    "bank": "AWINETAA",
                    "amount": beneficiariesAmount,
                },
            ]

        missingFields = [field for field in self.requiredFields if field not in payment_info]

        if missingFields:
            raise ValueError(f"The following required fields are missing from payment_info: {', '.join(missingFields)}")

        return "All required fields are present."

    async def makePayment(self, payment_info):
        try:
            self.validatePaymentInfo(payment_info)
            payment_info['nonce'] = str(uuid.uuid4())
            payment_info['expireDate'] = self.expireDate
            url = f"{BASE_URL}{MakePayment_url}"
            headers = {
                "Content-Type": "application/json",
                "x-arifpay-key": self.API_key,
            } 

            async with aiohttp.ClientSession() as session:
                async with session.post('https://gateway.arifpay.net/api/checkout/session', headers=headers, data=json.dumps(payment_info)) as response:
                    return(await response.text())
        except Exception as error:
            print(error)
            return str(error)
