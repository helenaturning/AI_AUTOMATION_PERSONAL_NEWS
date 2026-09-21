from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def add_slide(prs, title, content, image_placeholder=False, video_placeholder=False):
    slide_layout = prs.slide_layouts[1] # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    title_place = slide.shapes.title
    title_place.text = title
    
    body_place = slide.placeholders[1]
    tf = body_place.text_frame
    tf.text = content
    
    if image_placeholder:
        p = tf.add_paragraph()
        p.text = "\n[INDIQUEZ ICI : INSÉRER UNE CAPTURE D'ÉCRAN / IMAGE]"
        p.font.bold = True
        p.font.size = Pt(18)
    
    if video_placeholder:
        p = tf.add_paragraph()
        p.text = "\n[INDIQUEZ ICI : INSÉRER UNE DÉMONSTRATION VIDÉO]"
        p.font.bold = True
        p.font.size = Pt(18)

def main():
    prs = Presentation()
    
    # 1. Slide de Titre
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Projet Persona — G-AIA-410"
    subtitle.text = "Automatisation de Curation de Contenu & IA via n8n\nPrésentation de Revue de Projet\n\n[Insérer Logo Epitech ici]"
    
    # 2. La Problématique
    add_slide(prs, "La Problématique", 
              "• Besoin d'automatiser la veille technologique personnalisée.\n"
              "• Difficulté de gérer manuellement les profils utilisateurs et les préférences.\n"
              "• Nécessité d'un système fluide combinant authentification et curation intelligente.\n"
              "• Solution Persona : Une architecture n8n modulaire et scalable.")
    
    # 3. Architecture Technique (Introduction n8n)
    add_slide(prs, "Architecture Technique : n8n", 
              "• Platforme d'automatisation No-Code / Low-Code.\n"
              "• Déploiement via Docker pour une isolation totale et une portabilité maximale.\n"
              "• Utilisation de Workflows JSON pour une flexibilité totale.\n"
              "• Orchestration native des modèles LLM (Gemini, Groq/Llama).",
              image_placeholder=True) # Placeholder pour screenshot n8n
    
    # 4. Binôme 1 : Chatbot & Authentification
    add_slide(prs, "Binôme 1 : Chatbot & Authentification", 
              "• Flux : Chat Trigger → AI Agent (Gemini) → Simple Memory.\n"
              "• Fonctionnement :\n"
              "  - Inscription / Connexion sécurisée (logic-based via IA).\n"
              "  - Collecte dynamique du profil (E-mail, Intérêts, Heure).\n"
              "  - Mémoire conversationnelle (buffer de 20 messages).",
              image_placeholder=True) # Screenshot workflow persona.json
    
    # 5. Binôme 2 : Curation & Newsletter
    add_slide(prs, "Binôme 2 : Curation & Newsletter Quotidienne", 
              "• Flux : Schedule Trigger → RSS Feeds → Merge → IA Filter → Email.\n"
              "• Sources : TechCrunch (Tech) & Simplecast (IA).\n"
              "• Filtrage intelligent : L'IA ne retient que le contenu pertinent pour l'utilisateur.\n"
              "• Envoi : Newsletter formatée en HTML via SMTP (Outlook/Ethereal).",
              image_placeholder=True) # Screenshot workflow binome2.json
    
    # 6. Fonctionnalités Avancées & Bonus Implémentés
    add_slide(prs, "Fonctionnalités Avancées & Bonus Implémentés", 
              "• Personnalisation du Ton : La newsletter s'adapte au profil selon l'historique de discussion (via mémoire partagée).\n"
              "• Choix de la Langue : L'utilisateur définit sa langue d'édition dans le chatbot.\n"
              "• Analyse de Sentiment : Un indice de moral basé sur les actus est inclus à la fin de la newsletter.\n"
              "• Résilience et Fiabilité : Outils natifs (Split in Batches/Limit) et architecture Multi-Modèles puissante.")
    
    # 7. Défis Techniques & Solutions
    add_slide(prs, "Défis Techniques & Solutions", 
              "• Problème : Dépassement des quotas d'API Gemini sur les gros flux RSS.\n"
              "• Solution : Migration vers Groq pour la curation et ajout de nœuds Limit.\n"
              "• Problème : Persistance des données en Docker.\n"
              "• Solution : Utilisation de volumes Docker pour sauvegarder les configurations n8n.")
    
    # 8. Démonstration du Projet
    add_slide(prs, "Démonstration du Projet", 
              "• Vue d'ensemble du fonctionnement en direct.\n"
              "• Exemple d'interaction Chatbot.\n"
              "• Aperçu de la Newsletter finale reçue par e-mail.",
              video_placeholder=True) # Vidéo demo
    
    # 9. Conclusion
    add_slide(prs, "Conclusion & Perspectives", 
              "• Système complet, robuste et prêt pour la production.\n"
              "• Évolutivité : Facilité d'ajout de nouvelles sources (YouTube, Twitter, Google News).\n"
              "• Perspectives : Intégration d'une base de données SQL pour une gestion profil plus fine.",
              image_placeholder=False)
    
    prs.save('Persona_Presentation.pptx')
    print("Présentation générée avec succès : Persona_Presentation.pptx")

if __name__ == "__main__":
    main()
