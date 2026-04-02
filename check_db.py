import sqlite3
import os

db_path = "market_data.db"

# Check if DB file exists
if not os.path.exists(db_path):
    print(f"❌ NO DATABASE FILE: {db_path}")
else:
    print(f"✅ DB exists: {os.path.getsize(db_path)} bytes")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List ALL tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    if tables:
        print("\n✅ TABLES FOUND:")
        for table in tables:
            print(f"  - {table[0]}")
    else:
        print("\n❌ NO TABLES - Run fetching.py first!")
    
    conn.close()