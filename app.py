import os
import json
from dotenv import load_dotenv
from web3 import Web3, Account, HTTPProvider
from flask import Flask, render_template, request

# load environment variables from .env file
load_dotenv('.env')

# web3.py instance
w3 = Web3(HTTPProvider(os.environ.get('RPC_URL'))) 
print('Web3 Connected:',w3.isConnected())

# account setup
private_key= os.environ.get('PRIVATE_KEY') #private key of the account
public_key = Account.from_key(private_key)
account_address = public_key.address

# Contract instance
contract_artifacts_file = json.load(open('./contracts/Greeter.json'))
abi = contract_artifacts_file['abi']
contract_address = os.environ.get('CONTRACT_ADDRESS')
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

app = Flask(__name__)

@app.route("/")
def index():
    greeting = contract_instance.functions.getGreeting().call()
    return render_template("index.html", greeting=greeting)

@app.route("/setGreeting" , methods=['POST'])
def set_greeting():
    greeting_input = request.form.get("greeting")
    tx = contract_instance.functions.setGreeting(greeting_input).buildTransaction({'nonce': w3.eth.get_transaction_count(account_address)})
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash= w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print('Transaction submitted:', tx_hash.hex())
    w3.eth.wait_for_transaction_receipt(tx_hash)
    greeting = contract_instance.functions.getGreeting().call()
    return render_template("index.html", greeting=greeting)

if __name__ == '__main__':
    app.run(port=8000, host='localhost')
