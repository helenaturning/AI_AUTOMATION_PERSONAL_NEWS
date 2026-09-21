# Explication des Workflows n8n — Nœud par Nœud

Ce document explique en détail la structure des fichiers JSON exportés par n8n, et ce que fait chaque nœud dans les deux workflows du projet Persona.

> **Comment lire un fichier JSON n8n ?**
> Chaque nœud est un objet dans le tableau `"nodes"`. Les connexions entre nœuds sont dans `"connections"`. L'ordre visuel (position sur le canvas) est dans `"position"`.

---

## Binôme 1 — `persona.json` : Chatbot & Authentification

### Vue d'ensemble du flux

```
[Message reçu] → [AI Agent ←— Gemini] → (fin)
                              ↑
                         [Mémoire]
```

---

### Nœud 1 : `When chat message received`

```json
"type": "@n8n/n8n-nodes-langchain.chatTrigger"
```

**Rôle :** C'est le **point d'entrée** du workflow. Il écoute les messages entrants depuis l'interface de chat intégrée à n8n (ou un widget embarqué sur un site).

**Paramètres clés :**
- `webhookId` : identifiant unique de l'URL de réception des messages.
- `options: {}` : configuration par défaut (pas de restriction de format).

**En résumé :** Dès qu'un utilisateur envoie un message, ce nœud le reçoit et le transmet au suivant.

---

### Nœud 2 : `AI Agent`

```json
"type": "@n8n/n8n-nodes-langchain.agent",
"typeVersion": 3.1,
"retryOnFail": true
```

**Rôle :** C'est le **cerveau du chatbot**. C'est un agent LangChain qui reçoit le message, applique le prompt système, et génère une réponse.

**Paramètre clé — `systemMessage` (prompt système) :**

Le prompt est divisé en 3 phases :

| Phase | Ce que l'agent fait |
|---|---|
| **AUTHENTIFICATION** | Demande si l'utilisateur veut s'inscrire ou se connecter. Vérifie les credentials. Refuse les injections. |
| **COLLECTE DU PROFIL** | Demande successivement : e-mail, centres d'intérêt, heure de réception de la newsletter. |
| **RGPD** | Informe l'utilisateur du stockage de ses données. Propose une désinscription. |

**`retryOnFail: true`** : si l'API Gemini répond avec une erreur, le nœud réessaie automatiquement.

---

### Nœud 3 : `Google Gemini Chat Model`

```json
"type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini"
```

**Rôle :** C'est le **modèle de langage** utilisé par l'AI Agent. Il est connecté à l'agent via un lien de type `ai_languageModel` (non visible comme une flèche classique, c'est une liaison spéciale en bas du nœud).

**Credentials :** `googlePalmApi` — clé API Google Gemini à configurer dans les paramètres n8n.

---

### Nœud 4 : `Simple Memory`

```json
"type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
"contextWindowLength": 20
```

**Rôle :** Donne une **mémoire conversationnelle** à l'agent. Il conserve les 20 derniers messages échangés pour que le bot comprenne le contexte (ex: ne pas redemander l'e-mail si déjà donné).

**Connexion :** Reliée à l'agent via un lien `ai_memory`.

---

## Binôme 2 — `binome2.json` : News & Newsletter

### Vue d'ensemble du flux

```
[Cron] → [RSS IA] → [Limit] ──→ [Merge] → [Agent IA ←— Groq] → [Email]
       → [RSS Tech] → [Limit1] ─↗
```

---

### Nœud 1 : `Déclencheur Programmé`

```json
"type": "n8n-nodes-base.scheduleTrigger",
"field": "days"
```

**Rôle :** Lance le workflow **automatiquement chaque jour**. Remplace le déclencheur manuel. On peut régler l'heure exacte dans les paramètres `rule`.

---

### Nœud 2 : `Récupérer Actus IA`

```json
"type": "n8n-nodes-base.rssFeedRead",
"url": "https://feeds.simplecast.com/54nAGcIl"
```

**Rôle :** Fetche les derniers articles/épisodes d'un flux RSS dédié à l'IA. Retourne une liste d'items avec titre, lien, résumé, date.

---

### Nœud 3 : `Récupérer Actus Tech`

```json
"type": "n8n-nodes-base.rssFeedRead",
"url": "https://techcrunch.com/feed/"
```

**Rôle :** Idem, mais pour TechCrunch. Les deux nœuds RSS sont lancés **en parallèle** depuis le déclencheur.

---

### Nœud 3b : `Limit` et `Limit1`

```json
"type": "n8n-nodes-base.limit",
"keep": "lastItems"
```

**Rôle :** Chaque nœud RSS retourne potentiellement des milliers d'articles. Les nœuds **Limit** ne conservent que les derniers articles (par défaut 1) afin de ne pas surcharger l'API du modèle de langage. `Limit` est branché après "Actus IA", `Limit1` après "Actus Tech".

---

### Nœud 4 : `Fusionner les Actus`

```json
"type": "n8n-nodes-base.merge",
"typeVersion": 2.1
```

**Rôle :** Regroupe les articles des deux sources en **un seul flux de données** avant de les envoyer à l'IA. Entrée 0 = flux IA, Entrée 1 = flux Tech.

---

### Nœud 5 : `Filtrer et Résumer (IA)`

```json
"type": "@n8n/n8n-nodes-langchain.agent",
"typeVersion": 1.1
```

**Rôle :** Agent IA qui reçoit tous les articles et :
1. **Filtre** ceux qui correspondent aux centres d'intérêt (IA, Tech, Startups par défaut).
2. **Résume** chaque article retenu en 3-4 phrases.
3. **Formate** la réponse en **HTML** prêt à être envoyé par e-mail (`<h2>`, `<p>`, `<a href=...>`).

---

### Nœud 6 : `Groq Chat Model`

```json
"type": "@n8n/n8n-nodes-langchain.lmChatGroq",
"model": "openai/gpt-oss-20b"
```

**Rôle :** Modèle de langage **Groq** (gratuit, ultra-rapide) connecté à l'agent de filtrage/résumé via `ai_languageModel`. Groq a été choisi plutôt que Google Gemini pour ses limites de quota beaucoup plus généreuses sur le plan gratuit.

**Credentials :** `groqApi` — clé API Groq gratuite à récupérer sur [console.groq.com](https://console.groq.com).

---

### Nœud 7 : `Envoyer la Newsletter`

```json
"type": "n8n-nodes-base.emailSend",
"html": "={{ $json.output }}"
```

**Rôle :** Envoie l'e-mail HTML généré par l'IA via SMTP.

**Paramètres à configurer :**
- `fromEmail` : adresse expéditeur
- `toEmail` : adresse destinataire (à terme, dynamique selon le profil Binôme 1)
- `subject` : objet de l'e-mail
- `html` : corps du mail — directement la sortie de l'agent IA (`$json.output`)

---

## Comprendre les `connections` dans le JSON

La section `"connections"` décrit **qui envoie quoi à qui**. Exemple :

```json
"Déclencheur Programmé": {
  "main": [[
    { "node": "Récupérer Actus IA", "type": "main", "index": 0 },
    { "node": "Récupérer Actus Tech", "type": "main", "index": 0 }
  ]]
}
```

→ Le déclencheur envoie son signal aux **deux** nœuds RSS en même temps (parallèle).

Les types de connexion spéciaux :
- `"main"` → flux de données classique
- `"ai_languageModel"` → connexion du modèle LLM vers l'agent
- `"ai_memory"` → connexion de la mémoire vers l'agent
