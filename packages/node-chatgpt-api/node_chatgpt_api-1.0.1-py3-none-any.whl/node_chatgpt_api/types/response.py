class Response:
    error: str | bool

    response: str | None
    conversationId: str | None
    conversationSignature: str | None
    clientId: str | None
    invocationId: str | None
    details: str | None

    def __init__(self, raw_response):
        self.error = False

        try:
            self.error = raw_response["error"]
        except KeyError:
            pass

        if self.error:
            return

        self.response = raw_response["response"]
        self.conversationId = raw_response["conversationId"]
        self.conversationSignature = raw_response["conversationSignature"]
        self.clientId = raw_response["clientId"]
        self.invocationId = raw_response["invocationId"]
        self.details = raw_response["details"]


class BingResponse(Response):
    jailbreakConversationId: str | bool | None

    def __init__(self, raw_response):
        super().__init__(raw_response)

        if self.error:
            return

        try:
            self.jailbreakConversationId = raw_response["jailbreakConversationId"]
        except KeyError:
            pass
