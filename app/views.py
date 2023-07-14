from flask import render_template, request, Blueprint,redirect,url_for,flash
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import *

view = Blueprint('view',__name__)


@view.route('/')
def home():
    return render_template('home.html',user=current_user)


@view.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        service = request.form.get('service')
        service_pro=service_provider.query.filter(service_provider.service_type==service).all()
      
        if service_pro:
            return render_template('index.html',user=current_user,service_providers = service_pro)
        else:
            flash(f'no {service} currently available')       
    return render_template('index.html',user=current_user)

@view.route('/service/', methods=['GET', 'POST'])
@login_required
def service():
    service = request.args.get('my_var')
    service_pro=service_provider.query.filter(service_provider.service_type==service).all()
    if service_pro:
        return render_template('get_providers.html',user=current_user,service_providers = service_pro)
    else:
        return render_template('get_providers.html',user=current_user) 

# admin dashboard
@view.route('/admin')
@login_required
def admin():
  
    users = User.query.count()
    providers = service_provider.query.count()
    return render_template('Admin/Admin.html',users=users,providers=providers)

# about page
@view.route('/about')
def about():
    return render_template('About.html',user=current_user)     
  
# Admin Services
@view.route('/users')
def users():
    users = User.query.all()
    return render_template('Admin/users.html',users=users)

@view.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        Full_Name = request.form.get('Full_Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, name=Full_Name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('view.users'))
    return render_template("Admin/add_user.html")

@view.route('/users_delete/<int:users_id>')
@login_required
def users_delete(users_id):
    global user
    user = User.query.get_or_404(users_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('view.users'))

@view.route('/users_update/<int:users_id>',methods=['GET','POST'])
@login_required
def users_update(users_id):
    global user
    user = User.query.get_or_404(users_id)
    if request.method == 'POST':
        email = request.form.get('email')
        Full_Name = request.form.get('Full_Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user_check = User.query.filter_by(email=email).first()
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif user_check:
            user.name = Full_Name
            user.password = password1
            try:
                db.session.commit()
                flash('user updated!')
                return redirect(url_for('view.users'))
            except:
                flash('there was some issue updating the user')
        else:
            user.email = email
            user.name = Full_Name
            user.password = password1
            try:
                db.session.commit()
                flash('user updated!')
                return redirect(url_for('view.users_update'))
            except:
                flash('there was some issue updating the user')

    return render_template("Admin/update_user.html", user=user)

@view.route('/service_providers',methods=['GET','POST'])
@login_required
def provider():
    providers = service_provider.query.all()
    return render_template('Admin/providers.html',providers=providers)


@view.route('/service_providers/add',methods=['GET','POST'])
@login_required
def add_provider():
    if request.method=='POST':
        name= request.form.get('full_name')
        contact= request.form.get('contact')
        location= request.form.get('location')
        service_type= request.form.get('service_type')
        bio= request.form.get('bio')
        new_provider =  service_provider(name=name,contact=contact,location=location,service_type=service_type,bio=bio)
        db.session.add(new_provider)
        db.session.commit()
        return redirect('/service_providers')
    return render_template('Admin/add_provider.html')

@view.route('/providers_delete/<int:providers_id>')
@login_required
def providers_delete(providers_id):
    global provider
    provider = service_provider.query.get_or_404(providers_id)
    db.session.delete(provider)
    db.session.commit()
    return redirect(url_for('view.provider'))

@view.route('/providers_update/<int:providers_id>',methods=['GET','POST'])
@login_required
def providers_update(providers_id):
    global provider
    provider = service_provider.query.get_or_404(providers_id)
    if request.method == 'POST':
        name= request.form.get('full_name')
        contact= request.form.get('contact')
        location= request.form.get('location')
        service_type= request.form.get('service_type')
        bio= request.form.get('bio')
        # assign
        provider.name = name
        provider.contact = contact
        provider.location = location
        provider.service_type = service_type
        provider.bio = bio
        try:
            db.session.commit()
            flash('user updated!')
            return redirect(url_for('view.provider'))
        except:
            flash('there was some issue updating the user')
    return render_template("Admin/update_provider.html", provider=provider)

# end of Admin service

@view.route('/rating/', methods=['GET', 'POST'])
@login_required
def rate():
    val = request.args.get('val')
    id=request.args.get('id')
    provider = service_provider.query.get_or_404(id)
    service = provider.service_type
    rating = Rating.query.filter_by(service_provider_id=id).first()
    if rating:
        new_rating_value= round((rating.value+int(val))/5,2)
        rating.value=new_rating_value
        db.session.commit()
        return redirect(url_for('view.service', my_var=service))
    else:
        rate =  Rating(value=val, service_provider_id=id)
        db.session.add(rate)
        db.session.commit()
        return redirect( url_for('view.service', my_var=service))