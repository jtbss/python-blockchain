# python-blockchain
Use python to build a blockchain system.
## Install packages
Run the command
```
pip install -r requirements.txt
```
## Run
```
python node.py
```
After installing packages, open the browser with the URL `localhost:5000`
## Notice 1
There are two `node.py` files. One is `OLD_node.py`, which is the legacy version of `node.py` and it only enable users to interact with the blockchain locally in the terminal. The new `node.py` achieves APIs server, and the Web UI is allowed.
## Notice 2
The project is not perfect now because I am still working on it. To test it, it is better to delete the `blockchain.txt` file or clear the content of it before running the program.
## Install Pycrypto
Install `pycryptodome`, instead of `pycrypto`.
```
pip install pycryptodome
```
## Reference
https://www.bilibili.com/video/BV1Hb411c7oH/
