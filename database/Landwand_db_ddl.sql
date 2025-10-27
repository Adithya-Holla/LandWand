-- =====================================================
-- DATABASE CREATION
-- =====================================================
CREATE DATABASE IF NOT EXISTS landwand_db;
USE landwand_db;

-- =====================================================
-- TABLE: user_account
-- =====================================================
CREATE TABLE user_account (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    join_date DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    buyer TINYINT(1) NOT NULL DEFAULT 0,
    seller TINYINT(1) NOT NULL DEFAULT 0
);

-- =====================================================
-- TABLE: location
-- =====================================================
CREATE TABLE location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pincode VARCHAR(6) NOT NULL,
    landmark VARCHAR(50)
);

-- =====================================================
-- TABLE: property
-- =====================================================
CREATE TABLE property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    property_type VARCHAR(20) NOT NULL,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    posted_date DATE NOT NULL,
    price INT NOT NULL,
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES location(location_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE: listing
-- =====================================================
CREATE TABLE listing (
    listing_id INT AUTO_INCREMENT PRIMARY KEY,
    listing_date DATE NOT NULL,
    listing_status VARCHAR(20) NOT NULL,
    seller_id INT,
    property_id INT,
    FOREIGN KEY (seller_id) REFERENCES user_account(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (property_id) REFERENCES property(property_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE: enquiry
-- =====================================================
CREATE TABLE enquiry (
    enquiry_id INT AUTO_INCREMENT PRIMARY KEY,
    enquiry_date DATE NOT NULL,
    enquiry_status VARCHAR(20) NOT NULL,
    buyer_id INT,
    listing_id INT,
    FOREIGN KEY (buyer_id) REFERENCES user_account(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (listing_id) REFERENCES listing(listing_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE: transaction
-- =====================================================
CREATE TABLE transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_date DATE NOT NULL,
    transaction_amount INT NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    listing_id INT,
    FOREIGN KEY (listing_id) REFERENCES listing(listing_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- =====================================================
-- TABLE: user_transaction
-- =====================================================
CREATE TABLE user_transaction (
    user_id INT NOT NULL,
    transaction_id INT NOT NULL,
    PRIMARY KEY (user_id, transaction_id),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transaction(transaction_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE: property_amenities
-- =====================================================
CREATE TABLE property_amenities (
    amenity_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(255) NOT NULL,
    property_id INT,
    FOREIGN KEY (property_id) REFERENCES property(property_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- TABLE: images
-- =====================================================
CREATE TABLE images (
    images_id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    upload_date DATE NOT NULL,
    property_id INT,
    FOREIGN KEY (property_id) REFERENCES property(property_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- =====================================================
-- INDEXES (optional but improves query speed)
-- =====================================================
CREATE INDEX idx_listing_seller ON listing(seller_id);
CREATE INDEX idx_enquiry_buyer ON enquiry(buyer_id);
CREATE INDEX idx_property_location ON property(location_id);
CREATE INDEX idx_transaction_listing ON transaction(listing_id);
CREATE INDEX idx_images_property ON images(property_id);

-- =====================================================
-- SAMPLE CHECK (optional)
-- =====================================================
SHOW TABLES;
