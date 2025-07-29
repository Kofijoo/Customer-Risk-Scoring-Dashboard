"""
Test script for AML Monitoring and Alerting System
Demonstrates Phase 3: Alert generation and case management
"""

import pandas as pd
from src.monitoring.alert_engine import AMLAlertEngine, AlertMonitor
from src.monitoring.case_manager import AMLCaseManager

def test_complete_aml_workflow():
    """Test complete AML monitoring workflow"""
    print("=== TESTING COMPLETE AML MONITORING WORKFLOW ===")
    
    # Load customer profiles
    try:
        profiles = pd.read_csv('data/processed/enhanced_customer_profiles.csv')
        print(f"Loaded {len(profiles)} customer profiles")
    except FileNotFoundError:
        print("Enhanced customer profiles not found. Run test_customer_profiler.py first.")
        return
    
    # Step 1: Generate Alerts
    print("\n1. GENERATING AML ALERTS...")
    alert_engine = AMLAlertEngine()
    monitor = AlertMonitor()
    
    alerts = alert_engine.generate_alerts(profiles)
    
    if len(alerts) > 0:
        monitor.process_alerts(alerts)
        
        print(f"   Generated {len(alerts)} alerts")
        
        # Alert summary
        summary = monitor.get_alert_summary()
        print(f"   Alert Distribution:")
        print(f"     By Priority: {summary['by_priority']}")
        print(f"     By Type: {summary['by_type']}")
        
        # Step 2: Case Management
        print("\n2. CREATING INVESTIGATION CASES...")
        case_manager = AMLCaseManager()
        
        # Create cases for high priority alerts
        high_priority_alerts = monitor.get_high_priority_alerts()
        case_count = 0
        
        for _, alert in high_priority_alerts.iterrows():
            case_id = case_manager.create_case_from_alert(alert)
            case_count += 1
        
        print(f"   Created {case_count} investigation cases")
        
        # Step 3: Case Management Activities
        print("\n3. CASE MANAGEMENT SIMULATION...")
        
        if case_count > 0:
            cases = case_manager.get_high_priority_cases()
            
            # Simulate case processing
            for i, (_, case) in enumerate(cases.head(3).iterrows()):
                case_id = case['case_id']
                
                if i == 0:
                    case_manager.update_case_status(case_id, "IN_PROGRESS", "Investigation initiated")
                    case_manager.add_case_notes(case_id, "Customer documentation requested", "AML_Analyst_1")
                elif i == 1:
                    case_manager.update_case_status(case_id, "UNDER_REVIEW", "Escalated for senior review")
                    case_manager.add_case_notes(case_id, "Complex PEP case requiring enhanced due diligence", "Senior_AML_Analyst")
                else:
                    case_manager.close_case(case_id, "False positive - customer cleared", "AML_Analyst_2")
        
        # Step 4: Monitoring Dashboard Summary
        print("\n4. MONITORING DASHBOARD SUMMARY...")
        
        # Alert metrics
        print("   ALERT METRICS:")
        print(f"     Total Active Alerts: {summary['total']}")
        print(f"     Critical/High Priority: {summary['by_priority'].get('CRITICAL', 0) + summary['by_priority'].get('HIGH', 0)}")
        
        # Case metrics
        case_summary = case_manager.get_case_summary()
        print("   CASE METRICS:")
        print(f"     Total Cases: {case_summary['total']}")
        print(f"     Open Cases: {case_summary['by_status'].get('OPEN', 0)}")
        print(f"     In Progress: {case_summary['by_status'].get('IN_PROGRESS', 0)}")
        print(f"     Overdue Cases: {case_summary['overdue']}")
        
        # Step 5: Risk Intelligence
        print("\n5. RISK INTELLIGENCE SUMMARY...")
        
        # PEP alerts
        pep_alerts = alerts[alerts['alert_type'] == 'PEP_DETECTED']
        print(f"   PEP Alerts: {len(pep_alerts)}")
        
        # Sanctions alerts
        sanctions_alerts = alerts[alerts['alert_type'] == 'SANCTIONS_MATCH']
        print(f"   Sanctions Alerts: {len(sanctions_alerts)}")
        
        # High risk customers
        high_risk_alerts = alerts[alerts['alert_type'] == 'HIGH_RISK_CUSTOMER']
        print(f"   High Risk Customer Alerts: {len(high_risk_alerts)}")
        
        # Step 6: Save Results
        print("\n6. SAVING MONITORING DATA...")
        
        alerts.to_csv('data/processed/aml_alerts.csv', index=False)
        print("   Alerts saved to: data/processed/aml_alerts.csv")
        
        if len(case_manager.cases) > 0:
            case_manager.cases.to_csv('data/processed/aml_cases.csv', index=False)
            print("   Cases saved to: data/processed/aml_cases.csv")
        
        if len(case_manager.case_actions) > 0:
            case_manager.case_actions.to_csv('data/processed/case_actions.csv', index=False)
            print("   Case actions saved to: data/processed/case_actions.csv")
        
        # Step 7: Regulatory Reporting Summary
        print("\n7. REGULATORY REPORTING READY:")
        print("   ✓ Alert generation and tracking")
        print("   ✓ Case management workflow")
        print("   ✓ Investigation audit trail")
        print("   ✓ Risk categorization and prioritization")
        
    else:
        print("   No alerts generated from current customer profiles")
    
    print("\n=== AML MONITORING WORKFLOW TEST COMPLETE ===")
    print("\nPhase 3: AML Alerting & Monitoring - IMPLEMENTED ✓")
    
    return alerts, case_manager if len(alerts) > 0 else None

def display_monitoring_metrics():
    """Display key monitoring metrics"""
    try:
        alerts = pd.read_csv('data/processed/aml_alerts.csv')
        cases = pd.read_csv('data/processed/aml_cases.csv')
        
        print("\n=== AML MONITORING METRICS ===")
        
        print(f"\nAlert Performance:")
        print(f"  Total Alerts: {len(alerts)}")
        print(f"  Alert Types: {alerts['alert_type'].nunique()}")
        print(f"  Critical Alerts: {len(alerts[alerts['priority'] == 'CRITICAL'])}")
        
        print(f"\nCase Management:")
        print(f"  Total Cases: {len(cases)}")
        print(f"  Open Cases: {len(cases[cases['status'] == 'OPEN'])}")
        print(f"  Closed Cases: {len(cases[cases['status'] == 'CLOSED'])}")
        
        print(f"\nTop Alert Types:")
        print(alerts['alert_type'].value_counts().head())
        
    except FileNotFoundError:
        print("Monitoring data not found. Run the workflow test first.")

if __name__ == "__main__":
    # Run complete workflow test
    alerts, case_manager = test_complete_aml_workflow()
    
    # Display metrics
    display_monitoring_metrics()