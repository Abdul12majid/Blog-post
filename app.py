from flask import Flask, render_template, flash, url_for, redirect, request
from webforms import reg_form, loginform, post_form, SearchForm
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from datetime import datetime
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid as uuid
import os 



app = Flask(__name__)
app.config["SECRET_KEY"]='app_py'
#app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///#Blog_Post.db'
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:Non12$ense@localhost/users'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
	return register.query.get(int(user_id))


class register(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name_db = db.Column(db.String(30), nullable=False)
	username_db = db.Column(db.String(30), nullable=False, unique=True)
	about_author = db.Column(db.Text, nullable=True)
	profile_pic_db = db.Column(db.String(600), nullable=True)
	db_rel = db.relationship('posts_table', backref='poster')
	password_hash = db.Column(db.String(300))
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	
	@property
	def password(self):
		raise AttributeError("Password is not a readable attribute")
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
		
class posts_table(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	title_db = db.Column(db.String(500))
	content_db = db.Column(db.Text)
	poster_id = db.Column(db.Integer, db.ForeignKey(register.id))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	
@app.route("/")
@login_required
def home():
	return render_template("home.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404
	
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500
	
@app.route("/sign_up", methods=["POST", "GET"])
def sign_up():
	form = reg_form()
	name_db = None
	if form.validate_on_submit():
		user = register.query.filter_by(username_db=form.username.data).first()
		if user is None:
			hashed_password = generate_password_hash(form.password.data, "sha256")
			user = register(name_db=form.name.data, username_db=form.username.data, password_hash=hashed_password, about_author=form.about_author.data)
			db.session.add(user)
			db.session.commit()
		
		name_db = form.name.data
		form.name.data=" "
		form.username.data=" "
		form.password.data=" "
		flash("User Added, you can now login")
		return redirect(url_for("login", form=form))
		
	all_info = register.query.order_by(register.date_added)
	return render_template("sign_up.html", form=form, all_info=all_info, name_db=name_db)
	
@app.route("/update_info/<int:id>", methods=["POST", "GET"])
def update_user(id):
	user_to_update = register.query.get_or_404(id)
	form = reg_form()
	if form.validate_on_submit():
		user_to_update.name_db = form.name.data
		user_to_update.username_db = form.username.data
		new_hashed = generate_password_hash(form.password.data, "sha256")
		user_to_update.password_hash = new_hashed
		user_to_update.about_author = form.about_author.data
		user_to_update.profile_pic_db = request.files["profile_pic"]
		pic_filename = secure_filename(user_to_update.profile_pic_db.filename)
		pic_name = str(uuid.uuid1()) + "_" + pic_filename
		saver = request.files["profile_pic"]
		user_to_update.profile_pic_db = pic_name
		try:
			db.session.add(user_to_update)
			db.session.commit()
			saver.save(os.path.join(app.config['UPLOAD_FOLDER']), pic_name)
			flash("User updated")
		except:
			flash("Error error")
			return redirect(url_for('dashboard'))
		
	form.name.data = user_to_update.name_db
	form.username.data = user_to_update.username_db
	form.about_author.data = user_to_update.about_author
	form.password.data = " "
	
	return render_template("update_user.html", form=form, user_to_update=user_to_update)

@app.route("/delete_user/<int:id>")
def delete_user(id):
	user_to_delete=register.query.get_or_404(id)
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User deleted")
		return redirect(url_for('sign_up'))
	except:
		flash("Error Deleting")
		return render_template('sign_up.html')

@app.route("/login", methods=["POST", "GET"])
def login():
	form = loginform()
	if form.validate_on_submit():
		one_user = register.query.filter_by(username_db=form.username.data).first()
		if one_user:
			if check_password_hash(one_user.password_hash, form.password.data):
				login_user(one_user)
				flash("Login Successful")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong password, try again")
		else:
			flash("User does not exist, kindly register below")
			return redirect (url_for("sign_up"))
	return render_template("login.html", form=form)

@app.route("/logout""", methods=["POST", "GET"])
@login_required
def logout():
	logout_user()
	flash("you have been logged out")
	return redirect(url_for('login'))
	
@app.route("/add_post", methods=["POST", "GET"])
def add_post():
	form = post_form()
	if form.validate_on_submit():
		poste = current_user.id
		one_post = posts_table(title_db=form.title.data, poster_id=poste, content_db=form.content.data)
		
		form.title.data=" "
		form.content.data=" "
		db.session.add(one_post)
		db.session.commit()
		flash("Post Submitted")
	return render_template("add_post.html", form=form)

@app.route("/update_post/<int:id>", methods=["POST", "GET"])
def update_post(id):
	post_update = posts_table.query.get_or_404(id)
	form = post_form()
	if form.validate_on_submit():
		post_update.title_db = form.title.data
		post_update.content_db = form.content.data
		db.session.add(post_update)
		db.session.commit()
		flash("Post Updated")
		return redirect(url_for('posts', id=post_update.id))
	
	if current_user.id == post_update.poster.id:
		form.title.data=post_update.title_db
		form.content.data=post_update.content_db
	else:
		flash("You can't update post")
		return redirect('posts')
	return render_template('update_post.html', form=form)

@app.route("/delete_post/<int:id>", methods=["POST", "GET"])
@login_required
def delete_post(id):
	post_delete = posts_table.query.get_or_404(id)
	id = current_user.id
	if id == post_delete.poster.id:
		try:
			db.session.delete(post_delete)
			db.session.commit()
			flash("post deleted")
		except:
			flash("Error Deleting post")
			return render_template("posts.html")
	else:
		flash("You can't delete this post")
		return redirect(url_for("posts"))
	return redirect(url_for("posts"))
	
	
@app.route("/posts", methods=["POST", "GET"])
def posts():
	view_post = posts_table.query.order_by(posts_table.date_posted)
	return render_template("posts.html", view_post=view_post)

@app.route("/single_post/<int:id>", methods=["POST", "GET"])
def single(id):
	single_post = posts_table.query.get_or_404(id)
	return render_template("single_post.html", single_post=single_post)

@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
	x = current_user.id
	return render_template("dashboard.html", x=x)

@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)
	
@app.route("/search", methods=["POST"])
def search():
	form = SearchForm()
	db_search = posts_table.query
	if form.validate_on_submit():
		keywords = form.searched.data
		results = db_search.filter(posts_table.content_db.like('%' + keywords + '%'))
		show_results = results.order_by(posts_table.title_db)
		return render_template("search.html", form=form, show_results=show_results)
	return render_template("search.html", form=form)
	
@app.route('/admin')
@login_required
def admin():
	id = current_user.id
	if id ==1:
		return render_template('admin.html')
	else:
		flash('Access Denied')
		return redirect(url_for('dashboard'))


