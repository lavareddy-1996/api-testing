from config.config import RESTFUL_BOOKER_BASE_URL
from utils.json_reader import read_json


def test_create_booking_from_json(api_context):
    request_body = read_json("post_request_body.json")

    response = api_context.post(f"{RESTFUL_BOOKER_BASE_URL}/booking", data=request_body)

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print("--------------------------------- Response Body ---------------------")
    print(response_body)

    assert "bookingid" in response_body
    assert "booking" in response_body

    # Compared dynamically against the source JSON file rather than
    # hardcoded literals, so the test still passes if the test-data
    # file's values are updated.
    booking = response_body["booking"]
    assert booking["firstname"] == request_body["firstname"]
    assert booking["lastname"] == request_body["lastname"]
    assert booking["totalprice"] == request_body["totalprice"]
    assert booking["depositpaid"] == request_body["depositpaid"]
    assert booking["additionalneeds"] == request_body["additionalneeds"]
    assert booking["bookingdates"]["checkin"] == request_body["bookingdates"]["checkin"]
    assert booking["bookingdates"]["checkout"] == request_body["bookingdates"]["checkout"]
