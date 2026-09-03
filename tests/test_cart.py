def test_get_cart(client):
    response = client.get("/api/v1/carts/1")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["data"]["id"] == 1

def test_add_item_to_cart(client):
    payload = {"productId": 1, "quantity": 2}
    response = client.post("/api/v1/carts/1/items", json=payload)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert len(json_data["data"]["items"]) >= 1
    assert json_data["data"]["items"][0]["quantity"] == 2

def test_clear_cart(client):
    # Add item first
    client.post("/api/v1/carts/1/items", json={"productId": 1, "quantity": 1})

    # Clear
    response = client.delete("/api/v1/carts/1/clear")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert len(json_data["data"]["items"]) == 0
    assert json_data["data"]["subtotal"] == 0.0

def test_insufficient_stock_error(client):
    payload = {"productId": 1, "quantity": 99999}
    response = client.post("/api/v1/carts/1/items", json=payload)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["error"] == "Insufficient Stock"
