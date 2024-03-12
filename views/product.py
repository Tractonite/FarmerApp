from flask import Blueprint, render_template

product_bp = Blueprint('product', __name__)

@product_bp.route('/products')
def product_list():
    return render_template('product/product_list.html')

@product_bp.route('/products/int:product_id')
def product_detail(product_id):
    return render_template('product/product_detail.html', product_id=product_id)
