
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from uuid import uuid4
from bson.objectid import ObjectId
import datetime

from admin import Admin
from voter import Voter
from election import Election
from blockchain import Blockchain

# Creating a Web App
app = Flask(__name__)
app.secret_key = "vote4u-QmUWfZSo9YWNqHx5GYrGXpGJZBok5KDB7Q4JVgkub5JHQH"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/help')
def help():
    return render_template('help.html')


# Admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    admin = Admin.getAdmin({'username':username,'password':password})

    if admin is None:
        session.pop('admin', None)
        flash('Username or Password is wrong! Try Again', 'danger')
        return redirect(url_for('admin'))
    else:
        session['admin'] = username
        flash('Login successful', 'success')
        return redirect(url_for('dashboard'))

@app.route('/admin/logout')
def logout():
    session.pop('admin', None)
    flash('You have successfully logged out!', 'info')
    return redirect(url_for('index'))

@app.route('/admin/newadmin')
def newadmin():
    if 'admin' in session:
        return render_template('newadmin.html')
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/newadminDB', methods=['POST'])
def newadminDB():
    if 'admin' in session:
        username = request.form['username']
        password = request.form['password']
        admin = Admin(username, password)
        admin.addAdmin()
        return redirect(url_for('dashboard'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/dashboard')
def dashboard():
    if 'admin' in session:
        elections = Election.getElections()
        return render_template('dashboard.html', Elections = elections)
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/setElection')
def setElection():
    if 'admin' in session:
        return render_template('setElection.html')
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/setElectionDB', methods = ['POST'])
def setElectionDB():
    if 'admin' in session:
        title = request.form['title']
        description = request.form['description']
        edate = datetime.datetime.strptime(request.form['electionDate'], '%Y-%m-%d')
        start = request.form['start']
        end = request.form['end']
        candidates = []

        election = Election(title, description, edate, start, end, candidates)
        election.setElection()
        flash('Election Added successfully', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/approveVoter')
def approveVoter():
    if 'admin' in session:
        voters = Voter.getVoters({'status':False})
        return render_template('approveVoter.html', Voters=voters)
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/view/<voterID>/')
def view(voterID):
    if 'admin' in session:
        voter = Voter.getVoter({'_id': ObjectId(voterID)})
        return render_template('viewVoter.html', Voter = voter)
    else:
        return redirect(url_for('admin'))

@app.route('/admin/approve/<voterID>/')
def approvedVoter(voterID):
    if 'admin' in session:
        Voter.updateVoter({'_id':ObjectId(voterID)}, {'$set':{'status':True}})
        flash('Voter approved', 'success')
        return redirect(url_for('approveVoter'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/approveCandidate')
def approveCandidate():
    if 'admin' in session:
        elections = Election.getElections()
        return render_template('approveCandidate.html', Elections=elections)
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))

@app.route('/admin/approveCandidateDB/<status>/<electionID>/<candidateID>/')
def approveCandidateDB(status, electionID, candidateID):
    if 'admin' in session:
        if status == "1" :
            Election.updateElection({'_id':ObjectId(electionID), 'candidates.id': candidateID}, {'$set': {'candidates.$.status': True}})
        elif status == "0"  :
            Election.updateElection({'_id':ObjectId(electionID)}, {'$pull': {'candidates':{'id': candidateID}}})

        return redirect(url_for('approveCandidate'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('admin'))


# Voter
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/voter/authenticate', methods=['POST'])
def voter_authenticate():
    username = request.form['username']
    password = request.form['password']

    voter = Voter.getVoter({'username':username,'password':password})

    if voter is None:
        session.pop('voter', None)
        flash('Username or Password is wrong! Try Again', 'danger')
        return redirect(url_for('login'))
    else:
        session['voter'] = username
        flash('Login successful', 'success')
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
        flash('Registration successful. Update profile', 'info')
        return redirect(url_for('home'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/voter/logout')
def voter_logout():
    session.pop('voter', None)
    flash('You have successfully logged out!', 'warning')
    return redirect(url_for('index'))

@app.route('/voter/home')
def home():
    if 'voter' in session:
        username = session['voter']
        voter = Voter.getVoter({'username':username})
        elections = Election.getElections()
        return render_template('home.html', Voter = voter, Elections = elections)
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/voter/profile')
def profile():
    if 'voter' in session:
        username = session['voter']
        voter = Voter.getVoter({'username':username})
        return render_template('profile.html',Voter = voter)
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/voter/update', methods=['POST'])
def voter_update():
    if 'voter' in session:
        name = request.form['name']
        DOB = request.form['DOB']
        address = request.form['address']
        state = request.form['state']
        mobile = request.form['mobile']
        email = request.form['email']
        aadhaar = request.form['aadhaar']
        status = False

        new = {
            'name' : name,
            'DOB' : DOB,
            'address' : address,
            'state' : state,
            'mobile' : mobile,
            'email' : email,
            'aadhaar' : aadhaar,
            'status' : status
        }
        Voter.updateVoter({'username':session['voter']}, {'$set': new})
        flash('Profile updated successfully', 'info')
        return redirect(url_for('profile'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))


# Election
@app.route('/election/<electionID>')
def election(electionID):
    if 'voter' in session:
        election = Election.getElection({'_id':ObjectId(electionID)})
        return render_template('election.html', Election = election)
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/registerCandidate', methods = ['POST'])
def registerCandidate():
    if 'voter' in session:
        voter = Voter.getVoter({'username':session['voter']})
        electionID = request.form.get('electionID')
        election = Election.getElection({'_id':ObjectId(electionID)})
        if datetime.datetime.now() + datetime.timedelta(days=2) >= election['date']:
            flash("Candiate Registration is closed", 'danger')
        else :
            candidate = {
                'id' : str(uuid4()).replace('-', ''),
                'voterID' : voter['_id'],
                'name' : voter['name'],
                'slogan' : request.form['slogan'],
                'representing' : request.form['representing'],
                'qualification' : request.form['qualification'],
                'status' : False
            }
            Election.updateElection({'_id':ObjectId(electionID)}, {'$push': {'candidates': candidate}})
            flash('Your registration details as candidate are successfully recorderd', 'info')
        return redirect(url_for('home'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/vote/<electionID>/<candidateID>/')
def vote(electionID, candidateID):
    if 'voter' in session:
        voter = Voter.getVoter({'username': session['voter']})
        election = Election.getElection({'_id': ObjectId(electionID)})
        
        if election['date'].date() > datetime.datetime.now().date():
            flash(f"Election not yet started. Come back on {election['date'].date()}", 'danger')
        elif election['date'].date() < datetime.datetime.now().date():
            flash(f"Election ended on {election['date'].date()}", 'danger')
        elif election['date'].date() == datetime.datetime.now().date():
            if str(datetime.datetime.now().time())[:5] > election['starttime'] and str(datetime.datetime.now().time())[:5] < election['endtime']:
                flash('Vote recorded successfully', 'success')
                vote = {
                    'timestamp': str(datetime.datetime.now()),
                    'electionID': electionID,
                    'candidateID': candidateID,
                    'voter': str(voter['_id'])
                }
                response = Blockchain.add_transaction(vote)
                flash(response, 'info')
            else:
                flash(f"You can vote between {election['starttime']} to {election['endtime']}", 'info')
        return redirect(url_for('home'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))

@app.route('/result/<electionID>/')
def result(electionID):
    if 'admin' in session:
        election = Election.getElection({'_id': ObjectId(electionID)})
        if election['date'].date() < datetime.datetime.now().date():
            pass
        elif election['date'].date() == datetime.datetime.now().date() and election['endtime'] < str(datetime.datetime.now().time())[:5]:
            pass
        else:
            flash('Election not yet ended! Wait for Election to end to calculate result', 'warning')
            return redirect(url_for('dashboard'))

        result = {}
        response = Blockchain.get_chain()
        for block in response['chain']:
            IpfsBlock = Blockchain.get_by_hash(block['IpfsHash'])
            for txn_hash in IpfsBlock['data']:
                txn = Blockchain.get_by_hash(txn_hash)
                if txn['electionID'] == electionID:
                    if txn['candidateID'] not in result:
                        result[txn['candidateID']] = 1
                    else:
                        result[txn['candidateID']] += 1
        Election.updateElection({'_id':ObjectId(electionID)}, {'$set':{'result':result}})
        flash('Result calculated and published.', 'info')
        return redirect(url_for('dashboard'))
    else:
        flash('You need to Login first!', 'warning')
        return redirect(url_for('login'))


# Running the app
if __name__ == '__main__':
	app.run()

