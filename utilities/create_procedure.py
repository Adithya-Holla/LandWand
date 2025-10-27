"""
Create GetDataStats stored procedure
Run this to enable /api/data/stats endpoint and reach 100% test success
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.db_config import get_db_connection, close_db_connection

def create_procedure():
    """Create the GetDataStats stored procedure"""
    
    connection = None
    cursor = None
    
    try:
        print("🔌 Connecting to database...")
        connection = get_db_connection()
        
        if not connection:
            print("❌ Failed to connect to database")
            return False
        
        cursor = connection.cursor()
        
        # Drop procedure if exists
        print("🗑️  Dropping old procedure if exists...")
        cursor.execute("DROP PROCEDURE IF EXISTS GetDataStats")
        
        # Create new procedure
        print("✨ Creating GetDataStats stored procedure...")
        procedure_sql = """
        CREATE PROCEDURE GetDataStats()
        BEGIN
            SELECT 
                property_type,
                COUNT(*) as total_properties,
                AVG(price) as average_price,
                MIN(price) as min_price,
                MAX(price) as max_price,
                SUM(price) as total_value
            FROM property
            GROUP BY property_type
            ORDER BY total_properties DESC;
        END
        """
        
        cursor.execute(procedure_sql)
        connection.commit()
        
        print("✅ Stored procedure created successfully!")
        
        # Test the procedure
        print("\n🧪 Testing the procedure...")
        cursor.callproc('GetDataStats')
        
        for result in cursor.stored_results():
            rows = result.fetchall()
            columns = result.column_names
            
            print(f"\n📊 Results ({len(rows)} rows):")
            print("-" * 80)
            print(f"{'Property Type':<15} {'Count':<10} {'Avg Price':<15} {'Min':<15} {'Max':<15}")
            print("-" * 80)
            
            for row in rows:
                print(f"{str(row[0]):<15} {str(row[1]):<10} {str(row[2]):<15} {str(row[3]):<15} {str(row[4]):<15}")
        
        print("\n🎉 Success! The /api/data/stats endpoint will now work!")
        print("\n🚀 Run 'python test_live_api.py' to verify 100% success rate!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            close_db_connection(connection)

if __name__ == "__main__":
    print("="*80)
    print("  🔧 CREATING STORED PROCEDURE: GetDataStats")
    print("="*80)
    print()
    
    success = create_procedure()
    
    print()
    print("="*80)
    
    if success:
        print("✅ PROCEDURE CREATION COMPLETE!")
    else:
        print("❌ PROCEDURE CREATION FAILED")
    
    print("="*80)
    
    sys.exit(0 if success else 1)
