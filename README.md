# TrendSU-Cloth-Shop
## A full stack application with Django and Bootstrap
## CS308 Software Engineering course project in Sabancı University

This is a women cloth shop application that presents a number of products in
categories and let users select and add the desired product/products to the shopping
cart to purchase them.

There are 3 roles in application: Customers, Sales Managers, Product Managers


Functionalities of User Panel:
* The customers shall view the products, search for the products, comment on the
products, rate the products, include products in their wishlists, place new orders, cancel
existing orders, and return previously purchased products.
* The store has a limited stock of items, when the user selects a product, the number of
items in the stock must be shown. When the shopping is done, that product should be
decreased from the stock and the order for delivery processing should be forwarded to
the delivery department, which will process the order for shipping. During order
processing the user should be able to see the status as: processing, in-transit, and
delivered.
* Once payment is made and confirmed by the (mock-up) banking entity,
an invoice must be shown on the screen and a pdf copy of the invoice should be emailed
to the user. 
* Users should be able to make comments and give ratings to the products. The ratings
typically are between 1 and 5 stars or 1 and 10 points. The comments should be
approved by the product manager before they become visible. 
* The user should be able to search products depending on their names or descriptions.
Additionally, the user should be able to sort products depending on their price or
popularity
* A customer shall also be able to selectively return a product and ask for a refund. In
such a case, the customer will select an already purchased product from his/her order
history within 30 days of purchase.




Functionalities of Product Managers: 
* The product managers shall add/remove products as well as product categories, and
manage the stocks. Everything related to stock shall be done by the product manager.
The product manager is also in the role of delivery department since it controls the stock.
This means, the product manager shall view the invoices, products to be delivered, and
the corresponding addresses for delivery. A delivery list has the following properties:
delivery ID, customer ID, product ID, quantity, total price, delivery address, and a field
showing whether the delivery has been completed or not. Last but not least, the product
managers shall approve or disapprove the comments. 




Functionalities of Sales Managers: 
* The sales managers are responsible for setting the prices of the products. They shall set
a discount on the selected items. When the discount rate and the products are given, the
system automatically sets the new price and notify the users, whose wish list includes
the discounted product, about the discount. They shall also view all the invoices in a
given date range, can print them or save them as “pdf” files. Last but not least, they shall
calculate the revenue and loss/profit in between given dates.
* If a customer wants to return a product, the sales manager will evaluate the refund request
and upon receiving the product back to the store will authorize the refund. The product
will be added back to the stock and the purchased price will be refunded to the
customer's account.



