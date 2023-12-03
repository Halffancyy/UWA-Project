CREATE TRIGGER calculate_rentalCost AFTER UPDATE 
ON rentalContract
FOR EACH ROW
WHEN NEW.dateBack IS NOT NULL AND OLD.dateBack IS NULL
BEGIN
    UPDATE rentalContract
    SET rentalCost = (
        SELECT ROUND(pm.baseCost + (pm.dailyCost * (julianday(NEW.dateBack) - julianday(NEW.dateOut) + 1)), 2)
        FROM PhoneModel pm
        JOIN Phone p ON pm.modelNumber = p.modelNumber AND pm.modelName = p.modelName
        WHERE p.IMEI = NEW.IMEI
    )
    WHERE IMEI = NEW.IMEI AND dateOut = NEW.dateOut AND customerID = NEW.customerID;
END;