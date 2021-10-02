from flask import Flask, render_template, redirect, url_for, request, Blueprint, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import requests, os
from datetime import date
from . forms import LoginForm, RegisterForm, CreatePostForm, CreateCommentForm
from . import db
from .models import User, PhotoPost, Comment
from base64 import b64encode


views = Blueprint('views', __name__,template_folder='templates', static_folder='static')

@views.route('/')
def home():
    return render_template("index.html")

@views.route('/make-post', methods=['GET', 'POST'])
@login_required
def make_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = PhotoPost(
            img = form.img.data.read(),
            subtitle=form.subtitle.data,
            body=form.body.data,
            maps_url=form.maps_url.data,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('views.timeline'))
    return render_template("make-post.html", form=form)

@views.route('/view-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    form = CreateCommentForm()
    requested_post = PhotoPost.query.get(post_id)
    image = b64encode(requested_post.img).decode("utf-8")
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                text=form.comment.data,
                author_id=current_user.id,
                parent_post=requested_post
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('views.view_post', post_id=post_id)) #redirect stellt sicher, dass der Inhalt des Formulars gelöscht wird

    comments = Comment.query.filter_by(post_id=requested_post.id).all()
    return render_template("post.html",post=requested_post, image=image, form=form)

@views.route('/timeline')
@login_required
def timeline():
    posts = PhotoPost.query.order_by(PhotoPost.id.desc()).all()
    images = {}
    for i in range(0, len(posts)):
        images.update({posts[i].id: b64encode(posts[i].img).decode("utf-8")})
    return render_template("timeline.html", all_posts=posts, images=images)

