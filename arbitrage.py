from web3 import Web3
from hexbytes import HexBytes
from config import *
#import config 

def performArbitrage(): 
    hook() #  function needs be called at the start of each program execution run

    # connected to the course server
    # w3 = Web3(Web3.IPCProvider()) # uses the first available IPC file 
    w3 = config['connection_uri']
    print(w3.isConnected())
    #print(w3local.eth.get_block('latest'))
    
    address = config['dex_addrs'][1] # address of TokenDEX
    abi = dex_abi # ABI for DEX.sol
    contract = w3.eth.contract(address=address, abi=abi)
   
    contract.functions.k().call()

    # profit formula: 
    # ethAmountAfter * ethPrice + tcAmountAfter * tcPrice > ethAmountBefore * ethPrice + tcAmountBefore * tcPrice − gasFees
    # eth.estimateGas

    
performArbitrage() 