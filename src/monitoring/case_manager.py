import pandas as pd
from datetime import datetime, timedelta
from enum import Enum
import uuid

class CaseStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    UNDER_REVIEW = "UNDER_REVIEW"
    CLOSED = "CLOSED"
    ESCALATED = "ESCALATED"

class CaseType(Enum):
    AML_INVESTIGATION = "AML_INVESTIGATION"
    PEP_REVIEW = "PEP_REVIEW"
    SANCTIONS_CHECK = "SANCTIONS_CHECK"
    FRAUD_INVESTIGATION = "FRAUD_INVESTIGATION"
    ENHANCED_DUE_DILIGENCE = "ENHANCED_DUE_DILIGENCE"

class AMLCaseManager:
    """
    AML Case Management System
    Manages investigation cases generated from alerts
    """
    
    def __init__(self):
        self.cases = pd.DataFrame()
        self.case_actions = pd.DataFrame()
        
        self.sla_hours = {
            'CRITICAL': 4,   # 4 hours for critical cases
            'HIGH': 24,      # 24 hours for high priority
            'MEDIUM': 72,    # 72 hours for medium priority
            'LOW': 168       # 1 week for low priority
        }
    
    def create_case_from_alert(self, alert):
        """Create investigation case from alert"""
        case_type = self._determine_case_type(alert['alert_type'])
        
        case = {
            'case_id': str(uuid.uuid4()),
            'customer_id': alert['customer_id'],
            'alert_id': alert['alert_id'],
            'case_type': case_type.value,
            'priority': alert['priority'],
            'status': CaseStatus.OPEN.value,
            'created_at': datetime.now(),
            'assigned_to': self._auto_assign_case(alert['priority']),
            'due_date': self._calculate_due_date(alert['priority']),
            'description': f"Investigation case for {alert['alert_type']}: {alert['details']}",
            'risk_level': alert['risk_level']
        }
        
        # Add to cases dataframe
        new_case_df = pd.DataFrame([case])
        self.cases = pd.concat([self.cases, new_case_df], ignore_index=True)
        
        # Log case creation
        self._log_case_action(case['case_id'], 'CASE_CREATED', 'Case automatically created from alert')
        
        return case['case_id']
    
    def _determine_case_type(self, alert_type):
        """Determine case type based on alert type"""
        mapping = {
            'PEP_DETECTED': CaseType.PEP_REVIEW,
            'SANCTIONS_MATCH': CaseType.SANCTIONS_CHECK,
            'FRAUD_INDICATOR': CaseType.FRAUD_INVESTIGATION,
            'HIGH_RISK_CUSTOMER': CaseType.ENHANCED_DUE_DILIGENCE,
            'LARGE_TRANSACTION': CaseType.AML_INVESTIGATION,
            'SUSPICIOUS_PATTERN': CaseType.AML_INVESTIGATION
        }
        return mapping.get(alert_type, CaseType.AML_INVESTIGATION)
    
    def _auto_assign_case(self, priority):
        """Auto-assign cases based on priority"""
        # Simplified assignment logic
        if priority == 'CRITICAL':
            return 'Senior_AML_Analyst'
        elif priority == 'HIGH':
            return 'AML_Analyst_Team'
        else:
            return 'Junior_AML_Analyst'
    
    def _calculate_due_date(self, priority):
        """Calculate case due date based on SLA"""
        hours = self.sla_hours.get(priority, 168)
        return datetime.now() + timedelta(hours=hours)
    
    def update_case_status(self, case_id, new_status, notes=""):
        """Update case status"""
        if len(self.cases) > 0:
            mask = self.cases['case_id'] == case_id
            if mask.any():
                old_status = self.cases.loc[mask, 'status'].iloc[0]
                self.cases.loc[mask, 'status'] = new_status
                self.cases.loc[mask, 'last_updated'] = datetime.now()
                
                # Log status change
                self._log_case_action(
                    case_id, 
                    'STATUS_CHANGED', 
                    f"Status changed from {old_status} to {new_status}. {notes}"
                )
                
                print(f"Case {case_id} status updated to {new_status}")
    
    def assign_case(self, case_id, analyst_name):
        """Assign case to analyst"""
        if len(self.cases) > 0:
            mask = self.cases['case_id'] == case_id
            if mask.any():
                self.cases.loc[mask, 'assigned_to'] = analyst_name
                self.cases.loc[mask, 'last_updated'] = datetime.now()
                
                self._log_case_action(case_id, 'CASE_ASSIGNED', f"Case assigned to {analyst_name}")
                print(f"Case {case_id} assigned to {analyst_name}")
    
    def add_case_notes(self, case_id, notes, analyst_name):
        """Add investigation notes to case"""
        self._log_case_action(case_id, 'NOTES_ADDED', notes, analyst_name)
        print(f"Notes added to case {case_id}")
    
    def _log_case_action(self, case_id, action_type, description, analyst_name="SYSTEM"):
        """Log case action"""
        action = {
            'action_id': str(uuid.uuid4()),
            'case_id': case_id,
            'action_type': action_type,
            'description': description,
            'analyst_name': analyst_name,
            'timestamp': datetime.now()
        }
        
        new_action_df = pd.DataFrame([action])
        self.case_actions = pd.concat([self.case_actions, new_action_df], ignore_index=True)
    
    def get_case_summary(self):
        """Get summary of all cases"""
        if len(self.cases) == 0:
            return {"total": 0}
        
        summary = {
            "total": len(self.cases),
            "by_status": self.cases['status'].value_counts().to_dict(),
            "by_priority": self.cases['priority'].value_counts().to_dict(),
            "by_type": self.cases['case_type'].value_counts().to_dict(),
            "overdue": len(self.get_overdue_cases())
        }
        
        return summary
    
    def get_overdue_cases(self):
        """Get cases that are past due date"""
        if len(self.cases) == 0:
            return pd.DataFrame()
        
        now = datetime.now()
        overdue = self.cases[
            (self.cases['due_date'] < now) & 
            (self.cases['status'] != 'CLOSED')
        ]
        
        return overdue
    
    def get_high_priority_cases(self):
        """Get critical and high priority open cases"""
        if len(self.cases) == 0:
            return pd.DataFrame()
        
        high_priority = self.cases[
            (self.cases['priority'].isin(['CRITICAL', 'HIGH'])) &
            (self.cases['status'] != 'CLOSED')
        ].sort_values('created_at', ascending=False)
        
        return high_priority
    
    def close_case(self, case_id, resolution, analyst_name):
        """Close investigation case"""
        self.update_case_status(case_id, CaseStatus.CLOSED.value)
        self._log_case_action(case_id, 'CASE_CLOSED', f"Case closed. Resolution: {resolution}", analyst_name)
        
        if len(self.cases) > 0:
            mask = self.cases['case_id'] == case_id
            if mask.any():
                self.cases.loc[mask, 'closed_at'] = datetime.now()
                self.cases.loc[mask, 'resolution'] = resolution

def test_case_manager():
    """Test the AML case management system"""
    print("=== TESTING AML CASE MANAGER ===")
    
    # Load alerts if available
    try:
        alerts = pd.read_csv('data/processed/aml_alerts.csv')
    except FileNotFoundError:
        print("No alerts found. Run alert engine test first.")
        return
    
    # Initialize case manager
    case_manager = AMLCaseManager()
    
    # Create cases from high priority alerts
    high_priority_alerts = alerts[alerts['priority'].isin(['CRITICAL', 'HIGH'])]
    
    case_ids = []
    for _, alert in high_priority_alerts.head(5).iterrows():  # Test with first 5
        case_id = case_manager.create_case_from_alert(alert)
        case_ids.append(case_id)
    
    print(f"\nCreated {len(case_ids)} investigation cases")
    
    # Simulate case management activities
    if case_ids:
        # Update some case statuses
        case_manager.update_case_status(case_ids[0], CaseStatus.IN_PROGRESS.value, "Investigation started")
        case_manager.add_case_notes(case_ids[0], "Customer profile reviewed. Requesting additional documentation.", "AML_Analyst_1")
        
        if len(case_ids) > 1:
            case_manager.update_case_status(case_ids[1], CaseStatus.UNDER_REVIEW.value, "Escalated to senior analyst")
    
    # Display case summary
    summary = case_manager.get_case_summary()
    print(f"\nCase Management Summary:")
    print(f"  Total Cases: {summary['total']}")
    print(f"  By Status: {summary['by_status']}")
    print(f"  By Priority: {summary['by_priority']}")
    print(f"  Overdue Cases: {summary['overdue']}")
    
    # Show high priority cases
    high_priority_cases = case_manager.get_high_priority_cases()
    if len(high_priority_cases) > 0:
        print(f"\nHigh Priority Cases ({len(high_priority_cases)}):")
        print(high_priority_cases[['case_id', 'customer_id', 'case_type', 'priority', 'status', 'assigned_to']].head())
    
    # Save case data
    if len(case_manager.cases) > 0:
        case_manager.cases.to_csv('data/processed/aml_cases.csv', index=False)
        print(f"\nCases saved to: data/processed/aml_cases.csv")
    
    if len(case_manager.case_actions) > 0:
        case_manager.case_actions.to_csv('data/processed/case_actions.csv', index=False)
        print(f"Case actions saved to: data/processed/case_actions.csv")
    
    print("\n=== AML CASE MANAGER TEST COMPLETE ===")
    return case_manager

if __name__ == "__main__":
    case_manager = test_case_manager()