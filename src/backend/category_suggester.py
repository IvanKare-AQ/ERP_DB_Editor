"""
Category Suggester for ERP Database Editor
Provides smart category suggestions based on item characteristics using ML and AI.
"""

from typing import Dict, Any, Optional, List, Tuple
import json
import os
import re
from collections import Counter
import pandas as pd
from src.backend.ollama_handler import OllamaHandler


class CategorySuggester:
    """Provides smart category suggestions for ERP items using ML and AI."""
    
    def __init__(self, ollama_handler: Optional[OllamaHandler] = None, 
                 categories_file_path: Optional[str] = None,
                 json_handler: Optional[Any] = None):
        """Initialize the category suggester.
        
        Args:
            ollama_handler: Optional OllamaHandler instance. If None, creates a new one.
            categories_file_path: Optional path to categories JSON file. If None, uses default.
            json_handler: Optional JsonHandler instance for accessing existing data.
        """
        self.ollama_handler = ollama_handler or OllamaHandler()
        self.json_handler = json_handler
        
        # Determine categories file path
        if categories_file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            categories_file_path = os.path.join(project_root, "data", "airq_categories.json")
        
        self.categories_file_path = categories_file_path
        self._categories = None
        self._category_list = None  # Flattened list for validation
        self._category_patterns = None  # Cached patterns from existing data
    
    def load_categories(self) -> List[Dict[str, Any]]:
        """Load categories from JSON file."""
        if self._categories is not None:
            return self._categories
        
        try:
            if not os.path.exists(self.categories_file_path):
                print(f"Warning: Categories file not found: {self.categories_file_path}")
                self._categories = []
                return []
            
            with open(self.categories_file_path, 'r', encoding='utf-8') as f:
                self._categories = json.load(f)
            
            # Build flattened category list for validation
            self._build_category_list()
            
            return self._categories
        except Exception as e:
            print(f"Error loading categories: {e}")
            self._categories = []
            return []
    
    def _build_category_list(self):
        """Build a flattened list of all valid category paths for validation."""
        if self._categories is None:
            return
        
        self._category_list = []
        for category in self._categories:
            cat_name = category.get('category', '')
            for subcat in category.get('subcategories', []):
                subcat_name = subcat.get('name', '')
                for subsubcat in subcat.get('sub_subcategories', []):
                    subsubcat_name = subsubcat.get('name', '')
                    if cat_name and subcat_name and subsubcat_name:
                        self._category_list.append((cat_name, subcat_name, subsubcat_name))
    
    def _build_category_patterns(self) -> Dict[str, Tuple[str, str, str]]:
        """Build patterns from existing data: type → (category, subcategory, sub-subcategory)."""
        if self._category_patterns is not None:
            return self._category_patterns
        
        if not self.json_handler or not hasattr(self.json_handler, 'data'):
            self._category_patterns = {}
            return self._category_patterns
        
        data = self.json_handler.get_data()
        if data is None or data.empty:
            self._category_patterns = {}
            return self._category_patterns
        
        # Build type → category mapping
        type_to_category = {}
        
        def get_erp_type(erp_obj):
            if isinstance(erp_obj, dict):
                return erp_obj.get('type', '').strip().lower()
            return ''
        
        if 'ERP Name' in data.columns and 'Category' in data.columns:
            for _, row in data.iterrows():
                erp_name = row.get('ERP Name', {})
                erp_type = get_erp_type(erp_name)
                category = str(row.get('Category', '')).strip()
                subcategory = str(row.get('Subcategory', '')).strip()
                sub_subcategory = str(row.get('Sub-subcategory', '')).strip()
                
                if erp_type and category and subcategory and sub_subcategory:
                    if erp_type not in type_to_category:
                        type_to_category[erp_type] = []
                    type_to_category[erp_type].append((category, subcategory, sub_subcategory))
        
        # Find most common category for each type
        self._category_patterns = {}
        for erp_type, categories in type_to_category.items():
            if categories:
                # Count occurrences
                category_counts = Counter(categories)
                most_common = category_counts.most_common(1)[0][0]
                self._category_patterns[erp_type] = most_common
        
        return self._category_patterns
    
    def _find_similar_items(self, type_value: str, part_number: str, details: str, 
                           limit: int = 5) -> List[Tuple[str, str, str, float]]:
        """Find similar items in the database using text similarity.
        
        Returns:
            List of (category, subcategory, sub_subcategory, similarity_score) tuples
        """
        if not self.json_handler or not hasattr(self.json_handler, 'data'):
            return []
        
        data = self.json_handler.get_data()
        if data is None or data.empty:
            return []
        
        # Build search text from input
        search_parts = []
        if type_value:
            search_parts.append(type_value.lower())
        if part_number and part_number != "NO-PN":
            search_parts.append(part_number.lower())
        if details:
            search_parts.append(details.lower())
        
        if not search_parts:
            return []
        
        search_text = ' '.join(search_parts)
        
        # Calculate similarity for each item
        similarities = []
        
        def get_erp_full_text(erp_obj):
            if isinstance(erp_obj, dict):
                parts = []
                if erp_obj.get('type'):
                    parts.append(erp_obj.get('type', '').lower())
                if erp_obj.get('part_number') and erp_obj.get('part_number') != "NO-PN":
                    parts.append(erp_obj.get('part_number', '').lower())
                if erp_obj.get('additional_parameters'):
                    parts.append(erp_obj.get('additional_parameters', '').lower())
                return ' '.join(parts)
            return ''
        
        for _, row in data.iterrows():
            erp_name = row.get('ERP Name', {})
            item_text = get_erp_full_text(erp_name)
            category = str(row.get('Category', '')).strip()
            subcategory = str(row.get('Subcategory', '')).strip()
            sub_subcategory = str(row.get('Sub-subcategory', '')).strip()
            
            if not item_text or not category or not subcategory or not sub_subcategory:
                continue
            
            # Calculate simple similarity (word overlap)
            similarity = self._calculate_similarity(search_text, item_text)
            
            if similarity > 0:
                similarities.append((category, subcategory, sub_subcategory, similarity))
        
        # Sort by similarity and return top matches
        similarities.sort(key=lambda x: x[3], reverse=True)
        return similarities[:limit]
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity score between two texts (0.0 to 1.0)."""
        if not text1 or not text2:
            return 0.0
        
        # Simple word-based similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
        
        # Jaccard similarity (intersection over union)
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        if union == 0:
            return 0.0
        
        jaccard = intersection / union
        
        # Also check for substring matches (for part numbers, etc.)
        substring_bonus = 0.0
        for word1 in words1:
            for word2 in words2:
                if word1 in word2 or word2 in word1:
                    substring_bonus += 0.1
        
        # Combine scores
        similarity = min(1.0, jaccard + substring_bonus * 0.2)
        return similarity
    
    def suggest_category(
        self,
        current_category: Optional[str] = None,
        type_value: Optional[str] = None,
        part_number: Optional[str] = None,
        details: Optional[str] = None,
        model_name: str = "llama3.2",
        model_parameters: Optional[Dict[str, Any]] = None,
        use_ai: bool = True
    ) -> Dict[str, Any]:
        """Suggest category, subcategory, and sub-subcategory for an item.
        
        Uses a hybrid approach:
        1. Pattern matching from existing data (fastest, most accurate)
        2. Similarity matching with existing items (fast, accurate)
        3. AI suggestion as fallback (slower, handles edge cases)
        
        Args:
            current_category: Current category if item already has one (optional)
            type_value: Type field from ERP name (e.g., "Screw", "Bolt")
            part_number: Part number (PN) from ERP name
            details: Additional details/parameters from ERP name
            model_name: Ollama model to use for AI suggestions (if needed)
            model_parameters: Optional model parameters (temperature, etc.)
            use_ai: Whether to use AI as fallback (default: True)
            
        Returns:
            Dictionary with:
            - 'category': Suggested category name
            - 'subcategory': Suggested subcategory name
            - 'sub_subcategory': Suggested sub-subcategory name
            - 'confidence': Confidence level (high/medium/low)
            - 'reasoning': Brief explanation of the suggestion
            - 'valid': Whether the suggestion matches a valid category path
            - 'method': Method used ('pattern', 'similarity', 'ai', or 'none')
        """
        # Load categories for validation
        categories = self.load_categories()
        
        # Method 1: Pattern matching (fastest, most accurate for known types)
        if type_value:
            patterns = self._build_category_patterns()
            type_lower = type_value.strip().lower()
            
            if type_lower in patterns:
                category, subcategory, sub_subcategory = patterns[type_lower]
                valid = self._validate_suggestion(category, subcategory, sub_subcategory)
                
                return {
                    'category': category,
                    'subcategory': subcategory,
                    'sub_subcategory': sub_subcategory,
                    'confidence': 'high',
                    'reasoning': f'Pattern match: Items with type "{type_value}" are typically categorized as {category} > {subcategory} > {sub_subcategory}',
                    'valid': valid,
                    'method': 'pattern'
                }
        
        # Method 2: Similarity matching with existing items
        similar_items = self._find_similar_items(
            type_value or '',
            part_number or '',
            details or '',
            limit=5
        )
        
        if similar_items:
            # Get the most similar item's category
            best_match = similar_items[0]
            category, subcategory, sub_subcategory, similarity_score = best_match
            
            # Count how many similar items have the same category
            matching_count = sum(1 for item in similar_items 
                               if item[0] == category and item[1] == subcategory and item[2] == sub_subcategory)
            
            valid = self._validate_suggestion(category, subcategory, sub_subcategory)
            confidence = 'high' if similarity_score > 0.5 and matching_count >= 2 else 'medium'
            
            reasoning = f'Similarity match: Found {matching_count} similar item(s) with similarity score {similarity_score:.2f}. Most similar items are categorized as {category} > {subcategory} > {sub_subcategory}'
            
            return {
                'category': category,
                'subcategory': subcategory,
                'sub_subcategory': sub_subcategory,
                'confidence': confidence,
                'reasoning': reasoning,
                'valid': valid,
                'method': 'similarity'
            }
        
        # Method 3: AI fallback (only if use_ai is True and we have some input)
        if use_ai and (type_value or part_number or details):
            ai_suggestion = self._suggest_with_ai(
                current_category, type_value, part_number, details,
                model_name, model_parameters
            )
            if ai_suggestion and ai_suggestion.get('category'):
                return ai_suggestion
        
        # No suggestion found
        return {
            'category': current_category or '',
            'subcategory': '',
            'sub_subcategory': '',
            'confidence': 'low',
            'reasoning': 'No matching patterns or similar items found. Please select category manually.',
            'valid': False,
            'method': 'none'
        }
    
    def _suggest_with_ai(
        self,
        current_category: Optional[str],
        type_value: Optional[str],
        part_number: Optional[str],
        details: Optional[str],
        model_name: str,
        model_parameters: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Use AI to suggest category (fallback method)."""
        # Build context string for AI
        context_parts = []
        if current_category:
            context_parts.append(f"Current category: {current_category}")
        if type_value:
            context_parts.append(f"Type: {type_value}")
        if part_number:
            context_parts.append(f"Part number: {part_number}")
        if details:
            context_parts.append(f"Details: {details}")
        
        context = ", ".join(context_parts) if context_parts else "No context provided"
        
        # Build category list for AI reference
        category_reference = self._build_category_reference(self.load_categories())
        
        # Create prompt for category suggestion
        prompt = f"""You are an expert at categorizing industrial components and materials for an ERP system.

Available categories structure:
{category_reference}

Item information:
{context}

Task: Based on the item's type, part number, and details, suggest the most appropriate category path (Category > Subcategory > Sub-subcategory).

IMPORTANT:
- You MUST select category names that EXACTLY match one of the available categories listed above
- The category path must exist in the structure (Category > Subcategory > Sub-subcategory)
- If the current category is provided and seems appropriate, you may suggest keeping it
- If no exact match exists, suggest the closest match from the available categories
- Be precise with category names - use exact spelling and capitalization as shown

Return your response in this exact format (one line per field):
Category: [exact category name from the list above]
Subcategory: [exact subcategory name from the list above]
Sub-subcategory: [exact sub-subcategory name from the list above]
Reasoning: [brief explanation of why this category path was chosen]

Example response:
Category: Hardware
Subcategory: Fasteners
Sub-subcategory: Screws
Reasoning: The item is a screw based on the type and part number, fitting into the Hardware > Fasteners > Screws category."""
        
        try:
            # Check if Ollama is available
            if not self.ollama_handler.is_ollama_running():
                return None
            
            # Generate suggestion using Ollama
            response = self._generate_suggestion(prompt, model_name, model_parameters)
            
            if not response:
                return None
            
            # Parse response
            suggestion = self._parse_suggestion_response(response)
            suggestion['method'] = 'ai'
            
            # Validate suggestion against actual categories
            suggestion['valid'] = self._validate_suggestion(
                suggestion.get('category', ''),
                suggestion.get('subcategory', ''),
                suggestion.get('sub_subcategory', '')
            )
            
            return suggestion
            
        except Exception as e:
            print(f"Error generating AI suggestion: {e}")
            return None
    
    def _build_category_reference(self, categories: List[Dict[str, Any]]) -> str:
        """Build a reference string of available categories for the AI prompt."""
        if not categories:
            return "No categories available"
        
        lines = []
        for cat in categories[:20]:  # Limit to first 20 categories to avoid token limits
            cat_name = cat.get('category', '')
            if not cat_name:
                continue
            
            subcats = []
            for subcat in cat.get('subcategories', [])[:5]:  # Limit subcategories
                subcat_name = subcat.get('name', '')
                if not subcat_name:
                    continue
                
                subsubcats = []
                for subsubcat in subcat.get('sub_subcategories', [])[:5]:  # Limit sub-subcategories
                    subsubcat_name = subsubcat.get('name', '')
                    if subsubcat_name:
                        subsubcats.append(subsubcat_name)
                
                if subsubcats:
                    subcats.append(f"  - {subcat_name}: {', '.join(subsubcats)}")
            
            if subcats:
                lines.append(f"- {cat_name}:")
                lines.extend(subcats)
        
        return "\n".join(lines) if lines else "No categories available"
    
    def _generate_suggestion(self, prompt: str, model_name: str, model_parameters: Optional[Dict[str, Any]] = None) -> str:
        """Generate category suggestion using Ollama."""
        try:
            import requests
            
            # Prepare options
            options = {}
            if model_parameters:
                options.update(model_parameters)
            else:
                # Default parameters for category suggestions
                options = {
                    "temperature": 0.3,  # Lower temperature for more consistent suggestions
                    "top_p": 0.9,
                    "top_k": 40
                }
            
            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": options
            }
            
            response = requests.post(
                f"{self.ollama_handler.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                print(f"Error generating suggestion: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"Error in _generate_suggestion: {e}")
            return ""
    
    def _parse_suggestion_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response to extract category suggestions."""
        suggestion = {
            'category': '',
            'subcategory': '',
            'sub_subcategory': '',
            'confidence': 'medium',
            'reasoning': ''
        }
        
        if not response:
            return suggestion
        
        try:
            # Extract category
            category_match = re.search(r'Category:\s*(.+?)(?:\n|$)', response, re.IGNORECASE | re.MULTILINE)
            if category_match:
                suggestion['category'] = category_match.group(1).strip()
            
            # Extract subcategory
            subcategory_match = re.search(r'Subcategory:\s*(.+?)(?:\n|$)', response, re.IGNORECASE | re.MULTILINE)
            if subcategory_match:
                suggestion['subcategory'] = subcategory_match.group(1).strip()
            
            # Extract sub-subcategory
            sub_subcategory_match = re.search(r'Sub-subcategory:\s*(.+?)(?:\n|$)', response, re.IGNORECASE | re.MULTILINE)
            if sub_subcategory_match:
                suggestion['sub_subcategory'] = sub_subcategory_match.group(1).strip()
            
            # Extract reasoning
            reasoning_match = re.search(r'Reasoning:\s*(.+?)(?:\n\n|\Z)', response, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if reasoning_match:
                suggestion['reasoning'] = reasoning_match.group(1).strip()
            
            # Determine confidence based on completeness
            if suggestion['category'] and suggestion['subcategory'] and suggestion['sub_subcategory']:
                suggestion['confidence'] = 'high'
            elif suggestion['category'] and suggestion['subcategory']:
                suggestion['confidence'] = 'medium'
            else:
                suggestion['confidence'] = 'low'
                
        except Exception as e:
            print(f"Error parsing suggestion response: {e}")
        
        return suggestion
    
    def _validate_suggestion(self, category: str, subcategory: str, sub_subcategory: str) -> bool:
        """Validate that the suggested category path exists in the categories structure."""
        if not category or not subcategory or not sub_subcategory:
            return False
        
        if self._category_list is None:
            self._build_category_list()
        
        if self._category_list is None:
            return False
        
        # Normalize strings for comparison (strip whitespace, case-insensitive)
        category_norm = category.strip().lower()
        subcategory_norm = subcategory.strip().lower()
        sub_subcategory_norm = sub_subcategory.strip().lower()
        
        # Check if the path exists (case-insensitive, with whitespace tolerance)
        for cat, subcat, subsubcat in self._category_list:
            if (cat.strip().lower() == category_norm and
                subcat.strip().lower() == subcategory_norm and
                subsubcat.strip().lower() == sub_subcategory_norm):
                return True
        
        return False
    
    def _find_closest_match(self, category: str, subcategory: str, sub_subcategory: str) -> Optional[Tuple[str, str, str]]:
        """Find the closest matching category path if exact match doesn't exist."""
        if self._category_list is None:
            self._build_category_list()
        
        if not self._category_list:
            return None
        
        category_norm = category.strip().lower()
        subcategory_norm = subcategory.strip().lower()
        sub_subcategory_norm = sub_subcategory.strip().lower()
        
        # Try to find partial matches
        best_match = None
        best_score = 0
        
        for cat, subcat, subsubcat in self._category_list:
            score = 0
            if cat.strip().lower() == category_norm:
                score += 3
            elif category_norm in cat.strip().lower() or cat.strip().lower() in category_norm:
                score += 1
            
            if subcat.strip().lower() == subcategory_norm:
                score += 2
            elif subcategory_norm in subcat.strip().lower() or subcat.strip().lower() in subcategory_norm:
                score += 1
            
            if subsubcat.strip().lower() == sub_subcategory_norm:
                score += 2
            elif sub_subcategory_norm in subsubcat.strip().lower() or subsubcat.strip().lower() in sub_subcategory_norm:
                score += 1
            
            if score > best_score:
                best_score = score
                best_match = (cat, subcat, subsubcat)
        
        # Only return if we have a reasonable match (at least 3 points)
        return best_match if best_score >= 3 else None
    
    def get_all_categories(self) -> List[Tuple[str, str, str]]:
        """Get all valid category paths as a list of tuples (category, subcategory, sub-subcategory)."""
        if self._category_list is None:
            self.load_categories()
            self._build_category_list()
        
        return self._category_list.copy() if self._category_list else []
