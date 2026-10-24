drop table if exits ecommerce_ai_insights;
create table ecommerce_ai_insights {
    review_id varchar(50) primary key,
    order_id varchar(50),
    product_id varchar(50),
    product_name varchar(255),
    product_category varchar(100),
    review_text text,
    ai_predicted_category varchar(100)
};
