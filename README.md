# 🛡️ Security Incident Triage Prediction
**Predicting False Positives to Reduce Alert Fatigue**

## 📌 Project Overview
Security Operations Centers (SOCs) are plagued by alert fatigue. This project provides a production-ready solution to triage high volumes of security incidents using the Microsoft GUIDE dataset.

Instead of just a static notebook, this repository features a deployed Machine Learning API that classifies alerts into three categories:

  * **True Positive (TP):** Real threats requiring immediate action.
  * **False Positive (FP):** Benign activity misidentified as a threat.
  * **Benign Positive (BP):** Expected behavior that triggered an alert.

By accurately triaging alerts, we can help security analysts focus on real threats and ignore the "noise."

## 📊 Dataset & Features
The dataset contains millions of security events. Key steps taken in this project:
- **Data Cleaning:** Handled high-cardinality features and dropped columns with >40% missing values (e.g., `MitreTechniques`, `ThreatFamily`).
- **Feature Engineering:** Extracted `hour`, `day_of_week`, and `is_weekend` from timestamps to capture attacker behavior patterns.
- **Handling Imbalance:** Analyzed the distribution of `IncidentGrade` (approx. 21% False Positives).

## 🛠️ Tech Stack
- **Language:** Python 3.9
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-Learn, XGBoost
- **API Development:** FastAPI, Pydantic (Schema validation & Endpoint logic)
- **DevOps:** Docker
- **Testing:** cURL & Swagger UI (API verification)

## 📂 Project Structure
* `app.py`: The FastAPI communication layer.
* `models/`: Serialized model files (`.pkl`) and feature definitions.
* `notebooks/`: Exploratory Data Analysis and model selection.
* `Dockerfile`: The recipe for the isolated Linux-based environment.
* `requirements.txt`: Precise library versions for reproducibility.

## 🚀 Deployment & Usage

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

   Expected Response: {"prediction":"TruePositive","confidence":0.89, ...}

## 📊 Impact & Future Work

By automating the triage of alerts, this system allows SOC analysts to:

* **Filter Noise:** Ignore alerts with high False Positive probability.
* **Accelerate Response:** Focus on alerts with >85% True Positive confidence.
* **V2 Roadmap:** Implement automated retraining loops and integrate with real-world SIEM logs.
