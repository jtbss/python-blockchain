from functools import reduce
import json
# import pickle

from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10.0  # 挖矿奖励

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0) # 创世块
        self.chain = [genesis_block]  # 初始化 blockchain
        self.open_transactions = []  # 交易池
        self.load_data()
        self.hosting_node = hosting_node_id

    # 加载区块链数据
    def load_data(self):
        """ 1. mode 'rb' read the binary data
            2. use pickle to read and write data is better than using json
            3. because using json to load data may occur some order problem
        """
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                # file_content = pickle.loads(f.read())

                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                # if not file_content:
                #     return
                blockchain = json.loads(file_content[0][:-1]) # 加[:-1]是为了去掉结尾的 \n
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    # converted_tx = [OrderedDict([ # 这个步骤很重要，因为所有的 transactions 里面的字典数据都是使用 OrderedDict 生成的，和普通的 dict 不一样，不加这一步的话会导致验证区块失败
                    #                     ('sender', tx['sender']),
                    #                     ('recipient', tx['recipient']),
                    #                     ('amount', tx['amount'])
                    #                 ]) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'],
                        block['previous_hash'],
                        converted_tx,
                        block['proof'],
                        block['timestamp']
                    )
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain  # 存储变量

                open_transactions = json.loads(file_content[1])
                updated_open_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_open_transactions.append(updated_transaction)
                self.open_transactions = updated_open_transactions
        except (IOError, IndexError): # 处理文件为空的问题
            print('Handled exception...')
        finally:
            print('Cleanup!')

    # 将交易保存到本地文件中
    def save_data(self):
        """ 1. mode 'wb' for wirting binary data to files
            2. use pickle to dumps binary data
        """
        try:
            with open('blockchain.txt', mode='w') as f:
                # 因为 block 是 Block 类的对象，不可以直接使用 json.dumps 来转化为 String 类型
                # 所以需要将 blockchian 列表里面的所有 block 对象转化为 dict，使用 block.__dict__
                saveable_chain = [block.__dict__
                                for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp)
                                                for block_el in self.chain]]
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]

                f.write(json.dumps(saveable_chain))
                f.write('\n')
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')

    # 工作量证明 Proof-of-work
    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0

        verifier = Verification()
        while not verifier.valid_proof(self.open_transactions, last_hash, proof):
            proof +=1
        return proof

    # 计算用户的余额
    def get_balance(self):
        participant = self.hosting_node

        # 获得过往交易中用户发送出去的所有金额记录
        tx_sender = [[tx.amount
                    for tx in block.transactions if tx.sender == participant] for block in self.chain]
        # 获得在交易池中用户发出去的金额记录
        open_tx_sender = [tx.amount
                        for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender, 'tx_sender')

        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt), tx_sender, 0) # 简化版

        # 获得过往交易中用户总共得到的数量
        tx_recipient = [[tx.amount
                        for tx in block.transactions if tx.recipient == participant] for block in self.chain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt), tx_recipient, 0) # 简化版
        print(tx_recipient, 'tx_recipient')

        return amount_received - amount_sent  # 获得 - 送出去 = 余额

    # 获取最后一个区块
    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchian. """
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    # 新增交易
    def add_transaction(self, recipient, sender, amount=1.0):
        """
        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amont: The amount of coins sent with the transaction (default=1.0)
        """
        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    # 挖矿
    def mine_block(self):
        """Create a new block and add open transactions to it."""
        last_block = self.chain[-1]
        hashed_block = hash_block(last_block)  # 计算上一个块的 hash 值
        proof = self.proof_of_work() # PoW只针对 open_transactions 里的交易，不包括系统奖励的交易

        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD) # 系统奖励

        copied_transactions = self.open_transactions[:]  # 复制交易池记录（未加入奖励交易之前的）（深拷贝！）
        copied_transactions.append(reward_transaction) # 将系统奖励的coins加进去
        block = Block(len(self.chain), hashed_block, copied_transactions, proof) # 创建新块

        # 加入新块
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True


