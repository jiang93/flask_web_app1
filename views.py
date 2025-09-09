#/blog_port/views.py
from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_require
from puppycompany import db
from puppycompany import BlogPost
from puppycompany import BlogPostForm

blog_post = Blueprint('blog_posts', __name__)
## under __init__
# from puppycompany.blog_posts.view import blog_posts
# aap.register_blueprint(blog_posts)

# create post
@blog_post.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm
    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data, text=form.text.data, user_id=current_user.id)

        db.session.add(blog_post)
        db.commit()
        flash('Blog Post Created')
        return redirect(url_for(core.index))
    
    return render_template('create_post.html', form=form)

# read post
@blog_post.route('/read/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', title=blog_post.title, date=blog_post.date, post=blog_post)

#update post
@blog_post.route('/update/<int:blog_post_id>')
@login_required

def update_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    
    form = BlogPostForm

    if form.validate_on_submit():
        blog_post.title=form.title.data
        blog_post.text=form.text.data

        db.session.add(blog_post)
        db.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_post.blog_post'), blog_post.id=blog_post.id)
    
    elif request.method == 'GET':
        blog_post.title=form.title.data
        blog_post.text=form.text.data
    
    return render_template('create_post.html', title="Updating", form=form)

# delete post
@blog_post.route('/delete/<int:blog_post_id>')
@login_required

def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    
    if blog_post.author != current_user:
        abort(403)
    
    db.session.delete(blog_post)
    db.commit()
    flash('Blog Post Delete')
    return redirect(url_for('core.index'))