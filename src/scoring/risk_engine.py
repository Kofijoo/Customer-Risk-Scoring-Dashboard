import pandas as pd
import numpy as np

class RiskScoringEngine:
    """
    Customer Risk Scoring Engine based on PaySim transaction analysis
    Uses weighted scoring algorithm with risk factors identified from data
    """
    
    def __init__(self):
        # Risk weights based on PaySim analysis
        self.weights = {
            'transaction_type': 0.25,    # TRANSFER=high, CASH_OUT=medium
            'amount_risk': 0.30,         # Large amounts (>$578K high, >$100K medium)
            'fraud_history': 0.35,       # Previous fraud transactions (highest weight)
            'cash_pattern': 0.10         # High cash-out frequency
        }
        
        # Risk thresholds from PaySim analysis
        self.thresholds = {
            'high_amount': 578381.88,    # 95th percentile
            'medium_amount': 100000,     # Large transaction threshold
            'low_risk': 30,
            'medium_risk': 60,
            'high_risk': 85
        }
        
        # Transaction type risk scores
        self.tx_type_scores = {
            'TRANSFER': 85,      # 1.04% fraud rate (highest)
            'CASH_OUT': 60,      # 0.37% fraud rate (medium-high)
            'PAYMENT': 10,       # 0.00% fraud rate (low)
            'CASH_IN': 10,       # 0.00% fraud rate (low)
            'DEBIT': 10          # 0.00% fraud rate (low)
        }
    
    def calculate_transaction_type_score(self, customer_data):
        """Calculate risk score based on transaction types"""
        if 'type' not in customer_data.columns:
            return 0
        
        # Get most frequent transaction type
        most_common_type = customer_data['type'].mode().iloc[0] if len(customer_data) > 0 else 'PAYMENT'
        
        # Calculate weighted score based on transaction mix
        type_counts = customer_data['type'].value_counts()
        total_tx = len(customer_data)
        
        weighted_score = 0
        for tx_type, count in type_counts.items():
            proportion = count / total_tx
            type_score = self.tx_type_scores.get(tx_type, 10)
            weighted_score += proportion * type_score
        
        return min(weighted_score, 100)
    
    def calculate_amount_risk_score(self, customer_data):
        """Calculate risk score based on transaction amounts"""
        if 'amount' not in customer_data.columns or len(customer_data) == 0:
            return 0
        
        max_amount = customer_data['amount'].max()
        avg_amount = customer_data['amount'].mean()
        
        # High amount transactions
        if max_amount >= self.thresholds['high_amount']:
            amount_score = 90
        elif max_amount >= self.thresholds['medium_amount']:
            amount_score = 60
        elif avg_amount >= 50000:
            amount_score = 30
        else:
            amount_score = 10
        
        return amount_score
    
    def calculate_fraud_history_score(self, customer_data):
        """Calculate risk score based on fraud history"""
        if 'isFraud' not in customer_data.columns or len(customer_data) == 0:
            return 0
        
        fraud_count = customer_data['isFraud'].sum()
        total_tx = len(customer_data)
        fraud_rate = fraud_count / total_tx if total_tx > 0 else 0
        
        # Fraud history is the strongest predictor
        if fraud_rate >= 0.5:  # 50%+ fraud rate
            return 100
        elif fraud_rate >= 0.1:  # 10%+ fraud rate
            return 80
        elif fraud_count > 0:  # Any fraud history
            return 60
        else:
            return 0
    
    def calculate_cash_pattern_score(self, customer_data):
        """Calculate risk score based on cash transaction patterns"""
        if 'type' not in customer_data.columns or len(customer_data) == 0:
            return 0
        
        cash_out_count = (customer_data['type'] == 'CASH_OUT').sum()
        total_tx = len(customer_data)
        cash_out_rate = cash_out_count / total_tx if total_tx > 0 else 0
        
        # High cash-out activity is suspicious
        if cash_out_rate >= 0.8:  # 80%+ cash-out
            return 80
        elif cash_out_rate >= 0.5:  # 50%+ cash-out
            return 60
        elif cash_out_rate >= 0.2:  # 20%+ cash-out
            return 30
        else:
            return 10
    
    def calculate_customer_risk_score(self, customer_data):
        """Calculate overall risk score for a customer"""
        # Calculate individual risk components
        tx_type_score = self.calculate_transaction_type_score(customer_data)
        amount_score = self.calculate_amount_risk_score(customer_data)
        fraud_score = self.calculate_fraud_history_score(customer_data)
        cash_score = self.calculate_cash_pattern_score(customer_data)
        
        # Calculate weighted total score
        total_score = (
            tx_type_score * self.weights['transaction_type'] +
            amount_score * self.weights['amount_risk'] +
            fraud_score * self.weights['fraud_history'] +
            cash_score * self.weights['cash_pattern']
        )
        
        return {
            'total_score': round(total_score, 2),
            'risk_category': self.get_risk_category(total_score),
            'components': {
                'transaction_type': round(tx_type_score, 2),
                'amount_risk': round(amount_score, 2),
                'fraud_history': round(fraud_score, 2),
                'cash_pattern': round(cash_score, 2)
            }
        }
    
    def get_risk_category(self, score):
        """Convert numeric score to risk category"""
        if score >= self.thresholds['high_risk']:
            return 'CRITICAL'
        elif score >= self.thresholds['medium_risk']:
            return 'HIGH'
        elif score >= self.thresholds['low_risk']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def score_customer_portfolio(self, transaction_data):
        """Score all customers in the dataset"""
        print("Calculating risk scores for customer portfolio...")
        
        customer_scores = []
        customers = transaction_data['nameOrig'].unique()
        
        for customer_id in customers:
            customer_data = transaction_data[transaction_data['nameOrig'] == customer_id]
            risk_result = self.calculate_customer_risk_score(customer_data)
            
            customer_scores.append({
                'customer_id': customer_id,
                'risk_score': risk_result['total_score'],
                'risk_category': risk_result['risk_category'],
                'tx_count': len(customer_data),
                'total_amount': customer_data['amount'].sum(),
                'fraud_count': customer_data['isFraud'].sum() if 'isFraud' in customer_data.columns else 0,
                'components': risk_result['components']
            })
        
        return pd.DataFrame(customer_scores)

def test_risk_engine():
    """Test the risk scoring engine with PaySim data"""
    print("=== TESTING RISK SCORING ENGINE ===")
    
    # Load PaySim data
    df = pd.read_csv('data/raw/paysim_transactions.csv', nrows=10000)
    
    # Initialize risk engine
    engine = RiskScoringEngine()
    
    # Score customer portfolio
    risk_scores = engine.score_customer_portfolio(df)
    
    # Display results
    print(f"\nCustomers scored: {len(risk_scores):,}")
    print("\nRisk category distribution:")
    print(risk_scores['risk_category'].value_counts())
    
    print("\nTop 10 highest risk customers:")
    top_risk = risk_scores.nlargest(10, 'risk_score')
    print(top_risk[['customer_id', 'risk_score', 'risk_category', 'fraud_count', 'tx_count']])
    
    print("\nRisk score statistics:")
    print(f"Mean risk score: {risk_scores['risk_score'].mean():.2f}")
    print(f"Median risk score: {risk_scores['risk_score'].median():.2f}")
    print(f"Max risk score: {risk_scores['risk_score'].max():.2f}")
    
    return risk_scores

if __name__ == "__main__":
    risk_scores = test_risk_engine()
    print("\n=== RISK SCORING ENGINE TEST COMPLETE ===")