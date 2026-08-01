from typing import Any

from langchain_core.messages import (
    AIMessage,
    ChatMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from langchain_openai.chat_models.base import (
    _format_message_content,
    _lc_invalid_tool_call_to_openai_tool_call,
    _lc_tool_call_to_openai_tool_call,
)


def _convert_message_to_dict(message):
    message_dict: dict[str, Any] = {
        "content": _format_message_content(message.content)
    }

    if (name := message.name or message.additional_kwargs.get("name")) is not None:
        message_dict["name"] = name

    if isinstance(message, ChatMessage):
        message_dict["role"] = message.role

    elif isinstance(message, HumanMessage):
        message_dict["role"] = "user"

    elif isinstance(message, AIMessage):
        message_dict["role"] = "assistant"

        if message.tool_calls or message.invalid_tool_calls:

            tool_calls = [
                _lc_tool_call_to_openai_tool_call(tc)
                for tc in message.tool_calls
            ] + [
                _lc_invalid_tool_call_to_openai_tool_call(tc)
                for tc in message.invalid_tool_calls
            ]

            # ===== COPY GOOGLE extra_content =====
            if "tool_calls" in message.additional_kwargs:
                raw_calls = message.additional_kwargs["tool_calls"]

                for src, dst in zip(raw_calls, tool_calls):
                    if "extra_content" in src:
                        dst["extra_content"] = src["extra_content"]

            message_dict["tool_calls"] = tool_calls

        elif "tool_calls" in message.additional_kwargs:
            # KHÔNG LỌC extra_content
            message_dict["tool_calls"] = message.additional_kwargs["tool_calls"]

        elif "function_call" in message.additional_kwargs:
            message_dict["function_call"] = message.additional_kwargs["function_call"]

        if (
            "function_call" in message_dict
            or "tool_calls" in message_dict
        ):
            message_dict["content"] = message_dict["content"] or None

    elif isinstance(message, SystemMessage):
        message_dict["role"] = message.additional_kwargs.get(
            "__openai_role__",
            "system",
        )

    elif isinstance(message, FunctionMessage):
        message_dict["role"] = "function"

    elif isinstance(message, ToolMessage):
        message_dict["role"] = "tool"
        message_dict["tool_call_id"] = message.tool_call_id

        supported_props = {
            "content",
            "role",
            "tool_call_id",
        }

        message_dict = {
            k: v
            for k, v in message_dict.items()
            if k in supported_props
        }

    else:
        raise TypeError(message)

    return message_dict