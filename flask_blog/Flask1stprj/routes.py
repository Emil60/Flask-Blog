from Flask1stprj import app, db, mail, Message
from flask import render_template, flash, redirect, url_for, abort, request
from Flask1stprj.forms import RegisterForm, LoginForm, PostForm, ContactForm
from Flask1stprj.models import User, Post 
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/home')
@app.route('/')
def index():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page = 2)
    next_url = url_for('index', page=posts.next_num) if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title="Home", posts = posts, next_url = next_url, prev_url = prev_url)

@app.route('/about')
def about():
    return render_template('about.html',title="About")


@app.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            msg = Message(form.email.data, sender='me', recipients=['fakefake1478@gmail.com'])
            msg.body = "From: {} <{}> {}".format(form.email.data, form.number.data, form.message.data)
            mail.send(msg)
            flash("Zorsan", "success")
            return redirect(url_for('contact'))
        else:
            flash("OOPS", "danger")
    elif request.method == "GET":
        return render_template('contact.html',title="Contact", form = form)

@app.route('/services')
def services():
    return render_template('services.html',title="Services")

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(name = form.name.data, email = form.email.data, password = form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('{} account created'.format(form.name.data), 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html',title="Register Page",form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.name.data).first()
        #print(user)
        if user and user.password == form.password.data:
            login_user(user)
            flash('Hello {}'.format(form.name.data), 'success')
            return redirect(url_for('index'))
        else:
            flash('Your password or name entered wrong', 'danger')

    return render_template('login.html',title="Login Page",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data, subtitle = form.subtitle.data, post_text = form.post_text.data, user = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post is Created','success')
        return redirect(url_for('index'))
    return render_template('create_post.html',form=form, title="Create Post")


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post, title=post.title)

@app.route('/post/<int:post_id>/edit', methods=['GET','POST'])
def post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.post_text = form.post_text.data
        db.session.commit()
        flash('Post is edited','success')
        return redirect (url_for('post', post_id=post.id))
    
    elif request.method == "GET":
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.post_text.data = post.post_text

        return render_template('create_post.html',post=post, title='Edit post',form=form)

@app.route('/post/<int:post_id>/delete', methods=['GET'])
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Post is deleted','success')
    return redirect (url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
