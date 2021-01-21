'''
1. Open with localhost/register
2. Enter all details
3. PaymentGateways will be used according to the specified amount
4. The Availibility of the Payment Gateways is changed using the config.json file.
'''

from flask import Flask, render_template, url_for, flash, redirect, request, session, Response, stream_with_context, abort
from forms import RegistrationForm
import json
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route("/")
@app.route("/home")

#Loads JSON file which points out the availibility of each Payment Gateway.
#It takes boolean values (True of False) with each payment Gateway and checks if that particular payment gateway is available or not.

def home():
    with open("config.json") as cf:
        a = json.load(cf)
    CheapPaymentgateway = a['gateways']["CheapPaymentgateway"]
    ExpensivePaymentgateway = a['gateways']["ExpensivePaymentGateway"]
    PremiumPaymentgateway = a['gateways']["PremiumPaymentGateway"]
    Amount = session['amount']

    if(Amount <= 20):
        if(CheapPaymentgateway == True):
            return render_template('paymentgateway.html', value = 'Cheap Payment Gateway' , amount = Amount), 200
        else:
            abort(404), 404 #Aborts if not available
    
    elif(Amount > 20 and Amount <= 500):
        if(ExpensivePaymentgateway == True):
            return render_template('paymentgateway.html', value = 'Expensive Payment Gateway' , amount = Amount), 200
        else:
            if(CheapPaymentgateway):
                return render_template('paymentgateway.html', value = 'Cheap Payment Gateway' , amount = Amount), 200
            else:
                abort(404), 404 #Aborts if not available
    else:
        if(PremiumPaymentgateway == True):
            return render_template('paymentgateway.html', value = 'Premium Payment Gateway' , amount = Amount), 200
        else:
            #Tries PremiumPaymentGateway three times. If not available, aborts after those three tries. 
            for i in range(3):
                if(PremiumPaymentgateway != True):
                    time.sleep(1)
                    value = 'Retrying...' + str(i)
                    abort(404), 404
            abort(404)

    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        session['amount'] = float(form.amount.data)
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/paymentgateway")
def paymentgateway():
    return render_template('paymentgateway.html', title='PaymentGateway')

if __name__ == '__main__':
    app.run(debug=True, port=5050)