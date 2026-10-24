import os
import pandas as pd
from transformers import pipeline

def run_ai_classification():
    print("🤖 Initializing Hugging Face AI Engine...")
    
    input_path = os.path.join("data", "cleaned_reviews.csv")
    output_path = os.path.join("data", "ai_final_insights.csv")
    
    if not os.path.exists(input_path):
        print("❌ Error: cleaned_reviews.csv not found!")
        return
        
    # Load our clean dataset
    df = pd.read_csv(input_path)
    
    # Take a test batch of 100 rows for rapid evaluation and testing
    print("📊 Extracting test batch of 100 rows for AI evaluation...")
    test_df = df.head(100).copy()
    
    # Load a lightweight, powerful classification pipeline from Hugging Face
    # This model classifies text dynamically without needing extra training data
    classifier = pipeline("zero-shot-classification", model="BART-large-MNLI" if os.environ.get("USE_LARGE") else "typeform/distilbert-base-uncased-mnli")
    
    # Define corporate business tags we want the AI to look for
    candidate_labels = ["Product Quality", "Customer Service", "Delivery Issue", "Billing & Pricing"]
    
    ai_tags = []
    print("⚡ AI is processing text rows and extracting business categories...")
    
    for index, row in test_df.iterrows():
        text = str(row['Review_Text'])
        
        # Pass text to the AI model
        result = classifier(text, candidate_labels)
        
        # Grab the highest-scoring label predicted by the AI
        top_label = result['labels'][0]
        ai_tags.append(top_label)
        
        if (index + 1) % 20 == 0:
            print(f"🔄 Processed {index + 1}/100 rows...")
            
    # Append the AI insights as a new column
    test_df['AI_Predicted_Category'] = ai_tags
    
    # Save to final insights dataset
    test_df.to_csv(output_path, index=False)
    print(f"✅ Success! AI Classification complete. File saved at: {output_path}")

if __name__ == "__main__":
    run_ai_classification()

