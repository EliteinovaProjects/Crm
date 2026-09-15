import pandas as pd
import io
from typing import List, Dict, Any


class ExcelService:
    @staticmethod
    def generate_sample_lead_sheet() -> bytes:
        """Generate a sample Excel sheet for lead import"""
        sample_data = {
            "Name": ["John Doe", "Jane Smith", "Bob Johnson"],
            "Mobile": ["1234567890", "0987654321", "5551234567"],
            "Account": ["Account A", "Account B", "Account C"],
            "Email": ["john@example.com", "jane@example.com", "bob@example.com"],
            "Address": ["123 Main St", "456 Oak Ave", "789 Pine Rd"],
            "Description": ["Sample lead 1", "Sample lead 2", "Sample lead 3"]
        }
        
        df = pd.DataFrame(sample_data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sample Leads')
        
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def generate_sample_agent_sheet() -> bytes:
        """Generate a sample Excel sheet for agent import"""
        sample_data = {
            "Username": ["agent1", "agent2", "agent3"],
            "Email": ["agent1@example.com", "agent2@example.com", "agent3@example.com"],
            "Full Name": ["Agent One", "Agent Two", "Agent Three"],
            "Phone": ["1112223333", "4445556666", "7778889999"],
            "Password": ["password123", "password123", "password123"]
        }
        
        df = pd.DataFrame(sample_data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sample Agents')
        
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def parse_excel_file(file_content: bytes) -> List[Dict[str, Any]]:
        """Parse Excel file and return list of dictionaries"""
        try:
            df = pd.read_excel(io.BytesIO(file_content))
            # Convert DataFrame to list of dictionaries
            data = df.to_dict('records')
            return data
        except Exception as e:
            raise ValueError(f"Error parsing Excel file: {str(e)}")

    @staticmethod
    def generate_export_file(data: List[Dict[str, Any]], filename: str = "export") -> bytes:
        """Generate Excel file from data"""
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=filename)
        
        output.seek(0)
        return output.getvalue()

    @staticmethod
    def generate_csv_file(data: List[Dict[str, Any]]) -> bytes:
        """Generate CSV file from data"""
        df = pd.DataFrame(data)
        
        output = io.BytesIO()
        df.to_csv(output, index=False)
        
        output.seek(0)
        return output.getvalue()
