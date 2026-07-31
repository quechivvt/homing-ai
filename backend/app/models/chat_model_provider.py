class ChatModelProvider:

    def __init__(
        self,
        model,
        tools,
    ):
        self._chat = model.bind_tools(tools)

    def chat(self):
        print("\n===== MODEL =====")
        print(type(self._chat))
        print(self._chat)

        return self._chat