# Documentation Technique — Projet Persona (G-AIA-410)

## 1. Introduction

Le projet **Persona** a pour objectif de créer un système automatisé de gestion d'utilisateurs et de curation de contenu via l'intelligence artificielle. Il est construit sur **n8n**, une plateforme d'automatisation no-code/low-code qui permet de relier des services tiers sans écrire une application de zéro.

Le projet se compose de deux workflows complémentaires livrés en deux binômes.

---

## 2. Architecture Technique

### 2.1 Binôme 1 — Chatbot & Authentification
**Fichier :** `persona.json`

Ce workflow gère toute la partie conversationnelle et collecte de profil.

| Nœud | Type | Rôle |
|---|---|---|
| `When chat message received` | Chat Trigger | Point d'entrée : reçoit le message de l'utilisateur |
| `AI Agent` | LangChain Agent | Cerveau du chatbot, applique le prompt système |
| `Google Gemini Chat Model` | LLM | Modèle de langage (Google Gemini via API) |
| `Simple Memory` | Buffer Memory | Conserve les 20 derniers messages du contexte |

**Prompt système (résumé) :**
- Phase 1 — Authentification : inscription ou connexion (pseudo + mot de passe).
- Phase 2 — Collecte du profil : e-mail, centres d'intérêt, heure de réception.
- Conformité RGPD intégrée : information et option de désinscription.
- L'agent a `retryOnFail: true` pour la robustesse en cas d'erreur API.

> **Modification récente :** Le nœud "Code in JavaScript" (extraction de session) a été retiré du workflow pour simplifier la chaîne. L'agent répond désormais directement sans étape de post-traitement.

---

### 2.2 Binôme 2 — News & Newsletter
**Fichier :** `binome2.json`

Ce workflow automatise la curation et l'envoi quotidien de la newsletter.

| Nœud | Type n8n | Rôle |
|---|---|---|
| `Déclencheur Programmé` | `n8n-nodes-base.scheduleTrigger` | Lance le workflow automatiquement chaque jour |
| `Récupérer Actus IA` | `n8n-nodes-base.rssFeedRead` | Fetche un flux RSS dédié à l'IA |
| `Récupérer Actus Tech` | `n8n-nodes-base.rssFeedRead` | Fetche le flux TechCrunch |
| `Limit` / `Limit1` | `n8n-nodes-base.limit` | Limite chaque flux aux derniers articles (évite la surcharge API) |
| `Fusionner les Actus` | `n8n-nodes-base.merge` | Regroupe les articles des deux sources en un seul tableau |
| `Filtrer et Résumer (IA)` | `@n8n/n8n-nodes-langchain.agent` | Sélectionne les articles pertinents et génère un résumé HTML |
| `Groq Chat Model` | `@n8n/n8n-nodes-langchain.lmChatGroq` | Modèle de langage (Groq/Llama) utilisé pour le filtrage/résumé |
| `Envoyer la Newsletter` | `n8n-nodes-base.emailSend` | Envoie le résumé HTML par e-mail via SMTP |

---

## 3. Comment Construire ces Workflows Manuellement dans n8n

> Si vous deviez créer ce projet vous-même, voici exactement ce que vous auriez fait — **sans écrire de JSON à la main**.

Les fichiers `.json` sont des **exports automatiques** générés par n8n. Le travail réel se fait dans l'interface graphique :

1. **Lancer n8n** via Docker (`docker-compose up -d`) et ouvrir `http://localhost:5678`.
2. **Créer un nouveau Workflow** en cliquant sur "+ New Workflow".
3. **Ajouter un nœud** en cliquant sur le bouton `+` ou en cherchant dans le catalogue (ex: "Chat Trigger", "RSS Feed", "Email Send").
4. **Connecter les nœuds** : tirer une flèche du point de sortie d'un nœud vers l'entrée du suivant.
5. **Configurer chaque nœud** : URL du RSS, prompt IA, identifiants SMTP, etc.
6. **Tester** : cliquer sur "Execute Workflow" pour voir l'exécution pas à pas.
7. **Exporter** : menu en haut à droite → "Download" — cela génère le fichier `.json` que l'on commit dans le dépôt.

---

## 4. Guide de Déploiement et d'Importation

### 4.1 Démarrage de l'Environnement
```bash
docker-compose up -d
```
Interface disponible sur `http://localhost:5678` (identifiants : *admin* / *admin*).

### 4.2 Importation des Workflows
1. Connectez-vous à l'interface n8n.
2. Allez dans **Workflows** → **Add Workflow**.
3. En haut à droite → **Import from File**.
4. Sélectionnez `persona.json`.
5. Répétez pour `binome2.json`.

---

## 5. Protocole d'Évaluation

Si un évaluateur souhaite tester les deux binômes, voici les étapes :

### 5.1 Prérequis des Identifiants
- **Clé API Google Gemini** dans le nœud LLM du Binôme 1 (`Google Gemini Chat Model`).
- **Clé API Groq** (gratuite sur [console.groq.com](https://console.groq.com)) dans le nœud LLM du Binôme 2 (`Groq Chat Model`).
- **Paramètres SMTP** (ex: Ethereal, Gmail App Password) dans le nœud "Envoyer la Newsletter".

### 5.2 Test du Binôme 1
1. Activer le workflow "Persona" importé.
2. Ouvrir l'URL du Chat Trigger et démarrer une conversation.
3. Vérifier que le bot demande : inscription/connexion → e-mail → centres d'intérêt → heure de réception.

### 5.3 Test du Binôme 2
1. Ouvrir le workflow "Binôme 2".
2. Cliquer sur **"Execute Workflow"** pour forcer son exécution manuelle.
3. Vérifier que les nœuds RSS récupèrent bien des articles.
4. Vérifier que le nœud IA génère un résumé HTML cohérent.
5. Confirmer la réception de l'e-mail newsletter.

---

## 6. Conclusion

Le système Persona délivre une chaîne d'automatisation complète de niveau professionnel. L'architecture est modulaire : ajouter une source RSS ou changer le modèle LLM ne nécessite que quelques clics dans l'interface n8n.
