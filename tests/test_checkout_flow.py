def test_full_checkout_lifecycle(client):
    # 1. Register a new Customer
    cust_payload = {
        "name": "Bob Builder",
        "email": "bob.builder@example.com",
        "phone": "+1 555 987 6543",
        "address": "123 Market Street, Apt 4B",
        "city": "San Francisco",
        "zipCode": "94105"
    }
    cust_res = client.post("/api/v1/customers", json=cust_payload)
    assert cust_res.status_code == 201
    customer_id = cust_res.get_json()["data"]["id"]

    # 2. Get customer's cart
    cart_res = client.get(f"/api/v1/carts/customer/{customer_id}")
    assert cart_res.status_code == 200
    cart_id = cart_res.get_json()["data"]["id"]

    # 3. Add products to cart
    # Product 1 (Avocado $4.99 x 2 = $9.98)
    client.post(f"/api/v1/carts/{cart_id}/items", json={"productId": 1, "quantity": 2})
    # Product 4 (Milk $4.29 x 1 = $4.29)
    client.post(f"/api/v1/carts/{cart_id}/items", json={"productId": 4, "quantity": 1})

    # Verify cart totals: Subtotal $14.27, Tax (7%) $1.00, Delivery Fee $3.99, Total $19.26
    cart_view = client.get(f"/api/v1/carts/{cart_id}").get_json()["data"]
    assert cart_view["totalItemCount"] == 3
    assert cart_view["subtotal"] == 14.27
    assert cart_view["taxAmount"] == 1.00
    assert cart_view["deliveryFee"] == 3.99
    assert cart_view["totalAmount"] == 19.26

    # 4. Checkout
    checkout_payload = {
        "cartId": cart_id,
        "deliveryAddress": "123 Market Street, Apt 4B",
        "deliveryCity": "San Francisco",
        "deliveryZipCode": "94105",
        "deliveryInstructions": "Please ring buzzer #4B"
    }
    order_res = client.post("/api/v1/checkout", json=checkout_payload)
    assert order_res.status_code == 201
    order_data = order_res.get_json()["data"]
    assert order_data["status"] == "CONFIRMED"
    assert order_data["paymentStatus"] == "PAID"
    assert order_data["totalAmount"] == 19.26
    order_id = order_data["id"]
    order_number = order_data["orderNumber"]

    # 5. Verify cart is now empty
    cart_after = client.get(f"/api/v1/carts/{cart_id}").get_json()["data"]
    assert len(cart_after["items"]) == 0
    assert cart_after["subtotal"] == 0.0

    # 6. Lookup order by ID and order number
    res_by_id = client.get(f"/api/v1/orders/{order_id}")
    assert res_by_id.status_code == 200
    assert res_by_id.get_json()["data"]["orderNumber"] == order_number

    res_by_num = client.get(f"/api/v1/orders/number/{order_number}")
    assert res_by_num.status_code == 200
    assert res_by_num.get_json()["data"]["id"] == order_id

    # 7. Update order status to OUT_FOR_DELIVERY
    update_res = client.patch(f"/api/v1/orders/{order_id}/status", json={"status": "OUT_FOR_DELIVERY"})
    assert update_res.status_code == 200
    assert update_res.get_json()["data"]["status"] == "OUT_FOR_DELIVERY"
