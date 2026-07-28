# Homing Frontend

Frontend preview for the **Homing** project, an AI-powered platform that helps users discover and adopt rescued pets through conversational recommendations.

This project is built with **Vite + Vanilla HTML/CSS/JavaScript** and serves as a UI prototype before integrating with the backend API.

---

## Tech Stack

- HTML5
- CSS3
- JavaScript (ES6+)
- Vite

---

## Project Structure

```text
frontend/
├── public/
│   ├── logo.svg
│   ├── hero.jpg
│   ├── pets/
│   └── icons/
│
├── src/
│   ├── css/
│   │   ├── variables.css
│   │   ├── typography.css
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   ├── landing.css
│   │   └── chat.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   └── chat.js
│   │
│   └── data/
│
├── index.html
├── chat.html
├── package.json
└── README.md
```

---

## Features

### Landing Page

- Responsive navigation bar
- Hero section
- Why Homing section
- Featured Pets
- Newsletter
- Footer

### Chat Page

- AI chat interface
- User and AI message bubbles
- Conversation area
- Message input
- Back to Home navigation

---

## Getting Started

Install dependencies

```bash
npm install
```

Run development server

```bash
npm run dev
```

Open your browser at

```
http://localhost:5173
```

---

## Current Status

This frontend currently contains static UI components for demonstration purposes.

Upcoming integrations include:

- FastAPI backend
- OpenAI API
- Pet recommendation engine
- Conversation history
- Streaming AI responses
- PostgreSQL database

---

## Authors

Developed as part of the **Homing** AI Rescue Pet Adoption project.