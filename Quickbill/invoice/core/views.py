from flask import render_template, request, Blueprint, redirect, url_for
from invoice.forms import LoginForm, SignupForm
from invoice.models import User
from invoice import login_manager, db
from flask_login import login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from invoice import app
from invoice.models import User, Sales, Purchase, Items, SalesInvoice, PurchaseInvoice
core = Blueprint('core', __name__)
admin=Admin(app)
##################################
######### Home Page View #########
##################################


@core.route('/', methods=['GET', 'POST'])
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    form = LoginForm()
    if form.validate_on_submit():
        admin = User.query.filter_by(username=form.username.data).first()
        if admin is not None and admin.check_password(form.password.data):
            login_user(admin)
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('application.dashboard')
            return redirect(next)
    return render_template('index.html', form=form)

##################################
######### Sign Up Page View ######
##################################


@core.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    username = form.username.data
    if form.validate_on_submit():
        new_username = User.query.filter_by(username=username).first()
        if new_username:
            return redirect(url_for('core.index'))
        else:
            new_admin = User(username=form.username.data,
                             firstname=form.firstname.data, lastname=form.lastname.data,
                             password=form.password.data)
        db.session.add(new_admin)
        db.session.commit()
        return redirect(url_for('core.index'))
    return render_template('signup.html', form=form)


################################
########### LOG OUT ############
################################
@core.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect('/')


#####################################
############ Setting Model View #####
#####################################
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username=='pujafancy'
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('core.index'))

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Sales, db.session))
admin.add_view(MyModelView(SalesInvoice, db.session))
admin.add_view(MyModelView(Purchase, db.session))
admin.add_view(MyModelView(PurchaseInvoice, db.session))
admin.add_view(MyModelView(Items, db.session))

