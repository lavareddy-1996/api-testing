"""
End-to-end CRUD workflow against the Restful Booker API:
1) Create Booking (POST)               -> BookingID
2) Get Booking Details (GET)           -> By ID, By Names, By Dates
3) Create Token (POST /auth)
4) Partial Update Booking (PATCH)
5) Full Update Booking (PUT)
6) Delete Booking (DELETE)

These tests intentionally run in sequence and share state (booking_id,
token) across the file, so they use their own module-scoped fixture
rather than the shared root-level `api_context` fixture.
"""

import pytest
from playwright.sync_api import Playwright

from config.config import RESTFUL_BOOKER_BASE_URL
from utils.json_reader import read_json


@pytest.fixture(scope="module")
def booking_session_context(playwright: Playwright):
    context = playwright.request.new_context()
    yield context
    context.dispose()


# -------------------------------------------------------------------
# 1) Create Booking (POST)
# -------------------------------------------------------------------
def test_create_booking(booking_session_context):
    """Create a new booking and validate response"""
    data = read_json("post_request_body.json")

    response = booking_session_context.post(
        f"{RESTFUL_BOOKER_BASE_URL}/booking", data=data
    )

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print("\nCreate Booking Response:", response_body)

    assert "bookingid" in response_body
    assert "booking" in response_body

    booking = response_body["booking"]
    assert booking["firstname"] == data["firstname"]
    assert booking["lastname"] == data["lastname"]
    assert booking["totalprice"] == data["totalprice"]
    assert booking["depositpaid"] == data["depositpaid"]
    assert booking["bookingdates"]["checkin"] == data["bookingdates"]["checkin"]
    assert booking["bookingdates"]["checkout"] == data["bookingdates"]["checkout"]

    # Stored at module level so later tests in this file can reuse it.
    # This means test order matters within this file (by design).
    global booking_id
    booking_id = response_body["bookingid"]


# -------------------------------------------------------------------
# 2) Get Booking Details (GET)
# -------------------------------------------------------------------
def test_get_booking_by_id(booking_session_context):
    """Get booking details using booking ID"""
    response = booking_session_context.get(
        f"{RESTFUL_BOOKER_BASE_URL}/booking/{booking_id}"
    )

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nBooking details fetched by ID {booking_id}:", response_body)

    assert "firstname" in response_body
    assert "lastname" in response_body


def test_get_booking_by_name(booking_session_context):
    """Get bookings filtered by first and last name"""
    name_params = {"firstname": "Jim", "lastname": "Brown"}
    response = booking_session_context.get(
        f"{RESTFUL_BOOKER_BASE_URL}/booking", params=name_params
    )

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nBooking details fetched by Name {name_params}:", response_body)

    assert len(response_body) > 0
    for item in response_body:
        assert "bookingid" in item


def test_get_booking_by_dates(booking_session_context):
    """Get bookings filtered by check-in and check-out dates"""
    date_params = {"checkin": "2025-12-15", "checkout": "2025-12-20"}
    response = booking_session_context.get(
        f"{RESTFUL_BOOKER_BASE_URL}/booking", params=date_params
    )

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nBooking details fetched by Dates {date_params}:", response_body)

    # No count assertion here - an empty list is valid if no bookings
    # fall within this date range.
    for item in response_body:
        assert "bookingid" in item


# -------------------------------------------------------------------
# 3) Create Token (POST /auth)
# -------------------------------------------------------------------
def test_create_token(booking_session_context):
    """Create an authentication token for further operations"""
    data = read_json("token_request_body.json")
    response = booking_session_context.post(
        f"{RESTFUL_BOOKER_BASE_URL}/auth", data=data
    )

    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print("\nToken creation response:", response_body)

    assert "token" in response_body
    global token
    token = response_body["token"]
    assert len(token) > 5


# -------------------------------------------------------------------
# 4) Partial Update Booking (PATCH)
# -------------------------------------------------------------------
def test_partial_update_booking(booking_session_context):
    """Partially update an existing booking"""
    data = read_json("patch_request_body.json")

    response = booking_session_context.patch(
        f"{RESTFUL_BOOKER_BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={token}"},
        data=data,
    )
    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nPartial Update Response for booking {booking_id}:", response_body)

    for key in data.keys():
        assert key in response_body
        assert response_body[key] == data[key]


# -------------------------------------------------------------------
# 5) Full Update Booking (PUT)
# -------------------------------------------------------------------
def test_full_update_booking(booking_session_context):
    """Update entire booking record"""
    data = read_json("put_request_body.json")

    response = booking_session_context.put(
        f"{RESTFUL_BOOKER_BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={token}"},
        data=data,
    )
    assert response.ok
    assert response.status == 200

    response_body = response.json()
    print(f"\nFull Update Response for booking {booking_id}:", response_body)

    assert response_body["firstname"] == data["firstname"]
    assert response_body["lastname"] == data["lastname"]
    assert response_body["totalprice"] == data["totalprice"]


# -------------------------------------------------------------------
# 6) Delete Booking (DELETE)
# -------------------------------------------------------------------
def test_delete_booking(booking_session_context):
    """Delete booking using auth token"""
    response = booking_session_context.delete(
        f"{RESTFUL_BOOKER_BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={token}"},
    )

    # Note: restful-booker returns 201 on a successful delete, which is an
    # unusual choice (200/204 is more typical) - this is just how this
    # particular practice API behaves.
    assert response.status == 201
    assert response.status_text == "Created"

    print("\nBooking deleted successfully - ID:", booking_id)
