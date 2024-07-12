import os
from dotenv import load_dotenv

load_dotenv()

COOKIES = {
    "MUID": os.getenv("MUID"),
    "SRCHD": os.getenv("SRCHD"),
    "SRCHUID": os.getenv("SRCHUID"),
    "_UR": os.getenv("_UR"),
    "MicrosoftApplicationsTelemetryDeviceId": os.getenv("MicrosoftApplicationsTelemetryDeviceId"),
}

HEADERS = {
    "Authority": os.getenv("AUTHORITY"),
    "Method": os.getenv("METHOD"),
    "Path": os.getenv("PATH"),
    "Scheme": os.getenv("SCHEME"),
    "Accept": os.getenv("ACCEPT"),
    "Accept-Encoding": os.getenv("ACCEPT_ENCODING"),
    "Accept-Language": os.getenv("ACCEPT_LANGUAGE"),
    "User-Agent": os.getenv("USER_AGENT"),
}
