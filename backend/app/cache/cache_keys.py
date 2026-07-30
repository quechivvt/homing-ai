class CacheKey:

    @staticmethod
    def conversation_history(conversation_id: int) -> str:
        return f"conversation:{conversation_id}:history"

    @staticmethod
    def conversation_list(
        session_id: str,
    ) -> str:
        return f"conversation:list:{session_id}"

    @staticmethod
    def pet(pet_id: int) -> str:
        return f"pet:{pet_id}"

    @staticmethod
    def faq() -> str:
        return "faq"