# Analyse des données RH

Ce projet Python montre l'utilisation de **pandas**, **seaborn** et **matplotlib** pour effectuer une **analyse complète des données RH**. Il inclut :
 ## Fonctionnalités principales
 1. **Calculs**
    - Salaire annuel et total (Salaire + Prime)
    - Ancienneté des employés
    - Catégorisation par âge (Junior / Confirmé / Senior)
    - Score Pondore basé sur perfomance et ancienneté

2. **Analyses groupées**
   - Moyenne, médiane, et écart-type des salaires par Département, Ville et Catégorie d'âge
   - Top 5 employés les meiux payés par département
   - Moyenne des ventes par projet et par employé
   - Moyenne des heures travaillées selon le télétravail

3. **Pivot tables**
   - Ventes Mensuelles par département
   - Pivot mutli-index Département + Projet (total et moyenne des ventes)
   - Heatmap des ventes par mois et département

4. **Filtrages**
   - Sélection des employés selon critères de perfomance et salaire
   - Analyse spécifique des seniors et télétravail avcec perfomance faible
   - Top score par département avec score pondéré

5. **Reporting**
   - Exporting CSV avec toutes les analyses
   - PDF avec visualisations : heatmap et distribution des performances par département

 ## Outils utilisées
 - Python 3.x
 - pandas
 - seaborn
 - matplotlib

## Objectif
Ce projet permet de montrer comment combiner **préparation des données**, **analyses statistiques**, **pivot tables**, **visualisations graphiques** et **reporting automatisé** dans un seul fichier Python
