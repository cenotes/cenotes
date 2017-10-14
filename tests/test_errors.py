import pytest


def test_404(client):
    response = client.get("non_existent")
    assert response.status_code == 404
    assert response.json["success"] is False
    assert response.json["error"] != ""
    assert response.json["enotes"] == []
