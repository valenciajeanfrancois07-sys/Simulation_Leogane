import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

# Sélecteur de langue
lang = st.sidebar.selectbox("🌍 Language / Langue / Lang", ["English", "Français", "Kreyòl Ayisyen"])

# Tradiksyon pou tout seksyon yo
texts = {
    "English": {
        "title": "Simulation of Léogâne Population - Markov Chain",
        "intro": "This interactive tool models and analyzes the evolution of Léogâne's population across socio-economic states using a Markov chain.",
        "params": "Initial population configuration",
        "matrix": "Transition Matrix",
        "analysis": "Dynamic analysis of the population",
        "results": "Detailed numerical results",
        "final": "Final distribution by state",
        "export": "Export results as CSV"
    },
    "Français": {
        "title": "Simulation de la Population Léogânaise - Chaîne de Markov",
        "intro": "Cet outil interactif permet de modéliser et d’analyser l’évolution de la population de Léogâne à travers différents états socio-économiques, en utilisant une chaîne de Markov.",
        "params": "Configuration initiale de la population",
        "matrix": "Matrice de transition",
        "analysis": "Analyse dynamique de la population",
        "results": "Résultats numériques détaillés",
        "final": "Distribution finale par état",
        "export": "Exporter les résultats en CSV"
    },
    "Kreyòl Ayisyen": {
        "title": "Similasyon Popilasyon Léogâne - Chèn Markov",
        "intro": "Zouti entèaktif sa a sèvi pou modèlize ak analize evolisyon popilasyon Léogâne nan diferan eta sosyo-ekonomik, lè w ap itilize yon chèn Markov.",
        "params": "Konfigirasyon inisyal popilasyon an",
        "matrix": "Matrice Tranzisyon",
        "analysis": "Analiz dinamik popilasyon an",
        "results": "Rezilta nimerik detaye",
        "final": "Distribisyon final pa eta",
        "export": "Ekspòte rezilta yo an CSV"
    }
}

# Tradiksyon pou etats
etats_translations = {
    "English": ["Agriculture","Trade","Education","Services","Migration","Informal","Unemployment","Fishing","Diaspora"],
    "Français": ["Agriculture","Commerce","Éducation","Services","Migration","Informel","Chômage","Pêche","Diaspora"],
    "Kreyòl Ayisyen": ["Agrikilti","Komès","Edikasyon","Sèvis","Migrasyon","Enfòmèl","Chomaj","Pèch","Dyaspora"]
}

# Tradiksyon pou caption imaj
captions = {
    "English": "Statue of Queen Anacaona in Léogâne",
    "Français": "Statue de la Reine Anacaona à Léogâne",
    "Kreyòl Ayisyen": "Estati Rèn Anacaona nan Léogâne"
}

col1, col2 = st.columns([1, 10])
with col1:
    st.image("./Iconeb Simulation/Simulation-re.png", width=50)
with col2:
    st.title(texts[lang]["title"])

st.write(texts[lang]["intro"])

st.image("./Iconeb Simulation/Anacaona.jpg", caption=captions[lang], width=400)

# États socio-économiques de Léogâne
etats = etats_translations[lang]

# --- Section Paramètres ---
col1, col2 = st.sidebar.columns([1, 5])
with col1:
    st.image("./Iconeb Simulation/Parametre-re.png", width=30)
with col2:
    st.header(texts[lang]["params"])

# Population totale de Léogâne
total_pop = st.sidebar.number_input("Population totale", min_value=100, value=26984, key="total_pop")

# Valeurs initiales fictives
default_values = [8000, 5000, 4500, 3000, 1500, 2000, 1500, 1000, 484]
init_values = []
for i, (etat, default) in enumerate(zip(etats, default_values)):
    val = st.sidebar.number_input(f"{etat} initial", min_value=0, value=default, key=f"init_{i}")
    init_values.append(val)

# Normalisation
somme_init = sum(init_values)
etat_initial = np.array(init_values) * (total_pop / somme_init) if somme_init > 0 else np.array(init_values)

if somme_init > total_pop:
    st.warning("⚠️ La somme des valeurs initiales dépasse la population totale. Les données seront normalisées automatiquement.")
if somme_init != total_pop:
    st.warning(f"⚠️ La somme des valeurs initiales ({somme_init}) ne correspond pas à la population totale ({total_pop}). Les données seront normalisées automatiquement.")

# Matrice
use_default_matrix = st.sidebar.checkbox("Utiliser la matrice par défaut", value=True)
if use_default_matrix:
    M = np.array([
        [0.6,0.1,0.05,0.05,0.05,0.05,0.05,0.05,0.0],
        [0.1,0.6,0.05,0.1,0.05,0.05,0.05,0.0,0.0],
        [0.05,0.1,0.6,0.15,0.05,0.05,0.0,0.0,0.0],
        [0.05,0.1,0.1,0.6,0.05,0.05,0.05,0.0,0.0],
        [0.0,0.05,0.05,0.05,0.6,0.05,0.1,0.0,0.1],
        [0.05,0.1,0.05,0.05,0.05,0.6,0.1,0.0,0.0],
        [0.05,0.05,0.05,0.05,0.05,0.1,0.6,0.0,0.05],
        [0.05,0.05,0.0,0.05,0.05,0.05,0.05,0.6,0.1],
        [0.0,0.05,0.05,0.05,0.1,0.05,0.05,0.0,0.65]
    ])
else:
    st.subheader(texts[lang]["matrix"])
    M = []
    for i, etat in enumerate(etats):
        row = []
        st.write(f"Transitions depuis {etat}:")
        for j, cible in enumerate(etats):
            prob = st.slider(f"{etat} → {cible}", 0.0, 1.0, 0.1, key=f"slider_{i}_{j}")
            row.append(prob)
        row = np.array(row) / sum(row)
        M.append(row)
    M = np.array(M)

# Simulation
col1, col2 = st.columns([1, 10])
with col1:
    st.image("./Iconeb Simulation/Augmentation-re.png", width=40)
with col2:
    st.subheader(texts[lang]["analysis"])

n = st.sidebar.slider("Nombre de périodes", 1, 20, 5)
resultats = [etat_initial]
for i in range(n):
    resultats.append(resultats[-1] @ M)

df = pd.DataFrame(resultats, columns=etats)
df.index.name = "Période"

# Graphique
df_long = df.reset_index().melt(id_vars="Période", var_name="État", value_name="Population")
chart_evolution = alt.Chart(df_long).mark_line(point=True).encode(x="Période", y="Population", color="État").properties(width=600)
st.altair_chart(chart_evolution)

# Résultats
col1, col2 = st.columns([1, 10])
with col1:
    st.image("./Iconeb Simulation/List-re.png", width=40)
with col2:
    st.subheader(texts[lang]["results"])
st.dataframe(df)

# Distribution finale
col1, col2 = st.columns([1, 10])
with col1:
    st.image("./Iconeb Simulation/Simulation-re.png", width=40)
with col2:
    st.subheader(texts[lang]["final"])

df_final = df.iloc[-1].reset_index()
df_final.columns = ["État", "Population"]
chart_final = alt.Chart(df_final).mark_bar().encode(x=alt.X("État", sort=None), y="Population", color="État").properties(width=600)
st.altair_chart(chart_final)

# Export CSV
# Exportation CSV
csv = df.to_csv().encode("utf-8")

st.download_button(
    label=texts[lang]["export"],
    data=csv,
    file_name="simulation_population_leogane.csv",
    mime="text/csv",
)
