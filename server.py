from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# import sqlite3
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import requests
from datetime import date, datetime
from forex_python.converter import CurrencyRates
import re


currency = CurrencyRates()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# dbs = sqlite3.connect("users.db")

# cursor = dbs.cursor()


#to be codded 
#login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Database Table Creation Section
# app.app_context().push()

#to create tables
#inside terminal
# from server import app, db
# app.app_context().push()
# db.create_all()

#Sign up table which contains data of user
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    phoneno = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


# cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username varchar(250) NOT NULL UNIQUE, fname varchar(250), lname varchar(250), phoneno varchar(250), email varchar(250), password varchar(250))")
   
    # usernamess = db.relationship('userBalance', backref='user')

class remBal(UserMixin, db.Model):
    # __tablename__ = "users_balances"
    # username = db.Column(db.String(100), primary_key=True, db.ForeignKey('user.username'))
    username = db.Column(db.String(100), primary_key=True)
    balance = db.Column(db.Integer)

# cursor.execute("CREATE TABLE balances (username varchar(250) PRIMARY KEY, balance INTEGER)")

class clientTranscation(UserMixin, db.Model):
    # __tablename__ = "client_transcation"
    transcation_id = db.Column(db.String(100), primary_key=True)
    f_username = db.Column(db.String(100))
    t_username = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))

class lnAct(UserMixin, db.Model):
    # __tablename__ = "users_balances"
    # username = db.Column(db.String(100), primary_key=True, db.ForeignKey('user.username'))
    username = db.Column(db.String(100), primary_key=True)
    debt = db.Column(db.Integer)
    credits = db.Column(db.Integer)
    score = db.Column(db.Integer)

class lnTranscation(UserMixin, db.Model):
    # __tablename__ = "client_transcation"
    transcation_id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100))
    amount = db.Column(db.String(100))
    rem_debt = db.Column(db.Integer)
    intrest = db.Column(db.Integer)
    date = db.Column(db.String(100))
    time = db.Column(db.String(100))

class Erng(UserMixin, db.Model):
    username = db.Column(db.String(100), primary_key=True)
    loan_intrest = db.Column(db.Integer)
    transcationm_intrest = db.Column(db.Integer)
    topup_fee = db.Column(db.Integer)
    total = db.Column(db.Integer)
    
class Admin(UserMixin, db.Model):
    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(100))

class BnkAcc(UserMixin, db.Model):
    # __tablename__ = "client_transcation"
    ac_no = db.Column(db.Integer, primary_key=True)
    ifsc = db.Column(db.String(100))
    balance = db.Column(db.Integer)

#other class section

def password_validation(password):
    flag = 0

    while True:
        if (len(password)<=8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif not re.search("[_@$]" , password):
            flag = -1
            break
        elif re.search("\s" , password):
            flag = -1
            break
        else:
            flag = 0
            print("Valid Password")
            break
    if flag == 0:
        return 1
    else:
        return 0



@app.route("/login_or_sign_up", methods=["GET", "POST"])
def login_or_sign_up():

    #login
    if request.method == "POST":
        if request.form["submit"] == "log_in":


            l_username = request.form["l_username"]
            l_password = request.form["l_password"]
            print(l_username, l_password) 

            user = User.query.filter_by(username=l_username).first()
            if not user:
                flash("this username does not exist, Please Register")
                return redirect(url_for('login_or_sign_up'))
            elif not check_password_hash(user.password, l_password):
                flash("Password incorrect, PLease Try Again")
                return redirect(url_for('login_or_sign_up'))
            else:

                login_user(user)
                return redirect(url_for('home'))
        
        #sign up
        if request.form["submit"] == "Sign_up":

            if User.query.filter_by(username=request.form.get('s_username')).first():
            #User already exists
                flash("You've already signed up with that username, log in instead!")
                return redirect(url_for('login_or_sign_up'))


            s_username = request.form["s_username"]
            s_fname = request.form["s_fname"]
            s_lname = request.form["s_lname"]
            s_phoneno = request.form["s_phoneno"]
            s_email = request.form["s_email"]
            s_password = request.form["s_password"]
            print(s_username, s_fname, s_lname, s_phoneno, s_email, s_password)

            if password_validation(s_password) == 0:
                flash("Please match the password constrains while choosing password")
                return redirect(url_for('login_or_sign_up'))


            hash_and_salted_password = generate_password_hash(
                s_password,
                method='pbkdf2:sha256',
                salt_length=8
            )

            new_user = User(
                username = s_username,
                fname = s_fname,
                lname = s_lname,
                phoneno = s_phoneno,
                email = s_email,
                password = hash_and_salted_password
            )
            db.session.add(new_user)
            db.session.commit()

            # cursor.execute(f"INSERT INTO users VALUES({s_username}, {s_fname}, {s_lname}, {s_phoneno}, {s_email}, {hash_and_salted_password})")

            new_ub = remBal(
                username = s_username,
                balance = 1000
            )
            db.session.add(new_ub)
            db.session.commit()

            new_lact = lnAct(
                username = s_username,
                debt = 0,
                credits = 500,
                score = 500
            )

            db.session.add(new_lact)
            db.session.commit()
            
            # cursor.execute(f"INSERT INTO balances VALUES({s_username}, 100)")
            login_user(new_user)
            return redirect(url_for("home"))

            #database of new user
            # modelName = s_username + "db"
            # class modelName(db.Model):
            #     transcation_id = db.Column(db.Integer, primary_key=True)
            #     transaction_amt = db.Column(db.Integer)
            #     remaning_amt = db.Column(db.Integer)
            # # db.create_all()
            # modelName.__table__.create(db.session.bind, checkfirst=True)

            print("new user data inserted into database")


    return render_template("loginorsignup.html", logged_in=current_user.is_authenticated)

@app.route("/")
def main():
    return redirect(url_for('login_or_sign_up'))


#home page or main landing page
@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    # print(current_user.username)
    cu_bal = remBal.query.filter_by(username=current_user.username).first()
    cur_ln = lnAct.query.filter_by(username=current_user.username).first()
    return render_template("home.html", username=current_user.username, bal = cu_bal.balance, cur_ln=cur_ln, logged_in=True)

#logout
@app.route('/logout')
def logout():
    logout_user()
    c_u = "null"
    return redirect(url_for('login_or_sign_up'))




#pay section

#username pay
@app.route("/pay/username", methods=["GET", "POST"])
@login_required
def pay_username():
    fuser = remBal.query.filter_by(username=current_user.username).first()
    admn = Erng.query.filter_by(username="admin").first()
    if request.method == 'POST':
        p_username = request.form["username"]
        p_amount = int(request.form["amount"])
        # remBal.query.filter_by(username=request.form.get('l_username')).first()
        # User.query.filter_by(username=l_username).first()
        print(fuser.balance, p_username, p_amount)
        if fuser.balance < p_amount:
            flash("Insuffecient amount")
            return redirect(url_for('pay_username'))
        else:
            tuser = remBal.query.filter_by(username=p_username).first()
            if not tuser:
                flash("Username dosent exist")
                return redirect(url_for('pay_username'))
            else:
                #updating database
                tuser.balance += p_amount
                fuser.balance -= p_amount
                admn.transcationm_intrest = 0
                db.session.commit()
                flash(f"{p_amount} sucessfully sent to {p_username}")
                obj = clientTranscation.query.all()
                tno = int(obj[-1].transcation_id)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                f_username = fuser.username
                new_trans = clientTranscation(
                    transcation_id = tno + 1,
                    f_username = f_username,
                    t_username = p_username,
                    amount = p_amount,
                    date = date.today(),
                    time = current_time
                )
                db.session.add(new_trans)
                db.session.commit()




    return render_template("pay_username.html", username=current_user.username, logged_in=True, bal = fuser.balance)

#qr pay
@app.route("/pay/qr", methods=["GET", "POST"])
@login_required
def pay_qr():
    fuser = remBal.query.filter_by(username=current_user.username).first()
    return render_template("pay_qr.html",  username=current_user.username, bal = fuser.balance)

#phone no pay
@app.route("/pay/phoneno", methods=["GET", "POST"])
@login_required
def pay_phoneno():
    fuser = remBal.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        p_phonenumber = request.form["pno"]
        p_amount = int(request.form["amount"])
        # remBal.query.filter_by(username=request.form.get('l_username')).first()
        # fu = User.query.filter_by(phoneno=p_phonenumber).first()
        if fuser.balance < p_amount:
            flash("Insuffecient amount")
            return redirect(url_for('pay_phoneno'))
        else:
            tu = User.query.filter_by(phoneno=p_phonenumber).first()
            if not tu:
                flash("Phone Number dosent exist")
                return redirect(url_for('pay_username'))
            else:
                #updating database
                tuser = remBal.query.filter_by(username=tu.username).first()
                tuser.balance += p_amount
                fuser.balance -= p_amount
                db.session.commit()
                flash(f"{p_amount} sucessfully sent to {p_phonenumber}")
                obj = clientTranscation.query.all()
                tno = int(obj[-1].transcation_id)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                f_username = fuser.username
                new_trans = clientTranscation(
                    transcation_id = tno + 1,
                    f_username = f_username,
                    t_username = p_phonenumber,
                    amount = p_amount,
                    date = date.today(),
                    time = current_time
                )
                db.session.add(new_trans)
                db.session.commit()


    return render_template("pay_phoneno.html", username=current_user.username, logged_in=True, bal=fuser.balance)

#bank transfer
@app.route("/pay/banktransfer", methods=["GET", "POST"])
@login_required
def pay_banktransfer():
    fuser = remBal.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        acno = int(request.form["ac_no"])
        ifsc = request.form["ifsc"]
        p_amount = int(request.form["amount"])
        # remBal.query.filter_by(username=request.form.get('l_username')).first()
        # fu = User.query.filter_by(phoneno=p_phonenumber).first()
        if fuser.balance < p_amount:
            flash("Insuffecient amount")
            return redirect(url_for('pay_phoneno'))
        else:
            tu = BnkAcc.query.filter_by(ac_no=acno).first()
            if not tu:
                flash("Account Dosent Exist")
                return redirect(url_for('pay_username'))
            else:
                #updating database
                # tuser = remBal.query.filter_by(username=tu.username).first()
                tu.balance += p_amount
                fuser.balance -= p_amount
                db.session.commit()
                flash(f"{p_amount} sucessfully sent to {acno}")
                obj = clientTranscation.query.all()
                tno = int(obj[-1].transcation_id)
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                f_username = fuser.username
                new_trans = clientTranscation(
                    transcation_id = tno + 1,
                    f_username = f_username,
                    t_username = acno,
                    amount = p_amount,
                    date = date.today(),
                    time = current_time
                )
                db.session.add(new_trans)
                db.session.commit()
    return render_template("pay_banktransfer.html", username=current_user.username, logged_in=True, bal=fuser.balance)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    cu_bal = remBal.query.filter_by(username=current_user.username).first()
    trans = clientTranscation.query.all()
    return render_template("history.html",username=current_user.username, bal = cu_bal.balance, trans = trans)


#loan section
@app.route("/loan/avail", methods=["GET", "POST"])
@login_required
def loanavail():
    cur_ln = lnAct.query.filter_by(username=current_user.username).first()
    admn = Erng.query.filter_by(username="admin").first()
    if request.method == 'POST':
        c_bal = remBal.query.filter_by(username=current_user.username).first()
        admin_bal = remBal.query.filter_by(username="admin").first()
        l_amount = int(request.form["amount"])
        if l_amount > cur_ln.credits:
            flash("Insuffecient Credits")
        elif cur_ln.score < 450:
            flash("Insuffecient Score")
        else:
            cur_ln.debt += (l_amount) + (l_amount * 0.12)
            cur_ln.credits -= l_amount
            cur_ln.score -= 0.1*(cur_ln.score)
            db.session.commit()
            c_bal.balance += l_amount

            admn.loan_intrest += (l_amount *0.12)
            admn.total += l_amount *0.12
            admin_bal.balance += l_amount *0.12
            db.session.commit()

            obj = lnTranscation.query.all()
            tno = int(obj[-1].transcation_id)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            new_trans_ln = lnTranscation(
                transcation_id = tno+1,
                username = cur_ln.username,
                amount = "-" + str(l_amount),
                rem_debt = cur_ln.debt,
                intrest = l_amount *0.12,
                date = date.today(),
                time = current_time
            )
            db.session.add(new_trans_ln)
            db.session.commit()


            flash(f"Loan amount of {l_amount} granted sucessfully")
    return render_template("avail_loan.html", username=current_user.username, cur_ln=cur_ln)

@app.route("/loan/pay", methods=["GET", "POST"])
@login_required
def loanpay():
    c_bal = remBal.query.filter_by(username=current_user.username).first()
    cur_ln = lnAct.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        l_amount = int(request.form["amount"])
        if l_amount > cur_ln.debt:
            flash("Enterd ammount is more than total debt")
        elif l_amount > c_bal.balance:
            flash("Insuffecient amount in account")
        else:
            cur_ln.debt -= l_amount
            cur_ln.credits += (l_amount) + (0.1*l_amount)
            cur_ln.score += 0.1*(cur_ln.score)
            db.session.commit()
            c_bal.balance -= l_amount
            db.session.commit()

            obj = lnTranscation.query.all()
            tno = int(obj[-1].transcation_id)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            new_trans_ln = lnTranscation(
                transcation_id = tno+1,
                username = cur_ln.username,
                amount = "+" + str(l_amount),
                rem_debt = cur_ln.debt,
                intrest = 0,
                date = date.today(),
                time = current_time
            )
            db.session.add(new_trans_ln)
            db.session.commit()

            flash(f"Loan amount of {l_amount} Repayed sucessfully")

    return render_template("pay_loan.html", username=current_user.username, cur_ln=cur_ln, bal=c_bal.balance)


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():
    c_bal = remBal.query.filter_by(username=current_user.username).first()

    if request.method == 'POST':
        amount = int(request.form["amount"])
        # print(curr)  
        if request.form["curr"] == "rupee":
            amount = amount
        elif request.form["curr"] == "dollar":
            amount = amount * currency.convert("USD", "INR" , 1)
        elif request.form["curr"] == "euros":
            amount = amount * currency.convert("EUR", "INR" , 1)
        elif request.form["curr"] == "pounds":
            amount = amount * currency.convert("GBP", "INR" , 1)
        elif request.form["curr"] == "yen":
            amount = amount * currency.convert("JPY", "INR" , 1)
        elif request.form["curr"] == "rubel":
            amount = amount * currency.convert("RUB", "INR" , 1)   
            # print(amount)
        # amount = round(amount, 2)
        c_bal.balance += round(amount, 2)
        db.session.commit()
        obj = clientTranscation.query.all()
        tno = int(obj[-1].transcation_id)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # f_username = fuser.username
        new_trans = clientTranscation(
                    transcation_id = tno + 1,
                    f_username = "topup",
                    t_username = current_user.username,
                    amount = amount,
                    date = date.today(),
                    time = current_time
                )
        db.session.add(new_trans)
        db.session.commit()
        

    return render_template("topup.html", bal=c_bal.balance, username=current_user.username,)


@app.route("/addbankacc", methods=["GET", "POST"])
def addbankacc():
    if request.method == 'POST':
        acno = int(request.form["ac_no"])
        ifsc = request.form["ifsc"]
        p_amount = 0
        tu = BnkAcc.query.filter_by(ac_no=acno).first()
        if tu:
            flash("Account Already Exist")
            return redirect(url_for('addbankacc'))
        else:
            new_acc = BnkAcc(
                ac_no = acno,
                ifsc = ifsc,
                balance = p_amount
            )
            db.session.add(new_acc)
            db.session.commit()
            flash("Account Added Sucessfully")

    

    return render_template("addbankacc.html")



#admin section

@app.route("/admin", methods=["GET", "POST"])
def admin():
    return redirect(url_for("adminlogin"))

@app.route("/admin/earning", methods=["GET", "POST"])
def adminearning():
    admn = Erng.query.filter_by(username="admin").first()
    return render_template("adminearning.html", admn=admn)

@app.route("/admin/login", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        if request.form["submit"] == "admin_log_in":
            a_username = request.form["a_username"]
            a_password = request.form["a_password"]
            print(a_password, a_username)
            user = Admin.query.filter_by(username=a_username).first()

            if not user:
                flash("Admin credentials dosent match")
                return redirect(url_for('adminlogin'))
            elif not check_password_hash(user.password, a_password):
                flash("Admin credentials pass dosent match")
                return redirect(url_for('adminlogin'))
            else:
                return redirect(url_for('adminearning'))

    return render_template("adminlogin.html")



if __name__ == "__main__":
    app.run(debug=True)

