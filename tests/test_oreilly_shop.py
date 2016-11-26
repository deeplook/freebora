import requests


def test_shop_availability():
    "Test if O'Reilly online shop is reachable."

    url = 'http://shop.oreilly.com'
    resp = requests.get(url)
    assert resp.status_code == 200
