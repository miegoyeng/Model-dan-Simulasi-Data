# Asthma Machine Learning Pipeline

## Struktur Direktori
- dataset/                # berisi asthma_disease_data.csv
- notebooks/              # berisi asthma_ml_pipeline.ipynb

## Jalankan Notebook
1. Buka `notebooks/asthma_ml_pipeline.ipynb` di Jupyter.
2. Jalankan cell satu per satu sesuai urutan.

## Library yang Diperlukan (install di notebook)

!pip install pandas numpy matplotlib seaborn scikit-learn shap statsmodels


## Isi Notebook
1. Instalasi & import
2. Load dataset
3. EDA
4. Feature engineering (severity scoring)
5. Ordinal classification (RandomForest)
6. Model evaluation (CV, ROC-AUC, confusion matrix)
7. Explainable ML (Logistic regression odds ratio, SHAP)
8. Clustering (KMeans + t-SNE)
9. Visualisasi cluster vs severity
10. Save model

