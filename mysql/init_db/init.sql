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
