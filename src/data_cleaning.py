import os
import pandas as pd

def run_data_cleaning():
    print("🚀 Running Clean Data Pipeline for E-Commerce Dataset...")
    
    input_path = os.path.join("data", "messy_reviews.csv")
    output_path = os.path.join("data", "cleaned_reviews.csv")
    
    if not os.path.exists(input_path):
        print("❌ Error: data/messy_reviews.csv not found!")
        return
        
    # Load the dataset
    df = pd.read_csv(input_path, low_memory=False)
    print(f"📋 Initial Row Count: {len(df)}")
    
    # 1. Drop rows where the review text is empty or missing
    print("🧹 Filtering out missing or null text entries...")
    df = df.dropna(subset=['Review_Text'])
    
    # 2. Standarize strings and strip empty spaces
    df['Review_Text'] = df['Review_Text'].astype(str).str.strip()
    df['Product_Name'] = df['Product_Name'].fillna("Unknown Product").astype(str).str.strip()
    
    # 3. Save the clean tabular structure
    df.to_csv(output_path, index=False)
    print(f"✅ Success! Cleaned dataset saved at: {output_path} (Final rows: {len(df)})")

if __name__ == "__main__":
    run_data_cleaning()
