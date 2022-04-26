from web3 import Web3
from hexbytes import HexBytes
from config import *
import math 

hook() #  function needs be called at the start of each program execution run

def performArbitrage(): 
    arbitrage_address = '0xCcb76654cd083dE3497B80AB0115B6Da57DF6Fe5'   

    # w3 = Web3(Web3.IPCProvider()) # uses the first available IPC file 
    w3 = config['connection_uri']
    print(w3.isConnected())
    
    abi = dex_abi # ABI for DEX.sol

    dex_values = [{}, {}, {}, {}, {}] 
    i = 0
    for dex_address in config['dex_addrs']: # loop through all the dexes. 
        contract = w3.eth.contract(address=config['tokencc_addr'], abi=cc_abi)
        # The quantity of each that we currently have is qe and qt, for the quantity of ETH and TC, respectively
        # The values qe and qt are how much you (or, rather, the arbitrage.py program) have.
        dex_values[i]['qe'] = w3.eth.get_balance(config['account_address']) / (10**18)
        qe = dex_values[i]['qe']
        dex_values[i]['qt'] = contract.functions.balanceOf(config['account_address']).call() / (10**10) # this returns how much token the account address has 
        qt = dex_values[i]['qt'] 
       
        contract = w3.eth.contract(address=dex_address, abi=abi)
        dex_info = contract.functions.getDEXinfo().call()

        # The DEX values are x, y, and k
        dex_values[i]['xd'] = dex_info[5] / (10**18) # ether liquidity in dex 
        xd = dex_values[i]['xd']
        dex_values[i]['yd'] = dex_info[6] / (10**10) # token liquidity in dex 
        yd = dex_values[i]['yd']
        dex_values[i]['kd'] = dex_info[4] / (10**28)
        kd = dex_values[i]['kd']
        
        # The current prices are pe and pt, the price of ETH and TC, respectively
        # should i make call to contract or use value in config file? 
        dex_values[i]['pe'] = config['price_eth'] # contract.functions.getEtherPrice().call() / 100
        pe = dex_values[i]['pe']
        dex_values[i]['pt'] = config['price_tc'] # contract.functions.getTokenPrice().call() / 100
        pt = dex_values[i]['pt']

         # f is the percentage (out of 1.0) obtained after the DEX fees are removed
        dex_values[i]['f'] = 1 - (dex_info[7] / dex_info[8]) # 1 - numerator/denominator
        f = dex_values[i]['f']

        # The gas fees, g, this is in units of ETH. I will calculate Eth -> TC 
        transaction = contract.functions.exchangeEtherForToken().buildTransaction({
            'gas': 70000,
            'gasPrice': w3.toWei('10', 'gwei'),
            'value': w3.toWei(1, 'ether'), # the amount of gas shouldn't be dependent on how much ether is transfered 
            'from': config['account_address'],
            'nonce': w3.eth.get_transaction_count( config['account_address'] )
        })

        dex_values[i]['g'] = w3.eth.estimateGas(transaction) * 10 * (10**-9) * pe # 10 gwei per gas. 10^9 gwei in ether, multiply b y the price of ether -> USD 
        g = dex_values[i]['g']
        # print(g)

        # Our holdings are h_now (our current holdings) and h_after (our holdings after the transaction)
        # dollar amount of all the ETH and TC that it has
        dex_values[i]['h_now'] = qe*pe + qt*pt 
        h_now = dex_values[i]['h_now']
        
        # put through profit maximiaztion function
        # try trading in TC to receive eth 
        # δt =  − yd± √ (f*kd*pe/pt)
        δt1 = -yd + math.sqrt(f*kd*pe / pt) # how much token to trade in 
        δt2 = -yd - math.sqrt(f*kd*pe / pt) 
        # after holding formula: 
        after_holdings_1 = (qe+f*xd-f*kd/(yd+δt1)) * pe + (qt-δt1) * pt - (g*2) * pe # g*2 to take into account th approving of tokens 
        after_holdings_2 = (qe+f*xd-f*kd/(yd+δt2)) * pe + (qt-δt2) * pt - (g*2) * pe

        # try trading in eth to receive tc 
        δe1 = -xd + math.sqrt(f*kd*pt / pe) 
        δe2 = -xd - math.sqrt(f*kd*pt / pe) 
        after_holdings_3 = (qt+f*yd-f*kd/(xd+δe1)) * pt + (qe-δe1) * pe - g * pe
        after_holdings_4 = (qt+f*yd-f*kd/(xd+δe2)) * pt + (qe-δe2) * pe - g * pe
        
        greatest_after_holding = max(after_holdings_1, after_holdings_2, after_holdings_3, after_holdings_4)
        # compare to before holding. 
        if(greatest_after_holding > h_now):
            print('profit exists')
            dex_values[i]['h_after'] = greatest_after_holding
            if(after_holdings_1 == greatest_after_holding):
                dex_values[i]['tokenForEth'] = True 
                dex_values[i]['token_amount'] = δt1
                dex_values[i]['ether_amount'] = xd - (kd / (yd + δt1)) # etherLiquidity - (k / (tokenLiquidity + amountToken))
                dex_values[i]['g'] = g * 2
            elif(after_holdings_2 == greatest_after_holding):
                dex_values[i]['tokenForEth'] = True 
                dex_values[i]['token_amount'] = δt2
                dex_values[i]['ether_amount'] = xd - (kd / (yd + δt2))
                dex_values[i]['g'] = g * 2
            elif(after_holdings_3 == greatest_after_holding):
                dex_values[i]['tokenForEth'] = False 
                dex_values[i]['token_amount'] = yd - (kd / (xd + δe1)) # tokenLiquidity - (k / (etherLiquidity + msg.value)); 
                dex_values[i]['ether_amount'] = δe1
            elif(after_holdings_4 == greatest_after_holding):
                dex_values[i]['tokenForEth'] = False 
                dex_values[i]['token_amount'] = yd - (kd / (xd + δe2))
                dex_values[i]['ether_amount'] = δe2
        else: 
            print("no profit here")
            dex_values[i]['amount'] = 0
            dex_values[i]['tokenForEth'] = False 
            dex_values[i]['h_after'] = 0    
        i += 1
        # end for loop 

    # now compare the possible ending values of each dex. select the best one 
    winning_dex_index = -1
    best_trade_val = 0 #dex_values[i]['h_now']
    i = 0
    for x in dex_values:
        if(x['h_after'] > best_trade_val):
            best_trade_val = x['h_after']
            winning_dex_index = i
        i+=1
    if(winning_dex_index == -1):
        # no dexes have profit 
        output(0, 0, 0, 0)
    else:
        # output(ethAmt, tcAmt, fees, holdings)  # does fees take into account the dex fees? Directions say no 
        output(dex_values[winning_dex_index]['ether_amount'], dex_values[winning_dex_index]['token_amount'], dex_values[winning_dex_index]['g'], dex_values[winning_dex_index]['h_after'])

performArbitrage() 