import { API_URL } from "../config";

export async function getConversations(sessionId) {

    const response = await fetch(
        `${API_URL}/v1/conversations?session_id=${sessionId}`
    );

    if (!response.ok) {
        throw new Error("Cannot load conversations.");
    }

    return await response.json();
}

export async function getConversation(conversationId) {

    const response = await fetch(
        `${API_URL}/v1/conversations/${conversationId}`
    );

    if (!response.ok) {
        throw new Error("Cannot load conversation.");
    }

    return await response.json();
}

export async function deleteConversation(conversationId) {

    const response = await fetch(
        `${API_URL}/v1/conversations/${conversationId}`,
        {
            method: "DELETE"
        }
    );

    if (!response.ok) {
        throw new Error("Cannot delete conversation.");
    }

}