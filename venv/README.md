# Projet Persona — G-AIA-410

## Présentation

Ce dépôt contient les workflows n8n pour le projet **Persona**, un système automatisé de chatbot personnalisé et de newsletter par IA.

Le projet est divisé en **deux binômes** :

| Fichier | Binôme | Rôle |
|---|---|---|
| `persona.json` | Binôme 1 | Chatbot, authentification, collecte du profil utilisateur |
| `binome2.json` | Binôme 2 | Curation de news par IA et envoi de newsletter par e-mail |

---

## Contenu du Dépôt

- `persona.json` — Workflow Binôme 1 (chatbot conversation + authentification + profil)
- `binome2.json` — Workflow Binôme 2 (news + filtrage IA + newsletter)
- `docker-compose.yml` or `docker-compose up -d` — Déploiement rapide de n8n en local
- `documentation_projet.md` — Documentation complète du projet (aussi en PDF)

---

## Pourquoi Docker ?

n8n est une application Node.js complexe avec de nombreuses dépendances. L'installer globalement (`npm install -g n8n`) nécessite des droits administrateurs et peut créer des conflits avec d'autres projets sur la machine. 

**Docker** résout ces problèmes :
- ✅ Isolation totale : n8n tourne dans son propre environnement sans toucher au système
- ✅ Pas besoin de droits root pour faire tourner l'application
- ✅ Déploiement reproductible : n'importe qui peut lancer le projet avec une seule commande
- ✅ Les données sont persistées dans un volume Docker entre les redémarrages

## Lancer n8n (Docker)

**Pré-requis :** avoir Docker et Docker Compose installés.

```bash
# Lancer n8n en arrière-plan
docker-compose up -d

# Voir les logs en temps réel (optionnel)
docker-compose logs -f

# Arrêter n8n
docker-compose down
```

n8n sera disponible sur `http://localhost:5678`  
Identifiants par défaut : **admin** / **admin**

> Le fichier `docker-compose.yml` configure automatiquement le port, les identifiants et le volume de persistance des données.

---

## Importer les Workflows

1. Connectez-vous à l'interface n8n.
2. Cliquez sur **Workflows** → **Add Workflow**.
3. Menu en haut à droite → **Import from File**.
4. Sélectionnez `persona.json` (Binôme 1).
5. Répétez pour `binome2.json` (Binôme 2).

> **Important** : Après importation, vous devrez renseigner vos propres identifiants d'API dans les nœuds (API Google Gemini, SMTP pour les emails).

---

## Comment cela a été construit (processur normal n8n)

En conditions normales, ces workflows se créent **directement dans l'interface graphique n8n** par glisser-déposer :

1. On ouvre n8n dans le navigateur.
2. On crée un nouveau Workflow.
3. On ajoute des **nœuds** un par un depuis le catalogue.
4. On les connecte visuellement avec des flèches.
5. On configure chaque nœud (URL, prompt IA, credentials SMTP...).
6. On clique sur **"Execute Workflow"** pour tester.
7. On exporte via **"Download"** → le fichier JSON généré est celui du dépôt.

Les fichiers `.json` sont donc un *export* de ce travail visuel, pas quelque chose qu'on écrit à la main.

---

## Auteurs

Projet Epitech PGE2 — Promotion 2025
