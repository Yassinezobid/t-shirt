import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="SimuVetements - Business Plan",
    page_icon="👕",
    layout="wide"
)

# CSS personnalisé

def local_css():
    st.markdown("""
    <style>
    .main-header { font-size: 2.5rem; color: #333; text-align: center; margin-bottom: 1rem; font-weight: bold; }
    .sub-header { font-size: 1.8rem; color: #555; margin-top: 2rem; margin-bottom: 1rem; font-weight: bold; }
    .stDataFrame { border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Titre
st.markdown('<h1 class="main-header">👕 SimuProfit - Vente de T-shirts & Shorts</h1>', unsafe_allow_html=True)
st.markdown("### Simulez la rentabilité de votre boutique de vêtements en ligne")

# Initialisation session
if 'prix_vente' not in st.session_state:
    st.session_state.produits = {"T-shirt": "👕", "Short": "🩳"}
    # Prix de vente unitaire
    st.session_state.prix_vente = {"T-shirt": 220.0, "Short": 180.0}
    # Coût de production unitaire
    st.session_state.cout_unitaire = {"T-shirt": 80.0, "Short": 60.0}
    # Coût logistique par commande (packaging + livraison)
    st.session_state.cout_logistique = {"T-shirt": 20.0, "Short": 15.0}
    # Commandes par jour
    st.session_state.commandes_jour = {"T-shirt": 12, "Short": 8}
    # Paramètres généraux
    st.session_state.jours_activite = 30
    st.session_state.taux_impot = 20.0
    st.session_state.nb_associes = 2
    # Charges mensuelles
    st.session_state.charges_mensuelles = {
        "Hébergement site": 500.0,
        "Marketing": 1500.0,
        "Divers": 500.0
    }
    # Investissements initiaux
    st.session_state.charges_investissement = {
        "Création site e-commerce": 5000.0,
        "Stock initial T-shirts": 10000.0,
        "Stock initial Shorts": 8000.0
    }

# Calcul indicateurs
def calculer_indicateurs():
    revenus, couts, marges = {}, {}, {}
    for p in st.session_state.produits:
        q = st.session_state.commandes_jour[p]
        days = st.session_state.jours_activite
        rev = st.session_state.prix_vente[p] * q * days
        cost_unit = st.session_state.cout_unitaire[p] + st.session_state.cout_logistique[p]
        cost = cost_unit * q * days
        revenus[p] = rev
        couts[p] = cost
        marges[p] = rev - cost
    revenu_brut = sum(revenus.values())
    cout_variable = sum(couts.values())
    cout_fixe = sum(st.session_state.charges_mensuelles.values())
    cout_total = cout_variable + cout_fixe
    benefice_brut = revenu_brut - cout_total
    impot = max(benefice_brut, 0) * st.session_state.taux_impot / 100
    profit_net = benefice_brut - impot
    profit_par = profit_net / st.session_state.nb_associes if st.session_state.nb_associes else 0
    marge_nette = (profit_net / revenu_brut * 100) if revenu_brut else 0
    total_inv = sum(st.session_state.charges_investissement.values())
    if revenu_brut:
        seuil = cout_fixe / (1 - cout_variable / revenu_brut)
        marge_cv = (1 - cout_variable / revenu_brut) * 100
    else:
        seuil, marge_cv = 0, 0
    if total_inv and profit_net > 0:
        roi_m = profit_net / total_inv * 100
        roi_a = roi_m * 12
        retour = total_inv / profit_net
    else:
        roi_m, roi_a, retour = 0, 0, float('inf')
    return {
        'revenus': revenus,
        'couts': couts,
        'marges': marges,
        'revenu_brut': revenu_brut,
        'cout_variable': cout_variable,
        'cout_fixe': cout_fixe,
        'cout_total': cout_total,
        'benefice_brut': benefice_brut,
        'impot': impot,
        'profit_net': profit_net,
        'profit_par': profit_par,
        'seuil_rentabilite': seuil,
        'marge_cout_variable': marge_cv,
        'roi_mensuel': roi_m,
        'roi_annuel': roi_a,
        'temps_retour': retour,
        'marge_nette': marge_nette
    }

# Recalcul initial
ind = calculer_indicateurs()

# 1. Résumé financier
st.subheader("💰 Résumé financier")
df_metrics = pd.DataFrame({
    'Métrique': ['Profit Net Total','Par Associé','ROI Annuel (%)','Marge Nette (%)'],
    'Valeur': [
        f"{ind['profit_net']:.2f} Dh",
        f"{ind['profit_par']:.2f} Dh",
        f"{ind['roi_annuel']:.2f} %",
        f"{ind['marge_nette']:.2f} %"
    ]
}).set_index('Métrique')
st.dataframe(df_metrics, use_container_width=True)

# 2. Paramètres d'activité
st.subheader("📆 Paramètres d'activité")
col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.jours_activite = st.number_input("Jours d'activité/mois",1,31,st.session_state.jours_activite)
with col2:
    st.session_state.taux_impot = st.number_input("Taux d'impôt (%)",0.0,50.0,st.session_state.taux_impot)
with col3:
    st.session_state.nb_associes = st.number_input("Nombre d'associés",1,10,st.session_state.nb_associes)
ind = calculer_indicateurs()

# 3. Tableau de bord financier
st.subheader("📊 Tableau de bord financier")
st.bar_chart(pd.Series({
    'Revenu brut': ind['revenu_brut'],
    'Coût total': ind['cout_total'],
    'Bénéfice brut': ind['benefice_brut'],
    'Impôt': ind['impot'],
    'Profit net': ind['profit_net']
}))

# 4. Détails par produit (modifiable)
st.subheader("🍽️ Détails par produit")
for p, emoji in st.session_state.produits.items():
    st.markdown(f"#### {emoji} {p}")
    cols = st.columns(4)
    prix = cols[0].number_input("Prix unitaire (Dh)",0.0,10000.0,st.session_state.prix_vente[p],0.5,key=f"prix_{p}")
    prod_cost = cols[1].number_input("Coût production (Dh)",0.0,10000.0,st.session_state.cout_unitaire[p],0.5,key=f"prod_{p}")
    log_cost = cols[2].number_input("Coût packaging+livraison (Dh)",0.0,10000.0,st.session_state.cout_logistique[p],0.5,key=f"log_{p}")
    q = cols[3].number_input("Commandes/jour",0,1000,st.session_state.commandes_jour[p],1,key=f"cmd_{p}")
    st.session_state.prix_vente[p] = prix
    st.session_state.cout_unitaire[p] = prod_cost
    st.session_state.cout_logistique[p] = log_cost
    st.session_state.commandes_jour[p] = q
    st.markdown(f"- Revenu mensuel: **{ind['revenus'][p]:.2f} Dh**, Coût mensuel: **{ind['couts'][p]:.2f} Dh**, Marge: **{ind['marges'][p]:.2f} Dh**")

# 5. Charges mensuelles
st.subheader("💸 Charges mensuelles")
st.dataframe(pd.DataFrame.from_dict(st.session_state.charges_mensuelles,orient='index',columns=['Montant (Dh)']), use_container_width=True)

# 6. Investissements initiaux
st.subheader("🏗️ Investissements initiaux")
st.dataframe(pd.DataFrame.from_dict(st.session_state.charges_investissement,orient='index',columns=['Montant (Dh)']), use_container_width=True)

# 7. Analyse de rentabilité
st.subheader("🔍 Analyse de rentabilité")
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Seuil de rentabilité (Dh)",f"{ind['seuil_rentabilite']:.2f}")
    st.metric("Marge CV (%)",f"{ind['marge_cout_variable']:.2f}")
with col_b:
    st.metric("ROI mensuel (%)",f"{ind['roi_mensuel']:.2f}")
    st.metric("Temps retour (mois)",f"{ind['temps_retour']:.1f}")

# 8. Recommandations
st.subheader("💡 Recommandations")
if ind['profit_net'] > 0:
    st.success("✅ Projet rentable !")
else:
    st.error("⚠️ Projet non rentable.")

# Footer
st.markdown("---")
with st.expander("Conseils avancés"):
    st.markdown("""
- Marketing ciblé : utilisez les réseaux sociaux.
- Programme fidélité : offrez des réductions.
- Optimisation logistique : regroupez les envois.
""")
