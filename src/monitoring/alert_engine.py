import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
import uuid

class AlertType(Enum):
    HIGH_RISK_CUSTOMER = "HIGH_RISK_CUSTOMER"
    PEP_DETECTED = "PEP_DETECTED"
    SANCTIONS_MATCH = "SANCTIONS_MATCH"
    LARGE_TRANSACTION = "LARGE_TRANSACTION"
    SUSPICIOUS_PATTERN = "SUSPICIOUS_PATTERN"
    FRAUD_INDICATOR = "FRAUD_INDICATOR"

class AlertPriority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class AMLAlertEngine:
    """
    AML Alert Generation Engine
    Monitors customer risk profiles and generates alerts based on thresholds
    """
    
    def __init__(self):
        self.alert_thresholds = {
            'critical_risk_score': 85,
            'high_risk_score': 60,
            'large_transaction': 100000,
            'fraud_count_threshold': 1,
            'pep_alert': True,
            'sanctions_alert': True
        }
        
        self.alert_rules = {
            AlertType.HIGH_RISK_CUSTOMER: {
                'priority': AlertPriority.HIGH,
                'description': 'Customer risk score exceeds threshold'
            },
            AlertType.PEP_DETECTED: {
                'priority': AlertPriority.CRITICAL,
                'description': 'Politically Exposed Person identified'
            },
            AlertType.SANCTIONS_MATCH: {
                'priority': AlertPriority.CRITICAL,
                'description': 'Customer from sanctioned jurisdiction'
            },
            AlertType.LARGE_TRANSACTION: {
                'priority': AlertPriority.MEDIUM,
                'description': 'Large transaction amount detected'
            },
            AlertType.SUSPICIOUS_PATTERN: {
                'priority': AlertPriority.HIGH,
                'description': 'Suspicious transaction pattern identified'
            },
            AlertType.FRAUD_INDICATOR: {
                'priority': AlertPriority.CRITICAL,
                'description': 'Historical fraud activity detected'
            }
        }
    
    def generate_alerts(self, customer_profiles):
        """Generate alerts based on customer risk profiles"""
        print("Generating AML alerts...")
        
        alerts = []
        
        for _, customer in customer_profiles.iterrows():
            customer_alerts = self._evaluate_customer_alerts(customer)
            alerts.extend(customer_alerts)
        
        alerts_df = pd.DataFrame(alerts)
        
        if len(alerts_df) > 0:
            alerts_df['created_at'] = datetime.now()
            alerts_df['status'] = 'OPEN'
            alerts_df['assigned_to'] = None
            
        return alerts_df
    
    def _evaluate_customer_alerts(self, customer):
        """Evaluate individual customer for alert conditions"""
        alerts = []
        
        # High Risk Score Alert
        if customer['enhanced_risk_score'] >= self.alert_thresholds['critical_risk_score']:
            alerts.append(self._create_alert(
                customer['customer_id'],
                AlertType.HIGH_RISK_CUSTOMER,
                f"Critical risk score: {customer['enhanced_risk_score']}"
            ))
        elif customer['enhanced_risk_score'] >= self.alert_thresholds['high_risk_score']:
            alerts.append(self._create_alert(
                customer['customer_id'],
                AlertType.HIGH_RISK_CUSTOMER,
                f"High risk score: {customer['enhanced_risk_score']}"
            ))
        
        # PEP Alert
        if customer['is_pep'] and self.alert_thresholds['pep_alert']:
            alerts.append(self._create_alert(
                customer['customer_id'],
                AlertType.PEP_DETECTED,
                f"PEP Category: {customer['pep_category']}, Occupation: {customer['occupation']}"
            ))
        
        # Sanctions Alert
        if customer['sanctions_risk'] and self.alert_thresholds['sanctions_alert']:
            alerts.append(self._create_alert(
                customer['customer_id'],
                AlertType.SANCTIONS_MATCH,
                f"Sanctioned jurisdiction: {customer['nationality']}"
            ))
        
        # Fraud History Alert
        if 'fraud_count' in customer and customer['fraud_count'] >= self.alert_thresholds['fraud_count_threshold']:
            alerts.append(self._create_alert(
                customer['customer_id'],
                AlertType.FRAUD_INDICATOR,
                f"Fraud history: {customer['fraud_count']} incidents"
            ))
        
        # Large Transaction Alert (if transaction data available)
        if 'total_amount' in customer and customer['total_amount'] >= self.alert_thresholds['large_transaction']:
            alerts.append(self._create_alert(
                customer['customer_id'],
                AlertType.LARGE_TRANSACTION,
                f"Large transaction volume: ${customer['total_amount']:,.2f}"
            ))
        
        return alerts
    
    def _create_alert(self, customer_id, alert_type, details):
        """Create alert record"""
        rule = self.alert_rules[alert_type]
        
        return {
            'alert_id': str(uuid.uuid4()),
            'customer_id': customer_id,
            'alert_type': alert_type.value,
            'priority': rule['priority'].value,
            'description': rule['description'],
            'details': details,
            'risk_level': self._determine_risk_level(alert_type)
        }
    
    def _determine_risk_level(self, alert_type):
        """Determine risk level based on alert type"""
        critical_alerts = [AlertType.PEP_DETECTED, AlertType.SANCTIONS_MATCH, AlertType.FRAUD_INDICATOR]
        high_alerts = [AlertType.HIGH_RISK_CUSTOMER, AlertType.SUSPICIOUS_PATTERN]
        
        if alert_type in critical_alerts:
            return 'CRITICAL'
        elif alert_type in high_alerts:
            return 'HIGH'
        else:
            return 'MEDIUM'

class AlertMonitor:
    """
    Real-time alert monitoring and management
    """
    
    def __init__(self):
        self.active_alerts = pd.DataFrame()
        self.alert_history = pd.DataFrame()
    
    def process_alerts(self, new_alerts):
        """Process and categorize new alerts"""
        if len(new_alerts) == 0:
            return
        
        # Add to active alerts
        self.active_alerts = pd.concat([self.active_alerts, new_alerts], ignore_index=True)
        
        # Update alert history
        self.alert_history = pd.concat([self.alert_history, new_alerts], ignore_index=True)
        
        print(f"Processed {len(new_alerts)} new alerts")
    
    def get_alert_summary(self):
        """Get summary of current alerts"""
        if len(self.active_alerts) == 0:
            return {"total": 0, "by_priority": {}, "by_type": {}}
        
        summary = {
            "total": len(self.active_alerts),
            "by_priority": self.active_alerts['priority'].value_counts().to_dict(),
            "by_type": self.active_alerts['alert_type'].value_counts().to_dict(),
            "by_risk_level": self.active_alerts['risk_level'].value_counts().to_dict()
        }
        
        return summary
    
    def get_high_priority_alerts(self):
        """Get critical and high priority alerts"""
        if len(self.active_alerts) == 0:
            return pd.DataFrame()
        
        high_priority = self.active_alerts[
            self.active_alerts['priority'].isin(['CRITICAL', 'HIGH'])
        ].sort_values('created_at', ascending=False)
        
        return high_priority
    
    def close_alert(self, alert_id, resolution_notes=""):
        """Close an alert"""
        if len(self.active_alerts) > 0:
            mask = self.active_alerts['alert_id'] == alert_id
            if mask.any():
                self.active_alerts.loc[mask, 'status'] = 'CLOSED'
                self.active_alerts.loc[mask, 'closed_at'] = datetime.now()
                self.active_alerts.loc[mask, 'resolution_notes'] = resolution_notes
                print(f"Alert {alert_id} closed")

def test_alert_engine():
    """Test the AML alert engine"""
    print("=== TESTING AML ALERT ENGINE ===")
    
    # Load customer profiles
    try:
        profiles = pd.read_csv('data/processed/enhanced_customer_profiles.csv')
    except FileNotFoundError:
        print("Enhanced customer profiles not found. Run test_customer_profiler.py first.")
        return
    
    # Initialize alert engine
    alert_engine = AMLAlertEngine()
    monitor = AlertMonitor()
    
    # Generate alerts
    alerts = alert_engine.generate_alerts(profiles)
    
    if len(alerts) > 0:
        # Process alerts
        monitor.process_alerts(alerts)
        
        # Display results
        print(f"\nTotal alerts generated: {len(alerts)}")
        
        summary = monitor.get_alert_summary()
        print(f"\nAlert Summary:")
        print(f"  Total Active: {summary['total']}")
        print(f"  By Priority: {summary['by_priority']}")
        print(f"  By Type: {summary['by_type']}")
        
        # Show high priority alerts
        high_priority = monitor.get_high_priority_alerts()
        if len(high_priority) > 0:
            print(f"\nHigh Priority Alerts ({len(high_priority)}):")
            print(high_priority[['customer_id', 'alert_type', 'priority', 'details']].head(10))
        
        # Save alerts
        alerts.to_csv('data/processed/aml_alerts.csv', index=False)
        print(f"\nAlerts saved to: data/processed/aml_alerts.csv")
    else:
        print("No alerts generated")
    
    print("\n=== AML ALERT ENGINE TEST COMPLETE ===")
    return alerts, monitor

if __name__ == "__main__":
    alerts, monitor = test_alert_engine()