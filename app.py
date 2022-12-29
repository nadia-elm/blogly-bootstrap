"""Blogly application."""

from flask import Flask,request,redirect,render_template,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User,Post

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:secret@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY']='SECRET'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()
@app.route('/users')
@app.route('/')
def users_list():
    """display a list of all users"""
    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/users/new')
def new_user_form():
    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def add_new_user():
    first = request.form['F']
    last = request.form['L']
    image= request.form['image']
    new_user = User(first_name= first, last_name= last, image_url= image  or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user-detail.html', user= user)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route("/users/<int:user_id>/edit")
def edit_page(user_id):
        return render_template('edit.html')
   


@app.route("/users/<int:user_id>/edit",methods=['POST'])
def edit_user_details(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url= request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


    ############################################################################
@app.route("/users/<int:user_id>/posts/new")
def post_form(user_id):
    user = User.query.get(user_id)
    return render_template('post.html', user = user)

@app.route("/users/<int:user_id>/posts/new",methods=['POST'])
def create_post(user_id):
    post = Post(title = request.form['title'], content= request.form['content'],)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{user_id}")
    

@app.route("/posts/<int:post_id>")
def display_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post_display.html', post = post)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post= Post.query.get_or_404(post_id)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")



@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    

    return redirect(f"/users/{post.user_id}")







