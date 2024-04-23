import re
import json


def extract_json(text_response: str) -> dict[str, list[str | float]]:
    # This pattern matches a string that starts with '{' and ends with '}'
    pattern = r"\{[^{}]*\}"

    matches = re.finditer(pattern, text_response)

    for match in matches:
        json_str: str = match.group(0)
        try:
            # Validate if the extracted string is valid JSON
            json_obj: dict[str, list[str | float]] = json.loads(json_str)
        except json.JSONDecodeError:
            continue

    return json_obj
