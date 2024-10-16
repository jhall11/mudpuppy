import asyncio
import logging

from mudpuppy import (
    alias,
    trigger,
)
from mudpuppy_core import (
    AliasId,
    SessionId,
    mudpuppy_core,
)

from dune.guild import Guild


class Atreid(Guild):

    def __init__(self):
        logging.debug("Initializing new Atreid")
        super().__init__()
        logging.debug("done initializing Atreid class")

    @alias(mud_name="Dune (TLS)", pattern="^ka$", name="kill all")
    async def kill_all(self, session_id: SessionId, _alias_id: AliasId, _line: str, _groups):
        await mudpuppy_core.send_line(
            session_id,
            "rampage",
        )
        await self.do_combat_round(session_id, 0)

    @trigger(mud_name="Dune (TLS)", pattern="^You ran ", name="ran")
    async def ran(self, session_id: SessionId, _alias_id: AliasId, _line: str, _groups):
        await asyncio.sleep(1)
        await mudpuppy_core.send_line(
            session_id,
            "eat eration",
        )
        await mudpuppy_core.send_line(
            session_id,
            "request eration",
        )
