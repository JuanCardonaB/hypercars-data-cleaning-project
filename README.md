# Hyper Cars 2019 — Data Cleaning Project

## 🧹 Project Overview
This project focuses on **professional data cleaning and standardization** of a real-world automotive dataset — *Hyper Cars 2019*.  
The dataset includes information about top-performance hypercars, but the raw data contains multiple issues such as typos, missing values, inconsistent units, and incorrect formats.  

The goal is to apply **enterprise-level data cleaning practices**, ensuring data integrity, consistency, and reliability for further analysis or visualization.

---

## ⚙️ Data Cleaning Rules

### 1. Car Name
- Standardize names, fix typos, and merge duplicates.
- Validate using known hypercar models.
- Impute missing names based on engine, horsepower, or cost similarity.

### 2. Displacement
- Convert all values to liters (numeric).
- Fix invalid text entries.
- Restrict values between 0.8–9.0 L.
- Impute missing using mean displacement by engine type.

### 3. Engine Type
- Correct typos and ensure consistent naming (`V8`, `W16`, etc.).
- Detect anomalies with regex-based validation.
- Infer missing engines from horsepower and displacement.

### 4. Horsepower (hp)
- Convert to numeric and remove formatting issues.
- Cap within realistic performance ranges (400–1800 hp).
- Impute missing using regression-based estimation.

### 5. Transmission
- Normalize to readable formats (`7-speed`, `Automatic`).
- Fill missing using mode within similar performance ranges.

### 6. Top Speed
- Convert to numeric (mph) and rename column.
- Cap between 150–310 mph.
- Estimate missing using horsepower correlation models.

### 7. Cost
- Clean and convert to numeric (USD).
- Detect and fix outliers.
- Predict missing using regression (based on hp, top speed, and brand).

---

## 📈 Outcome
After cleaning, the dataset will be ready for:
- Exploratory data analysis (EDA)
- Predictive modeling
- Visualization dashboards

---

## 👤 Author & Contact
**Author:** Juan Cardona  
📧 **Contact:** juanjocarbol@gmail.com  
🔗 **LinkedIn:** [linkedin.com/in/juan-jose-cardona-bolivar](https://linkedin.com/in/juan-jose-cardona-bolivar)
