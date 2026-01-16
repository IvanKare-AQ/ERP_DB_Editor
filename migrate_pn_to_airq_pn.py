"""
Migration script to rename 'PN' column to 'AirQ_PN' in component_database.json
"""

import json
import os
import shutil
from datetime import datetime

def migrate_pn_to_airq_pn():
    """Rename 'PN' column to 'AirQ_PN' in component_database.json"""
    
    # Determine paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_file = os.path.join(current_dir, "data", "component_database.json")
    backup_file = os.path.join(current_dir, "data", f"component_database.json.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    print(f"Starting migration: PN -> AirQ_PN")
    print(f"Database file: {db_file}")
    
    # Check if file exists
    if not os.path.exists(db_file):
        print(f"Error: Database file not found: {db_file}")
        return False
    
    # Create backup
    print(f"Creating backup: {backup_file}")
    shutil.copy2(db_file, backup_file)
    
    # Load JSON file
    print("Loading database...")
    with open(db_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print("Error: Expected JSON array")
        return False
    
    # Count items
    total_items = len(data)
    print(f"Found {total_items} items")
    
    # Rename column in each item
    renamed_count = 0
    for item in data:
        if isinstance(item, dict) and 'PN' in item:
            item['AirQ_PN'] = item.pop('PN')
            renamed_count += 1
    
    print(f"Renamed 'PN' to 'AirQ_PN' in {renamed_count} items")
    
    # Save updated JSON
    print("Saving updated database...")
    with open(db_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Migration completed successfully!")
    print(f"Backup saved to: {backup_file}")
    return True

if __name__ == "__main__":
    try:
        success = migrate_pn_to_airq_pn()
        if success:
            print("\n✓ Migration successful")
        else:
            print("\n✗ Migration failed")
    except Exception as e:
        print(f"\n✗ Error during migration: {str(e)}")
        import traceback
        traceback.print_exc()
