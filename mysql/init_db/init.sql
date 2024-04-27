CREATE DATABASE thuoclongchau;
USE thuoclongchau;

CREATE TABLE Products (
    sku VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    webName VARCHAR(255),
    image VARCHAR(255),
    slug VARCHAR(255),
    ingredients TEXT,
    dosageForm VARCHAR(255),
    brand VARCHAR(255),
    displayCode INT,
    isActive BOOLEAN,
    isPublish BOOLEAN,
    searchScoring FLOAT,
    productRanking INT,
    specification VARCHAR(255)
);

CREATE TABLE Prices (
    id INT PRIMARY KEY,
    productSKU VARCHAR(255),
    measureUnitCode INT,
    measureUnitName VARCHAR(255),
    isSellDefault BOOLEAN,
    price FLOAT,
    currencySymbol VARCHAR(10),
    isDefault BOOLEAN,
    inventory INT,
    isInventory BOOLEAN,
    level INT,
    FOREIGN KEY (productSKU) REFERENCES Products(sku)
);

CREATE TABLE Categories (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    parentName VARCHAR(255),
    slug VARCHAR(255),
    level INT,
    isActive BOOLEAN,
    productSKU VARCHAR(255),
    FOREIGN KEY (productSKU) REFERENCES Products(sku)
);

CREATE TABLE Customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    passowrd VARCHAR(255) NULL,
    is_verified tinyint(1),
    phone VARCHAR(20),
    address VARCHAR(255)
);
CREATE TABLE Orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(id)
);
CREATE TABLE Order_Details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_sku VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(id),
    FOREIGN KEY (product_sku) REFERENCES Products(sku)
);