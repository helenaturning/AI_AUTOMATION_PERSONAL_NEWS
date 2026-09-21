
# Persona Project - G-AIA-410

## Overview

This repository contains the n8n workflows for the **Persona** project, an automated system for a personalized AI chatbot and newsletter.

The project is split between **two pairs**:

| File | Pair | Role |
|---|---|---|
| `persona.json` | Pair 1 | Chatbot, authentication, user profile collection |
| `binome2.json` | Pair 2 | AI news curation and newsletter delivery by email |

---

## Repository Contents

- `persona.json`  Pair 1 workflow (chatbot conversation + authentication + profile)
- `binome2.json`  Pair 2 workflow (news + AI filtering + newsletter)
- `docker-compose.yml` or `docker-compose up -d`   Quick local deployment of n8n
---

## Why Docker?

n8n is a complex Node.js application with many dependencies. Installing it globally (`npm install -g n8n`) requires administrator rights and can create conflicts with other projects on the machine.

**Docker** solves these problems:
- ✅ Full isolation: n8n runs in its own environment without touching the system
- ✅ No root rights needed to run the application
- ✅ Reproducible deployment: anyone can launch the project with a single command
- ✅ Data is persisted in a Docker volume between restarts

## Running n8n (Docker)

**Prerequisites:** Docker and Docker Compose installed.

```bash
# Start n8n in the background
docker-compose up -d

# View logs in real time (optional)
docker-compose logs -f

# Stop n8n
docker-compose down
```

n8n will be available at `http://localhost:5678`  
Default credentials: **admin** / **admin**

> The `docker-compose.yml` file automatically configures the port, the credentials, and the data persistence volume.

---

## Importing the Workflows

1. Log in to the n8n interface.
2. Click **Workflows** → **Add Workflow**.
3. Top-right menu → **Import from File**.
4. Select `persona.json` (Pair 1).
5. Repeat for `binome2.json` (Pair 2).

> **Important**: After importing, you will need to enter your own API credentials in the nodes (Google Gemini API, SMTP for emails).

---

## How It Was Built (normal n8n process)

Under normal conditions, these workflows are created **directly in the n8n graphical interface** by drag and drop:

1. Open n8n in the browser.
2. Create a new Workflow.
3. Add **nodes** one by one from the catalog.
4. Connect them visually with arrows.
5. Configure each node (URL, AI prompt, SMTP credentials...).
6. Click **"Execute Workflow"** to test.
7. Export via **"Download"** → the generated JSON file is the one in the repository.

The `.json` files are therefore an *export* of this visual work, not something written by hand.

---

## Authors
Helena AKOFFON
BANKOLE Ketsia