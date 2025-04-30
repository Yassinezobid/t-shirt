import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    .main-header {
        font-size: 2.5rem;
        color: #333333;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #555555;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .metric-value { font-size: 1.8rem; font-weight: bold; }
    .positive-value { color: #28a745; }
    .negative-value { color: #dc3545; }
    .stDataFrame { border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .chart-container { background-color: #fff; border-radius: 10px; padding: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Titre
st.markdown('<p class="main-header">👕 SimuProfit - Vente de T-shirts & Shorts</p>', unsafe_allow_html=True)
st.markdown("### Simulez la rentabilité de votre boutique de vêtements en ligne")

# Initialisation session
if 'prix_vente' not in st.session_state:
    produits = {"T-shirt": "👕", "Short": "🩳"}
    st.session_state.produits = produits
    st.session_state.prix_vente = {"T-shirt": 220.0, "Short": 180.0}
    st.session_state.cout_unitaire = {"T-shirt": 80.0, "Short": 60.0}
    st.session_state.commandes_jour = {"T-shirt": 12, "Short": 8}
    st.session_state.jours_activite = 30
    st.session_state.taux_impot = 20.0
    st.session_state.nb_associes = 2
    st.session_state.charges_mensuelles = {
        "Hébergement site": 500.0,
        "Marketing": 1500.0,
        "Packaging & Livraison": 1200.0,
        "Stockage": 800.0,
        "Divers": 500.0
    }
    st.session_state.charges_investissement = {
        "Création site e-commerce": 5000.0,
        "Photoshoot produits": 2500.0,
        "Équipement photo": 1500.0,
        "Stock initial T-shirts": 10000.0,
        "Stock initial Shorts": 8000.0,
        "Design logo & packaging": 2000.0,
        "Ordinateur": 10000.0
    }

charges_emojis = {
    "Hébergement site": "🌐",
    "Marketing": "📣",
    "Packaging & Livraison": "📦",
    "Stockage": "🏬",
    "Divers": "📋"
}

# Calcul indicateurs
def calculer_indicateurs():
    revenus, couts, marges = {}, {}, {}
    for p in st.session_state.produits:
        rev = st.session_state.prix_vente[p] * st.session_state.commandes_jour[p] * st.session_state.jours_activite
        cost = st.session_state.cout_unitaire[p] * st.session_state.commandes_jour[p] * st.session_state.jours_activite
        revenus[p], couts[p], marges[p] = rev, cost, rev - cost
    revenu_brut = sum(revenus.values())
    cout_variable = sum(couts.values())
    cout_fixe = sum(st.session_state.charges_mensuelles.values())
    cout_total = cout_variable + cout_fixe
    benefice_brut = revenu_brut - cout_total
    impot = benefice_brut * st.session_state.taux_impot/100 if benefice_brut>0 else 0
    profit_net = benefice_brut - impot
    profit_par = profit_net / st.session_state.nb_associes if st.session_state.nb_associes>0 else 0
    marge_nette = profit_net/revenu_brut*100 if revenu_brut>0 else 0
    total_inv = sum(st.session_state.charges_investissement.values())
    if revenu_brut>0:
        seuil = cout_fixe/(1 - cout_variable/revenu_brut)
        marge_cv = (1 - cout_variable/revenu_brut)*100
    else:
        seuil, marge_cv = 0, 0
    if total_inv>0 and profit_net>0:
        roi_m = profit_net/total_inv*100
        roi_a = roi_m*12
        retour = total_inv/profit_net
    else:
        roi_m, roi_a, retour = 0,0,float('inf')
    return dict(revenus=revenus, couts=couts, marges=marges,
                revenu_brut=revenu_brut, cout_variable=cout_variable, cout_fixe=cout_fixe,
                cout_total=cout_total, benefice_brut=benefice_brut, impot=impot,
                profit_net=profit_net, profit_par=profit_par,
                total_investissement=total_inv, seuil_rentabilite=seuil,
                marge_cout_variable=marge_cv, roi_mensuel=roi_m, roi_annuel=roi_a,
                temps_retour=retour, marge_nette=marge_nette)

ind = calculer_indicateurs()

# 1. Résumé financier
st.markdown("## 💰 Résumé financier")
cols = st.columns(4)
cols[0].metric("Profit Net Total", f"{ind['profit_net']:.2f} Dh")
cols[1].metric("Par Associé", f"{ind['profit_par']:.2f} Dh")
cols[2].metric("ROI Annuel", f"{ind['roi_annuel']:.2f}%")
cols[3].metric("Marge Nette (%)", f"{ind['marge_nette']:.2f}%")

# 2. Paramètres d'activité
st.markdown('<p class="sub-header">📆 Paramètres d\'activité</p>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.session_state.jours_activite = st.number_input("Jours d'activité/mois",1,31,st.session_state.jours_activite,key='j_act')
with c2:
    st.session_state.taux_impot = st.number_input("Taux d'impôt (%)",0.0,50.0,st.session_state.taux_impot,0.5,key='t_imp')
with c3:
    st.session_state.nb_associes = st.number_input("Nombre d'associés",1,10,st.session_state.nb_associes,1,key='n_assoc')
ind = calculer_indicateurs()

# 3. Tableau de bord (bar chart)
st.markdown('<p class="sub-header">📊 Tableau de bord</p>', unsafe_allow_html=True)
fig, ax = plt.subplots(figsize=(10,5))
labels = ['Revenu brut','Coût total','Bénéfice brut','Impôt','Profit net']
values = [ind['revenu_brut'], ind['cout_total'], ind['benefice_brut'], ind['impot'], ind['profit_net']]
bars = ax.bar(labels, values)
for i,bar in enumerate(bars):
    bar.set_color('#28a745' if values[i]>=0 else '#dc3545')
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50, f"{values[i]:.2f} Dh", ha='center')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
with st.container():
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Détails par produit
st.markdown('<p class="sub-header">📈 Détails par produit</p>', unsafe_allow_html=True)
with st.form('prod_form'):
    for i,p in enumerate(st.session_state.produits):
        emoji = st.session_state.produits[p]
        cols = st.columns(3)
        prix = cols[0].number_input(f"Prix {emoji} {p}",0.0,10000.0,st.session_state.prix_vente[p],0.5,key=f'prix_{i}')
        cout = cols[1].number_input(f"Coût {emoji} {p}",0.0,10000.0,st.session_state.cout_unitaire[p],0.5,key=f'cout_{i}')
        cmd = cols[2].number_input(f"Commandes/jour {emoji} {p}",0,1000,st.session_state.commandes_jour[p],1,key=f'cmd_{i}')
        st.session_state.prix_vente[p]=prix; st.session_state.cout_unitaire[p]=cout; st.session_state.commandes_jour[p]=cmd
        st.markdown('---')
    if st.form_submit_button('Mettre à jour'): ind = calculer_indicateurs()

# DataFrame résumé
data = []
for p in st.session_state.produits:
    data.append({
        'Produit': f"{st.session_state.produits[p]} {p}",
        'Prix(U)': f"{st.session_state.prix_vente[p]:.2f} Dh",
        'Coût(U)': f"{st.session_state.cout_unitaire[p]:.2f} Dh",
        'Commandes/j': st.session_state.commandes_jour[p],
        'Revenu M': f"{ind['revenus'][p]:.2f} Dh",
        'Coût M': f"{ind['couts'][p]:.2f} Dh",
        'Marge M': f"{ind['marges'][p]:.2f} Dh"
    })
df_prod = pd.DataFrame(data)
st.dataframe(df_prod,use_container_width=True)

# 5. Charges mensuelles
st.markdown('<p class="sub-header">💸 Charges mensuelles</p>', unsafe_allow_html=True)
with st.form('chg_form'):
    keys = list(st.session_state.charges_mensuelles.keys())
    half = len(keys)//2+len(keys)%2
    cols = st.columns(2)
    for idx,k in enumerate(keys[:half]):
        val = cols[0].number_input(f"{charges_emojis.get(k,'')} {k}",0.0,100000.0,st.session_state.charges_mensuelles[k],10.0,key=f'chg_{idx}')
        st.session_state.charges_mensuelles[k]=val
    for idx,k in enumerate(keys[half:]):
        val = cols[1].number_input(f"{charges_emojis.get(k,'')} {k}",0.0,100000.0,st.session_state.charges_mensuelles[k],10.0,key=f'chg_{idx+half}')
        st.session_state.charges_mensuelles[k]=val
    if st.form_submit_button('Mettre à jour'): ind = calculer_indicateurs()
# tableau charges
chgs = [{'Charge':f"{charges_emojis.get(k,'')} {k}", 'Montant':f"{v:.2f} Dh"} for k,v in st.session_state.charges_mensuelles.items()]
chgs.append({'Charge':'📊 TOTAL','Montant':f"{sum(st.session_state.charges_mensuelles.values()):.2f} Dh"})
st.dataframe(pd.DataFrame(chgs),use_container_width=True)

# 6. Investissements
st.markdown('<p class="sub-header">🏗️ Investissements initiaux</p>', unsafe_allow_html=True)
with st.form('inv_form'):
    for item,val in st.session_state.charges_investissement.items():
        amt = st.number_input(f"{item}",0.0,1000000.0,val,100.0,key=f'inv_{item}')
        st.session_state.charges_investissement[item]=amt
    if st.form_submit_button('Mettre à jour'): ind = calculer_indicateurs()
inv = [{'Investissement':i,'Montant':f"{v:.2f} Dh"} for i,v in st.session_state.charges_investissement.items()]
inv.append({'Investissement':'📊 TOTAL','Montant':f"{sum(st.session_state.charges_investissement.values()):.2f} Dh"})
st.dataframe(pd.DataFrame(inv),use_container_width=True)

# 7. Camemberts
st.markdown('<p class="sub-header">📉 Répartition des coûts</p>', unsafe_allow_html=True)
col1,col2 = st.columns(2)
with col1:
    fig1, ax1 = plt.subplots(figsize=(6,6))
    labels = [f"{st.session_state.produits[p]} {p}" for p in st.session_state.produits]
    vals = [ind['couts'][p] for p in st.session_state.produits]
    ax1.pie(vals, labels=labels, autopct='%1.1f%%', startangle=90); ax1.axis('equal')
    st.pyplot(fig1)
with col2:
    fig2, ax2 = plt.subplots(figsize=(6,6))
    lbls = [f"{charges_emojis.get(k,'')} {k}" for k in st.session_state.charges_mensuelles]
    vls = list(st.session_state.charges_mensuelles.values())
    ax2.pie(vls, labels=lbls, autopct='%1.1f%%', startangle=90); ax2.axis('equal')
    st.pyplot(fig2)

# 8. Analyse de rentabilité
st.markdown('<p class="sub-header">🔍 Analyse de rentabilité</p>', unsafe_allow_html=True)
col1,col2 = st.columns(2)
with col1:
    st.metric("Seuil de rentabilité", f"{ind['seuil_rentabilite']:.2f} Dh")
    st.metric("Marge sur coût variable", f"{ind['marge_cout_variable']:.2f}%")
with col2:
    st.metric("ROI mensuel", f"{ind['roi_mensuel']:.2f}%")
    st.metric("Temps retour (mois)", f"{ind['temps_retour']:.1f}")

# 9. Recommandations
st.markdown('<p class="sub-header">💡 Recommandations</p>', unsafe_allow_html=True)
if ind['profit_net']>0:
    st.success("✅ Votre projet est rentable !")
    top = sorted(ind['marges'].items(), key=lambda x:-x[1])[:2]
    st.markdown('### Produits les plus rentables')
    for p,m in top:
        st.markdown(f"- {st.session_state.produits[p]} {p} : {m:.2f} Dh")
    st.markdown('### Suggestions d\'optimisation')
    st.markdown('- Augmenter prix sur produits à forte demande')
    st.markdown('- Réduire coûts variables via négociation fournisseurs')
else:
    st.error("⚠️ Projet non rentable")
    st.markdown('- Réduire charges fixes ou variables')
    st.markdown('- Augmenter volume de vente ou prix')

# Footer & téléchargement
st.markdown("---")
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st.download_button("📊 Télécharger rapport (simulé)", data="Fonctionnalité en cours", file_name="rapport.txt", mime="text/plain")

with st.expander("Conseils avancés"):
    st.markdown("""
- **Marketing ciblé**: utilisez les réseaux sociaux.
- **Programme fidélité**: offrez des réductions.
- **Optimisation logistique**: regroupez les envois.
""")
