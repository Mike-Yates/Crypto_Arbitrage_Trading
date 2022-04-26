from web3 import Web3
from hexbytes import HexBytes
from config import *
#import config 

def performArbitrage(): 
    hook() #  function needs be called at the start of each program execution run
    arbitrage_address = '0xCcb76654cd083dE3497B80AB0115B6Da57DF6Fe5'   

    # w3 = Web3(Web3.IPCProvider()) # uses the first available IPC file 
    w3 = config['connection_uri']
    print(w3.isConnected())
    
    abi = dex_abi # ABI for DEX.sol
    

    dex_values = [{}, {}, {}, {}, {}] 
    # print(len(config['dex_addrs']))
    i = 0
    for dex_address in config['dex_addrs']: # loop through all the dexes. 
        contract = w3.eth.contract(address=dex_address, abi=abi)
        dex_info = contract.functions.getDEXinfo().call()

        # The DEX values are x, y, and k
        dex_values[i]['x'] = dex_info[5] / (10**18)# ether liquidity in dex 
        dex_values[i]['y'] = dex_info[6] / (10**10)# token liquidity in dex 
        dex_values[i]['k'] = dex_info[4] / (10**28)
        print(dex_values[i]['k'])
        # The current prices are pe and pt, the price of ETH and TC, respectively
        # should i make call to contract or use value in config file? 
        dex_values[i]['p_e'] = config['price_eth'] # contract.functions.getEtherPrice().call() / 100
        dex_values[i]['p_t'] = config['price_tc'] # contract.functions.getTokenPrice().call() / 100

        # The quantity of each that we currently have is qe and qt, for the quantity of ETH and TC, respectively
        # The values qe and qt are how much you (or, rather, the arbitrage.py program) have.
        dex_values[i]['qe'] = contract.functions.etherLiquidityForAddress(arbitrage_address).call() / (10**10)
        dex_values[i]['qt'] = contract.functions.tokenLiquidityForAddress(arbitrage_address).call() / (10**10)

        # Our holdings are h_now (our current holdings) and h_after (our holdings after the transaction)
        # dollar amount of all the ETH and TC that it has
        dex_values[i]['h_now'] = (dex_values[i]['qe'] * dex_values[i]['p_e'] + dex_values[i]['qt'] * dex_values[i]['p_t'])  
        
        
        # put through profit maximiaztion function, then check if it wouldve made profit or not 
        # try trading in TC 

        dex_values[i]['h_after'] = ''

        # The gas fees, g, this is in units of ETH


        # f is the percentage (out of 1.0) obtained after the DEX fees are removed
        dex_values[i]['f'] = 1 - (dex_info[7] / dex_info[8]) # 1 - numerator/denominator

        i += 1

    # check if the holdings 

    # profit formula: 
    # ethAmountAfter * ethPrice + tcAmountAfter * tcPrice > ethAmountBefore * ethPrice + tcAmountBefore * tcPrice − gasFees
    # eth.estimateGas

    
performArbitrage() 