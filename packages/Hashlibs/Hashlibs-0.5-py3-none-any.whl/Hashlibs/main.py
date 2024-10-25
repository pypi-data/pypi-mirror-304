def acf(selection):
    switcher = {
        0: '''
            1.Write a Python program that uses the hashlib library to create the hash of a given
            string
            2. Write a Python code for Solving Cryptographic Puzzle for leading zeros with expected
            nonce and given string
            3. Write a Python Program to generate Merkle Tree for a given set of Transactions
            4. Write a smart contract to demonstrate simple inheritance and deploy the contract on
            Remix Virtual Machine
            5. Write a smart contract to perform the addition of numbers and deploy the contract on
            Ganache.
            6. Write a smart contract to transfer funds from one Ganache Account to another.
            7. Write a Python code for extracting Live data with API Keys via Ehterscan.io
            8. Write a Python code for extracting Live data via Infura.io
            9. Write a smart contract to demonstrate the mapper function and deploy the contract on
            Sepolia Testnest via Metamask Wallet.
            10. Write a smart contract to demonstrate the use of view and pure functions and deploy
            the contract on RSK Testnest via Metamask Wallet.

        ''',
        1: '''
            Write a Python program that uses the hashlib library to create the hash of a given
            string
            import hashlib

            def create_hash(input_string):
                return hashlib.sha256(input_string.encode()).hexdigest()

            string = "Hello, World!"
            print(create_hash(string))

        ''',
        2: '''
            Write a Python code for Solving Cryptographic Puzzle for leading zeros with expected
            nonce and given string
            import hashlib

            def solve_puzzle(input_string, expected_nonce):
                nonce = 0
                while True:
                    hash = hashlib.sha256((input_string + str(nonce)).encode()).hexdigest()
                    if hash[:len(expected_nonce)] == expected_nonce:
                        return nonce
                    nonce += 1

            string = "Hello, World!"
            expected_nonce = "0000"
            print(solve_puzzle(string, expected_nonce))

        ''',
        3: '''
            Write a Python Program to generate Merkle Tree for a given set of Transactions
            import hashlib

            def create_merkle_tree(transactions):
                if len(transactions) == 0:
                    return None
                if len(transactions) == 1:
                    return transactions[0]
                if len(transactions) % 2 != 0:
                    transactions.append(transactions[-1])
                tree = []
                for i in range(0, len(transactions), 2):
                    tree.append(hashlib.sha256((transactions[i] + transactions[i + 1]).encode()).hexdigest())
                return create_merkle_tree(tree)

            transactions = ["Transaction1", "Transaction2", "Transaction3", "Transaction4"]
            print(create_merkle_tree(transactions))

        ''',
        4: '''
            Write a smart contract to demonstrate simple inheritance and deploy the contract on
            Remix Virtual Machine
            pragma solidity ^0.8.0;

            contract A {
                function foo() public pure returns (string memory) {
                    return "A";
                }
            }

            contract B is A {
                function bar() public pure returns (string memory) {
                    return "B";
                }
            }

        ''',
        5: '''
            Write a smart contract to perform the addition of numbers and deploy the contract on
            Ganache.
            pragma solidity ^0.8.0;

            contract Add {
                function add(uint a, uint b) public pure returns (uint) {
                    return a + b;
                }
            }

        ''',
        6: '''
            Write a smart contract to transfer funds from one Ganache Account to another.
            pragma solidity ^0.8.0;

            contract Transfer {
                function transfer(address payable recipient) public payable {
                    recipient.transfer(msg.value);
                }
            }

        ''',
        7: '''
            Write a Python code for extracting Live data with API Keys via Ehterscan.io
            
            import requests
import datetime
now = datetime.datetime.now()

def get_latest_block(api_key):
    url = "https://api.etherscan.io/api"
    params = {
        "module": "proxy",
        "action": "eth_getBlockByNumber",
        "tag": "latest",
        "boolean": "true",
        "apikey": api_key,
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data["result"]
        else:
            print("Request failed with status code:", response.status_code)
    except requests.RequestException as e:
        print("Request failed:", str(e))

    return None

# Replace "YOUR_API_KEY" with your actual API key
api_key = "EXK36NERHPD5487RG5F2RQI669A79VQUHR"            # Paste your API Key
print ("Current date and time : ", now.strftime("%d-%B-%Y"))
latest_block = get_latest_block(api_key)
#print(latest_block)
if latest_block is not None:
    print("Latest block information:")
    print("Block Number:", int(latest_block["number"], 16))
    print("Timestamp:", int(latest_block["timestamp"], 16))
    print("Miner Address:", latest_block["miner"])
    print("Difficulty:", int(latest_block["difficulty"], 16))
    print("Total Difficulty:", int(latest_block["totalDifficulty"], 16))
    print("Gas Limit:", int(latest_block["gasLimit"], 16))
    print("Gas Used:", int(latest_block["gasUsed"], 16))
    print("Transaction Count:", len(latest_block["transactions"]))
    print("Transactions:", latest_block["transactions"])
        ''',
        8: '''
            Write a Python code for extracting Live data via Infura.io
            
            import requests

# Infura HTTP endpoint
infura_url = 'https://mainnet.infura.io/v3/7329beded7a74ad085a6144b63645314'

# Make a request to retrieve the latest block number
response = requests.post(
    infura_url,
    json={
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
)
if response.status_code == 200:
    result = response.json()
    latest_block_number = int(result["result"], 16)  # Convert hexadecimal to decimal

    print("Latest Block Number:",latest_block_number)
    # Print the desired information
    print("Miner Address:", latest_block["miner"]) # Error
    print("Difficulty:", int(latest_block["difficulty"], 16))
    print("Total Difficulty:", int(latest_block["totalDifficulty"], 16))
    print("Gas Limit:", int(latest_block["gasLimit"], 16))
    print("Gas Used:", int(latest_block["gasUsed"], 16))
    print("Transaction Count:", len(latest_block["transactions"]))

else:
    print("Failed to retrieve the latest block. Error:", response.text)

        ''',
        9: '''
            Write a smart contract to demonstrate the mapper function and deploy the contract on
            Sepolia Testnest via Metamask Wallet.
            pragma solidity ^0.8.0;

            contract Mapper {
                mapping(address => uint) public balances;

                function deposit() public payable {
                    balances[msg.sender] += msg.value;
                }

                function withdraw(uint amount) public {
                    require(balances[msg.sender] >= amount, "Insufficient balance");
                    balances[msg.sender] -= amount;
                    payable(msg.sender).transfer(amount);
                }
            }

        ''',
        10: '''
            Write a smart contract to demonstrate the use of view and pure functions and deploy
            the contract on RSK Testnest via Metamask Wallet.
            pragma solidity ^0.8.0;

            contract ViewAndPure {
                function add(uint a, uint b) public pure returns (uint) {
                    return a + b;
                }

                function getBalance(address account) public view returns (uint) {
                    return account.balance;
                }
            }

        '''
    }

    return switcher.get(selection, "Invalid selection")


