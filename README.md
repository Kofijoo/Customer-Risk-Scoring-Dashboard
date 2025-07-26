# Customer Risk Scoring & AML Alerting System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Development-yellow.svg)]()

A **professional-grade risk assessment system** for financial institutions, combining rule-based scoring with enhanced customer profiling for AML compliance and fraud detection.

## 🎯 Overview

This system provides comprehensive customer risk assessment by analyzing:
- **Transaction patterns** from PaySim financial data
- **Customer demographics** with PEP (Politically Exposed Person) detection
- **Geographic risk factors** including sanctions and FATF classifications
- **Enhanced risk scoring** with weighted multi-factor analysis

## 🏗️ Architecture

```
├── data/
│   ├── raw/                    # PaySim transaction data
│   ├── processed/              # Enhanced customer profiles
│   └── external/               # Reference data (sanctions, PEP lists)
├── src/
│   ├── config/                 # Configuration and logging
│   ├── etl/                    # Data exploration and processing
│   ├── features/               # Customer profiling engine
│   ├── scoring/                # Risk scoring algorithms
│   ├── screening/              # AML screening (planned)
│   └── monitoring/             # Alert generation (planned)
├── dashboard/                  # Visualization components (planned)
├── models/                     # ML models and artifacts
├── notebooks/                  # Exploratory data analysis
└── tests/                      # Unit and integration tests
```

## ✨ Key Features

### 🔍 Risk Scoring Engine
- **Transaction Analysis**: Pattern detection for TRANSFER, CASH_OUT, and high-value transactions
- **Fraud History**: Weighted scoring based on historical fraud patterns
- **Amount Risk**: Threshold-based risk assessment for large transactions
- **Cash Pattern Analysis**: Detection of suspicious cash transaction behaviors

### 👤 Customer Profiling
- **Demographic Enhancement**: Age, nationality, occupation profiling
- **PEP Detection**: Automated identification of Politically Exposed Persons
- **Geographic Risk**: Country-based risk scoring using Basel AML Index
- **KYC Integration**: Account age and verification status analysis

### 🌍 AML Compliance
- **Sanctions Screening**: High-risk jurisdiction identification
- **FATF Classification**: Grey/blacklist country detection
- **Enhanced Due Diligence**: Multi-factor risk assessment
- **Regulatory Reporting**: Structured risk categorization

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pandas, numpy, pyyaml
- PaySim transaction dataset

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/customer-risk-scoring-dashboard.git
cd customer-risk-scoring-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Test the risk scoring engine
python -m src.scoring.risk_engine

# Generate customer profiles with enhanced risk scoring
python test_customer_profiler.py

# Explore PaySim data patterns
python analyze_paysim.py
```

## 📊 Sample Results

### Risk Distribution
```
Enhanced Risk Categories:
├── LOW: 874 customers (87.4%)
├── MEDIUM: 122 customers (12.2%)
├── HIGH: 4 customers (0.4%)
└── CRITICAL: 0 customers (0.0%)
```

### PEP Detection
```
PEP Categories:
├── NOT_PEP: 984 customers (98.4%)
├── DOMESTIC_PEP: 12 customers (1.2%)
└── FOREIGN_PEP: 4 customers (0.4%)
```

### Geographic Risk
```
High-Risk Jurisdictions:
├── Russia (RU): 33 customers
├── Iran (IR): 29 customers
├── North Korea (KP): 27 customers
└── Afghanistan (AF): 17 customers
```

## 🔧 Configuration

The system uses YAML-based configuration in `src/config/settings.yaml`:

```yaml
risk_scoring:
  weights:
    transaction_risk: 0.40
    country_risk: 0.20
    pep_risk: 0.25
    demographic_risk: 0.10
    geographic_risk: 0.05
  
  thresholds:
    high_risk: 85
    medium_risk: 60
    low_risk: 30
```

## 📈 Risk Scoring Algorithm

The enhanced risk score combines multiple factors:

```python
enhanced_risk_score = (
    transaction_risk * 0.40 +     # PaySim transaction patterns
    country_risk * 0.20 +         # Basel AML Index scores
    pep_risk * 0.25 +            # PEP status (highest weight)
    demographic_risk * 0.10 +     # Age, KYC, account factors
    geographic_risk * 0.05        # Sanctions, FATF flags
)
```

## 🧪 Testing

```bash
# Run risk engine tests
python test_config.py

# Test customer profiler
python test_customer_profiler.py

# Analyze PaySim data
python analyze_paysim.py
```

## 📋 Development Status

- ✅ **Phase 1**: Foundation & Data Analysis
- ✅ **Phase 2**: Risk Scoring Engine & Customer Profiling
- 🔄 **Phase 3**: AML Alerting & Monitoring (In Progress)
- ⏳ **Phase 4**: Dashboard & Visualization (Planned)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 References

- [Basel AML Index](https://index.baselgovernance.org/)
- [FATF Recommendations](https://www.fatf-gafi.org/)
- [PaySim Dataset](https://www.kaggle.com/datasets/ealaxi/paysim1)
- [PEP Screening Guidelines](https://www.fatf-gafi.org/)

## 📞 Support

For questions and support, please open an issue in the GitHub repository.

---

**Built for financial institutions requiring robust AML compliance and customer risk assessment capabilities.**