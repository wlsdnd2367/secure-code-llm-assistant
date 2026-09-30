import os


class MissingGoogleAPIKeyError(RuntimeError):
    """Raised when the Gemini API key has not been configured."""


def get_google_api_key() -> str:
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not api_key:
        raise MissingGoogleAPIKeyError(
            "GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return api_key
