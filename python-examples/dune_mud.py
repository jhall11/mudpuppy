from dune.character import Character
import logging

from mudpuppy_core import (
    Event,
    EventType,
    mudpuppy_core,
)

from mudpuppy import (
    on_mud_event,
)

logging.debug("Loading main dune script...")

char_map: dict[str, Character] = {}


@on_mud_event("Dune (TLS)", EventType.Prompt)
async def prompt_handler(event: Event):
    logging.debug(f'prompt is: "{str(event.prompt)}"')
    if str(event.prompt) == "Please enter your name: ":
        char_name = "havraha"
        await mudpuppy_core.send_line(event.id, char_name)
        char = char_map.get(char_name, Character(event.id, char_name))
        logging.debug(
            f"Detected login for {char_name};\nCharacter initialized: {repr(char)};\n list of characters: {repr(char_map)}")
    #     try to load char's settings/password and create a new event handler for autologin
    # elif str(event.prompt) == "Password: ":
    #     await mudpuppy_core.send_line(event.id, "ilovemath")


logging.debug("main dune script loaded!")
