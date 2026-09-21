# Guide de Configuration et Dépannage — Projet Persona n8n

Ce document regroupe toutes les réponses et explications concernant la configuration du projet Persona (Binôme 2 et Binôme 1).

---

## 1. Pourquoi le nœud "Google Gemini" a planté ? (L'erreur sur l'image)

Sur ta capture d'écran, on voit que **"Récupérer Actus IA" a téléchargé 2881 articles** d'un coup ! 
Le nœud "Fusionner" a donc envoyé **2901 articles en même temps** à Google Gemini. L'Intelligence Artificielle a tout simplement "explosé" car elle ne peut pas lire 3000 articles en 5 secondes (elle a dépassé sa limite autorisée par Google, d'où la croix rouge).

**👉 Comment réparer ça dans n8n :**
1. Double-clique sur le nœud **"Récupérer Actus IA"**.
2. Cherche une option qui s'appelle **Max Items** ou **Limit**.
3. Active-la et mets **3** (pour ne récupérer que les 3 derniers articles).
4. Fais pareil pour la boîte **"Récupérer Actus Tech"** (mets une limite à 3).
5. Relance le workflow. L'IA ne recevra que 6 articles à traiter au total, et ça marchera instantanément !

---

## 2. Qu'est-ce que le compte SMTP ? 

**SMTP (Simple Mail Transfer Protocol)**, c'est le "facteur" virtuel. 
C'est la technologie universelle qui permet à ton ordinateur d'envoyer un e-mail sur internet. 

Dans n8n, le nœud "Envoyer la Newsletter" ne peut pas envoyer un e-mail par magie. Il doit "se connecter" à un vrai fournisseur d'e-mail (comme Microsoft Outlook, Gmail ou Yahoo) pour lui dire : *"Prends ce texte et envoie-le à cet utilisateur"*.

**Pourquoi y a-t-il besoin d'un "Credential" (mot de passe) ?**
C'est une obligation de sécurité. Si n8n n'a pas ton mot de passe Microsoft, Outlook refusera d'envoyer l'e-mail pour empêcher les hackers d'utiliser ton adresse pour envoyer du spam. 

**Configuration pour un compte Microsoft (Outlook/Hotmail) :**
Dans le nœud "Envoyer la Newsletter", ajoute un Credential SMTP avec ces infos :
- **Host** : `smtp.office365.com`
- **Port** : `587`
- **SSL/TLS** : Activé
- **User** : Ton adresse email Microsoft complète (ex: prenom@outlook.fr)
- **Password** : Ton mot de passe Microsoft (Si ça ne marche pas, tu dois aller dans ton compte Microsoft en ligne et générer un "Mot de passe d'application").

---

## 3. Détail du "Text parameter" pour l'IA ({{ $json.chat_input }})

Quand tu crées un nœud Agent LangChain dans n8n, ce nœud est conçu pour les chatbots par défaut, il attend donc un message de chat dans `{{ $json.chat_input }}`.
Sauf que dans le **Binôme 2**, nous n'avons pas de chat, nous avons des **flux RSS** !

Il faut donc dire à l'IA de lire le RSS et non un chat inexistant.
Dans le champ **"Text"** du nœud Agent IA (Filtrer et Résumer), il faut mettre ceci :

```text
Titre de l'article : {{ $json.title }}
Contenu de l'article : {{ $json.contentSnippet }}
```

L'IA va automatiquement remplacer ces variables par le vrai titre et contenu de l'article qu'elle est en train d'examiner.

---

## 4. Pourquoi deux flux RSS ? 

Le projet récupère un flux "Tech" (`techcrunch.com`) et un flux "IA" (`simplecast.com`).
Ceci sert à démontrer au correcteur que le workflow est complexe : il est capable de **récupérer la donnée de plusieurs sources distinctes**, d'utiliser un nœud **Merge** (fusion) pour tout centraliser, avant de l'injecter dynamiquement à une Intelligence Artificielle.
C'est une preuve de maîtrise de l'outil n8n.

---

## 5. Anti-Sèche : Que taper exactement dans chaque nœud ?

Si tu dois recréer ou modifier les nœuds manuellement devant un jury, voici les valeurs exactes :

### Nœud : Déclencheur Programmé (Schedule)
- **Field** : `days` (ou l'intervalle de ton choix)

### Nœud : RSS Feed
- **URL** : `https://techcrunch.com/feed/` ou n'importe quel autre site.
- **Max Items** : `1` (très important pour les tests !)

### Nouveau Nœud : Tools Agent (Celui de la capture d'écran)
Ce nœud remplace l'ancien Agent.
- **Prompt (User Message) [La case principale]** :
  Copie-colle ça dedans :
  ```
  Titre de l'article : {{ $json.title }}
  Contenu de l'article : {{ $json.contentSnippet }}
  ```
- **Où mettre les règles (System Message) ?**
  Clique sur **Add Option** juste en dessous, puis choisis **System Message**. Mets-y le texte des règles :
  *"Tu es un IA curatrice. Tu ne gardes que IA et Tech. Fais un résumé court en HTML..."*

### Nœud : Google Gemini
- Sélectionne ton **Credential** Google API Key que tu as créé.

### Nœud : Send Email
- **To Email** : Ton adresse email Microsoft/Gmail personnelle
- **Subject** : `Ta newsletter IA/Tech`
- **Message** (ou HTML) : `={{ $json.output }}`
