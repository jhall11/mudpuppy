import asyncio
import importlib
import logging

from typing import Any, Dict

from mudpuppy import (
    alias,
    on_connected,
    on_disconnected,
    on_event,
    on_gmcp,
    on_mud_disconnected,
    on_mud_event,
    on_new_session,
    trigger,
    unload_handlers,
)
from mudpuppy_core import (
    AliasId,
    Event,
    EventType,
    SessionId,
    mudpuppy_core,
)
from dune.guild import Guild


class Character:
    session_id: int
    guild: Guild = None

    hp: int = 0
    max_hp: int = 0
    sp: int = 0
    max_sp: int = 0
    char_name: str = "Unknown"
    full_name: str = "Unknown"
    guild_name: str = "Unknown"
    money: int = 0
    bank_money: int = 0
    exp: int = 0
    level: int = 0
    kills: int = 0

    def __init__(self, session_id: int, name: str):
        logging.debug("Initializing new character")
        self.session_id = session_id
        self.char_name = name


        # if gmcp? define somewhere else?
        @on_gmcp("Char.Name")
        async def gmcp_name(_session_id: SessionId, data: Any):
            await self.name(data)

        @on_gmcp("Char.Status")
        async def gmcp_status(_session_id: SessionId, data: Any):
            await self.status(data)

        @on_gmcp("Char.Vitals")
        async def gmcp_vitals(_session_id: SessionId, data: Any):
            await self.vitals(data)

        logging.debug(f"done initiating character {self.char_name} on session {self.session_id}")


    async def vitals(self, data: Any):
        logging.debug(f"updating session {self.session_id} with gmcp vitals: {data}")
        self.hp = data.get("hp", self.hp)
        self.max_hp = data.get("maxhp", self.max_hp)
        self.sp = data.get("sp", self.sp)
        self.max_sp = data.get("maxsp", self.max_sp)

    async def name(self, data: Any):
        self.char_name = data.get("name", self.char_name)
        self.full_name = data.get("fullname", self.full_name)
        self.guild_name = data.get("guild", self.guild_name)
        try:
            if self.guild_name != "Unknown" and self.guild is None:
                guild_module = importlib.import_module("dune.guilds." + self.guild_name.lower())
                guild_class = getattr(guild_module, self.guild_name.capitalize())
                self.guild = guild_class()
        except ImportError as e:
            logging.warning("Failed to load guild {}: {}", self.guild_name, e)
        # todo load guild

    async def status(self, data: Any):
        self.money = data.get("money", self.money)
        self.bank_money = data.get("bankmoney", self.bank_money)
        self.exp = data.get("xp", self.exp)
        self.level = data.get("level", self.level)
        self.kills = data.get("kills", self.kills)
