import requests

class Blockchain:

    node = "http://127.0.0.1:8000"

    @staticmethod
    def add_transaction(data = {}):
        req = requests.post(f"{Blockchain.node}/api/create_transaction", json = data)
        return req.json()

    @staticmethod
    def get_transactions():
        req = requests.get(f"{Blockchain.node}/api/get_transactions")
        return req.json()

    @staticmethod
    def get_chain():
        req = requests.get(f"{Blockchain.node}/api/get_chain")
        return req.json()

    @staticmethod
    def get_by_hash(IpfsHash):
        req = requests.get(f"{Blockchain.node}/api/get_by_hash/{IpfsHash}")
        return req.json()
