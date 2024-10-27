import asyncio
import os
from typing import TYPE_CHECKING

import arrow
from pydis_core.utils import apply_monkey_patches

from sir_lancebot import log  # Changed from 'bot' to 'sir_lancebot'

if TYPE_CHECKING:
    from sir_lancebot.bot import Bot  # Changed from 'bot' to 'sir_lancebot'

log.setup()

# Set timestamp of when execution started (approximately)
start_time = arrow.utcnow()

# On Windows, the selector event loop is required for aiodns.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

apply_monkey_patches()

instance: "Bot" = None  # Global Bot instance.

