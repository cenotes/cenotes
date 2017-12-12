def test_404(client):
    response = client.get("non_existent")
    assert response.status_code == 404
    assert response.json["success"] is False
    assert response.json["error"] != ""
    assert response.json["key"] == ""
    assert response.json["payload"] == ""
    assert response.json["plaintext"] == ""
    assert response.json["expiration_date"] == ""
    assert response.json["max_visits"] == ""


def test_400(client):
    response = client.get("/notes/encrypt/")
    assert response.status_code == 400
    assert response.json["success"] is False
    assert response.json["error"] != ""
    assert response.json["key"] == ""
    assert response.json["payload"] == ""
    assert response.json["plaintext"] == ""
    assert response.json["expiration_date"] == ""
    assert response.json["max_visits"] == ""
