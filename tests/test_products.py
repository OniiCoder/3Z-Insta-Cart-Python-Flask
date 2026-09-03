def test_get_all_products(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert len(json_data["data"]) >= 12

def test_filter_products_by_category(client):
    response = client.get("/api/v1/products?category=PRODUCE")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert all(p["category"] == "PRODUCE" for p in json_data["data"])

def test_search_products(client):
    response = client.get("/api/v1/products?search=Avocado")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"] is True
    assert len(json_data["data"]) > 0
    assert "Avocado" in json_data["data"][0]["name"]

def test_create_product(client):
    payload = {
        "sku": "SKU-TEST-STRAWBERRY",
        "name": "Organic Strawberries",
        "description": "Fresh juicy California strawberries",
        "category": "PRODUCE",
        "price": 3.99,
        "stockQuantity": 50,
        "imageUrl": "https://example.com/strawberries.jpg",
        "unit": "1 lb container"
    }
    response = client.post("/api/v1/products", json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["success"] is True
    assert json_data["data"]["name"] == "Organic Strawberries"
    assert json_data["data"]["price"] == 3.99
