import frappe


def addToCart(product_id, total, price, quantity):
    product = frappe.get_doc({
        "doctype" : "cart",
        "product_id" : product_id,
        "total" : total,
        "price" : price,
        "quantity" : quantity,
        "parent" : "cart",
        "parenttype" : "cart"
    })

    product.insert(ignore_permissions=True)
    frappe.db.commit()
    return product


def get_cart_with_product_details(cart_id):
    cart_data = frappe.db.sql("""
        SELECT
            cart.name AS cart_id,
            cart.product_id,
            cart.total,
            cart.price,
            cart.quantity,
            product.name AS product_name,
            product.desc AS product_desc,
            product.price AS product_price
        FROM
            `tabcart` AS cart
        INNER JOIN
            `tabproduct` AS product ON cart.product_id = product.name
        WHERE
            cart.name = %s
    """, (cart_id), as_dict=True)

    if cart_data:
        return {
            "status_code": 200,
            "data": cart_data
        }
    else:
        return {
            "status_code": 404,
            "message": "No cart found with the specified ID"
        }
