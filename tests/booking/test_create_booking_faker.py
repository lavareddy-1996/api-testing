from datetime import datetime, timedelta

from faker import Faker

from config.config import RESTFUL_BOOKER_BASE_URL


def test_create_booking_with_faker(api_context):
    fake = Faker()

    first_name = fake.first_name()
    last_name = fake.last_name()
    totalprice = fake.random_int(500, 10000)
    depositpaid = fake.boolean()
    checkin_date = datetime.now().strftime("%Y-%m-%d")
    checkout_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    additional_needs = fake.word()

    request_body = {
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": {"checkin": checkin_date, "checkout": checkout_date},
        "additionalneeds": additional_needs,
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
    assert booking["firstname"] == first_name
    assert booking["lastname"] == last_name
    assert booking["totalprice"] == totalprice
    assert booking["depositpaid"] is depositpaid
    assert booking["additionalneeds"] == additional_needs
    assert booking["bookingdates"]["checkin"] == checkin_date
    assert booking["bookingdates"]["checkout"] == checkout_date
