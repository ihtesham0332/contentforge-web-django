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

TIMEOUT = 180
RETRIES = 2


def _get_token(user):
    token = getattr(user, "profile", None).hf_token if user.is_authenticated else ""
    return token or settings.API_AUTH_TOKEN


def _headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _post(endpoint, payload, token, timeout=TIMEOUT, retries=RETRIES):
    url = f"{settings.API_BASE_URL}{endpoint}"
    last_error = None
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, json=payload, headers=_headers(token), timeout=timeout)
            if resp.status_code == 404 and attempt < retries:
                logger.warning(f"404 on {endpoint} (attempt {attempt+1}), retrying...")
                import time; time.sleep(3)
                continue
            if resp.status_code == 500 and attempt < retries:
                logger.warning(f"500 on {endpoint} (attempt {attempt+1}), retrying...")
                import time; time.sleep(5)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout as e:
            last_error = e
            logger.warning(f"Timeout on {endpoint} (attempt {attempt+1})")
            if attempt < retries:
                import time; time.sleep(3)
        except requests.exceptions.RequestException as e:
            last_error = e
            logger.error(f"API error on {endpoint} (attempt {attempt+1}): {e}")
            if attempt < retries:
                import time; time.sleep(3)
        except json.JSONDecodeError as e:
            last_error = e
            logger.error(f"API returned non-JSON on {endpoint}")
            return {"error": "API returned an invalid response."}
    err_str = str(last_error)
    if "404" in err_str:
        return {"error": "The API is starting up — please wait a moment and try again."}
    if "500" in err_str or "Internal Server Error" in err_str:
        return {"error": "The AI model is loading. This can take 30-60 seconds on first use. Please try again."}
    return {"error": f"API request failed. Please try again."}


def warmup():
    try:
        resp = requests.get(
            f"{settings.API_BASE_URL}/",
            headers=_headers(_get_token(None)),
            timeout=30,
        )
        if resp.status_code == 200:
            logger.info("API warmup successful")
            return True
    except Exception as e:
        logger.warning(f"API warmup failed: {e}")
    return False


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
