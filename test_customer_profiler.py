import pandas as pd
import numpy as np

class CustomerProfileGenerator:
    """Generate synthetic customer profiles with AML/KYC risk factors"""
    
    def __init__(self):
        # Country risk ratings (based on Basel AML Index)
        self.country_risk = {
            'US': {'risk_score': 15, 'category': 'LOW'},
            'UK': {'risk_score': 20, 'category': 'LOW'},
            'DE': {'risk_score': 18, 'category': 'LOW'},
            'FR': {'risk_score': 22, 'category': 'LOW'},
            'SG': {'risk_score': 25, 'category': 'LOW'},
            'CH': {'risk_score': 12, 'category': 'LOW'},
            'RU': {'risk_score': 75, 'category': 'HIGH'},
            'CN': {'risk_score': 45, 'category': 'MEDIUM'},
            'IN': {'risk_score': 40, 'category': 'MEDIUM'},
            'BR': {'risk_score': 50, 'category': 'MEDIUM'},
            'NG': {'risk_score': 80, 'category': 'HIGH'},
            'AF': {'risk_score': 95, 'category': 'CRITICAL'},
            'IR': {'risk_score': 90, 'category': 'CRITICAL'},
            'KP': {'risk_score': 100, 'category': 'CRITICAL'}
        }
        
        # High-risk occupations for PEP classification
        self.high_risk_occupations = [
            'Government Official', 'Military Officer', 'Judge', 'Diplomat',
            'Central Bank Official', 'State Enterprise Executive', 'Political Party Official'
        ]
        
        # Standard occupations
        self.standard_occupations = [
            'Software Engineer', 'Teacher', 'Doctor', 'Lawyer', 'Accountant',
            'Manager', 'Sales Representative', 'Consultant', 'Analyst', 'Engineer'
        ]
    
    def generate_customer_demographics(self, customer_ids):
        """Generate demographic profiles for customers"""
        print(f"Generating demographic profiles for {len(customer_ids):,} customers...")
        
        profiles = []
        countries = list(self.country_risk.keys())
        country_weights = [1/risk['risk_score'] for risk in self.country_risk.values()]
        
        for customer_id in customer_ids:
            # Generate basic demographics
            age = np.random.randint(18, 81)
            nationality = np.random.choice(countries, p=np.array(country_weights)/sum(country_weights))
            
            # Determine PEP status (2% chance)
            is_pep = np.random.random() < 0.02
            if is_pep:
                occupation = np.random.choice(self.high_risk_occupations)
                pep_category = 'DOMESTIC_PEP' if np.random.random() < 0.7 else 'FOREIGN_PEP'
            else:
                occupation = np.random.choice(self.standard_occupations)
                pep_category = 'NOT_PEP'
            
            # Account information
            account_age_days = np.random.randint(30, 3650)
            kyc_status = np.random.choice(['COMPLETE', 'PENDING', 'INCOMPLETE'], p=[0.85, 0.10, 0.05])
            
            # Risk factors
            country_risk_score = self.country_risk[nationality]['risk_score']
            age_risk_score = self._get_age_risk_score(age)
            pep_risk_score = 80 if is_pep else 0
            
            profiles.append({
                'customer_id': customer_id,
                'age': age,
                'nationality': nationality,
                'occupation': occupation,
                'is_pep': is_pep,
                'pep_category': pep_category,
                'account_age_days': account_age_days,
                'kyc_status': kyc_status,
                'country_risk_score': country_risk_score,
                'age_risk_score': age_risk_score,
                'pep_risk_score': pep_risk_score
            })
        
        return pd.DataFrame(profiles)
    
    def _get_age_risk_score(self, age):
        """Calculate risk score based on age"""
        if 18 <= age <= 25:
            return 30  # Young adults - higher risk
        elif 26 <= age <= 40:
            return 15  # Working age - lower risk
        elif 41 <= age <= 60:
            return 10  # Established - lowest risk
        else:
            return 25  # Elderly - medium risk
    
    def enhance_with_geographic_risk(self, profiles_df):
        """Add geographic risk indicators"""
        print("Adding geographic risk indicators...")
        
        # High-risk jurisdiction flags
        profiles_df['high_risk_jurisdiction'] = profiles_df['nationality'].isin(['AF', 'IR', 'KP', 'RU'])
        profiles_df['sanctions_risk'] = profiles_df['nationality'].isin(['IR', 'KP', 'RU'])
        profiles_df['fatf_risk'] = profiles_df['nationality'].isin(['AF', 'IR', 'KP'])
        
        return profiles_df
    
    def generate_enhanced_risk_scores(self, profiles_df):
        """Calculate enhanced risk scores"""
        print("Calculating enhanced risk scores...")
        
        # Enhanced risk weights
        weights = {
            'country_risk': 0.30,
            'pep_risk': 0.40,
            'demographic_risk': 0.20,
            'geographic_risk': 0.10
        }
        
        # Calculate risk components
        profiles_df['demographic_risk_score'] = (
            profiles_df['age_risk_score'] + 
            (profiles_df['kyc_status'] == 'INCOMPLETE').astype(int) * 30 +
            (profiles_df['account_age_days'] < 90).astype(int) * 20
        )
        
        profiles_df['geographic_risk_score'] = (
            profiles_df['high_risk_jurisdiction'].astype(int) * 40 +
            profiles_df['sanctions_risk'].astype(int) * 60 +
            profiles_df['fatf_risk'].astype(int) * 80
        )
        
        # Calculate final enhanced risk score
        profiles_df['enhanced_risk_score'] = (
            profiles_df['country_risk_score'] * weights['country_risk'] +
            profiles_df['pep_risk_score'] * weights['pep_risk'] +
            profiles_df['demographic_risk_score'] * weights['demographic_risk'] +
            profiles_df['geographic_risk_score'] * weights['geographic_risk']
        ).round(2)
        
        # Enhanced risk categories
        profiles_df['enhanced_risk_category'] = profiles_df['enhanced_risk_score'].apply(
            lambda x: 'CRITICAL' if x >= 85 else 
                     'HIGH' if x >= 60 else 
                     'MEDIUM' if x >= 30 else 'LOW'
        )
        
        return profiles_df

def test_customer_profiler():
    """Test the customer profile generator"""
    print("=== TESTING CUSTOMER PROFILE GENERATOR ===")
    
    # Load PaySim data to get customer IDs
    df = pd.read_csv('data/raw/paysim_transactions.csv', nrows=5000)
    customer_ids = df['nameOrig'].unique()[:1000]  # Test with 1000 customers
    
    # Generate customer profiles
    profiler = CustomerProfileGenerator()
    
    # Create demographic profiles
    profiles = profiler.generate_customer_demographics(customer_ids)
    
    # Add geographic risk
    profiles = profiler.enhance_with_geographic_risk(profiles)
    
    # Generate enhanced risk scores
    enhanced_scores = profiler.generate_enhanced_risk_scores(profiles)
    
    # Display results
    print(f"\nCustomer profiles generated: {len(enhanced_scores):,}")
    
    print("\nEnhanced risk category distribution:")
    print(enhanced_scores['enhanced_risk_category'].value_counts())
    
    print("\nPEP distribution:")
    print(enhanced_scores['pep_category'].value_counts())
    
    print("\nCountry distribution (top 10):")
    print(enhanced_scores['nationality'].value_counts().head(10))
    
    print("\nTop 10 highest enhanced risk customers:")
    top_enhanced = enhanced_scores.nlargest(10, 'enhanced_risk_score')
    print(top_enhanced[['customer_id', 'enhanced_risk_score', 'enhanced_risk_category', 
                      'is_pep', 'nationality', 'age', 'occupation']])
    
    print("\nHigh-risk jurisdiction analysis:")
    high_risk_customers = enhanced_scores[enhanced_scores['high_risk_jurisdiction']]
    print(f"Customers from high-risk jurisdictions: {len(high_risk_customers)}")
    if len(high_risk_customers) > 0:
        print("High-risk jurisdictions found:")
        print(high_risk_customers['nationality'].value_counts())
    
    print("\nPEP analysis:")
    pep_customers = enhanced_scores[enhanced_scores['is_pep']]
    print(f"PEP customers identified: {len(pep_customers)}")
    if len(pep_customers) > 0:
        print("PEP occupations:")
        print(pep_customers['occupation'].value_counts())
    
    # Save enhanced profiles
    enhanced_scores.to_csv('data/processed/enhanced_customer_profiles.csv', index=False)
    print("\nEnhanced customer profiles saved to: data/processed/enhanced_customer_profiles.csv")
    
    return enhanced_scores

if __name__ == "__main__":
    enhanced_profiles = test_customer_profiler()
    print("\n=== CUSTOMER PROFILER TEST COMPLETE ===")