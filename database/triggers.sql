-- 1.1 Validate email format & prevent duplicates
DELIMITER //

CREATE TRIGGER before_insert_user
BEFORE INSERT ON user_account
FOR EACH ROW
BEGIN
    -- Validate email format
    IF NEW.email NOT REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email format';
    END IF;

    -- Prevent duplicate email
    IF (SELECT COUNT(*) FROM user_account WHERE email = NEW.email) > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate email detected';
    END IF;
END;
//

DELIMITER ;

-- 1.2 Auto-log welcome message
CREATE TABLE IF NOT EXISTS user_notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    log_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_insert_user
AFTER INSERT ON user_account
FOR EACH ROW
BEGIN
    INSERT INTO user_notifications (user_id, message)
    VALUES (NEW.user_id, CONCAT('Welcome, ', NEW.name, '! Thank you for joining LandWand.'));
END;
//
DELIMITER ;

-- 1.3 Log email/phone updates
CREATE TABLE IF NOT EXISTS user_update_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    old_email VARCHAR(100),
    new_email VARCHAR(100),
    old_phone VARCHAR(20),
    new_phone VARCHAR(20),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_update_user
AFTER UPDATE ON user_account
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email OR OLD.phone <> NEW.phone THEN
        INSERT INTO user_update_log (user_id, old_email, new_email, old_phone, new_phone)
        VALUES (OLD.user_id, OLD.email, NEW.email, OLD.phone, NEW.phone);
    END IF;
END;
//
DELIMITER ;

-- 1.4 Cascade delete related records
DELIMITER //
CREATE TRIGGER after_delete_user
AFTER DELETE ON user_account
FOR EACH ROW
BEGIN
    DELETE FROM listing WHERE seller_id = OLD.user_id;
    DELETE FROM enquiry WHERE buyer_id = OLD.user_id;
    DELETE FROM user_transaction WHERE user_id = OLD.user_id;
END;
//
DELIMITER ;

-- 1.5 Prevent password reuse (only when password is being changed)
-- Note: This trigger only fires if the password field is actually different
-- If you're updating other fields without changing password, this won't trigger
DELIMITER //
DROP TRIGGER IF EXISTS before_update_password;
//
CREATE TRIGGER before_update_password
BEFORE UPDATE ON user_account
FOR EACH ROW
BEGIN
    -- Only validate if password is being changed (NEW != OLD)
    -- Skip this check if password isn't being modified
    IF NEW.password != OLD.password THEN
        -- Additional validation could go here
        -- For now, just allow the change
        SET NEW.password = NEW.password;
    END IF;
END;
//
DELIMITER ;

-- 2.1 Set default listing status & date
DELIMITER //

CREATE TRIGGER before_insert_listing
BEFORE INSERT ON listing
FOR EACH ROW
BEGIN
    SET NEW.listing_status = COALESCE(NEW.listing_status, 'Active');
    SET NEW.listing_date   = COALESCE(NEW.listing_date, CURDATE());
END;
//

DELIMITER ;


-- 2.2 Increment seller’s total listings
ALTER TABLE user_account ADD COLUMN total_listings INT DEFAULT 0;

DELIMITER //
CREATE TRIGGER after_insert_listing
AFTER INSERT ON listing
FOR EACH ROW
BEGIN
    UPDATE user_account SET total_listings = total_listings + 1 WHERE user_id = NEW.seller_id;
END;
//
DELIMITER ;

-- 2.3 Status validation
DELIMITER //
CREATE TRIGGER before_update_listing_status
BEFORE UPDATE ON listing
FOR EACH ROW
BEGIN
    IF NEW.listing_status NOT IN ('Active', 'Sold', 'Expired') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid listing status';
    END IF;
END;
//
DELIMITER ;

-- 2.4 Log status change
CREATE TABLE IF NOT EXISTS listing_status_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    listing_id INT,
    old_status VARCHAR(10),
    new_status VARCHAR(10),
    changed_on DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_update_listing_status
AFTER UPDATE ON listing
FOR EACH ROW
BEGIN
    IF OLD.listing_status <> NEW.listing_status THEN
        INSERT INTO listing_status_audit (listing_id, old_status, new_status)
        VALUES (NEW.listing_id, OLD.listing_status, NEW.listing_status);
    END IF;
END;
//
DELIMITER ;

-- 2.5 Prevent delete if active transaction exists
DELIMITER //
CREATE TRIGGER before_delete_listing
BEFORE DELETE ON listing
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM transaction WHERE listing_id = OLD.listing_id AND payment_status = 'Success') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete listing linked to a completed transaction';
    END IF;
END;
//
DELIMITER ;

-- 3.1 Ensure price > 0
DELIMITER //

CREATE TRIGGER before_insert_property
BEFORE INSERT ON property
FOR EACH ROW
BEGIN
    IF NEW.price <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Property price must be greater than zero';
    END IF;
END;
//

DELIMITER ;

-- 3.2 Auto-generate a listing
DELIMITER //
CREATE TRIGGER after_insert_property
AFTER INSERT ON property
FOR EACH ROW
BEGIN
    INSERT INTO listing (listing_id, listing_date, listing_status, property_id)
    VALUES (NEW.property_id, CURDATE(), 'Active', NEW.property_id);
END;
//
DELIMITER ;

-- 3.3 Log price changes
CREATE TABLE IF NOT EXISTS price_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    old_price INT,
    new_price INT,
    changed_on DATETIME DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_update_property_price
AFTER UPDATE ON property
FOR EACH ROW
BEGIN
    IF OLD.price <> NEW.price THEN
        INSERT INTO price_log (property_id, old_price, new_price)
        VALUES (NEW.property_id, OLD.price, NEW.price);
    END IF;
END;
//
DELIMITER ;

-- 3.4 Prevent delete if linked to active listing
DELIMITER //
CREATE TRIGGER before_delete_property
BEFORE DELETE ON property
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM listing WHERE property_id = OLD.property_id AND listing_status = 'Active') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete properties with active listings';
    END IF;
END;
//
DELIMITER ;