from collections import OrderedDict
from utility.printable import Printable

class UTXO(Printable):
  def __init__(self, id, index, amount, sender, recipient):
    self.id = id
    self.index = index
    self.amount = amount
    self.sender = sender
    self.recipient = recipient
