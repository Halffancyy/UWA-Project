CREATE VIEW CustomerSummary AS
SELECT 
    r.customerId,
    p.modelName,
    SUM(julianday(r.dateBack) - julianday(r.dateOut) + 1) AS daysRented,
    IIF( CAST(substr(r.dateBack, 6, 2) AS INTEGER) >= 7,
        CAST(substr(r.dateBack, 1, 4) AS TEXT) || '/' || CAST(CAST(substr(r.dateBack, 3, 2) AS INTEGER) + 1 AS TEXT),
        CAST(CAST(substr(r.dateBack, 1, 4) AS INTEGER) - 1 AS TEXT) || '/' || CAST(substr(r.dateBack, 3, 2) AS TEXT)
    ) AS taxYear,
    SUM(r.rentalCost) AS rentalCost
FROM 
    rentalContract r
    LEFT JOIN Phone p ON r.IMEI = p.IMEI
WHERE 
    r.dateBack IS NOT NULL
GROUP BY 
    r.customerId, p.modelName, taxYear;