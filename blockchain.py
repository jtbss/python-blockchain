MINING_REWARD = 10  # 挖矿奖励

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
blockchain = list([genesis_block])
open_transactions = list()
owner = 'Gamtin'
participants = {'Gamtin'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


# 计算用户的余额
def get_balance(participant):
    # 获得过往交易中用户发送出去的所有金额记录
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    # 获得在交易池中用户发出去的金额记录
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]

    # 获得过往交易中用户总共得到的数量
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_received += tx[0]
    return amount_received - amount_sent  # 获得-送出去=余额


def get_last_blockchain_value():
    """ Returns the last value of the current blockchian. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


# 校验交易
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    if sender_balance >= transaction['amount']:  # 检验发送方的余额是否多于本次交易的金额
        return True
    else:
        return False


# 新增交易
def add_transaction(recipient, sender=owner, amount=1.0):
    """
    Arguments:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :amont: The amount of coins sent with the transaction (default=1.0)
    """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


# 挖矿
def mine_block():
    # pass
    last_block = blockchain[-1]
    # 给上一个块进行 hash 计算
    hashed_block = hash_block(last_block)
    reward_transaction = {  # 系统奖励
        'sender': 'SYSTEM',
        'recipient': owner,
        'amount': MINING_REWARD
    }

    copied_transactions = open_transactions[:]  # 复制交易池记录（未加入奖励交易之前的）（深拷贝！）
    open_transactions.append(reward_transaction)
    block = {  # 创建新块
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
    }

    # 加入新块
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transacntion amount please: '))

    return tx_recipient, tx_amount


def get_user_choice():
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    # block_index = 0
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print('Please choose')
    print('0: Print full blockchain')
    print('1: Add a new transacntion value')
    print('2: Mine a new block')
    print('3: Output the blockahcin blocks')
    print('4: Output participants')
    print('h: Manipulate the chain')
    print('q: Quit')

    user_choice = get_user_choice()

    if user_choice == '1':
        # tx_amount = get_transaction_value()
        tx_data = get_transaction_value()
        recipient, amount = tx_data

        if add_transaction(recipient, amount=amount): # 如果新增交易成功
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print('-' * 20)
        print('Open transactions')
        print(open_transactions)
        print('-' * 20)
    elif user_choice == '0':
        print(blockchain)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []  # 挖矿成功，交易池清空
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':  # 模拟hack攻击
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{
                    'sender': 'A',
                    'recipient': 'B',
                    'amount': 100.0
                }]
            }
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')

    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('User\'s balance:', get_balance('Gamtin'))
else:
    print('User left!')


print('Done!')
