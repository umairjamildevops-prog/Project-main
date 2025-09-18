from app import app

def test_healthz():
    client = app.test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

