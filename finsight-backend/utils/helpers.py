from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import hashlib
from dateutil import parser
import datetime
import json

def canonicalize_url(url: str) -> str:
    if not url:
        return None
    try:
        p = urlparse(url)
        scheme = p.scheme if p.scheme else "https"
        netloc = p.netloc.lower()
        path = p.path.rstrip('/')
        # remove utm_* and some tracking query params
        qs = dict(parse_qsl(p.query, keep_blank_values=True))
        qs = {k: v for k, v in qs.items() if not k.startswith('utm_')}
        query = urlencode(qs, doseq=True)
        canonical = urlunparse((scheme, netloc, path, '', query, ''))
        return canonical
    except Exception:
        return url

def make_fingerprint(url: str, title: str = "", summary: str = "") -> str:
    base = (url or (title + (summary or ""))).strip().lower()
    base = " ".join(base.split())  # normalize whitespace
    return hashlib.sha256(base.encode("utf-8")).hexdigest()

def parse_date_to_utc(datestr):
    """
    Parse many date formats to naive UTC datetime (no tzinfo).
    If datestr is already a datetime, normalize to UTC naive.
    """
    if datestr is None:
        return datetime.datetime.utcnow()
    if isinstance(datestr, datetime.datetime):
        dt = datestr
    else:
        try:
            dt = parser.isoparse(str(datestr))
        except Exception:
            try:
                dt = parser.parse(str(datestr))
            except Exception:
                return datetime.datetime.utcnow()
    # convert to UTC and return naive
    if dt.tzinfo is not None:
        dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt

def to_json_str(obj):
    try:
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)
