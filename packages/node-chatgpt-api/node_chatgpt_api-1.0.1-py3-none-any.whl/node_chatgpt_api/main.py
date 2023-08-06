import os
import requests
from pathlib import Path
from tempfile import gettempdir
from cache3 import DiskCache
from .types.message import Message, BingMessage
from .types.response import Response, BingResponse


class Client:
    def __init__(self, url="http://localhost:3000", **kwargs):
        self.url = url
        self.kwargs = kwargs

    def request(self, message: Message | BingMessage, **kwargs):
        data = message.to_dict()

        if self.kwargs:
            data = message.to_dict() | self.kwargs
        if kwargs:
            data = message.to_dict() | kwargs

        res = requests.post(self.url + "/conversation",
                            json=data).json()

        return res

    def ask(self, message: Message, **kwargs) -> Response:
        res = self.request(message, **kwargs)
        return Response(res)


class BingAIClient(Client):
    cache = DiskCache(str(Path(os.path.join(gettempdir(), "node-chatgpt-api_cache")).absolute()))

    def __init__(self, url="http://localhost:3000", **kwargs):
        super().__init__(url, **kwargs)

        if self.kwargs.get("jailbreakConversationId"):
            self._renew_jailbreak_conversation_id()

    @cache.memoize(timeout=60 * 60 * 24 * 7, tag="cached:jailbreakConversationId")
    def _renew_jailbreak_conversation_id(self):
        jailbreakConversationId = self.ask(BingMessage("Hi, who are you?", jailbreakConversationId=True),
                                           skipJailbreakCheck=True).jailbreakConversationId
        return jailbreakConversationId

    def ask(self, message: BingMessage, **kwargs) -> BingResponse:
        if not kwargs.get("skipJailbreakCheck") \
                and self.kwargs.get("jailbreakConversationId"):
            self.kwargs["jailbreakConversationId"] = self._renew_jailbreak_conversation_id()
        else:
            del kwargs["skipJailbreakCheck"]

        res = self.request(message, **kwargs)
        return BingResponse(res)
