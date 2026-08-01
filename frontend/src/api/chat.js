import { API_URL } from "../config";

export async function chat(request) {

    const response = await fetch(
        `${API_URL}/v1/chat`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(request)
        }
    );

    if (!response.ok) {
        throw new Error("Cannot chat.");
    }

    return await response.json();
}

export async function streamChat(request, onEvent) {

    const response = await fetch(
        `${API_URL}/v1/chat/stream`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
        }
    );

    if (!response.ok) {
        throw new Error("Cannot stream chat.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";

    while (true) {

        const { done, value } = await reader.read();

        if (done) {
            break;
        }

        buffer += decoder.decode(value, {
            stream: true,
        });

        const lines = buffer.split("\n");

        buffer = lines.pop() || "";

        for (const line of lines) {

            if (!line.trim()) {
                continue;
            }

            onEvent(JSON.parse(line));
        }
    }
}