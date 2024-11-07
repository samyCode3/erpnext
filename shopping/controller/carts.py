import frappe
from shopping.services.cart import addToCart, get_cart_with_product_details

@frappe.whitelist()
def add_to_cart(product_id, total, price, quantity):
    if frappe.request.method != "POST":
        return {
            "status_code": 400,
            "message": "Only POST requests are allowed for this endpoint"
        }
    product = addToCart(product_id, total, price, quantity)
    return product


@frappe.whitelist(allow_guest=True)
def get_cart_with_product(cart_id):
    if frappe.request.method != "GET":
      return {
            "status_code": 400,
            "message": "Only POST requests are allowed for this endpoint"
        }
    product = get_cart_with_product_details(cart_id)
    return product
      