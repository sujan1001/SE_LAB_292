"""Robust parsers for the Lab 7 bike-share rental exercise."""


def parse_ride_duration(text):
    """Convert an HH:MM duration to minutes, returning 0 for invalid input."""
    if not isinstance(text, str):
        return 0

    fields = text.strip().split(":")
    if len(fields) != 2 or not all(field.strip() for field in fields):
        return 0

    try:
        hours = int(fields[0].strip())
        minutes = int(fields[1].strip())
    except (TypeError, ValueError):
        return 0

    if hours < 0 or minutes < 0 or minutes >= 60:
        return 0
    return hours * 60 + minutes


def format_station_code(code):
    """Format a station code as ZONE-NUMBER without raising on bad input."""
    if not isinstance(code, str):
        return "UNKNOWN"

    normalized = code.strip().upper()
    if not normalized:
        return "UNKNOWN"
    return normalized[0] + "-" + normalized[1:]


def parse_ride_log(line):
    """Parse type,minutes,subscriber, returning a safe default for bad input."""
    default = ("", 0, False)
    if not isinstance(line, str):
        return default

    parts = line.split(",", 2)
    if len(parts) != 3:
        return default

    bike_type, minutes_text, subscriber = (part.strip() for part in parts)
    try:
        minutes = int(minutes_text)
    except (TypeError, ValueError):
        return default

    return bike_type, minutes, subscriber.lower() == "yes"


def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    print("Duration in minutes:", parse_ride_duration(value))

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    print("Formatted station code:", format_station_code(value))

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    print("Parsed ride log:", parse_ride_log(value))


if __name__ == "__main__":
    main()
