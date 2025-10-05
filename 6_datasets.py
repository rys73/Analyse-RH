import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

chemin = r"C:\Users\ighik\OneDrive\Escritorio\html\py-js\fichier_csv\fichiers_6\6_datasets.csv"
chemin_sauvegarde = r"C:\Users\ighik\OneDrive\Escritorio\html\py-js\fichier_csv\fichiers_6\6_datasets_sauvegarde.csv"
chemin_pdf = r"C:\Users\ighik\OneDrive\Escritorio\html\py-js\fichier_csv\fichiers_6\6_graphique.pdf"
fichier = pd.read_csv(chemin, encoding="latin1")
fichier.columns = fichier.columns.str.strip()

# 1. CALCULS AVANCES    
# 1.1 SALAIRE ANNUEL
fichier["Salaire_Annuel"] = fichier["Salaire"] * 12
# 1.2 SALAIRE TOTAL = SALAIRE ANNUEL + PRIME
fichier["Salaire_Total"] = fichier["Salaire_Annuel"] + fichier["Prime"]
# 1.3 ANCIENNETE 
fichier["Date_Embauche"] = pd.to_datetime(fichier["Date_Embauche"])
fichier["Anciennete"] = pd.Timestamp.now().year - fichier["Date_Embauche"].dt.year
# 1.4 CATEGORIE PAR AGE 
fichier["Categorie_Age"] = fichier["Age"].apply(lambda x: "Junior" if x < 30 else ("Confirme" if 30 <= x <= 40 else "Senior"))
# 1.5 SCORE PONDERE
fichier["Score_Pondere"] = (fichier["Performance_Score"] * fichier["Anciennete"]/10).round(2)

# 2. ANALYSE GROUPEE
# 2.1 MOYENNE/MEDIANE/ECART TYPE DU SALAIRE = DEPARTEMENT/VILLE/CATEGORIE AGE
transformation = fichier.groupby(["Categorie_Age", "Departement", "Ville"])["Salaire"].agg(moyenne="mean", mediane="median", ecart_type="std").reset_index()
# 2.2 TOP 5 EMPLOYES LES MIEUX PAYES PAR DEPARTEMENT
top_5 = (fichier.sort_values(["Departement", "Salaire"], ascending=[True, False]).groupby("Departement").head(5))
top_5 = top_5[["Departement", "Salaire"]]
# 2.3 MOYENNE DES VENTES PAR PROJET ET PAR EMPLOYES
colonne_vente = [f"Ventes_Mois{str(i).zfill(2)}" for i in range(1,13)]
moyenne_vente_projet = fichier.groupby("Projet")[colonne_vente].mean()
moyenne_vente_employes = fichier.groupby("Nom")[colonne_vente].mean()
# 2.4 MOYENNE DES HEURES TRAVAILLEES SELON TELETRAVAIL
moyenne_teletravail_oui = fichier[fichier["Teletravail"] == "Oui"].agg(Moyenne_Teletravail_Oui=("Heures_Semaine", "mean")).round(2)
moyenne_teletravail_non = fichier[fichier["Teletravail"] == "Non"].agg(Moyenne_Teletravail_Non=("Heures_Semaine", "mean")).round(2)

# 3. PIVOT TABLES
# 3.1 PIVOT TABLE DES VENTES MENSUELLES PAR DEPARTEMENT
pivot_vente_mensuelle_dep = fichier.pivot_table(
    columns="Departement",
    values=colonne_vente,
    aggfunc=["sum", "mean"],
    fill_value=0).round(2)
# 3.2 PIVOT TABLE MULTI-INDEX : DEPARTEMENT + PROJET => TOTAL VENTES + MOYENNE
pivot_ventes_total_moyenne = fichier.pivot_table(
    index=["Departement", "Projet"],
    values=colonne_vente,
    aggfunc=["sum", "mean"],
    fill_value=0
).round(2)
# 3.3 HEATMAP DES VENTES PAR MOIS ET DEPARTEMENT
with PdfPages(chemin_pdf) as pdf:
  ventes_par_dep = fichier.groupby("Departement")[colonne_vente].sum()
  plt.figure(figsize=(12,6))
  sns.heatmap(ventes_par_dep, annot=True, fmt=".0f", cmap="coolwarm")
  plt.title("Ventes par Mois et par Département")
  plt.xlabel("Mois")
  plt.ylabel("Département")
  pdf.savefig()
  plt.close()

# 5.2 GENERER UN PDF OU HTML RESUME AVEC GRAPHIQUE :, 
  plt.figure(figsize=(10,6))
  sns.stripplot(x="Departement",y="Performance_Score", data=fichier)
  plt.title("Distribution des Perfomances par Departement")
  plt.xlabel("Departement")
  plt.ylabel("Performance Score Des Employes")
  plt.xticks(rotation=45)
  plt.tight_layout()
  pdf.savefig()
  plt.close()

# 4. FILTRAGES
# 4.1 SELECTION LES EMPLOYES PAR FILTRAGE (SALAIRE TOTAL > 70 000 ET PERFOMANCE SCORE > 85)
selection_filtrage_1 = fichier.query("Salaire_Total > 70000 and Performance_Score > 85").sort_values("ID")
# 4.2 SELECTION DES EMPLOYES SENIOR EN TELETRAVIL AVEC PERFORMANCE < 70
selection_filtrage_2 = fichier.query("Categorie_Age == 'Senior' and Performance_Score < 70 and Teletravail == 'Oui'").sort_values("ID")
# 4.3 TOP SCORE PAR DEPARTEMENT AVEC LA MEILLEURE MOYENNE DE PERFORMANCE
top3_de_performance = fichier.sort_values(["Departement", "Score_Pondere"], ascending=[True, False]).groupby("Departement").head(3)
top3_de_performance = top3_de_performance[["Departement", "Score_Pondere"]]
# 5. REPORTING
# 5.1 EXPORT CSV AVEC TOUTES LES ANALYSES REGROUPEES
fichier.to_csv(chemin_sauvegarde, index=False, encoding="latin1")