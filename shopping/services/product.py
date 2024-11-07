import frappe 

SUCCESS = 200
NOT_FOUND = 404
BAD_REQUEST = 400

def get_product():
    product = frappe.db.sql("""SELECT * FROM `tabproduct`""", as_dict=True)
    
    if product:
        status_code = SUCCESS
        body = product
    else:
        status_code = NOT_FOUND
        body = "Unable to get data... please try again"

    # Correctly constructing the product_response dictionary
    product_response = {
        "status_code": status_code,
        "body": body
    }

    return product_response



def before_create(product_name): 
    product_response = None
    
    # Query to check if product exists
    product = frappe.db.sql("""SELECT * FROM `tabproduct` WHERE product_name = %s""", (product_name,), as_dict=True)
    
    if product:
        status_code = 400  # BAD_REQUEST code
        message = "Product name has been taken already"
        product_response = {
            "status_code": status_code,
            "message": message
        }
    
    return product_response


def create_product(product_name, price, desc):
    product_response = before_create(product_name)
    if(product_response): 
          return product_response
    else:
      product = frappe.get_doc({
        "doctype": "product",  # Ensure this matches your doctype name
        "product_name": product_name,
        "price": price,
        "desc": desc
    })
    
    product.insert()  # This inserts the document into the database
    
    frappe.db.commit()  # Manually commit the transaction to save changes to the database

    return product_response

def get_product_byId(name): 
    product = frappe.db.sql("""SELECT * FROM `tabproduct` WHERE name = %s""", (name,), as_dict=True)
    
    if product:
        status_code = SUCCESS
        message = "Data was retrieved successfully"
        body = product
    else:
        status_code = NOT_FOUND
        message = "Product was not found"
        body = None  # Set `body` to `None` when the product is not found

    # Constructing the response dictionary
    response_product = {
        "status_code": status_code,
        "message": message,
        "body": body
    }
    
    return response_product

def update_product(product_name, price, name):
    try:
        # Execute the update SQL query
        frappe.db.sql("""
            UPDATE `tabproduct`
            SET price = %s,
                product_name = %s
            WHERE name = %s
        """, (price, product_name, name))
        
        # Commit the transaction
        frappe.db.commit()

        # Prepare the success response
        product_response = {
            "status_code": SUCCESS,
            "message": "Product updated successfully"
        }
    except Exception as e:
        # Rollback in case of any error
        frappe.db.rollback()
        product_response = {
            "status_code": BAD_REQUEST,
            "message": f"Failed to update product: {str(e)}"
        }

    return product_response

def delete_product(name): 
    try:
        frappe.db.sql("""
            DELETE FROM `tabproduct` WHERE name = %s
        """, (name,), as_dict = True)
        frappe.db.commit()

        product_response = {
            "status_code": SUCCESS,
            "message": "Product updated successfully"
        }
    except Exception as e:
        frappe.db.rollback()
        product_response = {
            "status_code": BAD_REQUEST,
            "message": f"Failed to update product: {str(e)}"
        }

    return product_response



