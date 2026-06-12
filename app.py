app.py
%%writefile app.py
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from fpdf import FPDF
import io

# Configuration de la page
st.set_page_config(
    page_title="CV Optimizer AI - Décrochez plus d'entretiens",
    page_icon="📄",
    layout="centered"
)

# --- STYLE CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main-title { font-size: 2.6rem; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 0.5rem; }
    .subtitle { font-size: 1.2rem; text-align: center; color: #4B5563; margin-bottom: 2rem; }
    .section-gains { background-color: #FEF3C7; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #D97706; margin-top: 2rem; color: #1F2937; }
    .payment-box { background-color: #F3F4F6; padding: 1.5rem; border-radius: 10px; border: 1px solid #E5E7EB; margin-top: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- FONCTION DE GÉNÉRATION PDF ---
def creer_pdf(texte_cv, mots_ajoutes):
    pdf = FPDF()
    pdf.add_page()
    
    # En-tête du CV
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(30, 58, 138) # Bleu foncé
    pdf.cell(0, 15, "MON CV OPTIMISÉ", ln=True, align="C")
    
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(107, 114, 128)
    pdf.cell(0, 10, "Généré et optimisé par l'IA de CV Optimizer AI", ln=True, align="C")
    pdf.ln(10)
    
    # Section Compétences clés ajoutées par l'IA
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(217, 119, 6) # Couleur Ambre
    pdf.cell(0, 10, "COMPÉTENCES OPTIMISÉES POUR L'OFFRE (Mots-clés ATS) :", ln=True)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(31, 41, 55)
    liste_mots = ", ".join([m.capitalize() for m in mots_ajoutes])
    pdf.multi_cell(0, 8, liste_mots)
    pdf.ln(5)
    
    # Contenu principal du CV
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 10, "PARCOURS ET EXPÉRIENCES :", ln=True)
    
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(31, 41, 55)
    pdf.multi_cell(0, 8, texte_cv)
    
    # Sauvegarde dans un flux de mémoire pour Streamlit
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# --- LOGIQUE D'ANALYSE NLP ---
def analyser_cv(cv, job):
    texts = [cv.lower(), job.lower()]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score = int(similarity * 100)
    
    words_job = set(re.findall(r'\b\w{5,}\b', job.lower()))
    words_cv = set(re.findall(r'\b\w{5,}\b', cv.lower()))
    missing_keywords = list(words_job - words_cv)[:5]
    
    return score, missing_keywords

# --- EN-TÊTE DU SITE ---
st.markdown("<div class='main-title'>📄 CV Optimizer AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Optimisez votre CV pour passer les filtres des recruteurs (ATS) et doublez vos chances d'entretien.</div>", unsafe_allow_html=True)
st.divider()

# --- INPUTS ---
st.subheader("1. Vos informations")
col1, col2 = st.columns(2)
with col1:
    cv_text = st.text_area("Collez le texte de votre CV actuel :", placeholder="Ex: Expériences, compétences...", height=200)
with col2:
    job_text = st.text_area("Collez la description de l'offre d'emploi :", placeholder="Ex: Compétences requises...", height=200)

# Initialisation des variables dans la session Streamlit pour s'en souvenir après les clics
if "analyse_faite" not in st.session_state:
    st.session_state.analyse_faite = False
if "paiement_valide" not in st.session_state:
    st.session_state.paiement_valide = False

# --- BOUTON ANALYSE ---
st.write("")
if st.button("🚀 Analyser mon score de compatibilité", use_container_width=True):
    if cv_text.strip() == "" or job_text.strip() == "":
        st.warning("⚠️ Veuillez remplir à la fois le CV et l'offre d'emploi.")
    else:
        score, manquants = analyser_cv(cv_text, job_text)
        st.session_state.score = score
        st.session_state.manquants = manquants
        st.session_state.analyse_faite = True
        st.session_state.paiement_valide = False # Réinitialise le paiement pour un nouveau test

# --- AFFICHAGE RÉSULTATS ET PAIEMENT ---
if st.session_state.analyse_faite:
    st.divider()
    st.subheader("📊 Vos Résultats")
    
    score = st.session_state.score
    manquants = st.session_state.manquants
    
    if score < 40:
        st.error(f"Score de compatibilité : {score}% (Insuffisant pour passer les filtres)")
    elif score < 70:
        st.warning(f"Score de compatibilité : {score}% (Peut être amélioré)")
    else:
        st.success(f"Score de compatibilité : {score}% (Excellent profil !)")
        
    st.progress(score / 100)
    
    st.markdown("### 🔍 Mots-clés importants manquants dans votre CV :")
    if manquants:
        cols = st.columns(len(manquants))
        for i, word in enumerate(manquants):
            cols[i].info(f"**{word}**")
    else:
        st.write("Aucun mot-clé majeur manquant.")

    # Zone de Monétisation
    if not st.session_state.paiement_valide:
        st.markdown("""
            <div class='section-gains'>
                <h3>💰 Débloquez votre CV Parfait et Optimisé</h3>
                <p>Notre algorithme va réinjecter de façon transparente les mots-clés manquants pour propulser votre score à plus de 90% et générer un format PDF professionnel conforme.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulaire de paiement sécurisé simulé
        st.markdown("<div class='payment-box'>🔒 <b>Passerelle de paiement sécurisée (Stripe)</b>", unsafe_allow_html=True)
        card_number = st.text_input("Numéro de carte bancaire", placeholder="4242 4242 4242 4242", max_chars=19)
        c1, c2 = st.columns(2)
        with c1:
            card_expiry = st.text_input("Date d'expiration", placeholder="MM/AA", max_chars=5)
        with c2:
            card_cvc = st.text_input("CVC", placeholder="123", type="password", max_chars=3)
            
        if st.button("💳 Payer 5.99€ et générer mon PDF", type="primary", use_container_width=True):
            if len(card_number) < 16 or len(card_expiry) < 5 or len(card_cvc) < 3:
                st.error("❌ Veuillez remplir correctement les informations de la carte de test.")
            else:
                with st.spinner("Traitement du paiement en cours via Stripe..."):
                    import time
                    time.sleep(2) # Simule l'attente de la banque
                st.session_state.paiement_valide = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # Une fois payé, on affiche le bouton de téléchargement du PDF
    if st.session_state.paiement_valide:
        st.success("✅ Paiement réussi ! Votre CV optimisé a été généré avec succès.")
        
        # Appel de la fonction de création du PDF
        pdf_file = creer_pdf(cv_text, manquants)
        
        st.download_button(
            label="📥 Télécharger mon CV Optimisé (PDF)",
            data=pdf_file,
            file_name="cv_optimise.pdf",
            mime="application/pdf",
            use_container_width=True
        )
