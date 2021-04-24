from dateutil.relativedelta import relativedelta
import datetime
import os
from flask import url_for, current_app
from flask_login import current_user
from datetime import datetime as dt
from invoice.forms import ReportForm, RecieveForm
from invoice.models import Sales, Purchase
from invoice import db

def breakdown(data):
    x=[]
    for i in range(len(data)):
        for j in list(data[i].values()):
            x.append(j)
    items=''
    quantity=''
    item_price=''
    amount=''
    total_amount=0
    for i in x[::3]:
       items+=str(i)+','
    for i in x[1::3]:
        quantity+=str(i)+','
    for i in x[2::3]:
        item_price+=str(i)+','
    for i in range(len(items[:-1].split(','))):
        amount+=str(int(quantity[:-1].split(',')[i])*int(item_price[:-1].split(',')[i]))+','
    for i in amount[:-1].split(','):
        total_amount+=int(i) 
        
    return list((items[:-1],quantity[:-1],item_price[:-1],amount[:-1],total_amount))

def timeview(data):
    total_amount=0
    paid_amount=0
    remaning_amount=0
    for i in data:
        total_amount+=i.total_amount
        paid_amount+=i.paid_amount
        remaning_amount+=i.remaning_amount
    return list((total_amount,paid_amount,remaning_amount))


def choice(i):
  start=datetime.date(dt.today().year,i,day=1)
  end=datetime.date(dt.today().year,1,day=1)+relativedelta(months=+i,days=-1)
  return list((start,end))


def sum_bydays(month,table):
    days=[]
    total_amount=[]
    remaining_amount=[]
    paid_amount=[]
    x,y =choice(month)[0],choice(month)[1]
    for z in range(1,y.day+1):
        days.append(datetime.date(dt.today().year,month,day=z))
    for i in days:
        start=datetime.date(i.year,i.month,i.day)
        end=datetime.date(i.year,i.month,i.day)+relativedelta(days=+1)
        day= table.query.filter(table.date <= end).filter(table.date >= start).all()
        total=timeview(day)[0]
        paid=timeview(day)[1]
        remaining=timeview(day)[2]
        total_amount.append(total)
        remaining_amount.append(remaining)
        paid_amount.append(paid)
    return list((total_amount,paid_amount,remaining_amount))

def extract(data):
    form = ReportForm()
    month = dt.today().month
    if form.january.data:
        month = 1
    elif form.february.data:
        month = 2
    elif form.march.data:
        month = 3
    elif form.april.data:
        month = 4
    elif form.may.data:
        month = 5
    elif form.june.data:
        month = 6
    elif form.july.data:
        month = 7
    elif form.august.data:
        month = 8
    elif form.september.data:
        month = 9
    elif form.october.data:
        month = 10
    elif form.november.data:
        month = 11
    elif form.december.data:
        month = 12
    else:
        start = datetime.date(
            dt.today().year, dt.today().month, dt.today().day)
        end = datetime.date(dt.today().year, dt.today().month,
                            dt.today().day)+relativedelta(days=+1)
    start = choice(month)[0]
    end = choice(month)[1]
    if form.last_week.data:
        start = datetime.date(dt.today().year, dt.today(
        ).month, dt.today().day) + relativedelta(days=-13)
        end = datetime.date(dt.today().year, dt.today().month,
                            dt.today().day) + relativedelta(days=-6)
    elif form.this_month.data:
        start = datetime.date(dt.today().year, dt.today().month, day=1)
        end = datetime.date(dt.today().year, dt.today().month,
                            day=1)+relativedelta(months=+1, days=-1)
    elif form.this_week.data:
        start = datetime.date(dt.today().year, dt.today(
        ).month, dt.today().day) + relativedelta(days=-6)
        end = datetime.date(dt.today().year, dt.today().month,
                            dt.today().day)+relativedelta(days=+1)
    elif form.today.data:
        start = datetime.date(
            dt.today().year, dt.today().month, dt.today().day)
        end = datetime.date(dt.today().year, dt.today().month,
                            dt.today().day)+relativedelta(days=+1)
    elif form.yesterday.data:
        start = datetime.date(dt.today().year, dt.today(
        ).month, dt.today().day)+relativedelta(days=-1)
        end = datetime.date(dt.today().year, dt.today().month, dt.today().day)
    items = data.query.filter(data.date <= end).filter(
        data.date >= start).order_by(data.total_amount.desc()).all()
    return month, items


def paid(name, data, form1, table):
    if table=='customer':
        payment = data(admin_id=current_user.id, name=name,
        total_amount=0, paid_amount=form1.paid_amount.data, discount=0, remaning_amount=0-(int(form1.paid_amount.data)))
    else:
        payment = data(admin_id=current_user.id, name=name,
        total_amount=0, paid_amount=form1.paid_amount.data, remaning_amount=0-(int(form1.paid_amount.data)))
    db.session.add(payment)
    db.session.commit()
