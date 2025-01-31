from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, VCard, bcrypt
from forms import RegistrationForm, LoginForm, VCardForm
from config import Config
import os
from werkzeug.utils import secure_filename
import json
import qrcode
from io import BytesIO
import base64
from flask_migrate import Migrate
from flask_mail import Mail, Message

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

app = Flask(__name__)
app.config.from_object(Config)
app.config['WTF_CSRF_ENABLED'] = True  
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  
app.config['MAIL_PASSWORD'] = 'your_email_password'  

mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    vcards = VCard.query.all()
    return render_template('index.html', vcards=vcards, format_company_name=format_company_name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('create_vcard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/create_vcard', methods=['GET', 'POST'])
@login_required
def create_vcard():
    form = VCardForm()

    if form.validate_on_submit():  
        company_name = form.company.data.strip()  

        
        existing_vcard = VCard.query.filter_by(company=company_name).first()
        if existing_vcard:
            flash('This company name is already taken. Please choose a unique name.', 'danger')
            return render_template('create_vcard.html', form=form)

        services_data = []
        for i in range(len(form.service_titles.data)):
            services_data.append({
                'title': form.service_titles.data[i],
                'description': form.service_descriptions.data[i],
                'image': None  
            })

        
        for i, service_image in enumerate(form.service_images.data):
            if service_image:
                filename = secure_filename(service_image.filename)
                image_path = os.path.join('static/uploads', filename)
                service_image.save(image_path)
                services_data[i]['image'] = image_path

        try:
            
            print("Form Data:", form.data)
            print("Form Errors:", form.errors)

            
            banner_path = None
            if form.banner_image.data:
                banner_filename = secure_filename(form.banner_image.data.filename)
                banner_path = os.path.join('static/uploads', banner_filename)
                form.banner_image.data.save(banner_path)

            
            gallery_paths = []
            if form.gallery_images.data:  
                for gallery_image in form.gallery_images.data:
                    if gallery_image:
                        filename = secure_filename(gallery_image.filename)
                        gallery_path = os.path.join('static/uploads', filename)
                        gallery_image.save(gallery_path)
                        gallery_paths.append(gallery_path)  

            
            profile_photo_path = None
            if form.profile_photo.data:
                profile_filename = secure_filename(form.profile_photo.data.filename)
                profile_photo_path = os.path.join('static/uploads', profile_filename)
                form.profile_photo.data.save(profile_photo_path)

            
            vcard = VCard(
                full_name=form.full_name.data,
                company=company_name,  
                designation=form.designation.data,
                phone=form.phone.data,
                email=form.email.data,
                website=form.website.data,
                address=form.address.data,
                linkedin=form.linkedin.data,
                twitter=form.twitter.data,
                instagram=form.instagram.data,
                facebook=form.facebook.data,
                about=form.about.data,
                monday=form.monday.data,
                tuesday=form.tuesday.data,
                wednesday=form.wednesday.data,
                thursday=form.thursday.data,
                friday=form.friday.data,
                saturday=form.saturday.data,
                sunday=form.sunday.data,
                banner_image=banner_path, 
                services=json.dumps(services_data), 
                gallery_images=','.join(gallery_paths),  
                description=form.description.data,  
                profile_photo=profile_photo_path,   
                owner=current_user  
            )

            
            db.session.add(vcard)
            db.session.commit()

            flash('V Card created successfully!', 'success')
            return redirect(url_for('vcard_preview', company_name=format_company_name(vcard.company)))
        except Exception as e:
            db.session.rollback()  
            flash(f"Error creating VCard: {str(e)}", 'danger')
            print(f"Error: {str(e)}")  

    return render_template('create_vcard.html', form=form)

@app.route('/edit_vcard/<int:vcard_id>', methods=['GET', 'POST'])
@login_required
def edit_vcard(vcard_id):
    
    vcard = VCard.query.get_or_404(vcard_id)

    
    if vcard.owner != current_user:
        flash("You don't have permission to edit this VCard.", 'danger')
        return redirect(url_for('home'))  

    
    form = VCardForm(obj=vcard)

    if form.validate_on_submit():
        
        
        
        vcard.full_name = form.full_name.data
        vcard.company = form.company.data
        vcard.designation = form.designation.data
        vcard.phone = form.phone.data
        vcard.email = form.email.data
        vcard.website = form.website.data
        vcard.address = form.address.data
        vcard.linkedin = form.linkedin.data
        vcard.twitter = form.twitter.data
        vcard.instagram = form.instagram.data
        vcard.facebook = form.facebook.data
        vcard.description = form.description.data
        vcard.about = form.about.data
        vcard.monday = form.monday.data
        vcard.tuesday = form.tuesday.data
        vcard.wednesday = form.wednesday.data
        vcard.thursday = form.thursday.data
        vcard.friday = form.friday.data
        vcard.saturday = form.saturday.data
        vcard.sunday = form.sunday.data

        
        if form.banner_image.data:
            banner_filename = secure_filename(form.banner_image.data.filename)
            banner_path = os.path.join('static/uploads', banner_filename)
            form.banner_image.data.save(banner_path)
            vcard.banner_image = banner_path

        
        if form.profile_photo.data:
            profile_filename = secure_filename(form.profile_photo.data.filename)
            profile_photo_path = os.path.join('static/uploads', profile_filename)
            form.profile_photo.data.save(profile_photo_path)
            vcard.profile_photo = profile_photo_path

        
        gallery_paths = []
        for gallery_image in form.gallery_images.data:
            if gallery_image:
                gallery_filename = secure_filename(gallery_image.filename)
                gallery_path = os.path.join('static/uploads', gallery_filename)
                gallery_image.save(gallery_path)
                gallery_paths.append(gallery_path)
        vcard.gallery_images = ','.join(gallery_paths)

        
        services_data = []
        for i in range(len(form.service_titles.data)):
            services_data.append({
                'title': form.service_titles.data[i],
                'description': form.service_descriptions.data[i],
                'image': None  
            })
        
        for i, service_image in enumerate(form.service_images.data):
            if service_image:
                filename = secure_filename(service_image.filename)
                image_path = os.path.join('static/uploads', filename)
                service_image.save(image_path)
                services_data[i]['image'] = image_path
        vcard.services = json.dumps(services_data)

        
        try:
            db.session.commit()
            flash("VCard updated successfully!", 'success')
            return redirect(url_for('vcard_preview', company_name=format_company_name(vcard.company)))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating VCard: {str(e)}", 'danger')

    return render_template('edit_vcard.html', form=form, vcard=vcard)

def format_company_name(company_name):
    """ Space ko hyphen me replace kare aur lowercase kare """
    return company_name.replace(" ", "-").lower()

@app.template_filter('from_json')
def from_json(value):
    return json.loads(value) if value else []

@app.route('/add_testimonial/<int:vcard_id>', methods=['POST'])
def add_testimonial(vcard_id):
    vcard = VCard.query.get_or_404(vcard_id)
    testimonials = json.loads(vcard.testimonials) if vcard.testimonials else []

    new_testimonial = {
        "name": request.form['name'],
        "comment": request.form['comment']
    }

    testimonials.append(new_testimonial)
    vcard.testimonials = json.dumps(testimonials)
    db.session.commit()
    
    return redirect(url_for('vcard_preview', company_name=vcard.company, vcard_id=vcard_id))

@app.route('/send_inquiry/<int:vcard_id>', methods=['POST'])
def send_inquiry(vcard_id):
    vcard = VCard.query.get_or_404(vcard_id)
    
    
    user_name = request.form.get('name')
    user_email = request.form.get('email')
    user_phone = request.form.get('phone')
    user_message = request.form.get('message')

    
    vcard_owner_name = vcard.full_name  
    vcard_company_name = vcard.company  

    
    subject = f"New Inquiry for {vcard_owner_name} from {vcard_company_name}"
    recipient_email = vcard.email  

    
    body = f"""
📢 You have received a new inquiry from your VCard:

🏢 Company Name: {vcard_company_name}
🧑‍💼 VCard Owner: {vcard_owner_name}

🔹 Inquirer Name: {user_name}
📧 Inquirer Email: {user_email}
📞 Inquirer Phone: {user_phone}
💬 Message**: {user_message}

Please respond to the inquiry as soon as possible.
    """

    
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[recipient_email])
    msg.body = body
    mail.send(msg)

    flash("Your inquiry has been sent successfully!", "success")
    return redirect(url_for('vcard_preview', vcard_id=vcard.id, company_name=vcard.company))

@app.route('/<string:company_name>')
def vcard_preview(company_name):
    
    formatted_name = company_name.replace("-", " ")  

    
    vcard = VCard.query.filter(VCard.company.ilike(formatted_name)).first()

    if not vcard:
        return "<h2 style='color: red;'>V Card Not Found</h2>", 404
    
    
    formatted_name_for_url = formatted_name.replace(" ", "-")  
    
    
    qr_data = f"https://mybusinesscardapp.onrender.com/{formatted_name_for_url}"  
    
    
    qr_code_image = qrcode.make(qr_data)
    
    
    qr_code_io = BytesIO()
    qr_code_image.save(qr_code_io)
    qr_code_io.seek(0)  
    
    
    qr_code_base64 = base64.b64encode(qr_code_io.getvalue()).decode('utf-8')

    return render_template('vcard_preview.html', vcard=vcard, qr_code_base64=qr_code_base64, user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
