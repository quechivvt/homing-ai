import "./css/base.css";
import "./css/chat.css";
import "./css/components.css";
import "./css/layout.css";
import "./css/typography.css";
import "./css/variables.css";

import {
    deleteConversation,
    getConversation,
    getConversations
} from "./api/conversation";

import { streamChat } from "./api/chat";
import { getSessionId } from "./session";

import DOMPurify from "dompurify";
import hljs from "highlight.js";
import { marked } from "marked";

import "highlight.js/styles/github.css";

marked.setOptions({

    breaks: true,

    highlight(code, language) {

        if (
            language &&
            hljs.getLanguage(language)
        ) {

            return hljs.highlight(
                code,
                {
                    language
                }
            ).value;

        }

        return hljs.highlightAuto(
            code
        ).value;

    }

});

const params =
    new URLSearchParams(
        window.location.search
    );

let conversationId =
    params.get(
        "conversation_id"
    );

const historyBtn =
    document.querySelector(
        ".history-btn"
    );

const historyDropdown =
    document.querySelector(
        ".history-dropdown"
    );

const historyList =
    document.querySelector(
        ".history-list"
    );

const form =
    document.querySelector(
        ".chat-input"
    );

const input =
    form.querySelector(
        "input"
    );

const sendButton =
    form.querySelector(
        "button"
    );

const newChatBtn =
    document.querySelector(
        ".new-chat-btn"
    );

init();

async function init() {

    bindEvents();

    if (!conversationId) {
        return;
    }

    try {

        const conversation =
            await getConversation(
                conversationId
            );

        renderConversation(
            conversation
        );

    } catch (error) {

        console.error(error);

    }

}

function renderConversation(conversation) {
    const container = document.querySelector(".conversation");

    container.innerHTML = "";

    conversation.messages.forEach(renderMessage);

    scrollToBottom();
}

function bindEvents() {

    historyBtn.addEventListener(
        "click",
        openHistory
    );

    newChatBtn.addEventListener(
        "click",
        newChat
    );

    historyDropdown.addEventListener(
        "click",
        e => e.stopPropagation()
    );

    document.addEventListener(
        "click",
        () => {

            historyDropdown.classList.add(
                "hidden"
            );

        }
    );

    form.addEventListener(
        "submit",
        sendMessage
    );

}

async function openHistory(e) {

    e.stopPropagation();

    historyDropdown.classList.toggle(
        "hidden"
    );

    if (
        historyDropdown.classList.contains(
            "hidden"
        )
    ) {
        return;
    }

    try {

        await loadHistory();

    } catch (error) {

        console.error(error);

    }

}

async function loadHistory() {

    const conversations =
        await getConversations(
            getSessionId()
        );

    renderHistory(
        conversations
    );

}

function renderHistory(conversations) {

    historyList.innerHTML = "";

    conversations.forEach(conversation => {

        const item =
            document.createElement(
                "div"
            );

        item.className =
            "history-item";

        const remove =
            document.createElement(
                "button"
            );

        remove.className =
            "history-delete";

        remove.innerHTML =
            "&times;";
        
                remove.onclick = async (e) => {

            e.stopPropagation();

            try {

                await deleteConversation(
                    conversation.id
                );

                if (
                    conversation.id ===
                    conversationId
                ) {

                    conversationId = null;

                    history.replaceState(
                        {},
                        "",
                        "/chat"
                    );

                    document.querySelector(
                        ".conversation"
                    ).innerHTML = "";

                }

                await loadHistory();

            } catch (error) {

                console.error(error);

            }

        };

        const title =
            document.createElement(
                "span"
            );

        title.textContent =
            conversation.title ||
            "Untitled";

        item.append(
            title,
            remove
        );

        item.onclick =
            async () => {

                try {

                    conversationId =
                        conversation.id;

                    history.pushState(
                        {},
                        "",
                        `?conversation_id=${conversationId}`
                    );

                    const data =
                        await getConversation(
                            conversationId
                        );

                    console.log(data);

                    renderConversation(
                        data
                    );

                    historyDropdown.classList.add(
                        "hidden"
                    );

                } catch (error) {

                    console.error(
                        error
                    );

                }

            };

        historyList.appendChild(
            item
        );

    });

}


function renderMessage(message) {
    message.content.forEach(item => {
        switch (item.type) {
            case "text":
                renderTextMessage(message.role, item.text);
                break;

            case "pet_card":
                renderPetCard(item);
                break;

            default:
                console.warn("Unknown content type:", item);
        }
    });
}

function renderTextMessage(role, text) {

    const container = document.querySelector(".conversation");

    const message = document.createElement("div");
    message.className = `message ${role === "assistant" ? "ai" : "user"}`;

    if (role === "assistant") {
        const avatar = document.createElement("img");
        avatar.src = "/logo.svg";
        avatar.alt = "AI";
        avatar.className = "avatar";
        message.appendChild(avatar);
    }

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    bubble.dataset.text = text;

    bubble.innerHTML = DOMPurify.sanitize(
        marked.parse(text)
    );

    message.appendChild(bubble);

    container.appendChild(message);

    scrollToBottom();

    return bubble;
}

function renderLoadingMessage() {
    const container = document.querySelector(".conversation");

    const message = document.createElement("div");
    message.className = "message ai loading-message";

    const avatar = document.createElement("img");
    avatar.src = "/logo.svg";
    avatar.alt = "AI";
    avatar.className = "avatar";

    const bubble = document.createElement("div");
    bubble.className = "bubble ai-bubble";

    bubble.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    message.append(avatar, bubble);

    container.appendChild(message);

    scrollToBottom();

    return message;
}



async function sendMessage(e) {

    e.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    sendButton.disabled = true;

    renderTextMessage("user", message);

    input.value = "";
    input.focus();

    const loading = renderLoadingMessage();

    // Bubble AI để stream token
    let aiBubble = null;
    let loadingRemoved = false;

    try {

        await streamChat(
            {
                session_id: getSessionId(),
                conversation_id: conversationId,
                message,
            },
            (event) => {

                console.log(event);

                switch (event.event) {

                    case "conversation":

                        conversationId = event.conversation_id;

                        history.replaceState(
                            {},
                            "",
                            `?conversation_id=${conversationId}`
                        );

                        break;

                    case "token":

                        if (!loadingRemoved) {

                            loading.remove();
                            loadingRemoved = true;

                            aiBubble = renderTextMessage(
                                "assistant",
                                ""
                            );

                        }

                        appendToken(aiBubble, event.token);

                        break;

                    case "pet_card":

                        renderPetCard(event.pet);

                        break;

                    case "tool_start":

                        console.log(
                            "Tool:",
                            event.tool,
                            "started"
                        );

                        break;

                    case "tool_end":

                        console.log(
                            "Tool:",
                            event.tool,
                            "finished"
                        );

                        break;

                    case "done":

                        if (!loadingRemoved) {
                            loading.remove();
                        }

                        break;

                    case "error":

                        throw new Error(event.message);

                }

            }
        );

        await loadHistory();

    } catch (error) {

        console.error(error);

        loading.remove();

        alert("Cannot connect to server.");

    } finally {

        sendButton.disabled = false;

    }

}

function appendToken(bubble, token) {

    bubble.dataset.text =
        (bubble.dataset.text || "") + token;

    bubble.innerHTML = DOMPurify.sanitize(
        marked.parse(
            bubble.dataset.text
        )
    );

    scrollToBottom();
}

function renderPetCard(card) {

    const container =
        document.querySelector(
            ".conversation"
        );

    const message =
        document.createElement(
            "div"
        );

    message.className =
        "message ai";

    const avatar =
        document.createElement(
            "img"
        );

    avatar.src =
        "/logo.svg";

    avatar.alt =
        "AI";

    avatar.className =
        "avatar";

    const bubble =
        document.createElement(
            "div"
        );

    bubble.className =
        "bubble ai-bubble";

    const petCard =
        document.createElement(
            "div"
        );

    petCard.className =
        "pet-card";

    petCard.innerHTML = `
        <img
            src="${card.image_url}"
            alt="${card.name}"
            class="pet-image"
        >

        <div class="pet-info">

            <h3>${card.name}</h3>

            <a
                href="${card.detail_url}"
                target="_blank"
            >
                View detail
            </a>

        </div>
    `;

    bubble.appendChild(
        petCard
    );

    message.append(
        avatar,
        bubble
    );

    container.appendChild(
        message
    );

}

function scrollToBottom() {

    const container =
        document.querySelector(
            ".conversation"
        );

    requestAnimationFrame(() => {

        container.scrollTop =
            container.scrollHeight;

    });

}

function newChat() {

    conversationId = null;

    history.replaceState(
        {},
        "",
        window.location.pathname
    );

    document.querySelector(
        ".conversation"
    ).innerHTML = "";

    input.value = "";

    input.focus();

}

