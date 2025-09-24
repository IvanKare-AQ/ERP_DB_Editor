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
            
            # Handle duplicate column names by keeping only the first occurrence
            columns_to_keep = []
            seen_columns = set()
            
            for col in self.data.columns:
                base_name = col.strip()  # Remove any trailing spaces
                if base_name not in seen_columns:
                    columns_to_keep.append(col)
                    seen_columns.add(base_name)
            
            # Filter data to keep only unique columns
            self.data = self.data[columns_to_keep]
            
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
    
    def convert_multiline_to_single_line(self) -> dict:
        """Convert multiline cells to single line entries."""
        if self.data is None:
            return {"converted": 0, "total_cells": 0}
        
        converted_count = 0
        total_cells = 0
        
        # Create a copy of the data to work with
        data_copy = self.data.copy()
        
        for column in data_copy.columns:
            for index, value in data_copy[column].items():
                total_cells += 1
                
                # Check if the value is a string and contains newlines
                if isinstance(value, str) and ('\n' in value or '\r' in value):
                    # Replace newlines and carriage returns with spaces
                    cleaned_value = value.replace('\n', ' ').replace('\r', ' ')
                    
                    # Remove multiple consecutive spaces
                    cleaned_value = ' '.join(cleaned_value.split())
                    
                    # Update the value in the copy
                    data_copy.at[index, column] = cleaned_value
                    converted_count += 1
        
        # Update the original data with the cleaned version
        self.data = data_copy
        
        return {
            "converted": converted_count,
            "total_cells": total_cells,
            "percentage": (converted_count / total_cells * 100) if total_cells > 0 else 0
        }
    
    def remove_nen_prefix(self) -> dict:
        """Remove 'NEN' prefix and subsequent spaces from all cells."""
        if self.data is None:
            return {"converted": 0, "total_cells": 0}
        
        converted_count = 0
        total_cells = 0
        
        # Create a copy of the data to work with
        data_copy = self.data.copy()
        
        for column in data_copy.columns:
            for index, value in data_copy[column].items():
                total_cells += 1
                
                # Check if the value is a string and starts with "NEN"
                if isinstance(value, str) and value.strip().upper().startswith('NEN'):
                    # Remove "NEN" and any subsequent spaces at the beginning
                    cleaned_value = value.strip()
                    if cleaned_value.upper().startswith('NEN'):
                        # Remove "NEN" prefix and any spaces that follow
                        cleaned_value = cleaned_value[3:]  # Remove "NEN"
                        cleaned_value = cleaned_value.lstrip()  # Remove leading spaces
                        
                        # Update the value in the copy
                        data_copy.at[index, column] = cleaned_value
                        converted_count += 1
        
        # Update the original data with the cleaned version
        self.data = data_copy
        
        return {
            "converted": converted_count,
            "total_cells": total_cells,
            "percentage": (converted_count / total_cells * 100) if total_cells > 0 else 0
        }
