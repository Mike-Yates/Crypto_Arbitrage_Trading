import hexbytes

# The configuration options to connect to the blockchain and the DEXes
config = {
    # the address of the Ethereum account that this program is controlling – 
    # it is the balance that this account has, in both ETH and TC, that constitutes the holdings of this account
    'account_address': '0x5cdaceb62d1de4cc57dfab6039379439450c4a4b', 

    # the (decrypted) private key for that account
    'account_private_key': hexbytes.HexBytes('c9376204f7632f8379cda4c336a0463f2f196665f9792f6387fbec5c80beeb13'),
    
    # whether the connection URI (which is on the next line in this file) is a geth.ipc file or a URL – this will determine how the web3 provider is created
    'connection_is_ipc': True,

    # connect to the blockchain – this will either be the path to a geth.ipc file or a URL to the course server;
    # you either have to pass it to a Web3.IPCProvider() call or a Web3.WebsocketProvider() call
    'connection_uri': '/path/to/geth.ipc',


    'price_eth': 100.00, # the current price of ETH, in USD, as a float – this is without all the extra decimal places
    'price_tc': 10.0, # the current price of TC, in USD, as a float – this is without all the extra decimal places
    
    # the smart contract addresses of the various TokenDEX smart contracts; there will be at least two in this list
    'dex_addrs': ['0x123456789abcdef0123456789abcdef123456789', '0x123456789abcdef0123456789abcdef123456789', 
                  '0x123456789abcdef0123456789abcdef123456789', '0x123456789abcdef0123456789abcdef123456789',
                  '0x123456789abcdef0123456789abcdef123456789'],
    'tokencc_addr': '0x123456789abcdef0123456789abcdef123456789', # the smart address of the TokenCC smart contract
}

# This should do nothing for now -- we are going to use it when grading.  You
# should call this first thing once the program starts, but after the import
# lines.
def hook():
    pass

# This will print the output into the format required by the homework.  It
# should not be changed.
def output(ethAmt, tcAmt, fees, holdings):
    if ethAmt == 0 and tcAmt == 0:
        print("No profitable arbitrage trades available")
        return
    assert ethAmt * tcAmt < 0, "Exactly one of ethAmt and tcAmt should be negative, the other positive"
    if ethAmt < 0:
        print("Exchanged %.4f ETH for %.4f TC; fees: %.2f USD; prices: ETH %.2f USD, TC: %.2f USD; holdings: %.2f USD" %
              (ethAmt, tcAmt, fees, config['price_eth'], config['price_tc'], holdings))
    else:
        print("Exchanged %.4f TC for %.4f ETH; fees: %.2f USD; prices: ETH %.2f USD, TC: %.2f USD; holdings: %.2f USD" %
              (tcAmt, ethAmt, fees, config['price_eth'], config['price_tc'], holdings))

# This is the ABI for DEX.sol
dex_abi = '[{"anonymous":false,"inputs":[],"name":"liquidityChangeEvent","type":"event"},{"inputs":[],"name":"addLiquidity","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenAmount","type":"uint256"},{"internalType":"uint256","name":"_feeNumerator","type":"uint256"},{"internalType":"uint256","name":"_feeDenominator","type":"uint256"},{"internalType":"address","name":"_erc20token","type":"address"},{"internalType":"address","name":"_etherpricer","type":"address"}],"name":"createPool","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"erc20TokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"etherLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"who","type":"address"}],"name":"etherLiquidityForAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"etherPricerAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"exchangeEtherForToken","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"}],"name":"exchangeTokenForEther","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"feeDenominator","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feeNumerator","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feesEther","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"feesToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDEXinfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"string","name":"","type":"string"},{"internalType":"string","name":"","type":"string"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getEtherPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPoolLiquidityInUSDCents","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTokenCCAbbreviation","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getTokenPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"k","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountEther","type":"uint256"}],"name":"removeLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"p","type":"address"}],"name":"setEtherPricer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenDecimals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenLiquidity","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"who","type":"address"}],"name":"tokenLiquidityForAddress","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]';

# This is the ABI for the TokenCC contract (formally for ERC20.sol and IERC165.sol combined)
cc_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]';

# This function will attempt to ascertain why a transaction reverted, and
# print that out.
def printRevertReason(w3,txhash):
    tx = w3.eth.get_transaction(txhash)
    replay_tx = {
        'to': tx['to'],
        'from': tx['from'],
        'value': tx['value'],
        'data': tx['input'],
    }
    # replay the transaction locally:
    try:
        w3.eth.call(replay_tx, tx.blockNumber - 1)
    except Exception as e: 
        print(e)