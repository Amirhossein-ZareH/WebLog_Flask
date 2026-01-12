from flask import Flask , render_template , request , flash , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , login_user , logout_user , login_required , current_user , UserMixin

app = Flask(__name__,template_folder="templates")

app.config["SECRET_KEY"] = "zsedguihionjojinmjkpkmkm4784868448476y673sw3w4342"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

db = SQLAlchemy(app)
#1
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "برای دسترسی به این صفحه باید به حساب کاربری خود وارد شوید"

# id - name/username - email - password
class User(UserMixin, db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(80) , unique = True , nullable=False)
    email = db.Column(db.String(120) , unique =  True , nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    #7
    posts = db.relationship("Post" , backref = "author" , lazy = True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
#2
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# id - title - content - created_at
class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(200) , nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable =False, default=datetime.utcnow)
    #8
    user_id = db.Column(db.Integer , db.ForeignKey("user.id") , nullable=False)

# ORM
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", posts = posts)
#3
@app.route('/register' , methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
    
        if User.query.filter_by(username=username).first():
            flash("نام کاربری قبلا استفاده شده است" , "danger")
            return render_template("register.html")
        
        if User.query.filter_by(email=email).first():
            flash("این ایمیل قبلا استفاده شده است" , "danger")
            return render_template("register.html")
    
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("ثبت نام شما با موفقیت انجام شد")
        return redirect(url_for("login"))
    
    return render_template("register.html")

#5
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html" , username=current_user.username)

#4
@app.route('/login' , methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("ورود شما با موفقیت انجام شد")
            return redirect(url_for("dashboard"))
        else:
            flash("نام کاربری یا رمزعبور اشتباه است")
    return render_template("login.html")

#6
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/create_post' , methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        
        if not title or content:
            flash("عنوان و محتوا الزامی میباشد!!!" , "danger")
            return render_template("create_post.html")
        
        post = Post(title=title , content=content , user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("مقاله شما با موفقیت ذخیره شد")
        return redirect(url_for("index"))
    return render_template('create_post.html')

@app.route('/edit_post/<int : id>' , methods=["GET", "POST"])
@login_required
def create_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        flash("شما اجازه ویرایش این پست را ندارید" , "danger")
        return render_template("edit_post.html")
    
    if request.method == "POST":
        post.title = request.form["title"]
        post.content = request.form["content"]
        
        if not post.title or post.content:
            flash("عنوان و محتوا الزامی میباشد!!!" , "danger")
            return render_template("edit_post.html")
        
        db.session.commit()
        
def create_tables():
    with app.app_context():
        db.create_all()
        
        #9 delete this
        # if Post.query.count() == 0:
        #     sample_post = [
        #         Post(title="مقاله لیزر", content="متن مقاله لیزر"),
        #         Post(title="مقاله هوش مصنوعی", content="متن مقاله هوش مصنوعی"),
        #         Post(title="مقاله الگوریتم", content="متن مقاله الگوریتم")
        #     ]
            # for post in sample_post:
            #     db.session.add(post)
            # db.session.commit()

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)