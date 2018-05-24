genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Adithya'


def get_last_blockchian_value():
    """To return the last value in the current Blockchain"""
    if(len(blockchain) < 1):
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }
    blockchain.append(block)


def get_transaction_info():
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Enter the transaction amount: "))
    return (tx_recipient, tx_amount)


def verify_chain():
    for (index, block) in enumerate(blockchain):
        if(index == 0):
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
        print('-'*30)


flag = True

while flag:
    print('Choose one of the following:')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output Blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    
    user_choice = input('Your choice: ')

    if(user_choice == '1'):
        tx_info = get_transaction_info()
        recipient, amount = tx_info
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif(user_choice == '2'):
        mine_block()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == 'h':
        if(len(blockchain)>=1):
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'ushe', 'recipient':'Adithya', 'amount': 10.0}]
            }
    elif(user_choice == 'q'):
        flag = False
    else:
        print("Invalid input!!!")
    if not verify_chian():
        print_blockchain_elements()
        print('Invalid Blockchain')
        break
else:
    print('User Aborted!')
