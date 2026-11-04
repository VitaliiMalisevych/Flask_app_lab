import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app, request
from werkzeug.utils import secure_filename
from app.products import products_bp, db
from app.products.forms import ProductForm


def save_image(file):
    if not file or not file.filename:
        return None
    ext = os.path.splitext(secure_filename(file.filename))[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file.save(os.path.join(upload_folder, filename))
    return filename


def delete_image(filename):
    if filename:
        file_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        if os.path.exists(file_path):
            os.remove(file_path)


@products_bp.route('/')
def list_products():
    products = db.all()
    return render_template('products/list.html', products=products)


@products_bp.route('/<int:doc_id>')
def detail_product(doc_id):
    product = db.get(doc_id=doc_id)
    if not product:
        flash('Товар не знайдено!', 'danger')
        return redirect(url_for('products.list_products'))
    return render_template('products/detail_product.html', product=product)


@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        image_filename = save_image(form.image.data)
        product_data = {
            'name': form.name.data,
            'price': form.price.data,
            'amount': form.amount.data,
            'description': form.description.data,
            'image': image_filename
        }
        db.insert(product_data)
        flash('Товар успішно додано!', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/form.html', form=form, title="Додати товар")


@products_bp.route('/edit/<int:doc_id>', methods=['GET', 'POST'])
def edit_product(doc_id):
    product = db.get(doc_id=doc_id)
    if not product:
        flash('Товар не знайдено!', 'danger')
        return redirect(url_for('products.list_products'))

    form = ProductForm()

    if form.validate_on_submit():
        image_filename = product.get('image')
        if form.image.data and hasattr(form.image.data, 'filename') and form.image.data.filename:
            delete_image(image_filename)
            image_filename = save_image(form.image.data)

        updated_data = {
            'name': form.name.data,
            'price': form.price.data,
            'amount': form.amount.data,
            'description': form.description.data,
            'image': image_filename
        }
        db.update(updated_data, doc_ids=[doc_id])
        flash('Товар успішно оновлено!', 'success')
        return redirect(url_for('products.list_products'))

    elif request.method == 'GET':
        form.name.data = product.get('name')
        form.price.data = product.get('price')
        form.amount.data = product.get('amount')
        form.description.data = product.get('description')

    return render_template('products/form.html', form=form, title="Редагувати товар", product=product)


@products_bp.route('/delete/<int:doc_id>', methods=['POST'])
def delete_product(doc_id):
    product = db.get(doc_id=doc_id)
    if product:
        delete_image(product.get('image'))
        db.remove(doc_ids=[doc_id])
        flash('Товар видалено!', 'success')
    else:
        flash('Товар не знайдено!', 'danger')
    return redirect(url_for('products.list_products'))