import frappe
from shopping.services.product import get_product, create_product, get_product_byId, update_product, delete_product

@frappe.whitelist(allow_guest=True)
def get_products():
    product = get_product()
    return product


@frappe.whitelist()
def create_products(product_name, price, desc):
    product = create_product(product_name, price, desc)
    return product

@frappe.whitelist( allow_guest = True) 
def getById(name):
    product = get_product_byId(name)
    return product

@frappe.whitelist()
def update_products(name, price, product_name):
    # Enforce POST request
    if frappe.request.method != "POST":
        return {
            "status_code": 400,
            "message": "Only POST requests are allowed for this endpoint"
        }
    
    # Call the update_product function
    return update_product(name, price, product_name)

@frappe.whitelist()
def delete_products(name):
    # Enforce DELETE request
    if frappe.request.method != "DELETE":
        return {
            "status_code": 400,
            "message": "Only DELETE requests are allowed for this endpoint"
        }
    
    # Ensure the name parameter is provided
    if not name:
        return {
            "status_code": 400,
            "message": "Missing required field: name"
        }
    
    # Call the delete_product function
    return delete_product(name)