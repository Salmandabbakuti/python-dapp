import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from flask import Flask, render_template, request

# web3.py instance
w3 = Web3(HTTPProvider("https://ropsten.infura.io/<Your infura Api Token")) #Modify
print(w3.isConnected())
contract_address = Web3.toChecksumAddress("0xcbe74e21b070a979b9d6426b11e876d4cb618daf")
key="<Your Private Key>" #Modify
account_address= Web3.toChecksumAddress("<Your Account Address>") #Modify
truffleFile = json.load(open('./build/contracts/greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

app = Flask(__name__)


@app.route("/")
def index():
    print(w3.isConnected())
    greeting = contract_instance.functions.getGreeting().call()
    print(greeting)
    contract_data = {
        'greeting': greeting
    }

    return render_template('index.html',**contract_data)

@app.route("/greet" , methods=['GET','POST'])
def ind():
    greeting = request.form.get("write") 
    tx = contract_instance.functions.greet(greeting).buildTransaction({'nonce': w3.eth.getTransactionCount(account_address)})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    tx_hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    gree = contract_instance.functions.getGreeting().call()
    contract_data = {
        'greeting': gree
        }
    return render_template('index.html', **contract_data)


if __name__ == '__main__':
    app.run(debug = True)
