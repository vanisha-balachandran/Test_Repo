import requests
import json


def test_post_headers_body_json():
    url = "http://127.0.0.1:5000/projectpost"

    # Additional headers.
    headers = {'Content-Type': 'application/json'}

    # Body
    payload = {"name": "vanisha", 'countrycode': "AAA","district": "XXX", "population":123456}

    # convert dict to json string by json.dumps() for body data.
    resp = requests.post(url, headers=headers, data=json.dumps(payload, indent=4))

    # Validate response headers and body contents, e.g. status code.
    assert resp.status_code == 200
    resp_body = resp.json()
    assert resp_body['url'] == url

    # print response full body as text
    print(resp.text)