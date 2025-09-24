"""
Excel Handler for ERP Database Editor
Handles Excel file operations including loading, saving, and data manipulation.
"""

import pandas as pd
import os
from typing import Optional, Dict, Any


class ExcelHandler:
    """Handles Excel file operations for the ERP Database Editor."""
    
    def __init__(self):
        """Initialize the Excel handler."""
        self.data = None
        self.file_path = None
        
    def load_file(self, file_path: str) -> None:
        """Load an Excel file into memory."""
        try:
            # Read the Excel file
            self.data = pd.read_excel(file_path)
            self.file_path = file_path
            
            # Clean the data
            self.clean_data()
            
        except Exception as e:
            raise Exception(f"Failed to load Excel file: {str(e)}")
            
    def clean_data(self) -> None:
        """Clean and prepare the data for display."""
        if self.data is not None:
            # Fill NaN values with empty strings
            self.data = self.data.fillna('')
            
            # Ensure required columns exist
            required_columns = [
                'Article Category', 'Article Subcategory', 'Article Sublevel', 'ERP name'
            ]
            
            for col in required_columns:
                if col not in self.data.columns:
                    self.data[col] = ''
                    
    def save_file(self, file_path: str, data: Optional[pd.DataFrame] = None) -> None:
        """Save data to an Excel file."""
        try:
            # Use provided data or current data
            save_data = data if data is not None else self.data
            
            if save_data is None:
                raise Exception("No data to save")
                
            # Save to Excel file
            save_data.to_excel(file_path, index=False)
            
        except Exception as e:
            raise Exception(f"Failed to save Excel file: {str(e)}")
            
    def get_data(self) -> Optional[pd.DataFrame]:
        """Get the current data."""
        return self.data
        
    def has_data(self) -> bool:
        """Check if data is loaded."""
        return self.data is not None and not self.data.empty
        
    def get_file_path(self) -> Optional[str]:
        """Get the current file path."""
        return self.file_path
        
    def get_column_names(self) -> list:
        """Get the column names from the current data."""
        if self.data is not None:
            return list(self.data.columns)
        return []
        
    def get_unique_values(self, column: str) -> list:
        """Get unique values from a specific column."""
        if self.data is not None and column in self.data.columns:
            return self.data[column].unique().tolist()
        return []
