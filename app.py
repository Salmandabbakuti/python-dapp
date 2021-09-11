import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from flask import Flask, render_template, request

# web3.py instance
w3 = Web3(HTTPProvider("https://testnet-rpc.gochain.io/")) #for cotract deployed on gochain
# w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/<api key>")) # for contract deployed on ropsten
print('Web3 Connected:',w3.isConnected())
contract_address = Web3.toChecksumAddress("0x452b60571ae66f17e597faf49bbc8444884b60b9") #contract address deployed on gochain
# contract_address = Web3.toChecksumAddress("0xcbe74e21b070a979b9d6426b11e876d4cb618daf") #contract address deployed on roposten
key="" #Modify
account_address= Web3.toChecksumAddress("") #Modify
truffleFile = json.load(open('./build/contracts/greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

app = Flask(__name__)


@app.route("/")
def index():
    print('Web3 Connected: ',w3.isConnected())
    greeting = contract_instance.functions.getGreeting().call()
    contract_data = {
        'greeting': greeting
    }
    return render_template('index.html',**contract_data)

@app.route("/greet" , methods=['GET','POST'])
def greet():
    greeting_input = request.form.get("write")
    print(greeting_input)
    tx = contract_instance.functions.greet(greeting_input).buildTransaction({'nonce': w3.eth.getTransactionCount(account_address)})
    signed_tx = w3.eth.account.signTransaction(tx, key)
    tx_hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print('Transaction submitted:', tx_hash.hex())
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    greeting = contract_instance.functions.getGreeting().call()
    contract_data = {
        'greeting': greeting
        }
    return render_template('index.html', **contract_data)


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
