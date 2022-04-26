from web3 import Web3
from hexbytes import HexBytes
from config import *
#import config 

def performArbitrage(): 
    hook() #  function needs be called at the start of each program execution run
    # w3 = Web3(Web3.WebsocketProvider('wss://andromeda.cs.virginia.edu/geth')) 
    #w3remote = Web3(Web3.WebsocketProvider('wss://andromeda.cs.virginia.edu/geth'))
    #w3local = Web3(Web3.IPCProvider('\\.\pipe\geth.ipc'))
    #print(w3remote.isConnected())

    # connected to the course server
    w3 = Web3(Web3.IPCProvider()) # uses the first available IPC file 
    print(w3.isConnected())
    #print(w3local.eth.get_block('latest'))
    
    address= config['dex_addrs'][2] # address of TokenDEX
    # interesting enough, the dex abi provided on the collab home page and the config.py file are different 
    abi = dex_abi # ABI for DEX.sol

    contract = w3.eth.contract(address=address, abi=abi)

    # print(contract.functions.dexes(4).call()) # we can call a function on it 
    
    # profit formula: 
   
    print(contract.functions.etherLiquidity().call())
    # ethAmountAfter * ethPrice + tcAmountAfter * tcPrice > ethAmountBefore * ethPrice + tcAmountBefore * tcPrice − gasFees
    # eth.estimateGas

    
performArbitrage() 