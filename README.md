# 🛡️ Security Incident Triage Prediction
**Predicting False Positives to Reduce Alert Fatigue**

## 📌 Project Overview
Security Operations Centers (SOCs) are overwhelmed by thousands of alerts daily. To manage and respond effectively, they need alerts that are accurate and actionable. False positives not only exhaust analysts but also risk diverting their attention away from genuine threats, reducing the overall security posture of the organization.

This project uses the **Microsoft GUIDE dataset** to build a Machine Learning model that classifies incidents as `True Positive`, `False Positive`, or `Benign Positive`.

By accurately triaging alerts, we can help security analysts focus on real threats and ignore the "noise."

## 📊 Dataset & Features
The dataset contains millions of security events. Key steps taken in this project:
- **Data Cleaning:** Handled high-cardinality features and dropped columns with >40% missing values (e.g., `MitreTechniques`, `ThreatFamily`).
- **Feature Engineering:** Extracted `hour`, `day_of_week`, and `is_weekend` from timestamps to capture attacker behavior patterns.
- **Handling Imbalance:** Analyzed the distribution of `IncidentGrade` (approx. 21% False Positives).

## 🛠️ Tech Stack
- **Language:** Python 3.9
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn
- **Environment:** Jupyter Notebook / Anaconda

## 📂 Project Structure
- `notebooks/`: Contains the Exploratory Data Analysis (EDA) and model prototyping.
- `data/`: (Local only) Folder for storing the Large CSV files.
- 'models/': Contains the exported train model and requirements.txt file 

## 🚀 How to Run
1. **Clone the repo:** `git clone https://github.com/YOUR_USERNAME/security.git`
2. **Download Data:** Get the `GUIDE_Train.csv` from [Kaggle](https://www.kaggle.com/datasets/microsoft/ai4cyber-guide-dataset).
3. **Setup Folder:** Place the CSV in a `/data` folder.
4. **Run Notebook:** Open `notebooks/incident_triage.ipynb` in Jupyter.
