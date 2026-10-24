import os
import sqlite3
import pandas as pd

def run_database_loader():
    print("Initializing Relational Database Loader...")
    
    # Define file paths
    csv_path = os.path.join("data", "ai_final_insights.csv")
    schema_path = os.path.join("sql", "schema.sql")
    db_path = os.path.join("data", "corporate_insights.db")
    
    # Check if AI insights file exists
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found! Please run the AI script first.")
        return

    # 1. Connect to the SQLite Database (creates file automatically)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. Read and execute the SQL Schema Blueprint
    print("Executing SQL schema and building relational table architecture...")
    with open(schema_path, "r") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    
    # 3. Load the data using Pandas and push it to SQL
    print("Performing bulk data upload to database table...")
    df = pd.read_csv(csv_path)
    
    # Map CSV column names exactly to our SQL schema columns
    db_columns = [
        'Review_ID', 'Order_ID', 'Customer_ID', 'Product_ID', 
        'Product_Name', 'Product_Category', 'Review_Text', 'AI_Predicted_Category'
    ]
    
    # Ensure we filter for just these columns and rename them to match SQL lowercase
    upload_df = df[db_columns].copy()
    upload_df.columns = [col.lower() for col in db_columns]
    
    # Push data to the SQLite table
    upload_df.to_sql("ecommerce_ai_insights", conn, if_exists="append", index=False)
    conn.commit()
    
    # 4. Verification Step (Prove the data is inside SQL)
    print("Running SQL verification query...")
    cursor.execute("SELECT COUNT(*) FROM ecommerce_ai_insights;")
    row_count = cursor.fetchone()[0]
    
    print(f"Success! Relational database populated. Table contains {row_count} rows.")
    
    # Close connection securely
    conn.close()

if __name__ == "__main__":
    run_database_loader()
