import { v4 as uuidv4 } from "uuid";

function uuid() {
    return uuidv4();
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