from web3 import Web3
from hexbytes import HexBytes
import config.py

def performArbitrage(): 
    hook()
    print("performArbitrage() has been called") 
    # w3 = Web3(Web3.WebsocketProvider('wss://andromeda.cs.virginia.edu/geth')) 
    #w3remote = Web3(Web3.WebsocketProvider('wss://andromeda.cs.virginia.edu/geth'))
    #w3local = Web3(Web3.IPCProvider('\\.\pipe\geth.ipc'))
    #print(w3remote.isConnected())

    # connected to the course server
    w3local = Web3(Web3.IPCProvider()) # uses the first available IPC file 
    print(w3local.isConnected())
    #print(w3local.eth.get_block('latest'))
    

    
    address='0x0123456789abcdef0123456789abcdef01234567' # address of TokenDEX
    abi='[...]'

    # profit formula: 
    # ethAmountAfter * ethPrice + tcAmountAfter * tcPrice > ethAmountBefore * ethPrice + tcAmountBefore * tcPrice − gasFees
    # eth.estimateGas

    
performArbitrage() 