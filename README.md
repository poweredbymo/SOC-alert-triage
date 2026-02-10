# Security Incident Triage Prediction
**Predicting False Positives to Reduce Alert Fatigue**

## Project Overview
Security Operations Centers (SOCs) are plagued by alert fatigue. This project provides a production-ready solution to triage high volumes of security incidents using the Microsoft GUIDE dataset.

Instead of just a static notebook, this repository features a deployed Machine Learning API that classifies alerts into three categories:

  * **True Positive (TP):** Real threats requiring immediate action.
  * **False Positive (FP):** Benign activity misidentified as a threat.
  * **Benign Positive (BP):** Expected behavior that triggered an alert.

By accurately triaging alerts, we can help security analysts focus on real threats and ignore the "noise."

## Tech Stack
- **Language:** Python 3.9
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, XGBoost
- **API Development:** FastAPI, Pydantic (Schema validation & Endpoint logic)
- **DevOps:** Docker
- **Testing:** cURL & Swagger UI (API verification)

## Project Structure
* `app.py`: The FastAPI communication layer.
* `models/`: Serialized model files (`.pkl`) and feature definitions.
* `notebooks/`: Exploratory Data Analysis and model selection.
* `Dockerfile`: The recipe for the isolated Linux-based environment.
* `requirements.txt`: Precise library versions for reproducibility.

## Data Science Methodology

This project utilizes the **Microsoft GUIDE** dataset. The following steps were taken to transform ~13M raw security events into a deployable classifier.
  
### 1. Data Acquisition
* **Source:** [Microsoft GUIDE Dataset (Kaggle)](https://www.kaggle.com/datasets/Microsoft/microsoft-security-incident-prediction) 
* **Status:** Raw CSVs are excluded from this repo via `.gitignore` to maintain a lightweight footprint. Users should place `GUIDE_Train.csv` in a `/data` folder locally.

### 2. Exploratory Data Analysis (EDA)
Initial analysis revealed a significant class imbalance and high-cardinality features:
* **Target Distribution:** Benign Positive (44%), True Positive (34%), False Positive (21%).
* **Feature Pruning:** Dropped 10+ columns with >40% missing values (e.g., `MitreTechniques`, `ThreatFamily`, `SuspicionLevel`).
* **Noise Reduction:** Removed unique identifiers like `OrgId` and `IncidentId` which provide no predictive power.

### 3. Feature Engineering
To capture attacker behavior patterns, several "Temporal Features" were derived from the raw `Timestamp`:
* `hour`: The hour of the day (0-23) to identify "after-hours" anomalies.
* `dow`: Day of the week (0-6).
* `is_weekend`: Binary flag (1 if Sat/Sun) to detect weekend-specific spikes in malicious activity.

### 4. Data Pipeline & Validation
The final training set was prepared using a stratified split to preserve class ratios:
* **Numeric Encoding:** Categorical targets mapped to `0 (FalsePositive)`, `1 (BenignPositive)`, and `2 (TruePositive)`.
* **Validation Strategy:** 80/20 train-test split with stratification.
* **Feature Consistency:** A `features.json` schema is used by the FastAPI app to ensure the production API receives the exact same column order as the training phase.

## 🔬 Model Selection & Optimization

The goal was to find a model that balanced high precision (to avoid missing real threats) with speed. I conducted a comparative analysis of three architectures:

| Model | Why it was tested | Result |
| :--- | :--- | :--- |
| **Logistic Regression** | Baseline for linear separability. | High speed, but struggled with complex patterns. |
| **Random Forest** | To handle non-linear relationships. | Strong accuracy, but large model size. |
| **XGBoost** | Gradient boosting for peak performance. Recommended to handle millions of examples | **Winner:** Best F1-score and efficiency. |

### Hyperparameter Tuning (GridSearchCV)
To prevent overfitting and ensure the model generalized well to unseen security data, I performed a **Grid Search** over the following parameters:
* `learning_rate`: Optimized for stable convergence.
* `max_depth`: Tuned to capture complex interactions without memorizing noise.
* `n_estimators`: Balanced for performance and training time.

This optimization significantly improved the model's ability to distinguish between **Benign Positives** and **True Positives**, which are often the most difficult classes to separate in SOC logs.


## Deployment & Usage

This project is containerized using **Docker** for consistent deployment across environments.

### Running with Docker
1. **Build the image:**
   ```bash
   docker build -t alert-triage-api .
2. **Run the container:**
   ```bash
   docker run -p 8000:8000 alert-triage-api
3. **Input alert features through UI:**
   Once the container is running, open your browser to: http://localhost:8000/docs
   You can use the Swagger UI to manually input alert features and see the model's confidence scores in real-time.
4. **Verify with a request (cURL):**
   You can send alerts directly to the API using curl:
   ```bash
     curl -X 'POST' 'http://localhost:8000/predict' \
     -H 'Content-Type: application/json' \
     -d '{"features": {"DetectorId": 3, "hour": 14, "dow": 2, "is_weekend": 0, "OSFamily": 1, "CountryCode": 5}}' 
   ```
   Expected Response: {"prediction":"TruePositive","confidence":0.89, ...}

## Impact & Future Work

By automating the triage of alerts, this system allows SOC analysts to:

* **Filter Noise:** Ignore alerts with high False Positive probability.
* **Accelerate Response:** Focus on alerts with >85% True Positive confidence.
* **V2 Roadmap:** Implement automated retraining loops and integrate with real-world SIEM logs.
