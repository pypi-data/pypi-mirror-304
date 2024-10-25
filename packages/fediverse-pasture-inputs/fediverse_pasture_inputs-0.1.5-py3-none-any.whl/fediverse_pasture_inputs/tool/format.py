from unittest.mock import AsyncMock, MagicMock
from bovine.testing import actor

import json

from fediverse_pasture_inputs.types import InputData
from fediverse_pasture.runner import ActivitySender


def activity_sender():
    aactor = MagicMock()
    aactor.id = actor["id"]
    aactor.build = MagicMock(return_value=actor)
    bovine_actor = AsyncMock()
    bovine_actor.get = AsyncMock(return_value={"inbox": "inbox"})
    sender = ActivitySender.for_actor(bovine_actor, aactor)
    sender.sleep_after_getting_inbox = False
    return sender


def write_json(fp, data):
    fp.write("```json\n")
    fp.write(json.dumps(data, indent=2, sort_keys=True))
    fp.write("\n```\n\n")


async def page_from_inputs(fp, inputs: InputData):
    sender = activity_sender()

    fp.write(f"# {inputs.title}\n\n")
    fp.write(inputs.frontmatter)

    fp.write("\n\n## Objects \n\n")

    for idx, ex in enumerate(inputs.examples):
        sender.init_create_note(lambda x: {**x, **ex})
        fp.write(f"\n### Object {idx+1}\n\n")
        obj = sender.note
        obj["@context"] = [
            "https://www.w3.org/ns/activitystreams",
            {"Hashtag": "as:Hashtag", "sensitive": "as:sensitive"},
        ]
        write_json(fp, obj)

    fp.write("\n\n## Activities \n\n")

    for idx, ex in enumerate(inputs.examples):
        sender.init_create_note(lambda x: {**x, **ex})
        await sender.send("http://remote.example/")

        fp.write(f"\n### Activity {idx+1}\n\n")
        write_json(fp, sender.activity)
