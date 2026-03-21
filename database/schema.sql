CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100),
    color VARCHAR(50)
);

-- Example data
INSERT INTO products (name, category, brand, color) VALUES
('Nike Air Shoes', 'Shoes', 'Nike', 'Black'),
('Adidas Running Shoes', 'Shoes', 'Adidas', 'White'),
('Puma Sneakers', 'Shoes', 'Puma', 'Black'),
('Nike Hoodie', 'Clothing', 'Nike', 'Black'),
('Adidas T-shirt', 'Clothing', 'Adidas', 'White'),
('Puma Jacket', 'Clothing', 'Puma', 'Blue');
