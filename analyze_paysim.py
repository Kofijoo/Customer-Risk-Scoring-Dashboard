import pandas as pd

def explore_paysim_data():
    print("Analyzing PaySim dataset for risk scoring...")
    
    # Load sample from actual file
    sample_df = pd.read_csv('data/raw/paysim_transactions.csv', nrows=50000)
    
    print("=== PAYSIM DATASET ANALYSIS ===")
    print(f"Sample shape: {sample_df.shape}")
    print(f"Columns: {list(sample_df.columns)}")
    
    # Risk-focused analysis
    print("\n=== RISK INDICATORS ===")
    
    # Fraud analysis
    if 'isFraud' in sample_df.columns:
        fraud_rate = sample_df['isFraud'].mean()
        fraud_count = sample_df['isFraud'].sum()
        print(f"Fraud transactions: {fraud_count:,} ({fraud_rate*100:.3f}%)")
    
    # Transaction type risk analysis
    if 'type' in sample_df.columns:
        print("\nTransaction types (risk relevance):")
        type_counts = sample_df['type'].value_counts()
        for tx_type, count in type_counts.items():
            fraud_in_type = sample_df[sample_df['type'] == tx_type]['isFraud'].sum() if 'isFraud' in sample_df.columns else 0
            fraud_rate_type = fraud_in_type / count * 100 if count > 0 else 0
            print(f"  {tx_type}: {count:,} transactions ({fraud_rate_type:.2f}% fraud)")
    
    # Customer analysis
    if 'nameOrig' in sample_df.columns:
        unique_customers = sample_df['nameOrig'].nunique()
        avg_tx_per_customer = len(sample_df) / unique_customers
        print(f"\nCustomer base: {unique_customers:,} unique customers")
        print(f"Avg transactions per customer: {avg_tx_per_customer:.1f}")
    
    # Amount analysis for risk thresholds
    if 'amount' in sample_df.columns:
        print("\nTransaction amounts (risk thresholds):")
        print(f"  Mean: ${sample_df['amount'].mean():,.2f}")
        print(f"  Median: ${sample_df['amount'].median():,.2f}")
        print(f"  95th percentile: ${sample_df['amount'].quantile(0.95):,.2f}")
        print(f"  99th percentile: ${sample_df['amount'].quantile(0.99):,.2f}")
    
    # High-risk transaction patterns
    print("\n=== HIGH-RISK PATTERNS ===")
    
    # Large cash transactions
    if 'type' in sample_df.columns and 'amount' in sample_df.columns:
        cash_transactions = sample_df[sample_df['type'].isin(['CASH_OUT', 'CASH_IN'])]
        if len(cash_transactions) > 0:
            large_cash = cash_transactions[cash_transactions['amount'] > 100000]
            print(f"Large cash transactions (>$100K): {len(large_cash):,}")
    
    # Zero balance after transaction (potential money laundering)
    if 'newbalanceOrig' in sample_df.columns:
        zero_balance = sample_df[sample_df['newbalanceOrig'] == 0]
        print(f"Transactions ending in zero balance: {len(zero_balance):,}")
    
    return sample_df

def generate_customer_risk_features(df):
    """Generate risk features per customer for scoring"""
    print("\nGenerating customer risk features...")
    
    # Group by customer
    customer_features = df.groupby('nameOrig').agg({
        'amount': ['count', 'sum', 'mean', 'max'],
        'isFraud': 'sum',
        'type': lambda x: (x == 'CASH_OUT').sum()  # Count of cash-out transactions
    }).round(2)
    
    # Flatten column names
    customer_features.columns = ['tx_count', 'total_amount', 'avg_amount', 'max_amount', 'fraud_count', 'cash_out_count']
    
    # Calculate risk score components
    customer_features['fraud_rate'] = (customer_features['fraud_count'] / customer_features['tx_count']).round(4)
    customer_features['cash_out_rate'] = (customer_features['cash_out_count'] / customer_features['tx_count']).round(4)
    customer_features['high_amount_rate'] = (customer_features['max_amount'] > 100000).astype(int)
    
    print(f"\n=== CUSTOMER RISK FEATURES ===")
    print(f"Customers analyzed: {len(customer_features):,}")
    print("\nTop 10 highest risk customers:")
    print(customer_features.nlargest(10, 'fraud_count')[['tx_count', 'fraud_count', 'fraud_rate', 'cash_out_rate']])
    
    return customer_features

if __name__ == "__main__":
    sample_data = explore_paysim_data()
    customer_features = generate_customer_risk_features(sample_data)
    print("\n=== ANALYSIS COMPLETE ===")
    print("PaySim dataset successfully analyzed for risk scoring insights!")