# Mayfpay.top Beta Api V1

import requests


class MayfPayApi:

    def __init__(self, api_token: str, kassa_id: int, kassa_s_key: str):
        self.api_token = api_token
        self.kassa_id = kassa_id
        self.kassa_s_key = kassa_s_key
        self.base_url = "https://mayfpay.top/api/v1"

    def get_kassa_balance(self):
        url = f"{self.base_url}/kassa/balance"
        params = {
            "api_token": self.api_token,
            "kassa_id": self.kassa_id,
            "kassa_s_key": self.kassa_s_key
        }
        response = requests.get(url, params=params)
        response_json = response.json()
        return response_json

    def create_invoice(self, amount: float, order_id: str, expire_invoice: int, payment_method: str, comment: str, data: dict):
        url = f"{self.base_url}/kassa/invoices/create"
        params = {
            "api_token": self.api_token,
            "kassa_s_key": self.kassa_s_key,
            "kassa_id": self.kassa_id,
            "amount": amount,
            "order_id": order_id,
            "expire_invoice": expire_invoice,
            "payment_method": payment_method,
            "comment": comment,
            "data": data
        }
        response = requests.post(url, params=params)
        response_json = response.json()
        return response_json
    
    def check_invoice(self, order_id):
        endpoint = f"{self.base_url}kassa/invoice/check"
        headers = {"Content-Type": "application/json"}
        params = {"api_token": self.api_token, "order_id": order_id}

        response = requests.get(endpoint, headers=headers, params=params)
        return response.json()
