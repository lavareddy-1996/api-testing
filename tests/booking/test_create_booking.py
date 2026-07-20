from config.config import RESTFUL_BOOKER_BASE_URL


def test_create_booking(api_context):
    request_body = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 1000,
        "depositpaid": True,
        "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
        "additionalneeds": "Breakfast",
    }

    response = api_context.post(f"{RESTFUL_BOOKER_BASE_URL}/booking", data=request_body)

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print("--------------------------------- Response Body ---------------------")
    print(response_body)

    assert "bookingid" in response_body
    assert "booking" in response_body

    booking = response_body["booking"]
    assert booking["firstname"] == "Jim"
    assert booking["lastname"] == "Brown"
    assert booking["totalprice"] == 1000
    assert booking["depositpaid"] is True
    assert booking["additionalneeds"] == "Breakfast"
    assert booking["bookingdates"]["checkin"] == "2018-01-01"
    assert booking["bookingdates"]["checkout"] == "2019-01-01"
