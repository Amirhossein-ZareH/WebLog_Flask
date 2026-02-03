from flask import Flask , render_template , request , flash , redirect , url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , login_user , logout_user , login_required , current_user , UserMixin

app = Flask(__name__,template_folder="templates")

app.config["SECRET_KEY"] = "zsedguihionjojinmjkpkmkm4784868448476y673sw3w4342"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "برای دسترسی به این صفحه باید به حساب کاربری خود وارد شوید"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(80) , unique = True , nullable=False)
    email = db.Column(db.String(120) , unique =  True , nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    posts = db.relationship("Post" , backref = "author_rel" , lazy = True)  # تغییر نام backref
    comments = db.relationship("Comment" , backref = "author_rel" , lazy = True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # اصلاح شد به 'user.id'
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # رابطه با کاربر
    author = db.relationship('User', backref=db.backref('user_posts', lazy=True))
    
    # رابطه با نظرات
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Comment(db.Model):
    __tablename__ = 'comments'  # اضافه کردن نام جدول
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.Text , nullable=False)
    created_at = db.Column(db.DateTime , nullable = False , default=datetime.utcnow)
    user_id = db.Column(db.Integer , db.ForeignKey("user.id") , nullable = False)  # اصلاح به user.id
    post_id = db.Column(db.Integer , db.ForeignKey("posts.id") , nullable = False)  # اصلاح به posts.id
    
    # رابطه با کاربر
    author = db.relationship('User', backref=db.backref('user_comments', lazy=True))

@app.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("index.html", posts = posts)

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
        flash("ثبت نام شما با موفقیت انجام شد", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    user_posts = Post.query.filter_by(author_id=current_user.id).order_by(Post.created_at.desc()).all()  # اصلاح به author_id
    return render_template("dashboard.html" , user=current_user, posts=user_posts)

@app.route('/login' , methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("ورود شما با موفقیت انجام شد", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("نام کاربری یا رمزعبور اشتباه است", "danger")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("با موفقیت خارج شدید", "success")
    return redirect(url_for("index"))

@app.route('/create_post' , methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if not title or not content:
            flash("عنوان و محتوا الزامی میباشد!!!", "danger")
            return render_template("create_post.html")
        
        post = Post(title=title, content=content, author_id=current_user.id)  # اصلاح به author_id
        db.session.add(post)
        db.session.commit()
        flash("مقاله شما با موفقیت ذخیره شد", "success")
        return redirect(url_for("index"))
    return render_template('create_post.html')

@app.route('/edit_post/<int:id>' , methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if post.author_id != current_user.id:  # اصلاح به author_id
        flash("شما اجازه ویرایش این پست را ندارید", "danger")
        return redirect(url_for("index"))
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        if not title or not content:
            flash("عنوان و محتوا الزامی میباشد!!!", "danger")
            return render_template("edit_post.html", post=post)
        
        post.title = title
        post.content = content
        db.session.commit()
        flash("مقاله شما با موفقیت ویرایش شد", "success")
        return redirect(url_for("index"))
    
    return render_template("edit_post.html", post=post)

@app.route("/delete_post/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author_id != current_user.id:  # اصلاح به author_id
        flash("شما دسترسی لازم برای حذف این مقاله را ندارید !!!", "danger")
        return redirect(url_for("index"))
    
    db.session.delete(post)
    db.session.commit()
    flash("مقاله شما با موفقیت حذف شد", "success")
    return redirect(url_for("index"))

@app.route("/post/<int:id>", methods=["GET", "POST"])
def post_detail(id):
    post = Post.query.get_or_404(id)
    
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("برای ثبت نظر باید وارد شوید", "warning")
            return redirect(url_for("login"))
        
        content = request.form.get("comment", "").strip()
        if not content:
            flash("نظر نمی‌تواند خالی باشد", "danger")
            return redirect(url_for("post_detail", id=id))
        
        comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash("نظر شما با موفقیت ثبت شد", "success")
        return redirect(url_for("post_detail", id=id))
    
    comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.desc()).all()
    return render_template("post_detail.html", post=post, comments=comments)

@app.route("/delete_comment/<int:id>")
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    
    if comment.user_id != current_user.id:
        flash("شما اجازه حذف این نظر را ندارید", "danger")
        return redirect(url_for("post_detail", id=comment.post_id))
    
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    flash("نظر شما حذف شد", "success")
    return redirect(url_for("post_detail", id=post_id))

def create_tables():
    with app.app_context():
        db.create_all()
        

if __name__ == "__main__":
    create_tables()
    app.run(debug=True)