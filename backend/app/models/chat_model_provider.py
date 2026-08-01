class ChatModelProvider:

    def __init__(
        self,
        model,
        tools,
    ):
        self._chat = model.bind_tools(tools)

    def chat(self):

        return self._chat