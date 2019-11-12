
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from uuid import uuid4

from blockchain import Blockchain
from admin import Admin
from voter import Voter

# Creating a Web App
app = Flask(__name__)
app.secret_key = "vote4u"

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

#app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')

#admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/dashboard')
def dashboard():
    if 'admin' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('admin'))

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin'))
""" 
@app.route('/admin/adduser')
def adduser():
    if 'username' in session:
        return render_template('adduser.html')
    else:
        return redirect(url_for('admin'))
"""
@app.route('/admin/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    admin = Admin.getAdmin({'username':username,'password':password})

    if admin is None:
        session.pop('admin', None)
        return redirect(url_for('admin'))
    else:
        session['admin'] = username
        return redirect(url_for('dashboard'))

#voter
@app.route('/voter/home')
def home():
    if 'voter' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/voter/profile')
def profile():
    if 'voter' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

@app.route('/voter/logout')
def voter_logout():
    session.pop('voter', None)
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registerCandidate')
def registerCandidate():
    return render_template('registerCandidate.html')

@app.route('/voter/authenticate', methods=['POST'])
def voter_authenticate():
    username = request.form['username']
    password = request.form['password']

    voter = Voter.getVoter({'username':username,'password':password})

    if voter is None:
        session.pop('voter', None)
        return redirect(url_for('login'))
    else:
        session['voter'] = username
        return redirect(url_for('home'))

@app.route('/voter/register', methods=['POST'])
def voter_register():
    username = request.form['username']
    password = request.form['password']

    voter = Voter.getVoter({'username':username})

    if voter is None:
        voter = Voter(username = username, password = password)
        voter.addVoter()
        session['voter'] = username
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(voter = node_address, voteFor = 'Party1', constituency = 'const1')
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['voter', 'voteFor', 'constituency']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['voter'], json['voteFor'], json['constituency'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

if __name__ == '__main__':
	app.run()

'''
# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)

'''
