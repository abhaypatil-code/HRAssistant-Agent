"""
Employee Data Lookup Tool
Handles querying employee information from CSV database
"""
import pandas as pd
import os
from typing import Dict, Optional, List
import config


class EmployeeLookup:
    """
    Employee data lookup and query handler
    """
    
    def __init__(self, csv_path: str = None):
        """
        Initialize employee lookup with CSV data
        
        Args:
            csv_path: Path to employee CSV file
        """
        self.csv_path = csv_path or config.EMPLOYEE_DATA_PATH
        self.df = None
        self.load_data()
    
    def load_data(self):
        """
        Load employee data from CSV
        """
        try:
            if os.path.exists(self.csv_path):
                self.df = pd.read_csv(self.csv_path)
                print(f"✓ Loaded {len(self.df)} employee records")
            else:
                raise FileNotFoundError(f"Employee data file not found: {self.csv_path}")
        except Exception as e:
            print(f"✗ Error loading employee data: {e}")
            self.df = pd.DataFrame()
    
    def get_all_employee_ids(self) -> List[str]:
        """
        Get list of all employee IDs
        
        Returns:
            List of employee IDs
        """
        if self.df is not None and not self.df.empty:
            return self.df['EmpID'].tolist()
        return []
    
    def get_employee_info(self, emp_id: str) -> Optional[Dict]:
        """
        Get complete employee information
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Dictionary with employee data or None if not found
        """
        if self.df is None or self.df.empty:
            return None
        
        employee = self.df[self.df['EmpID'] == emp_id]
        
        if employee.empty:
            return None
        
        return employee.iloc[0].to_dict()
    
    def get_leave_balance(self, emp_id: str) -> Optional[Dict]:
        """
        Get leave balance for an employee
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Dictionary with leave balances or None
        """
        emp_info = self.get_employee_info(emp_id)
        
        if not emp_info:
            return None
        
        return {
            'EmpID': emp_id,
            'Name': emp_info.get('Name'),
            'CasualLeave': emp_info.get('CasualLeave', 0),
            'SickLeave': emp_info.get('SickLeave', 0),
            'EarnedLeave': emp_info.get('EarnedLeave', 0),
            'TotalLeaves': (
                emp_info.get('CasualLeave', 0) + 
                emp_info.get('SickLeave', 0) + 
                emp_info.get('EarnedLeave', 0)
            )
        }
    
    def get_manager_info(self, emp_id: str) -> Optional[Dict]:
        """
        Get manager information for an employee
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Dictionary with manager details or None
        """
        emp_info = self.get_employee_info(emp_id)
        
        if not emp_info:
            return None
        
        manager_name = emp_info.get('Manager')
        
        # Find manager's details
        if self.df is not None and manager_name:
            manager = self.df[self.df['Name'] == manager_name]
            if not manager.empty:
                manager_data = manager.iloc[0].to_dict()
                return {
                    'EmployeeName': emp_info.get('Name'),
                    'ManagerName': manager_data.get('Name'),
                    'ManagerEmail': manager_data.get('Email'),
                    'ManagerPhone': manager_data.get('Phone'),
                    'ManagerRole': manager_data.get('Role'),
                    'ManagerDepartment': manager_data.get('Department')
                }
        
        return {
            'EmployeeName': emp_info.get('Name'),
            'ManagerName': manager_name,
            'ManagerEmail': 'N/A',
            'ManagerPhone': 'N/A',
            'ManagerRole': 'N/A',
            'ManagerDepartment': 'N/A'
        }
    
    def get_department_info(self, emp_id: str) -> Optional[Dict]:
        """
        Get department and role information
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Dictionary with department details or None
        """
        emp_info = self.get_employee_info(emp_id)
        
        if not emp_info:
            return None
        
        department = emp_info.get('Department')
        
        # Get department team members
        team_members = []
        if self.df is not None and department:
            dept_employees = self.df[self.df['Department'] == department]
            team_members = dept_employees['Name'].tolist()
        
        return {
            'EmpID': emp_id,
            'Name': emp_info.get('Name'),
            'Department': department,
            'Role': emp_info.get('Role'),
            'Manager': emp_info.get('Manager'),
            'TeamSize': len(team_members),
            'JoiningDate': emp_info.get('JoiningDate')
        }
    
    def search_employee(self, name: str) -> List[Dict]:
        """
        Search employee by name (partial match)
        
        Args:
            name: Employee name or partial name
            
        Returns:
            List of matching employee dictionaries
        """
        if self.df is None or self.df.empty:
            return []
        
        matches = self.df[self.df['Name'].str.contains(name, case=False, na=False)]
        return matches.to_dict('records')
    
    def get_employees_by_department(self, department: str) -> List[Dict]:
        """
        Get all employees in a department
        
        Args:
            department: Department name
            
        Returns:
            List of employee dictionaries
        """
        if self.df is None or self.df.empty:
            return []
        
        dept_employees = self.df[self.df['Department'].str.contains(department, case=False, na=False)]
        return dept_employees.to_dict('records')
    
    def format_leave_response(self, emp_id: str) -> str:
        """
        Format leave balance as a friendly response
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Formatted string response
        """
        leave_data = self.get_leave_balance(emp_id)
        
        if not leave_data:
            return f"I couldn't find leave information for employee ID {emp_id}. Please check the employee ID and try again."
        
        response = f"""Here's the leave balance for {leave_data['Name']} (ID: {emp_id}):

📅 **Casual Leave**: {leave_data['CasualLeave']} days remaining
🏥 **Sick Leave**: {leave_data['SickLeave']} days remaining
✈️ **Earned Leave**: {leave_data['EarnedLeave']} days remaining

**Total Available Leaves**: {leave_data['TotalLeaves']} days

You can apply for leave through the HR portal. Remember to get manager approval before making any travel arrangements!"""
        
        return response
    
    def format_manager_response(self, emp_id: str) -> str:
        """
        Format manager information as a friendly response
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Formatted string response
        """
        manager_data = self.get_manager_info(emp_id)
        
        if not manager_data:
            return f"I couldn't find manager information for employee ID {emp_id}."
        
        response = f"""Here's the manager information for {manager_data['EmployeeName']}:

👤 **Manager Name**: {manager_data['ManagerName']}
📧 **Email**: {manager_data['ManagerEmail']}
📱 **Phone**: {manager_data['ManagerPhone']}
💼 **Role**: {manager_data['ManagerRole']}
🏢 **Department**: {manager_data['ManagerDepartment']}

Feel free to reach out to your manager for any work-related queries or approvals!"""
        
        return response
    
    def format_department_response(self, emp_id: str) -> str:
        """
        Format department information as a friendly response
        
        Args:
            emp_id: Employee ID
            
        Returns:
            Formatted string response
        """
        dept_data = self.get_department_info(emp_id)
        
        if not dept_data:
            return f"I couldn't find department information for employee ID {emp_id}."
        
        response = f"""Here's the department information for {dept_data['Name']}:

🏢 **Department**: {dept_data['Department']}
💼 **Role**: {dept_data['Role']}
👤 **Manager**: {dept_data['Manager']}
👥 **Team Size**: {dept_data['TeamSize']} members
📅 **Joining Date**: {dept_data['JoiningDate']}

You're part of a great team! Feel free to collaborate and reach out to your colleagues."""
        
        return response


# Singleton instance
_employee_lookup = None

def get_employee_lookup() -> EmployeeLookup:
    """
    Get singleton instance of EmployeeLookup
    
    Returns:
        EmployeeLookup instance
    """
    global _employee_lookup
    if _employee_lookup is None:
        _employee_lookup = EmployeeLookup()
    return _employee_lookup
