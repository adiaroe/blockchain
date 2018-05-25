MINING_REWARD = 10

genesis_block =  {
    'previous_hash':'', 
    'index':0, 
    'transactions':[]
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Adithya'
participants =  {'Adithya'}


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0.0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0.0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent


def get_last_blockchian_value():
    """To return the last value in the current Blockchain"""
    if (len(blockchain) < 1):
        return None
    return blockchain[-1]


def add_transaction(recipient, sender = owner, amount = 1.0):
    transaction =  {
        'sender':sender, 
        'recipient':recipient, 
        'amount':amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def hash_block(block):
    return '-'.join([str(block[key])for key in block])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction =  {
        'sender':'MINING', 
        'recipient':owner, 
        'amount':MINING_REWARD
    }
    duplicate_open_transactions = open_transactions[:]
    duplicate_open_transaction.append(reward_transaction)
    block =  {
        'previous_hash':hashed_block, 
        'index':len(blockchain), 
        'transactions':duplicate_open_transaction
    }
    blockchain.append(block)
    return True


def get_transaction_info():
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Enter the transaction amount: "))
    return (tx_recipient, tx_amount)


def verify_chain():
    for (index, block)in enumerate(blockchain):
        if (index == 0):
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def print_blockchain_elements():
    """Output all the blocks of the current blockchain"""
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 30)


def verify_transactions():
    return all([verify_transaction(tx)for tx in open_transactions])


flag = True

while flag:
    print('Choose one of the following:')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output Blockchain blocks')
    print('4: Output the list of participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    
    user_choice = input('Your choice: ')

    if (user_choice == '1'):
        tx_info = get_transaction_info()
        recipient, amount = tx_info
        if add_transaction(recipient, amount = amount):
            print("Added Transaction!")
        else:
            print("Transaction Failed!")
        print(open_transactions)
    elif (user_choice == '2'):
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if (verify_transaction()):
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if (len(blockchain) >= 1):
            blockchain[0] =  {
                'previous_hash':'', 
                'index':0, 
                'transactions':[ {'sender':'ushe', 'recipient':'Adithya', 'amount':10.0}]
            }
    elif (user_choice == 'q'):
        flag = False
    else:
        print("Invalid input!!!")
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid Blockchain')
        break
    print(get_balance('Adithya'))
else:
    print('User Aborted!')
