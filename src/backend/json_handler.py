"""
JSON Handler for ERP Database Editor
Handles JSON file operations including loading, saving, and data manipulation.
Replaces the ExcelHandler.
"""

import pandas as pd
import json
import os
from typing import Optional, Dict, Any, List


class JsonHandler:
    """Handles JSON file operations for the ERP Database Editor."""
    
    def __init__(self):
        """Initialize the JSON handler."""
        self.data = None
        self.categories = None
        # Determine path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.file_path = os.path.join(project_root, "data", "component_database.json")
        self.categories_file_path = os.path.join(project_root, "data", "airq_categories.json")
        self.added_file_path = os.path.join(project_root, "data", "new_items.json")
        self.added_data = pd.DataFrame()
        self.schema_columns: List[str] = []
        self._added_items_loaded = False  # Track if added items have been loaded (lazy loading)
        
    def load_categories(self) -> None:
        """Load the categories JSON file into memory."""
        try:
            if not os.path.exists(self.categories_file_path):
                print(f"Warning: Categories file not found: {self.categories_file_path}")
                self.categories = []
                return

            with open(self.categories_file_path, 'r', encoding='utf-8') as f:
                self.categories = json.load(f)
                
        except Exception as e:
            print(f"Failed to load categories file: {str(e)}")
            self.categories = []

    def get_categories(self) -> list:
        """Get the loaded categories structure."""
        return self.categories if self.categories else []
        
    def load_file(self, file_path: Optional[str] = None) -> None:
        """Load the JSON file into memory."""
        try:
            # Use default path if none provided
            path_to_load = file_path if file_path else self.file_path
            
            # Check if file exists
            if not os.path.exists(path_to_load):
                # If it doesn't exist, initialize empty DataFrame or raise error
                # For now, let's assume it should exist as per instructions
                raise FileNotFoundError(f"Database file not found: {path_to_load}")

            # Read the JSON file
            with open(path_to_load, 'r', encoding='utf-8') as f:
                data_list = json.load(f)
            
            # Convert to Pandas DataFrame
            self.data = pd.DataFrame(data_list)
            self.file_path = path_to_load
            self.schema_columns = list(self.data.columns)
            
            # Clean the data
            self.clean_data()
            
        except Exception as e:
            raise Exception(f"Failed to load JSON file: {str(e)}")
            
    def clean_data(self) -> None:
        """Clean and prepare the data for display."""
        if self.data is not None:
            # Fill NaN/None values with empty strings
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
            
            # Normalize column names to remove leading/trailing spaces
            self.data.columns = self.data.columns.str.strip()
            
            # Ensure ERP Name column exists and is object dtype
            if 'ERP Name' in self.data.columns:
                if self.data['ERP Name'].dtype != 'object':
                    self.data['ERP Name'] = self.data['ERP Name'].astype('object')
            else:
                import copy
                empty_dict = {'full_name': '', 'type': '', 'part_number': '', 'additional_parameters': ''}
                self.data['ERP Name'] = pd.Series([copy.deepcopy(empty_dict) for _ in range(len(self.data))], dtype='object')
            
            # Ensure core category hierarchy columns exist
            required_columns = [
                'Category', 'Subcategory', 'Sub-subcategory'
            ]
            
            for col in required_columns:
                # Check if column exists (with or without trailing spaces)
                col_exists = any(existing_col.strip() == col.strip() for existing_col in self.data.columns)
                if not col_exists:
                    self.data[col] = ''
            
            # Ensure Image column exists
            image_col_exists = any(existing_col.strip() == 'Image' for existing_col in self.data.columns)
            if not image_col_exists:
                if 'ERP Name' in self.data.columns:
                    erp_name_pos = self.data.columns.get_loc('ERP Name') + 1
                    self.data.insert(erp_name_pos, 'Image', '')
                else:
                    self.data['Image'] = ''
                    
    def save_file(self, file_path: Optional[str] = None, data: Optional[pd.DataFrame] = None) -> None:
        """Save data to a JSON file."""
        try:
            # Use provided data or current data
            save_data = data if data is not None else self.data
            path_to_save = file_path if file_path else self.file_path
            
            if save_data is None:
                raise Exception("No data to save")
                
            # Reverse column renaming for saving to JSON if we want to maintain the JSON schema
            # "ERP name" -> "ERP Name"
            
            # Convert DataFrame to list of dicts
            json_data = save_data.to_dict(orient='records')
            
            # Save to JSON file
            with open(path_to_save, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
            
        except Exception as e:
            raise Exception(f"Failed to save JSON file: {str(e)}")
            
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
        return self.schema_columns if self.schema_columns else []
        
    def get_unique_values(self, column: str) -> list:
        """Get unique values from a specific column."""
        if self.data is not None and column in self.data.columns:
            return self.data[column].unique().tolist()
        return []
    
    def enrich_data(self) -> None:
        """Enrich the data with properties from the categories structure."""
        if self.data is None or not self.categories:
            return
            
        # Create mappings for enrichment
        # (Category, Subcategory, Sub-subcategory) -> {property: value}
        enrichment_map = {}
        
        for category in self.categories:
            cat_name = category.get('category')
            if not cat_name:
                continue
                
            for sub in category.get('subcategories', []):
                sub_name = sub.get('name')
                if not sub_name:
                    continue
                    
                for subsub in sub.get('sub_subcategories', []):
                    subsub_name = subsub.get('name')
                    if not subsub_name:
                        continue
                        
                    key = (cat_name, sub_name, subsub_name)
                    props = {
                        'Stage': subsub.get('stage', ''),
                        'Origin': subsub.get('origin', ''),
                        'Serialized': subsub.get('serialized', ''),
                        'Usage': subsub.get('usage', '')
                    }
                    enrichment_map[key] = props
        
        # Apply enrichment to DataFrame
        # This is iterative and might be slow for large datasets, but robust
        # A vectorized approach would be better if possible
        
        # Initialize new columns if they don't exist
        for col in ['Stage', 'Origin', 'Serialized', 'Usage']:
            if col not in self.data.columns:
                self.data[col] = ''
                
        # Apply values
        # We'll use apply along axis 1, or iterate. Vectorized lookup is tricky with multi-key.
        # Let's use a loop over the map, filtering the dataframe.
        
        for (cat, sub, subsub), props in enrichment_map.items():
            mask = (
                (self.data['Category'] == cat) & 
                (self.data['Subcategory'] == sub) & 
                (self.data['Sub-subcategory'] == subsub)
            )
            
            if mask.any():
                for col, val in props.items():
                    if val:
                        self.data.loc[mask, col] = val

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

    # ------------------------------------------------------------------
    # Added items management
    # ------------------------------------------------------------------
    def load_added_items(self) -> None:
        """Load the temporary file that stores draft items created in the Add tab."""
        try:
            if not os.path.exists(self.added_file_path):
                with open(self.added_file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=4)
                self.added_data = pd.DataFrame(columns=self.get_column_names())
                return

            with open(self.added_file_path, 'r', encoding='utf-8') as f:
                draft_list = json.load(f)

            self.added_data = pd.DataFrame(draft_list)
            if not self.added_data.empty:
                self.added_data = self.added_data.fillna('')
            self._ensure_added_schema()

        except Exception as e:
            print(f"Failed to load added items file: {e}")
            self.added_data = pd.DataFrame(columns=self.get_column_names())

    def save_added_items(self) -> None:
        """Persist the current draft items to disk."""
        try:
            data_to_save = self.added_data if self.added_data is not None else pd.DataFrame()
            json_data = data_to_save.to_dict(orient='records')
            with open(self.added_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save added items: {e}")

    def get_added_data(self) -> pd.DataFrame:
        """Return a copy of the draft items DataFrame."""
        if self.added_data is not None and not self.added_data.empty:
            return self.added_data.copy()
        return pd.DataFrame(columns=self.get_column_names())

    def add_added_item(self, item: Dict[str, Any]) -> None:
        """Append a new draft item to the temporary DataFrame."""
        if self.added_data is None or self.added_data.empty:
            self.added_data = pd.DataFrame(columns=self.get_column_names())

        self._ensure_added_schema()
        self.added_data = pd.concat([self.added_data, pd.DataFrame([item])], ignore_index=True)

    def get_next_available_pn(self) -> int:
        """Return the next unique PN value across both primary and draft data."""
        pn_values = []

        def collect_pn(series: pd.Series):
            if series is None:
                return
            numeric = pd.to_numeric(series, errors='coerce').dropna()
            pn_values.extend(numeric.astype(int).tolist())

        if self.data is not None and 'PN' in self.data.columns:
            collect_pn(self.data['PN'])

        if self.added_data is not None and 'PN' in self.added_data.columns:
            collect_pn(self.added_data['PN'])

        return max(pn_values) + 1 if pn_values else 1

    def get_category_properties(self, category: str, subcategory: str, sub_subcategory: str) -> Dict[str, Any]:
        """Fetch enrichment values for a specific category path."""
        if not self.categories:
            return {}

        for cat in self.categories:
            if cat.get('category') != category:
                continue
            for sub in cat.get('subcategories', []):
                if sub.get('name') != subcategory:
                    continue
                for subsub in sub.get('sub_subcategories', []):
                    if subsub.get('name') != sub_subcategory:
                        continue
                    return {
                        'stage': subsub.get('stage', ''),
                        'origin': subsub.get('origin', ''),
                        'serialized': subsub.get('serialized', ''),
                        'usage': subsub.get('usage', '')
                    }
        return {}

    def _ensure_added_schema(self) -> None:
        """Ensure the draft DataFrame contains the same columns as the main dataset."""
        base_columns = self.get_column_names()
        if not base_columns:
            return

        for column in base_columns:
            if column not in self.added_data.columns:
                self.added_data[column] = ''

