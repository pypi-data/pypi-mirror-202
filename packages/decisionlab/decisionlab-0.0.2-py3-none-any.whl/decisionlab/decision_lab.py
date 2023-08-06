import os
from ast import literal_eval
from urllib.request import urlopen
import json

URL_BASE = 'https://api.justdecision.com/v1/public'


class DecisionLab:
    def __init__(self, uuid=None):
        self.uuid = uuid or os.environ.get('DECISION_LAB_UUID')
        if not self.uuid:
            raise ValueError("UUID must be provided or set as an environment variable 'DECISION_LAB_UUID'")

    def get_decisions_list(self):
        url = f'{URL_BASE}/{self.uuid}'
        with urlopen(url) as response:
            data = response.read().decode()
            return json.loads(data)

    def get_decision(self, decision_name):
        url = f'{URL_BASE}/{self.uuid}/{decision_name}'
        with urlopen(url) as response:
            data = response.read().decode()
            response_json = json.loads(data)

        # Check if the response contains an error message
        if isinstance(response_json, dict) and response_json.get('success') is False:
            return []

        # Safely evaluate the response if it is a string representation of a literal
        if isinstance(response_json, str):
            try:
                response_json = literal_eval(response_json)
            except (ValueError, SyntaxError):
                pass  # Keep the response as a string if it cannot be evaluated as a literal

        return response_json
