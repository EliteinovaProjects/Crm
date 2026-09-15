import random
import string
from datetime import datetime


def generate_id(prefix: str = "", length: int = 8) -> str:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{timestamp}{random_str}"


def generate_lead_id() -> str:
    return generate_id("LD", 6)


def generate_user_id() -> str:
    return generate_id("USR", 6)


def generate_campaign_id() -> str:
    return generate_id("CMP", 6)


def generate_agent_id() -> str:
    return generate_id("AGT", 6)
