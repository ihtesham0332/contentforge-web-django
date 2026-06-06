import json
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

PLATFORMS = [
    ("youtube", "YouTube"),
    ("instagram", "Instagram"),
    ("linkedin", "LinkedIn"),
    ("facebook", "Facebook"),
    ("twitter", "X / Twitter"),
    ("tiktok", "TikTok"),
    ("pinterest", "Pinterest"),
]

TIMEOUT = 120


def _get_token(user):
    token = getattr(user, "profile", None).hf_token if user.is_authenticated else ""
    return token or settings.API_AUTH_TOKEN


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _post(endpoint, payload, token, timeout=TIMEOUT):
    url = f"{settings.API_BASE_URL}{endpoint}"
    try:
        resp = requests.post(url, json=payload, headers=_headers(token), timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        logger.warning(f"API timeout on {endpoint}")
        return {"error": "Request timed out. The model is processing — please try again."}
    except requests.exceptions.RequestException as e:
        logger.error(f"API error on {endpoint}: {e}")
        return {"error": f"API request failed: {str(e)}"}
    except json.JSONDecodeError:
        logger.error(f"API returned non-JSON on {endpoint}")
        return {"error": "API returned an invalid response."}


def analyze_seo(content, token):
    return _post("/analyze-seo", {"content": content}, token)


def analyze_youtube(content, token):
    return _post("/analyze/youtube", {"content": content}, token)


def analyze_instagram(content, token):
    return _post("/analyze/instagram", {"content": content}, token)


def analyze_linkedin(content, token):
    return _post("/analyze/linkedin", {"content": content}, token)


def analyze_facebook(content, token):
    return _post("/analyze/facebook", {"content": content}, token)


def analyze_twitter(content, token):
    return _post("/analyze/twitter", {"content": content}, token)


def analyze_tiktok(content, token):
    return _post("/analyze/tiktok", {"content": content}, token)


def analyze_pinterest(content, token):
    return _post("/analyze/pinterest", {"content": content}, token)


def analyze_grammar(text, token):
    return _post("/analyze/grammar", {"text": text}, token)


FUNCTIONS = {
    "seo": analyze_seo,
    "youtube": analyze_youtube,
    "instagram": analyze_instagram,
    "linkedin": analyze_linkedin,
    "facebook": analyze_facebook,
    "twitter": analyze_twitter,
    "tiktok": analyze_tiktok,
    "pinterest": analyze_pinterest,
}
