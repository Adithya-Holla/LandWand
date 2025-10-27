-- =====================================================
-- ADDITIONAL STORED PROCEDURES FOR API
-- Run this to enable the /api/data/stats endpoint
-- =====================================================

USE landwand_db;

-- Drop procedure if it exists
DROP PROCEDURE IF EXISTS GetDataStats;

-- =====================================================
-- PROCEDURE: GetDataStats
-- Purpose: Get property statistics by type
-- Used by: GET /api/data/stats endpoint
-- =====================================================
DELIMITER $$

CREATE PROCEDURE GetDataStats()
BEGIN
    SELECT 
        property_type,
        COUNT(*) as total_properties,
        AVG(price) as average_price,
        MIN(price) as min_price,
        MAX(price) as max_price,
        SUM(price) as total_value
    FROM property
    GROUP BY property_type
    ORDER BY total_properties DESC;
END$$

DELIMITER ;

-- =====================================================
-- Test the procedure
-- =====================================================
CALL GetDataStats();

-- =====================================================
-- Optional: Add more useful procedures
-- =====================================================

-- Drop procedures if they exist
DROP PROCEDURE IF EXISTS GetUserStats;
DROP PROCEDURE IF EXISTS GetRecentProperties;

-- Procedure: Get user statistics
DELIMITER $$

CREATE PROCEDURE GetUserStats()
BEGIN
    SELECT 
        COUNT(*) as total_users,
        SUM(buyer) as total_buyers,
        SUM(seller) as total_sellers,
        SUM(buyer AND seller) as both_buyer_and_seller,
        MIN(join_date) as first_user_date,
        MAX(join_date) as latest_user_date
    FROM user_account;
END$$

DELIMITER ;

-- Procedure: Get recent properties with location info
DELIMITER $$

CREATE PROCEDURE GetRecentProperties(IN days_back INT)
BEGIN
    SELECT 
        p.property_id,
        p.property_type,
        p.title,
        p.price,
        p.posted_date,
        l.city,
        l.state,
        l.country
    FROM property p
    LEFT JOIN location l ON p.location_id = l.location_id
    WHERE p.posted_date >= DATE_SUB(CURDATE(), INTERVAL days_back DAY)
    ORDER BY p.posted_date DESC;
END$$

DELIMITER ;

-- =====================================================
-- Test all procedures
-- =====================================================
SELECT '=== Testing GetDataStats ===' as Test;
CALL GetDataStats();

SELECT '=== Testing GetUserStats ===' as Test;
CALL GetUserStats();

SELECT '=== Testing GetRecentProperties (30 days) ===' as Test;
CALL GetRecentProperties(30);

-- =====================================================
-- Verify procedures were created
-- =====================================================
SELECT 
    ROUTINE_NAME as procedure_name,
    CREATED as created_date
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = 'landwand_db' 
    AND ROUTINE_TYPE = 'PROCEDURE'
ORDER BY ROUTINE_NAME;
