import re
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Any


VENDOR_ID_PATTERN = re.compile(r"^[A-Z]{2}_[0-9]{3}$")
YEAR_WEEK_PATTERN = re.compile(r"^[0-9]{6}$")


