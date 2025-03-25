
from src.t8_client.module import convert_unix_to_iso


def test_convert_unix_to_iso() -> None:
    timestamp = 1609459200
    iso_string = convert_unix_to_iso(timestamp)
    assert iso_string == ("2021-01-01T00:00:00"), (
        f"Expected '2021-01-01T00:00:00', got {iso_string}"
    )
    timestamp = 0
    iso_string = convert_unix_to_iso(timestamp)
    assert iso_string == ("1970-01-01T00:00:00"), (
        f"Expected '1970-01-01T00:00:00', got {iso_string}"
    )
