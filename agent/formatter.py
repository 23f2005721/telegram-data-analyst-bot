"""
formatter.py

Guarantees that every response returned to Telegram
is valid JSON.
"""

import json


class Formatter:

    @staticmethod
    def success(data):

        return json.dumps(
            data,
            ensure_ascii=False
        )

    @staticmethod
    def error(message):

        return json.dumps(
            {
                "error": message
            },
            ensure_ascii=False
        )
