from flask import render_template, request, Blueprint, redirect, url_for
from invoice.forms import ReportForm, MainForm, AddItemForm, RecieveForm, AddClientForm
from invoice.models import Sales, Purchase, Items, Customer, Supplier, SalesInvoice, PurchaseInvoice
from invoice.helper_functions import breakdown, timeview, choice, sum_bydays, extract, paid
from flask_login import login_user, login_required, logout_user, current_user
import datetime
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from invoice import login_manager, db

application = Blueprint('application', __name__)

####################################
######### Dashboard Page View ######
####################################


@application.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ReportForm()
    month = dt.today().month
    month_list = [0, 'January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    sitems = extract(SalesInvoice)[1]
    pitems = extract(PurchaseInvoice)[1]
    month = extract(SalesInvoice)[0]
    s_paiddata = sum_bydays(month, SalesInvoice)[1]
    s_totaldata = sum_bydays(month, SalesInvoice)[0]
    s_remaindata = sum_bydays(month, SalesInvoice)[2]
    p_paiddata = sum_bydays(month, PurchaseInvoice)[1]
    p_totaldata = sum_bydays(month, PurchaseInvoice)[0]
    p_remaindata = sum_bydays(month, PurchaseInvoice)[2]

    smonth_total = timeview(sitems)[0]
    smonth_paid = timeview(sitems)[1]
    smonth_remain = timeview(sitems)[2]
    pmonth_total = timeview(pitems)[0]
    pmonth_paid = timeview(pitems)[1]
    pmonth_remain = timeview(pitems)[2]

    labels = list(range(1, len(s_totaldata)+1))
    return render_template('dashboard.html', form=form, sitems=sitems, pitems=pitems,
                           smonth_total=smonth_total, smonth_paid=smonth_paid, smonth_remain=smonth_remain,
                           pmonth_total=pmonth_total, pmonth_paid=pmonth_paid, pmonth_remain=pmonth_remain,
                           s_totaldata=s_totaldata, s_paiddata=s_paiddata, s_remaindata=s_remaindata,
                           p_totaldata=p_totaldata, p_paiddata=p_paiddata, p_remaindata=p_remaindata, labels=labels, month_name=month_list[month], title='Dashboard')


####################################
######### Add Sales Page View ######
####################################
@application.route('/add_sales', methods=['GET', 'POST'])
@login_required
def sales():
    form = MainForm()
    last_entry = SalesInvoice.query.order_by(SalesInvoice.id.desc()).first()
    if last_entry == None:
        last_entry = 0
    else:
        last_entry = last_entry.id
    date = dt.today().strftime("%d/%m/%Y")
    users = Customer.query.all()
    len_users = list(range(len(users)))
    if form.validate_on_submit():
        name = form.name.data
        item = form.item.data[:-2].split('/n')
        description = form.description.data[:-2].split('/n')
        alternate_quantity = form.alternate_quantity.data[:-2].split('/n')
        quantity = form.quantity.data[:-2].split('/n')
        rate = form.rate.data[:-2].split('/n')
        per = form.per.data[:-2].split('/n')
        amount = form.amount.data[:-2].split('/n')
        paid_amount = int(form.paid_amount.data)
        discount = int(form.discount.data)
        total_amount = int(form.total_amount.data)
        remaning_amount = total_amount - paid_amount - discount

        invoice = SalesInvoice(admin_id=current_user.id, name=name, paid_amount=paid_amount,
                               total_amount=total_amount, discount=discount, remaning_amount=remaning_amount)
        db.session.add(invoice)
        db.session.commit()
        for i in range(len(item)):
            sales = Sales(invoice_id=last_entry+1, item=item[i], description=description[i],
                          alternate_quantity=alternate_quantity[i], quantity=quantity[i], rate=rate[i],
                          per=per[i], amount=amount[i])
            db.session.add(sales)
            db.session.commit()
        return redirect(url_for('application.salesvoucher'))
    return render_template('desc.html', form=form, title='Sales', last_entry=last_entry,
                           date=date, users=users, len_users=len_users)



####################################
####### Add Purchase Page View #####
####################################

@application.route('/purchases', methods=['GET', 'POST'])
@login_required
def purchases():
    form = MainForm()
    last_entry = PurchaseInvoice.query.order_by(
        PurchaseInvoice.id.desc()).first()
    if last_entry == None:
        last_entry = 0
    else:
        last_entry = last_entry.id
    date = dt.today().strftime("%d/%m/%Y")
    users = Supplier.query.all()
    len_users = list(range(len(users)))
    if form.validate_on_submit():
        name = form.name.data
        item = form.item.data[:-2].split('/n')
        description = form.description.data[:-2].split('/n')
        alternate_quantity = form.alternate_quantity.data[:-2].split('/n')
        quantity = form.quantity.data[:-2].split('/n')
        rate = form.rate.data[:-2].split('/n')
        per = form.per.data[:-2].split('/n')
        amount = form.amount.data[:-2].split('/n')
        paid_amount = int(form.paid_amount.data)
        total_amount  = int(form.paid_amount.data)
        remaning_amount = total_amount - paid_amount
        invoice = PurchaseInvoice(admin_id=current_user.id, name=name, paid_amount=paid_amount,
                                  total_amount=total_amount, remaning_amount=remaning_amount)
        db.session.add(invoice)
        db.session.commit()
        for i in range(len(item)):
            purchase = Purchase(invoice_id=last_entry+1, item=item[i], description=description[i],
                                alternate_quantity=alternate_quantity[i], quantity=quantity[i], rate=rate[i], per=per[i], amount=amount[i])
            db.session.add(purchase)
            db.session.commit()
        return redirect(url_for('application.purchasevoucher'))
    return render_template('desc.html', form=form, title='Purchase', last_entry=last_entry,
                           date=date, users=users, len_users=len_users)


####################################
####### Sales Invoice Page View ####
####################################
@application.route('/salesvoucher')
@login_required
def salesvoucher(last_entry=0):
    if last_entry == 0:
        last_entry = SalesInvoice.query.order_by(
            SalesInvoice.id.desc()).first()
    else:
        last_entry = last_entry
    name = last_entry.name
    sales = Sales.query.filter_by(invoice_id=last_entry.id)
    item_range = list(range(10))
    item_len = list(range(sales.count()))
    if len(item_len) <= 10:
        tabs = list(range(1))
    else:
        tabs = list(range((len(item_len)//10)+1))
    for i in item_len:
        total_alternate_quantity = sum(
            [float(i) for i in sales[i].alternate_quantity])
        total_quantity = sum([float(i) for i in sales[i].quantity])
    return render_template('sales/invoice.html', name=name, item_len=item_len, item_range=item_range, last_entry=last_entry, sales=sales,
                           total_alternate_quantity=total_alternate_quantity, total_quantity=total_quantity, tabs=tabs, title='Sales | Invoice', discount = last_entry.discount)

####################################
##### Purchase Voucher Page View ###
####################################
@application.route('/purchasevoucher')
@login_required
def purchasevoucher(last_entry=0):
    if last_entry == 0:
        last_entry = PurchaseInvoice.query.order_by(
            PurchaseInvoice.id.desc()).first()
    else:
        last_entry = last_entry
    name = last_entry.name
    sales = Purchase.query.filter_by(invoice_id=last_entry.id)
    item_range = list(range(10))
    item_len = list(range(sales.count()))
    if len(item_len) <= 10:
        tabs = list(range(1))
    else:
        tabs = list(range((len(item_len)//10)+1))
    for i in item_len:
        total_alternate_quantity = sum(
            [float(i) for i in sales[i].alternate_quantity])
        total_quantity = sum([float(i) for i in sales[i].quantity])
    return render_template('sales/invoice.html', name=name, item_len=item_len, item_range=item_range, last_entry=last_entry, sales=sales,
                           total_alternate_quantity=total_alternate_quantity, total_quantity=total_quantity, tabs=tabs, title='Purchase | Invoice', discount = 0)


####################################
####### Sales Entries Page View ####
####################################
@application.route('/salesentries', methods=["GET", "POST"])
@login_required
def salesentries():
    form = ReportForm()
    items = extract(SalesInvoice)[1]
    return render_template('sales/salesentries.html', items=items, form=form, title='Sales')

####################################
##### Purchase Entries Page View ###
####################################
@application.route('/purchaseentries', methods=["GET", "POST"])
@login_required
def purchaseentries():
    form = ReportForm()
    items = extract(PurchaseInvoice)[1]
    return render_template('purchase/purchaseentries.html', items=items, form=form, title='Purchase')

#############################################
####### Sales Invoice(From Id) Page View ####
#############################################
@application.route('/<int:id>/salesvoucher', methods=["GET", "POST"])
@login_required
def voucher_id(id):
    return salesvoucher(last_entry=SalesInvoice.query.filter_by(id=id).first())

#############################################
### Purchase Invoice(From Id) Page View #####
#############################################
@application.route('/<int:id>/purchase', methods=["GET", "POST"])
@login_required
def pvoucher_id(id):
    return purchasevoucher(last_entry=PurchaseInvoice.query.filter_by(id=id).first())

#############################################
####### Customer Profile Page View ##########
#############################################

@application.route('/<costumer_name>/costumer', methods=["GET", "POST"])
@login_required
def profile(costumer_name):
    form1 = RecieveForm()
    total_amount = 0
    paid_amount = 0
    remaning_amount = 0
    client = Customer.query.filter_by(
        companyname=costumer_name).first()
    items = SalesInvoice.query.filter_by(
        name=costumer_name)
    for i in items:
        total_amount += i.total_amount
        paid_amount += i.paid_amount
        remaning_amount += i.remaning_amount
    if form1.submit.data:
        paid(costumer_name, SalesInvoice, form1, 'customer')
    return render_template('profile.html', name=costumer_name, total_amount=total_amount, items=items,
                           paid_amount=paid_amount, remaning_amount=remaning_amount, title=costumer_name, client=client, form1=form1)


@application.route('/<int:id>/sdelete', methods=["GET", "POST"])
@login_required
def delete_sales(id):
    entry = Sales.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('salesentries'))

#############################################
####### Supplier Profile Page View ##########
#############################################
@application.route('/<seller_name>/seller', methods=["GET", "POST"])
@login_required
def sellerprofile(seller_name):
    form1 = RecieveForm()
    total_amount = 0
    paid_amount = 0
    remaning_amount = 0
    client = Supplier.query.filter_by(
        companyname=seller_name).first()
    items = PurchaseInvoice.query.filter_by(
        name=seller_name)
    for i in items:
        total_amount += i.total_amount
        paid_amount += i.paid_amount
        remaning_amount += i.remaning_amount
    if form1.submit.data:
        paid(seller_name, PurchaseInvoice, form1, 'seller')
    return render_template('profile.html', name=seller_name, items=items, total_amount=total_amount,
                           paid_amount=paid_amount, remaning_amount=remaning_amount, title=seller_name, client=client, form1=form1)


@application.route('/<int:id>/pdelete', methods=["GET", "POST"])
@login_required
def delete_purchase(id):
    entry = Purchase.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('purchaseentries'))


@application.route('/<int:id>/update', methods=["GET", "POST"])
@login_required
def update(id):
    users = Customer.query.all()
    form = MainForm()
    invoice = SalesInvoice.query.filter_by(id=id).first()
    last_entry = Sales.query.filter_by(invoice_id=id)
    date = invoice.date.strftime("%d/%m/%Y")
    name = invoice.name
    item_len = list(range(last_entry.count()))
    
    if form.validate_on_submit():
        invoice.name = form.name.data
        invoice.total_amount = form.total_amount.data
        invoice.paid_amount = form.paid_amount.data
        invoice.remaning_amount = form.remaning_amount.data

        item = form.item.data[:-2].split('/n')
        description = form.description.data[:-2].split('/n')
        alternate_quantity = form.alternate_quantity.data[:-2].split('/n')
        quantity = form.quantity.data[:-2].split('/n')
        rate = form.rate.data[:-2].split('/n')
        per = form.per.data[:-2].split('/n')
        amount = form.amount.data[:-2].split('/n')
        for i in item_len:
            last_entry[i].item = item[i]
            last_entry[i].description = description[i]
            last_entry[i].alternate_quantity = alternate_quantity[i]
            last_entry[i].quantity = quantity[i]
            last_entry[i].rate = rate[i]
            last_entry[i].per = per[i]
            last_entry[i].amount = amount[i]
        db.session.commit()
        for i in range(len(item_len), len(form.item.data[:-2].split('/n'))):
            sales = Sales(invoice_id=id, item=item[i], description=description[i],
                          alternate_quantity=alternate_quantity[i], quantity=quantity[i], rate=rate[i],
                          per=per[i], amount=amount[i])
            db.session.add(sales)
            db.session.commit()
        return redirect(url_for('application.voucher_id', id=invoice.id))

    return render_template('update.html', name=name, date=date, form=form, users=users,  role='costumer', last_entry=last_entry, item_len=item_len, invoice=invoice)


@application.route('/<int:id>/pupdate', methods=["GET", "POST"])
@login_required
def pupdate(id):
    users = Supplier.query.all()
    form = MainForm()
    invoice = PurchaseInvoice.query.filter_by(id=id).first()
    last_entry = Purchase.query.filter_by(invoice_id=id)
    date = invoice.date.strftime("%d/%m/%Y")
    name = invoice.name
    item_len = list(range(last_entry.count()))
    invoice.disount = 0
    if form.validate_on_submit():
        invoice.name = form.name.data
        invoice.total_amount = form.total_amount.data
        invoice.paid_amount = form.paid_amount.data
        invoice.remaning_amount = form.remaning_amount.data

        item = form.item.data[:-2].split('/n')
        description = form.description.data[:-2].split('/n')
        alternate_quantity = form.alternate_quantity.data[:-2].split('/n')
        quantity = form.quantity.data[:-2].split('/n')
        rate = form.rate.data[:-2].split('/n')
        per = form.per.data[:-2].split('/n')
        amount = form.amount.data[:-2].split('/n')
        for i in item_len:
            last_entry[i].item = item[i]
            last_entry[i].description = description[i]
            last_entry[i].alternate_quantity = alternate_quantity[i]
            last_entry[i].quantity = quantity[i]
            last_entry[i].rate = rate[i]
            last_entry[i].per = per[i]
            last_entry[i].amount = amount[i]
        db.session.commit()
        for i in range(len(item_len), len(form.item.data[:-2].split('/n'))):
            purchase = Purchase(invoice_id=id, item=item[i], description=description[i],
                          alternate_quantity=alternate_quantity[i], quantity=quantity[i], rate=rate[i],
                          per=per[i], amount=amount[i])
            db.session.add(purchase)
            db.session.commit()
        return redirect(url_for('application.pvoucher_id', id=invoice.id))

    return render_template('update.html', name=name, date=date, form=form, users=users,  role='costumer', last_entry=last_entry, item_len=item_len, invoice=invoice)


@application.route('/add_item', methods=['GET', 'POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        item_name = form.item_name.data
        item_brand = form.item_brand.data
        item_category = form.item_category.data
        item_price = form.item_price.data
        item_quantity = form.item_quantity.data
        item = Items(item_name=item_name, item_brand=item_brand,
                     item_category=item_category, item_price=item_price, item_quantity=item_quantity)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('application.item_list'))
    return render_template('items/add_items.html', form=form)


@application.route('/item_list', methods=['GET', 'POST'])
def item_list():
    items = Items.query.all()
    return render_template('items/item_inventory.html', items=items)


@application.route('/client', methods=['GET', 'POST'])
def client():
    costumer = Customer.query.all()
    return render_template('client_list.html', items=costumer)


@application.route('/add_costumer', methods=['GET', 'POST'])
def add_costumers():
    form = AddClientForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        companyname = form.companyname.data
        email = form.email.data
        primary_no = form.primary_phone.data
        secondary_no = form.secondary_phone.data
        address = form.address.data
        pan_no = form.pan_no.data
        costumer = Customer(firstname=firstname, lastname=lastname, companyname=companyname, email=email,
                            primary_no=primary_no, secondary_no=secondary_no, address=address, pan_no=pan_no)
        db.session.add(costumer)
        db.session.commit()
        return redirect(url_for('application.client'))
    return render_template('add_costumer.html', form=form)


@application.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    form = AddClientForm()
    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        companyname = form.companyname.data
        email = form.email.data
        primary_no = form.primary_phone.data
        secondary_no = form.secondary_phone.data
        address = form.address.data
        pan_no = form.pan_no.data
        supplier = Supplier(firstname=firstname, lastname=lastname, companyname=companyname, email=email,
                            primary_no=primary_no, secondary_no=secondary_no, address=address, pan_no=pan_no)
        db.session.add(supplier)
        db.session.commit()
        return redirect(url_for('application.supplier'))
    return render_template('add_costumer.html', form=form)


@application.route('/supplier', methods=['GET', 'POST'])
def supplier():
    supplier = Supplier.query.all()
    return render_template('client_list.html', items=supplier)


@application.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html')
