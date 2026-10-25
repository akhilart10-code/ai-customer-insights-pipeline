import os
import sqlite3
import pandas as pd

def run_database_loader():
    print("Initializing Relational Database Loader...")
    
    csv_path = os.path.join("data", "ai_final_insights.csv")
    schema_path = os.path.join("sql", "schema.sql")
    db_path = os.path.join("data", "corporate_insights.db")
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found! Please run the AI script first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Executing SQL schema and building relational table architecture...")
    with open(schema_path, "r") as sql_file:
        sql_script = sql_file.read()
    cursor.executescript(sql_script)
    conn.commit()
    
    print("Performing bulk data upload to database table...")
    df = pd.read_csv(csv_path)
    
    db_columns = [
        'Review_ID', 'Order_ID', 'Customer_ID', 'Product_ID', 
        'Product_Name', 'Product_Category', 'Review_Text', 'AI_Predicted_Category'
    ]
    
    upload_df = df[db_columns].copy()
    upload_df.columns = [col.lower() for col in db_columns]

    upload_df.to_sql("ecommerce_ai_insights", conn, if_exists="append", index=False)
    conn.commit()
    
    print("Running SQL verification query...")
    cursor.execute("SELECT COUNT(*) FROM ecommerce_ai_insights;")
    row_count = cursor.fetchone()[0]
    
    print(f"Success! Relational database populated. Table contains {row_count} rows.")
    
    conn.close()

if __name__ == "__main__":
    run_database_loader()
