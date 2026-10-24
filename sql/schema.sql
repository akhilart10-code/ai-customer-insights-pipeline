DROP TABLE IF EXISTS ecommerce_ai_insights;

CREATE TABLE ecommerce_ai_insights (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    product_category VARCHAR(100),
    review_text TEXT,
    ai_predicted_category VARCHAR(100)
);
