#/core/views.py
from puppycompanyblog.models import BlogPost
from flask import render_template, url_for, request, Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page', 2, type=int)
    blog_post = BlogPost.query.order_by(BlogPost.date.desc()).pageinate(page=page, per_page=6)
    return render_template('index.html', blog_post=blog_post)

@core.route('/info')
def info():
    return render_template('info.html')