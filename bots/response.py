"""
Create the final JSON response.
"""


def build_response(answer, log_url):
    return {
        "answer": answer,
        "log_url": log_url
    }
