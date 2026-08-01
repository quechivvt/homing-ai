import json

class StreamEncoder:

    @staticmethod
    def encode(event) -> str:
        return (
            json.dumps(
                event.model_dump(mode="json"),
                ensure_ascii=False,
            )
            + "\n"
        )