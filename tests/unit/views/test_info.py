def test_get_info(app):
    response = app.test_client().get("/info/")

    assert response.status_code == 200
    assert '"name":"ras-rm-secure-message-v2"'.encode() in response.data
