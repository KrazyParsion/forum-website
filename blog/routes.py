from flask import abort, render_template, redirect, url_for, flash, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from blog import app, db, login_required
from blog.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from blog.models import User, Post, Comment

# Root endpoint 
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if session.get('user_id'):
        current_user=User.query.get(session['user_id'])
    else:
        current_user="Guest"
    # return f"Welcome {session['username']}"
    all_posts = Post.query.all()
    return render_template('dashboard.html', title='dashboard', posts=all_posts, current_user=current_user)

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username taken.', 'danger') 
        else:
            flash('Succcess!', 'success') 
            username=form.username.data
            password=form.password.data
            hashed_password=generate_password_hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('sign_in')) 
    return render_template('sign_up.html', title='Sign Up', form=form) 

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if request.method == "POST":
        username=form.username.data
        password=form.password.data
        # username = request.form["username"]
        # password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        flash('Invalid username or password.', 'danger')
    return render_template('sign_in.html', title='Sign In', form=form)

@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect(url_for("sign_in"))

@app.route('/posts', methods=['GET'])
@login_required
def posts():
    all_posts = Post.query.all()
    return render_template('posts.html', title='Posts', posts=all_posts)

@app.route('/posts/sort/newest', methods=['GET'])
def sort_newest_post():
    all_posts = Post.query.all()
    new_posts = all_posts[::-1]
    return render_template('posts.html', title='Posts', posts=new_posts)

@app.route('/post/sort/upvotes', methods=['GET'])
def sort_upvotes_post():
    all_posts = Post.query.order_by(Post.upvotes.desc()).all()
    return render_template('posts.html', title='Posts', posts=all_posts)


@app.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    current_user = User.query.get(session['user_id'])
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_post.html', title='Create Post', form=form, legend='Create Post')

@app.route('/post/<int:post_id>', methods=["POST", "GET"])
@login_required
def post(post_id):
    form = CommentForm()
    current_user = User.query.get(session['user_id'])
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, post_id=post_id, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect((url_for('post', post_id=post_id))
)
    post=Post.query.get_or_404(post_id)
    comments=Comment.query.filter_by(post_id=post_id).all()
    current_user = User.query.get(session['user_id'])
    return render_template('post.html', title=post.title, post=post, comments=comments, current_user=current_user, form=form)

@app.route('/post/<int:post_id>/upvote')
@login_required
def upvote(post_id):
    post=Post.query.get_or_404(post_id)
    post.upvotes += 1
    db.session.commit()
    return redirect(url_for('posts'))

@app.route('/post/<int:post_id>/downvote')
@login_required
def downvote(post_id):
    post=Post.query.get_or_404(post_id)
    post.downvotes += 1
    db.session.commit()
    return redirect(url_for('posts'))

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = User.query.get(session['user_id'])
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.content = form.content.data
        post.date_updated = datetime.utcnow()
        db.session.commit() 
        flash('Your post has been updated', 'success') 
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        return render_template('create_post.html', title='New Post', form=form, legend='Update Post')
    
# @app.route('/post/<int:post_id>/comment', methods=['GET', 'POST'])
# @login_required
# def comment_post(post_id):
#     comment = CommentForm()
#     post=Post.query.get_or_404(post_id)
#     current_user = User.query.get(session['user_id'])
#     return render_template('post.html', title=post.title, post=post, current_user=current_user)




@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user = User.query.get(session['user_id'])
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for('dashboard'))

@app.route('/database', methods=['GET', 'POST'])
def database():
    all_users = User.query.all()
    all_posts = Post.query.all()
    return render_template('database.html', title='Database', users=all_users, posts=all_posts)
