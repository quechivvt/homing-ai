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