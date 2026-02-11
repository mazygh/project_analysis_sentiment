"""
Application Streamlit pour l'Analyse de Sentiment avec DistilBERT
Auteur: Analyse de Sentiment NLP
Date: 2026
"""

import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import time

# Configuration de la page
st.set_page_config(
    page_title="Analyseur de Sentiment IA",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 3em;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        border: 2px solid #4CAF50;
    }
    .sentiment-positive {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .sentiment-negative {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        font-size: 3em;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)


# Fonction de mise en cache pour charger le modèle
@st.cache_resource
def load_model(model_name):
    """Charge le modèle et le tokenizer avec mise en cache"""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        return tokenizer, model
    except Exception as e:
        st.error(f"Erreur lors du chargement du modèle: {e}")
        return None, None


def get_prediction(text, tokenizer, model):
    """
    Prédit le sentiment d'un texte donné
    
    Args:
        text (str): Texte à analyser
        tokenizer: Tokenizer du modèle
        model: Modèle de classification
    
    Returns:
        dict: Dictionnaire contenant le sentiment et la probabilité
    """
    try:
        # Encodage du texte
        input_ids = tokenizer.encode(text, return_tensors='pt', truncation=True, max_length=512)
        
        # Prédiction
        with torch.no_grad():
            output = model(input_ids)
        
        # Calcul des probabilités
        probs = torch.nn.functional.softmax(output.logits, dim=-1)
        
        # Extraction des résultats
        confidence = torch.max(probs).item()
        prediction_idx = torch.argmax(probs).item()
        
        # Mapping des labels
        id2label = {1: 'positive', 0: 'negative'}
        sentiment = id2label[prediction_idx]
        
        # Probabilités individuelles
        prob_negative = probs[0][0].item()
        prob_positive = probs[0][1].item()
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'prob_negative': prob_negative,
            'prob_positive': prob_positive
        }
    except Exception as e:
        st.error(f"Erreur lors de la prédiction: {e}")
        return None


def create_gauge_chart(confidence, sentiment):
    """Crée un graphique en jauge pour la confiance"""
    color = "#4CAF50" if sentiment == "positive" else "#f5576c"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Niveau de Confiance", 'font': {'size': 24}},
        number={'suffix': "%", 'font': {'size': 40}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#ffebee'},
                {'range': [50, 75], 'color': '#fff3e0'},
                {'range': [75, 100], 'color': '#e8f5e9'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "#333", 'family': "Arial"}
    )
    
    return fig


def create_probability_chart(prob_negative, prob_positive):
    """Crée un graphique en barres pour les probabilités"""
    df = pd.DataFrame({
        'Sentiment': ['Négatif', 'Positif'],
        'Probabilité': [prob_negative * 100, prob_positive * 100]
    })
    
    colors = ['#f5576c', '#4CAF50']
    
    fig = px.bar(
        df, 
        x='Sentiment', 
        y='Probabilité',
        color='Sentiment',
        color_discrete_map={'Négatif': colors[0], 'Positif': colors[1]},
        text='Probabilité'
    )
    
    fig.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside',
        textfont_size=14
    )
    
    fig.update_layout(
        showlegend=False,
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="",
        yaxis_title="Probabilité (%)",
        yaxis=dict(range=[0, 110]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'size': 14}
    )
    
    return fig


def display_sentiment_result(result):
    """Affiche les résultats de l'analyse de sentiment"""
    if result['sentiment'] == 'positive':
        st.markdown(f"""
            <div class="sentiment-positive">
                <h2>😊 Sentiment POSITIF</h2>
                <h3>Confiance: {result['confidence']*100:.2f}%</h3>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="sentiment-negative">
                <h2>😞 Sentiment NÉGATIF</h2>
                <h3>Confiance: {result['confidence']*100:.2f}%</h3>
            </div>
        """, unsafe_allow_html=True)


def main():
    """Fonction principale de l'application"""
    
    # En-tête
    st.markdown("<h1>🎭 Analyseur de Sentiment IA</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Propulsé par DistilBERT - Analyse de sentiment en temps réel</p>",
        unsafe_allow_html=True
    )
    
    # Barre latérale
    with st.sidebar:
        st.image("https://huggingface.co/front/assets/huggingface_logo.svg", width=200)
        st.title("⚙️ Configuration")
        
        # Choix du modèle
        model_choice = st.selectbox(
            "Sélectionner le modèle",
            ["distilbert-base-uncased-finetuned-sst-2-english", "Modèle personnalisé (local)"],
            help="Choisissez le modèle pré-entraîné ou votre modèle local"
        )
        
        if model_choice == "Modèle personnalisé (local)":
            model_name = st.text_input("Chemin du modèle", "sentiment-distilbert")
        else:
            model_name = model_choice
        
        st.markdown("---")
        
        # Informations sur le modèle
        st.subheader("📊 À propos du modèle")
        st.info("""
        **DistilBERT** est une version compressée de BERT, 
        60% plus rapide tout en conservant 97% de ses capacités.
        
        - **Tâche**: Classification de texte
        - **Classes**: Positif / Négatif
        - **Précision**: ~90.6%
        """)
        
        st.markdown("---")
        
        # Exemples de textes
        st.subheader("💡 Exemples")
        examples = {
            "Positif 😊": "I love this product! It's absolutely amazing and exceeded all my expectations.",
            "Négatif 😞": "This is the worst experience I've ever had. Completely disappointed.",
            "Neutre 😐": "The product arrived on time. It works as described in the manual."
        }
        
        selected_example = st.radio("Essayer un exemple:", list(examples.keys()))
        
        st.markdown("---")
        
        # Statistiques (si historique disponible)
        if 'history' in st.session_state and len(st.session_state.history) > 0:
            st.subheader("📈 Statistiques")
            pos_count = sum(1 for h in st.session_state.history if h['sentiment'] == 'positive')
            neg_count = len(st.session_state.history) - pos_count
            
            col1, col2 = st.columns(2)
            col1.metric("Positifs", pos_count, delta=None)
            col2.metric("Négatifs", neg_count, delta=None)
    
    # Initialisation de l'historique
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # Zone principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Entrez votre texte")
        
        # Tabs pour différents modes d'entrée
        tab1, tab2 = st.tabs(["✍️ Saisie manuelle", "📋 Exemples"])
        
        with tab1:
            user_text = st.text_area(
                "Texte à analyser:",
                height=150,
                placeholder="Tapez ou collez votre texte ici...",
                help="Entrez le texte dont vous souhaitez analyser le sentiment"
            )
        
        with tab2:
            user_text = st.text_area(
                "Texte d'exemple:",
                value=examples[selected_example],
                height=150
            )
        
        # Bouton d'analyse
        analyze_button = st.button("🔍 Analyser le Sentiment", type="primary")
        
        if analyze_button and user_text:
            with st.spinner("🤖 Analyse en cours..."):
                # Simulation d'un temps de traitement pour l'effet visuel
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                # Chargement du modèle
                tokenizer, model = load_model(model_name)
                
                if tokenizer and model:
                    # Prédiction
                    result = get_prediction(user_text, tokenizer, model)
                    
                    if result:
                        # Ajout à l'historique
                        st.session_state.history.append({
                            'text': user_text[:50] + '...' if len(user_text) > 50 else user_text,
                            'sentiment': result['sentiment'],
                            'confidence': result['confidence'],
                            'timestamp': datetime.now().strftime("%H:%M:%S")
                        })
                        
                        # Affichage des résultats
                        st.markdown("---")
                        st.subheader("📊 Résultats de l'Analyse")
                        
                        # Résultat principal
                        display_sentiment_result(result)
                        
                        # Graphiques
                        col_chart1, col_chart2 = st.columns(2)
                        
                        with col_chart1:
                            st.plotly_chart(
                                create_gauge_chart(result['confidence'], result['sentiment']),
                                use_container_width=True
                            )
                        
                        with col_chart2:
                            st.plotly_chart(
                                create_probability_chart(result['prob_negative'], result['prob_positive']),
                                use_container_width=True
                            )
                        
                        # Détails supplémentaires
                        with st.expander("📋 Détails de l'analyse"):
                            st.json({
                                "Sentiment": result['sentiment'].upper(),
                                "Confiance": f"{result['confidence']*100:.2f}%",
                                "Probabilité Négatif": f"{result['prob_negative']*100:.2f}%",
                                "Probabilité Positif": f"{result['prob_positive']*100:.2f}%",
                                "Longueur du texte": len(user_text),
                                "Nombre de mots": len(user_text.split())
                            })
                        
                        # Recommandations
                        st.markdown("---")
                        st.subheader("💡 Interprétation")
                        
                        if result['confidence'] > 0.9:
                            st.success("✅ Le modèle est très confiant dans sa prédiction (>90%)")
                        elif result['confidence'] > 0.7:
                            st.info("ℹ️ Le modèle est moyennement confiant dans sa prédiction (70-90%)")
                        else:
                            st.warning("⚠️ Le modèle est peu confiant dans sa prédiction (<70%). Le texte pourrait être ambigu.")
        
        elif analyze_button and not user_text:
            st.warning("⚠️ Veuillez entrer un texte à analyser.")
    
    with col2:
        st.subheader("📜 Historique")
        
        if len(st.session_state.history) > 0:
            # Afficher les 5 dernières analyses
            for i, entry in enumerate(reversed(st.session_state.history[-5:])):
                sentiment_emoji = "😊" if entry['sentiment'] == 'positive' else "😞"
                sentiment_color = "#4CAF50" if entry['sentiment'] == 'positive' else "#f5576c"
                
                st.markdown(f"""
                    <div style="background-color: {sentiment_color}20; padding: 10px; 
                         border-radius: 8px; margin: 5px 0; border-left: 4px solid {sentiment_color};">
                        <strong>{sentiment_emoji} {entry['sentiment'].upper()}</strong><br/>
                        <small>{entry['text']}</small><br/>
                        <small>🕒 {entry['timestamp']} | 📊 {entry['confidence']*100:.1f}%</small>
                    </div>
                """, unsafe_allow_html=True)
            
            # Bouton pour effacer l'historique
            if st.button("🗑️ Effacer l'historique"):
                st.session_state.history = []
                st.rerun()
        else:
            st.info("Aucune analyse effectuée pour le moment.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Développé avec ❤️ en utilisant Streamlit et Hugging Face Transformers</p>
            <p>Modèle: DistilBERT | Framework: PyTorch | Interface: Streamlit</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
