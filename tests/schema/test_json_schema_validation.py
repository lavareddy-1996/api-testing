from jsonschema import validate, ValidationError, FormatChecker

json_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "suite": {"type": "string"},
                "city": {"type": "string"},
                "zipcode": {"type": "string"},
                "geo": {
                    "type": "object",
                    "properties": {
                        "lat": {"type": "string"},
                        "lng": {"type": "string"},
                    },
                    "required": ["lat", "lng"],
                },
            },
            "required": ["street", "suite", "city", "zipcode", "geo"],
        },
        "phone": {"type": "string"},
        "website": {"type": "string"},
        "company": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "catchPhrase": {"type": "string"},
                "bs": {"type": "string"},
            },
            "required": ["name", "catchPhrase", "bs"],
        },
    },
    "required": [
        "id",
        "name",
        "username",
        "email",
        "address",
        "phone",
        "website",
        "company",
    ],
}


def validate_schema(response_body, schema):
    """Validates the API response against the given JSON schema."""
    try:
        validate(instance=response_body, schema=schema, format_checker=FormatChecker())
        print("Schema validation passed")
        return True
    except ValidationError as e:
        print("Schema validation failed")
        print(f"Error: {e.message}")
        return False


def test_json_schema_validation(api_context):
    response = api_context.get("https://jsonplaceholder.typicode.com/users/1")
    assert response.status == 200

    response_body = response.json()
    print(response_body)

    assert validate_schema(response_body, json_schema)
