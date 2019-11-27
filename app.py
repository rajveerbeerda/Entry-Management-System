from flask import Flask, request, jsonify, render_template, make_response, redirect, url_for, flash, sessions, session, get_flashed_messages
import csv
import pandas as pd
from datetime import datetime


from pyfile import sendTexts, checkoutTexts
from checkout_fn import checkOut

app = Flask(__name__)
app.secret_key = "abc"


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/checkin', methods=['GET', 'POST'])
def checkin():
    if request.method=='POST':
        visitorName = request.form['visitorName']
        visitorEmail = request.form['visitorEmail']
        visitorPhone = request.form['visitorPhone']

        curTime = datetime.now()
        checkinTime = str(curTime.strftime("%I:%M %p"))

        hostName = request.form['hostName']
        hostAddress = request.form['hostAddress']

        visitorDetails = [visitorName, visitorEmail, visitorPhone, checkinTime, hostName, hostAddress]
        session['visitorDetails'] = visitorDetails

        flag = sendTexts(visitorName, visitorEmail, visitorPhone, hostName, hostAddress, checkinTime)
        msg = ['Sorry! We are having some issue for your request. Please check your connection and try again.',
               'Your details have been sent to your host.']

        session['msg'] = msg[flag]
        return redirect(url_for('requestSubmitted'))
    return render_template('checkin.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    df = pd.read_csv('visitor.csv')
    df = df[df['status'] == 1]
    names = df[['name', 'phone']]

    lst = []
    for i in range(len(names)):
        lst.append(list(names.iloc[i]))


    if request.method=='POST':
        name, phone = map(str, str(request.form['optradio']).split(','))
        lst = checkOut(name, phone)

        flag = checkoutTexts(lst[0], lst[1], lst[2], lst[3], lst[4], lst[6], lst[7])
        msg = ['Sorry! We are having some issue for your request. Please check your connection and try again.',
               'Your request for checkout is successfully completed.']
        session['msg'] = msg[flag]

        return redirect(url_for('requestSubmitted'))
    if len(lst)!=0:
        return render_template('checkout.html', visitors_list=lst)
    else:
        return render_template('request-submitted.html', message='There are no visitors currently.')


@app.route('/request-submitted')
def requestSubmitted():
    msg = session['msg']

    return render_template('request-submitted.html', message = msg)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)