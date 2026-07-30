import "./css/base.css";
import "./css/components.css";
import "./css/landing.css";
import "./css/layout.css";
import "./css/variables.css";

import { getConversations } from "./api/conversation";
import { getSessionId } from "./session";

const buttons = document.querySelectorAll(
    'a[href="./chat.html"]'
);

buttons.forEach(button => {

    button.addEventListener("click", async (e) => {

        e.preventDefault();

        try {

            const sessionId = getSessionId();

            const conversations =
                await getConversations(sessionId);

            if (conversations.length === 0) {

                window.location.href = "/chat.html";

                return;
            }

            conversations.sort((a, b) =>
                new Date(b.updated_at) -
                new Date(a.updated_at)
            );

            window.location.href =
                `/chat.html?conversation_id=${conversations[0].id}`;

        } catch (error) {

            console.error(error);

            alert("Cannot connect to server.");

        }

    });

});