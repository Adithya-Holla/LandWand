-- 3. Enquiry Management
DELIMITER //

CREATE PROCEDURE make_enquiry(IN buyer INT, IN list_id INT)
BEGIN
  INSERT INTO enquiry (enquiry_date, enquiry_status, buyer_id, listing_id)
  VALUES (CURDATE(), 'Pending', buyer, list_id);
END;
//

CREATE PROCEDURE update_enquiry_status(IN eid INT, IN status VARCHAR(10))
BEGIN
  UPDATE enquiry SET enquiry_status = status WHERE enquiry_id = eid;
END;
//

CREATE PROCEDURE delete_enquiry(IN eid INT)
BEGIN
  DELETE FROM enquiry WHERE enquiry_id = eid;
END;
//

CREATE PROCEDURE get_enquiries_by_buyer(IN bid INT)
BEGIN
  SELECT * FROM enquiry WHERE buyer_id = bid;
END;
//

CREATE PROCEDURE get_enquiries_for_seller(IN sid INT)
BEGIN
  SELECT e.*
  FROM enquiry e
  JOIN listing l ON e.listing_id = l.listing_id
  WHERE l.seller_id = sid;
END;
//

CREATE PROCEDURE auto_close_old_enquiries()
BEGIN
  UPDATE enquiry
  SET enquiry_status = 'Closed'
  WHERE enquiry_status = 'Pending' AND DATEDIFF(CURDATE(), enquiry_date) > 30;
END;
//

DELIMITER ;

-- 4. Transaction Management
DELIMITER //

CREATE PROCEDURE record_transaction(IN lid INT, IN amt DECIMAL(10,2), IN buyer INT)
BEGIN
  INSERT INTO `transaction` (transaction_date, transaction_amount, payment_status, listing_id)
  VALUES (CURDATE(), amt, 'Pending', lid);
  
  SET @tid = LAST_INSERT_ID();
  INSERT INTO user_transaction (user_id, transaction_id) VALUES (buyer, @tid);
END;
//

CREATE PROCEDURE update_payment_status(IN tid INT, IN status VARCHAR(10))
BEGIN
  UPDATE `transaction` SET payment_status = status WHERE transaction_id = tid;
END;
//

CREATE PROCEDURE get_transaction_details(IN tid INT)
BEGIN
  SELECT * FROM `transaction` WHERE transaction_id = tid;
END;
//

CREATE PROCEDURE get_transactions_by_user(IN uid INT)
BEGIN
  SELECT t.*
  FROM `transaction` t
  JOIN user_transaction ut ON t.transaction_id = ut.transaction_id
  WHERE ut.user_id = uid;
END;
//

CREATE PROCEDURE generate_monthly_sales_report(IN month INT, IN year INT)
BEGIN
  SELECT MONTH(transaction_date) AS Month, SUM(transaction_amount) AS TotalSales
  FROM `transaction`
  WHERE YEAR(transaction_date) = year AND MONTH(transaction_date) = month
  GROUP BY MONTH(transaction_date);
END;
//

CREATE PROCEDURE calculate_total_revenue()
BEGIN
  SELECT SUM(transaction_amount) AS TotalRevenue
  FROM `transaction` WHERE payment_status = 'Success';
END;
//

CREATE PROCEDURE get_top_selling_cities(IN lim INT)
BEGIN
  SELECT l.city, SUM(t.transaction_amount) AS TotalSales
  FROM `transaction` t
  JOIN listing li ON t.listing_id = li.listing_id
  JOIN property p ON li.property_id = p.property_id
  JOIN location l ON p.location_id = l.location_id
  WHERE t.payment_status = 'Success'
  GROUP BY l.city
  ORDER BY TotalSales DESC
  LIMIT lim;
END;
//

DELIMITER ;

-- 5. Analytics & Reporting
DELIMITER //

CREATE PROCEDURE get_citywise_price_summary()
BEGIN
  SELECT l.city, AVG(price) AS AvgPrice, MIN(price) AS MinPrice, MAX(price) AS MaxPrice
  FROM property p JOIN location l ON p.location_id = l.location_id
  GROUP BY l.city;
END;
//

CREATE PROCEDURE get_seller_performance_report()
BEGIN
  SELECT u.user_id, u.name,
         COUNT(DISTINCT l.listing_id) AS TotalListings,
         COUNT(DISTINCT e.enquiry_id) AS TotalEnquiries,
         SUM(t.transaction_amount) AS TotalSales
  FROM user_account u
  LEFT JOIN listing l ON u.user_id = l.seller_id
  LEFT JOIN enquiry e ON l.listing_id = e.listing_id
  LEFT JOIN `transaction` t ON l.listing_id = t.listing_id
  GROUP BY u.user_id;
END;
//

CREATE PROCEDURE get_buyer_activity_report()
BEGIN
  SELECT u.user_id, u.name,
         COUNT(DISTINCT e.enquiry_id) AS TotalEnquiries,
         COUNT(DISTINCT ut.transaction_id) AS Purchases
  FROM user_account u
  LEFT JOIN enquiry e ON u.user_id = e.buyer_id
  LEFT JOIN user_transaction ut ON u.user_id = ut.user_id
  GROUP BY u.user_id;
END;
//

CREATE PROCEDURE get_site_overview()
BEGIN
  SELECT 
    (SELECT COUNT(*) FROM listing WHERE listing_status='Active') AS ActiveListings,
    (SELECT COUNT(*) FROM user_account) AS Users,
    (SELECT COUNT(*) FROM `transaction`) AS Transactions;
END;
//

CREATE PROCEDURE get_property_full_details(IN pid INT)
BEGIN
  SELECT p.*, l.city, l.state, GROUP_CONCAT(pa.name SEPARATOR ', ') AS Amenities
  FROM property p
  JOIN location l ON p.location_id = l.location_id
  LEFT JOIN property_amenities pa ON p.property_id = pa.property_id
  WHERE p.property_id = pid
  GROUP BY p.property_id;
END;
//

CREATE PROCEDURE get_unsold_properties_report()
BEGIN
  SELECT p.* FROM property p
  JOIN listing l ON p.property_id = l.property_id
  WHERE l.listing_status <> 'Sold';
END;
//

CREATE PROCEDURE get_recently_sold_properties(IN days INT)
BEGIN
  SELECT p.*, t.transaction_date
  FROM property p
  JOIN listing l ON p.property_id = l.property_id
  JOIN `transaction` t ON l.listing_id = t.listing_id
  WHERE t.payment_status = 'Success'
    AND DATEDIFF(CURDATE(), t.transaction_date) <= days;
END;
//

CREATE PROCEDURE get_properties_with_no_enquiries()
BEGIN
  SELECT p.*
  FROM property p
  LEFT JOIN listing l ON p.property_id = l.property_id
  LEFT JOIN enquiry e ON l.listing_id = e.listing_id
  WHERE e.enquiry_id IS NULL;
END;
//

DELIMITER ;

-- 6. Maintenance & Admin
DELIMITER //

CREATE PROCEDURE archive_old_listings()
BEGIN
  CREATE TABLE IF NOT EXISTS listing_archive LIKE listing;
  INSERT INTO listing_archive SELECT * FROM listing WHERE DATEDIFF(CURDATE(), listing_date) > 365;
  DELETE FROM listing WHERE DATEDIFF(CURDATE(), listing_date) > 365;
END;
//

CREATE PROCEDURE purge_deleted_users()
BEGIN
  DELETE FROM user_account
  WHERE user_id NOT IN (SELECT DISTINCT seller_id FROM listing WHERE seller_id IS NOT NULL);
END;
//

CREATE PROCEDURE reset_demo_data()
BEGIN
  DELETE FROM enquiry;
  DELETE FROM `transaction`;
  UPDATE property SET price = price * 0.9;
  UPDATE listing SET listing_status = 'Active';
END;
//

CREATE PROCEDURE recalculate_all_stats()
BEGIN
  UPDATE user_account u
  SET total_listings = (SELECT COUNT(*) FROM listing WHERE seller_id = u.user_id);
END;
//

DELIMITER ;
