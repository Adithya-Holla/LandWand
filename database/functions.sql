-- 1. Average price by city
DELIMITER //
CREATE FUNCTION get_average_price_by_city(in_city VARCHAR(50))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE avg_price DECIMAL(10,2);
  SELECT AVG(p.price) INTO avg_price
  FROM property p
  JOIN location l ON p.location_id = l.location_id
  WHERE l.city = in_city;
  RETURN IFNULL(avg_price, 0);
END;
//
DELIMITER ;

-- 1.2 Max price by city
DELIMITER //
CREATE FUNCTION get_max_price_by_city(in_city VARCHAR(50))
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE max_price INT;
  SELECT MAX(p.price) INTO max_price
  FROM property p
  JOIN location l ON p.location_id = l.location_id
  WHERE l.city = in_city;
  RETURN IFNULL(max_price, 0);
END;
//
DELIMITER ;

-- 1.3 Min price by city
DELIMITER //
CREATE FUNCTION get_min_price_by_city(in_city VARCHAR(50))
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE min_price INT;
  SELECT MIN(p.price) INTO min_price
  FROM property p
  JOIN location l ON p.location_id = l.location_id
  WHERE l.city = in_city;
  RETURN IFNULL(min_price, 0);
END;
//
DELIMITER ;

-- 1.4 Average price by type
DELIMITER //
CREATE FUNCTION get_average_price_by_type(in_type VARCHAR(20))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE avg_price DECIMAL(10,2);
  SELECT AVG(price) INTO avg_price FROM property WHERE property_type = in_type;
  RETURN IFNULL(avg_price, 0);
END;
//
DELIMITER ;

-- 1.5 Property age
DELIMITER //
CREATE FUNCTION get_property_age(in_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE years_old INT;
  SELECT TIMESTAMPDIFF(YEAR, posted_date, CURDATE()) INTO years_old
  FROM property WHERE property_id = in_id;
  RETURN IFNULL(years_old, 0);
END;
//
DELIMITER ;



-- 2.1 Determine user role
DELIMITER //

CREATE FUNCTION get_user_role(uid INT)
RETURNS VARCHAR(10)
DETERMINISTIC
BEGIN
    DECLARE role VARCHAR(10);

    SELECT CASE
        WHEN buyer = 1 AND seller = 1 THEN 'Both'
        WHEN buyer = 1 THEN 'Buyer'
        WHEN seller = 1 THEN 'Seller'
        ELSE 'Unknown'
    END
    INTO role
    FROM user_account
    WHERE user_id = uid;

    RETURN role;
END;
//

DELIMITER ;

-- 2.2 Total listings by seller
DELIMITER //
CREATE FUNCTION get_total_listings(seller_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM listing WHERE seller_id = seller_id;
  RETURN total;
END;
//
DELIMITER ;

-- 2.3 Total purchases by buyer
DELIMITER //
CREATE FUNCTION get_total_purchases(buyer_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(ut.transaction_id) INTO total
  FROM user_transaction ut
  JOIN transaction t ON ut.transaction_id = t.transaction_id
  WHERE ut.user_id = buyer_id AND t.payment_status = 'Success';
  RETURN total;
END;
//
DELIMITER ;

-- 2.4 Total enquiries by user
DELIMITER //
CREATE FUNCTION get_total_enquiries(uid INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM enquiry WHERE buyer_id = uid;
  RETURN total;
END;
//
DELIMITER ;

-- 2.5 Days since join
DELIMITER //
CREATE FUNCTION get_user_join_days(uid INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE days_since INT;
  SELECT DATEDIFF(CURDATE(), join_date) INTO days_since
  FROM user_account WHERE user_id = uid;
  RETURN IFNULL(days_since, 0);
END;
//
DELIMITER ;


-- 3.1 Enquiries per listing
DELIMITER //

CREATE FUNCTION get_total_enquiries_for_listing(list_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total
    FROM enquiry
    WHERE listing_id = list_id;
    RETURN total;
END;
//

DELIMITER ;


-- 3.2 Pending enquiries
DELIMITER //
CREATE FUNCTION get_pending_enquiries(list_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM enquiry
  WHERE listing_id = list_id AND enquiry_status = 'Pending';
  RETURN total;
END;
//
DELIMITER ;

-- 3.3 Sold % of total listings
DELIMITER //
CREATE FUNCTION get_sold_percentage()
RETURNS DECIMAL(5,2)
DETERMINISTIC
BEGIN
  DECLARE sold_count INT;
  DECLARE total_count INT;
  SELECT COUNT(*) INTO sold_count FROM listing WHERE listing_status = 'Sold';
  SELECT COUNT(*) INTO total_count FROM listing;
  RETURN IFNULL((sold_count / total_count) * 100, 0);
END;
//
DELIMITER ;

-- 3.4 Active listings
DELIMITER //
CREATE FUNCTION get_active_listings_count()
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM listing WHERE listing_status = 'Active';
  RETURN total;
END;
//
DELIMITER ;

-- 3.5 Properties by location
DELIMITER //
CREATE FUNCTION get_total_properties_in_location(loc_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM property WHERE location_id = loc_id;
  RETURN total;
END;
//
DELIMITER ;



-- 4.1 Total site revenue
DELIMITER //

CREATE FUNCTION get_total_revenue()
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
    DECLARE revenue DECIMAL(15,2);
    SELECT SUM(transaction_amount) INTO revenue
    FROM transaction
    WHERE payment_status = 'Success';
    RETURN IFNULL(revenue, 0);
END;
//

DELIMITER ;


-- 4.2 Revenue by seller
DELIMITER //
CREATE FUNCTION get_revenue_by_seller(sid INT)
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
  DECLARE total DECIMAL(15,2);
  SELECT SUM(t.transaction_amount) INTO total
  FROM transaction t
  JOIN listing l ON t.listing_id = l.listing_id
  WHERE l.seller_id = sid AND t.payment_status = 'Success';
  RETURN IFNULL(total, 0);
END;
//
DELIMITER ;

-- 4.3 Revenue by city
DELIMITER //
CREATE FUNCTION get_revenue_by_city(in_city VARCHAR(50))
RETURNS DECIMAL(15,2)
DETERMINISTIC
BEGIN
  DECLARE revenue DECIMAL(15,2);
  SELECT SUM(t.transaction_amount) INTO revenue
  FROM transaction t
  JOIN listing l ON t.listing_id = l.listing_id
  JOIN property p ON l.property_id = p.property_id
  JOIN location x ON p.location_id = x.location_id
  WHERE x.city = in_city AND t.payment_status = 'Success';
  RETURN IFNULL(revenue, 0);
END;
//
DELIMITER ;

-- 4.4 Get transaction status
DELIMITER //
CREATE FUNCTION get_transaction_status(tid INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
  DECLARE status VARCHAR(20);
  SELECT payment_status INTO status FROM transaction WHERE transaction_id = tid;
  RETURN status;
END;
//
DELIMITER ;

-- 4.5 Total transactions
DELIMITER //
CREATE FUNCTION get_total_transactions()
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM transaction;
  RETURN total;
END;
//
DELIMITER ;


-- 5.1 Full address by location
DELIMITER //

CREATE FUNCTION get_full_location(loc_id INT)
RETURNS VARCHAR(200)
DETERMINISTIC
BEGIN
    DECLARE info VARCHAR(200);
    SELECT CONCAT(city, ', ', state, ', ', pincode)
    INTO info
    FROM location
    WHERE location_id = loc_id;
    RETURN info;
END;
//

DELIMITER ;


-- 5.2 Listing duration
DELIMITER //
CREATE FUNCTION get_listing_duration(list_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE days_active INT;
  SELECT DATEDIFF(CURDATE(), listing_date) INTO days_active
  FROM listing WHERE listing_id = list_id;
  RETURN IFNULL(days_active, 0);
END;
//
DELIMITER ;

-- 5.3 Amenity count
DELIMITER //
CREATE FUNCTION get_amenity_count(pid INT)
RETURNS INT
DETERMINISTIC
BEGIN
  DECLARE total INT;
  SELECT COUNT(*) INTO total FROM property_amenities WHERE property_id = pid;
  RETURN total;
END;
//
DELIMITER ;

-- 5.4 Listing status for property
DELIMITER //
CREATE FUNCTION get_property_listing_status(pid INT)
RETURNS VARCHAR(20)
DETERMINISTIC
BEGIN
  DECLARE status VARCHAR(20);
  SELECT listing_status INTO status FROM listing WHERE property_id = pid;
  RETURN status;
END;
//
DELIMITER ;

-- 5.5 Property image URLs (comma-separated)
DELIMITER //
CREATE FUNCTION get_property_images(pid INT)
RETURNS VARCHAR(1000)
DETERMINISTIC
BEGIN
  DECLARE urls VARCHAR(1000);
  SELECT GROUP_CONCAT(image_url SEPARATOR ', ') INTO urls
  FROM images WHERE property_id = pid;
  RETURN IFNULL(urls, 'No images');
END;
//
DELIMITER ;


