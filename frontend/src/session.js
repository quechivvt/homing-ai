function uuid() {
    return crypto.randomUUID();
}

export function getSessionId() {

    let sessionId = localStorage.getItem("session_id");

    if (!sessionId) {

        sessionId = uuid();

        localStorage.setItem(
            "session_id",
            sessionId,
        );
    }

    return sessionId;
}