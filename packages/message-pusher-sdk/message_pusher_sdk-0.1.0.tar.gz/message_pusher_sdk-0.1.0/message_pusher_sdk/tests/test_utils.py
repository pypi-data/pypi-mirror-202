"""Sample unit test module using pytest-describe and expecter."""
# pylint: disable=redefined-outer-name,unused-variable,expression-not-assigned,singleton-comparison

from pathlib import Path

from htutil import file

from message_pusher_sdk.message_pusher_sdk import MessagePusherSDK


def describe_feet_to_meters():
    def push(expect):
        cfg = file.read_json(Path(__file__).parent / "config.json")
        sdk = MessagePusherSDK(cfg["host"], cfg["token"])
        resp = sdk.push(cfg["username"], "title", "desc", "")

        expect(resp) == None
