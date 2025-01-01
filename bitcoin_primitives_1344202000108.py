
import hashlib
import time
    
     # Function Νο 1 that implements the mining process of a new block from the blockchain.
     # It repeatedly generates a hash for the block until the nonce that satisfies the specified target is found.
     # It returns the nonce that was found.
def mining(merkle_root_hash, previous_block_hash, difficulty):
    
    nonce = 0
    leading_zeros = '0' * difficulty

    start_time = time.time()  #Start Time
    
    while True:    # Repetition until the nonce is found
        header = merkle_root_hash + previous_block_hash + str(nonce)  # Create header for block
        block_hash = hashlib.sha256(header.encode()).hexdigest()  # Create hash for block
        
        if block_hash.startswith(leading_zeros):# Check if the hash satisfies the target
            end_time = time.time()  # Final Time
            mining_time = end_time - start_time  
            print(f"Nonce found: {nonce}")
            print(f"Mining time: {mining_time} seconds")
            return nonce  # Return the nonce if found successfully.
        
        nonce += 1     # Increment the nonce for the next mining round.
    
    #Function No2 that constructs the Merkle tree from a list of transactions.
    #It returns a list of lists representing the levels of the Merkle tree.
    
def construct_merkle_tree(transactions):   # Initialize the levels with the transactions
    
    levels = [transactions]
    while len(levels[-1]) > 1:
        current_level = levels[-1]  # The current list of transactions
        new_level = []  # The new list that will result from the function
        for i in range(0, len(current_level), 2):
            tx1 = current_level[i]
            if i + 1 < len(current_level):
                tx2 = current_level[i + 1]
                txs = tx1 + tx2
            else:
                txs = tx1 + tx1
            hash_val = hashlib.sha256(txs.encode()).hexdigest()
            new_level.append(hash_val)
        levels.append(new_level)  # Adding the new list to the levels of the Merkle tree
    return levels

# Function Νο3 that generates the proof of existence of a transaction in the Merkle tree
# It returns a dictionary with pairs that include the level and the sibling node of the transaction

def generate_proof(transaction, merkle_tree):
    
    proof = {}  # Initializing the dictionary for the proof
    for level_index, level in enumerate(merkle_tree[:-1]):
        for i, node_hash in enumerate(level):
            if i % 2 == 0:
                next_level = merkle_tree[level_index + 1]
                sibling_index = i + 1 if i + 1 < len(level) else i  # The index of the sibling node
            if sibling_index < len(next_level):  # Checking if the sibling node exists
                sibling_hash = next_level[sibling_index]
                if node_hash == transaction:
                    proof[level_index + 1] = sibling_hash
                elif sibling_hash == transaction:
                    proof[level_index + 1] = node_hash
    return proof

previous_block = "00000000000000"
difficulty = 4
transactions = ["Tx1", "Tx2", "Tx3", "Tx4", "Tx5", "Tx6", "Tx7"]
merkle_tree = construct_merkle_tree(transactions)
merkle_root = merkle_tree[-1][0]  # The Merkle root is located at the last level and the first element of the list

start_time = time.time()  # Start time
nonce = mining(merkle_root, previous_block, difficulty)
end_time = time.time()  # End time
time_taken = end_time - start_time  # Calculate mining time

proof = generate_proof("Tx6", merkle_tree)

print("Merkle tree: ", merkle_tree)
print("Merkle root: ", merkle_root)
print("Nonce: ", nonce)
print("Time taken: ", time_taken) 
print("The proof that contains the pairs: ", proof)
for level, pair in proof.items():
    print(f"Level {level}: {pair}")
