import functools
import hashlib as hl
from collections import OrderedDict

from hash_util import hash_string_256, hash_block

MINING_REWARD = 10

# creating a genesis block which denotes the starting block without any transactions
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}
# initializing the current blockchain with the genesis block
blockchain = [genesis_block]
# store open transactions to evnetually mine a block
open_transactions = []
owner = 'Adithya'
# intializing the participant list with the owner's name
participants = {owner}


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    """Get the remaining balance of a particular participant

    Arguments:
        participant: The participant for whom we calculate the for
    """
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    # print(tx_sender)
    amount_sent = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    return (amount_received - amount_sent)


def get_last_blockchian_value():
    """To return the last value in the current Blockchain"""
    if (len(blockchain) < 1):
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    duplicate_open_transactions = open_transactions[:]
    duplicate_open_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': duplicate_open_transactions,
        'proof': proof
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
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is Invalid !  !  ! ')
            return False
    return True


def print_blockchain_elements():
    """Output all the blocks of the current blockchain"""
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print(' - ' * 30)


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


flag = True

while flag:
    print('Choose one of the following:')
    print('1:Add a new transaction value')
    print('2:Mine a new block')
    print('3:Output Blockchain blocks')
    print('4:Output the list of participants')
    print('5:Check transaction validity')
    print('h:Manipulate the chain')
    print('q:Quit')

    user_choice = input('Your choice:')

    if (user_choice == '1'):
        tx_info = get_transaction_info()
        recipient, amount = tx_info
        if add_transaction(recipient, amount=amount):
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
        if (verify_transactions()):
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[1] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'ushe', 'recipient': 'Adithya', 'amount': 10.0}]
            }
    elif (user_choice == 'q'):
        flag = False
    else:
        print("Invalid input!!!")
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid Blockchain')
        break
    print(f"Balance of {owner}: {get_balance(owner):6.2f}")
else:
    print('User Aborted ! ')
