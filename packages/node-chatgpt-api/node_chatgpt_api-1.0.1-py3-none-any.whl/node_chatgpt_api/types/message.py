class Message:
    message: str | None
    conversationId: str | None
    parentMessageId: str | None
    conversationSignature: str | None
    clientId: str | None
    invocationId: str | None

    def __init__(self, message, **kwargs):
        self.message = message
        self.conversationId = kwargs.get("conversationId")
        self.parentMessageId = kwargs.get("parentMessageId")
        self.conversationSignature = kwargs.get("conversationSignature")
        self.clientId = kwargs.get("clientId")
        self.invocationId = kwargs.get("invocationId")

    def to_dict(self):
        data = {
            "message": self.message,
            "conversationId": self.conversationId,
            "parentMessageId": self.parentMessageId,
            "conversationSignature": self.conversationSignature,
            "clientId": self.clientId,
            "invocationId": self.invocationId,
            "stream": False
        }

        return {x: y for x, y in data.items() if y is not None}


class BingMessage(Message):
    jailbreakConversationId: str | bool | None

    def __init__(self, message, **kwargs):
        super().__init__(message, **kwargs)

        self.jailbreakConversationId = kwargs.get("jailbreakConversationId")

    def to_dict(self):
        data = super().to_dict()

        if self.jailbreakConversationId:
            data["jailbreakConversationId"] = self.jailbreakConversationId

        return data
