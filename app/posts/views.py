from flask import render_template, redirect, url_for, flash, request

from app import db
from app.posts import post_bp
from app.posts.models import Post, Tag
from app.posts.forms import PostForm
from app.users.models import User


def load_authors(form):
    users = db.session.scalars(
        db.select(User).order_by(User.id)
    ).all()
    form.author_id.choices = [
        (user.id, user.username) for user in users
    ]


def load_tags(form):
    tags = db.session.scalars(
        db.select(Tag).order_by(Tag.id)
    ).all()
    form.tags.choices = [
        (tag.id, tag.name) for tag in tags
    ]


@post_bp.route('/')
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )

    posts = db.session.scalars(stmt).all()

    return render_template(
        'posts/all_posts.html',
        posts=posts
    )


@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()

    load_authors(form)
    load_tags(form)

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            posted=form.publish_date.data,
            is_active=form.enabled.data,
            author_id=form.author_id.data
        )

        post.tags = db.session.scalars(
            db.select(Tag).where(
                Tag.id.in_(form.tags.data)
            )
        ).all()

        db.session.add(post)
        db.session.commit()

        flash('Пост успішно створено!', 'success')

        return redirect(url_for('post.all_posts'))

    return render_template(
        'posts/add_post.html',
        form=form,
        title='Створити пост'
    )


@post_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)

    return render_template(
        'posts/detail_post.html',
        post=post
    )


@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)

    form = PostForm(obj=post)

    load_authors(form)
    load_tags(form)

    if request.method == 'GET':
        form.enabled.data = post.is_active
        form.publish_date.data = post.posted
        form.author_id.data = post.author_id
        form.tags.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.enabled.data
        post.posted = form.publish_date.data
        post.author_id = form.author_id.data

        post.tags = db.session.scalars(
            db.select(Tag).where(
                Tag.id.in_(form.tags.data)
            )
        ).all()

        db.session.commit()

        flash('Пост успішно оновлено!', 'success')

        return redirect(
            url_for('post.detail_post', id=post.id)
        )

    return render_template(
        'posts/add_post.html',
        form=form,
        title='Редагувати пост',
        post=post
    )


@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()

        flash('Пост успішно видалено!', 'success')

        return redirect(url_for('post.all_posts'))

    return render_template(
        'posts/delete_confirm.html',
        post=post
    )
