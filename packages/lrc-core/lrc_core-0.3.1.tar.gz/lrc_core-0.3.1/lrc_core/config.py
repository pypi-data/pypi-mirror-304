"""Config for lrc_core.
"""

import os
from dotenv import load_dotenv

load_dotenv()

TELNET_LOGIN_TIMEOUT = int(os.getenv("TELNET_LOGIN_TIMEOUT", "3"))
TELNET_LOGIN_DEFAULT_PASSWORD_PROMPT = os.getenv(
    "TELNET_LOGIN_DEFAULT_PROMPT", "Password:"
)


TELNET_LOGIN_PROMPT_REPLY_MAPPING = {
    TELNET_LOGIN_DEFAULT_PASSWORD_PROMPT: "Login Administrator",
    "E13": "60-1634-11",
}
TELNET_LOGIN_ALTERNATIVE_PASSWORD_PROMPTS = list(
    filter(
        lambda s: s != TELNET_LOGIN_DEFAULT_PASSWORD_PROMPT,
        TELNET_LOGIN_PROMPT_REPLY_MAPPING.keys(),
    )
)

SMP_IP = os.getenv("SMP_IP", "172.22.246.207")
SMP_PW = os.getenv("SMP_PW", None)

EPIPHAN_URL = os.getenv("EPIPHAN_URL", "http://172.23.8.102")
EPIPHAN_USER = os.getenv("EPIPHAN_USER", "admin")
EPIPHAN_PW = os.getenv("EPIPHAN_PW", None)
