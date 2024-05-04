
INSERT_PRODUCT_QUERY = """
    INSERT INTO Products (sku, name, webName, image, slug, ingredients, dosageForm, brand, displayCode,
                          isActive, isPublish, searchScoring, productRanking, specification)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        webName = VALUES(webName),
        image = VALUES(image),
        slug = VALUES(slug),
        ingredients = VALUES(ingredients),
        dosageForm = VALUES(dosageForm),
        brand = VALUES(brand),
        displayCode = VALUES(displayCode),
        isActive = VALUES(isActive),
        isPublish = VALUES(isPublish),
        searchScoring = VALUES(searchScoring),
        productRanking = VALUES(productRanking),
        specification = VALUES(specification)
"""

INSERT_PRICE_QUERY = """
    INSERT INTO Prices (id, productSKU, measureUnitCode, measureUnitName, isSellDefault, price,
                        currencySymbol, isDefault, inventory, isInventory, level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        measureUnitCode = VALUES(measureUnitCode),
        measureUnitName = VALUES(measureUnitName),
        isSellDefault = VALUES(isSellDefault),
        price = VALUES(price),
        currencySymbol = VALUES(currencySymbol),
        isDefault = VALUES(isDefault),
        inventory = VALUES(inventory),
        isInventory = VALUES(isInventory),
        level = VALUES(level)
"""

INSERT_CATEGORY_QUERY = """
    INSERT INTO Categories (id, name, parentName, slug, level, isActive, productSKU)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        parentName = VALUES(parentName),
        slug = VALUES(slug),
        level = VALUES(level),
        isActive = VALUES(isActive)
"""

GET_ALL_PRODUCTS_QUERY = """
    SELECT p.sku, p.webName, p.image, p.specification, 
           GROUP_CONCAT(pr.price SEPARATOR ';') AS price, 
           pr.currencySymbol,  -- Include currencySymbol in GROUP BY
           GROUP_CONCAT(pr.measureUnitName SEPARATOR ';') AS measureUnitName
    FROM Products p
    JOIN Prices pr ON p.sku = pr.productSKU
    GROUP BY p.sku, pr.currencySymbol;
"""

SEARCH_PRODUCTS_QUERY = """
    SELECT p.sku, p.webName, p.image, p.specification, 
           GROUP_CONCAT(pr.price SEPARATOR ';') AS price, 
           pr.currencySymbol,  -- Include currencySymbol in GROUP BY
           GROUP_CONCAT(pr.measureUnitName SEPARATOR ';') AS measureUnitName
    FROM Products p
    JOIN Prices pr ON p.sku = pr.productSKU
    WHERE p.webName LIKE %s
    GROUP BY p.sku, pr.currencySymbol;
"""