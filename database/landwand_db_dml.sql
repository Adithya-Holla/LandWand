USE landwand_db;

-- =====================================================
-- INSERT INTO user_account
-- =====================================================
INSERT INTO user_account (join_date, name, email, password, phone, buyer, seller) VALUES
('2025-01-15', 'Arjun Mehta', 'arjun.mehta@example.com', 'pass123', '9876543210', 1, 0),
('2025-02-10', 'Priya Sharma', 'priya.sharma@example.com', 'pass234', '9876501234', 1, 1),
('2025-02-28', 'Rohit Singh', 'rohit.singh@example.com', 'pass345', '9988776655', 0, 1),
('2025-03-05', 'Neha Kapoor', 'neha.kapoor@example.com', 'pass456', '9123456789', 1, 0),
('2025-03-15', 'Vikram Patel', 'vikram.patel@example.com', 'pass567', '9345678901', 1, 1),
('2025-03-21', 'Simran Yadav', 'simran.yadav@example.com', 'pass678', '9789054321', 1, 0),
('2025-04-01', 'Aditya Rao', 'aditya.rao@example.com', 'pass789', '9988771122', 0, 1),
('2025-04-10', 'Kavita Nair', 'kavita.nair@example.com', 'pass890', '9765432109', 1, 0),
('2025-04-20', 'Suresh Gupta', 'suresh.gupta@example.com', 'pass901', '9654321234', 0, 1),
('2025-04-25', 'Meenakshi Iyer', 'meenakshi.iyer@example.com', 'pass012', '9543210987', 1, 0);

-- =====================================================
-- INSERT INTO location
-- =====================================================
INSERT INTO location (city, country, state, pincode, landmark) VALUES
('Mumbai', 'India', 'Maharashtra', '400001', 'Gateway of India'),
('Delhi', 'India', 'Delhi', '110001', 'India Gate'),
('Bengaluru', 'India', 'Karnataka', '560001', 'MG Road'),
('Chennai', 'India', 'Tamil Nadu', '600001', 'Marina Beach'),
('Pune', 'India', 'Maharashtra', '411001', 'Shaniwarwada'),
('Hyderabad', 'India', 'Telangana', '500001', 'Charminar'),
('Kolkata', 'India', 'West Bengal', '700001', 'Howrah Bridge'),
('Ahmedabad', 'India', 'Gujarat', '380001', 'Sabarmati Ashram'),
('Jaipur', 'India', 'Rajasthan', '302001', 'Hawa Mahal'),
('Lucknow', 'India', 'Uttar Pradesh', '226001', 'Bara Imambara');

-- =====================================================
-- INSERT INTO property
-- =====================================================
INSERT INTO property (property_type, title, description, posted_date, price, location_id) VALUES
('Apartment', '2BHK Sea View', 'Modern sea-facing apartment', '2025-05-01', 9500000, 1),
('Villa', 'Luxury Villa', 'Spacious villa with pool', '2025-05-02', 25000000, 2),
('Flat', 'Affordable 1BHK', 'Ideal for singles/couples', '2025-05-05', 4500000, 3),
('House', '3BHK Independent House', 'Corner plot with garden', '2025-05-06', 12000000, 4),
('Duplex', 'Stylish Duplex', 'Comes with car park', '2025-05-10', 15000000, 5),
('Apartment', 'Smart Home', 'Fully automated apartment', '2025-05-12', 11000000, 6),
('Villa', 'Green Villa', 'Eco-friendly villa near park', '2025-05-15', 18000000, 7),
('Flat', 'Studio Flat', 'Compact fully furnished unit', '2025-05-16', 3500000, 8),
('Apartment', 'Lakeview Apartment', 'Prime location property', '2025-05-18', 7500000, 9),
('Villa', 'Heritage Villa', 'Classic architecture', '2025-05-20', 20000000, 10);

-- =====================================================
-- INSERT INTO listing
-- =====================================================
INSERT INTO listing (listing_date, listing_status, seller_id, property_id) VALUES
('2025-06-01', 'Active', 3, 1),
('2025-06-02', 'Active', 9, 2),
('2025-06-03', 'Active', 3, 3),
('2025-06-04', 'Inactive', 7, 4),
('2025-06-05', 'Active', 9, 5),
('2025-06-06', 'Sold', 7, 6),
('2025-06-07', 'Active', 3, 7),
('2025-06-08', 'Active', 9, 8),
('2025-06-09', 'Pending', 7, 9),
('2025-06-10', 'Active', 3, 10);

-- =====================================================
-- INSERT INTO enquiry
-- =====================================================
INSERT INTO enquiry (enquiry_date, enquiry_status, buyer_id, listing_id) VALUES
('2025-06-15', 'Open', 1, 1),
('2025-06-16', 'Closed', 4, 2),
('2025-06-17', 'Open', 6, 3),
('2025-06-18', 'Open', 8, 4),
('2025-06-19', 'Closed', 10, 5),
('2025-06-20', 'Open', 1, 6),
('2025-06-21', 'Pending', 4, 7),
('2025-06-22', 'Closed', 6, 8),
('2025-06-23', 'Open', 8, 9),
('2025-06-24', 'Closed', 10, 10);

-- =====================================================
-- INSERT INTO transaction
-- =====================================================
INSERT INTO transaction (transaction_date, transaction_amount, payment_status, listing_id) VALUES
('2025-07-01', 9500000, 'Completed', 1),
('2025-07-02', 25000000, 'Completed', 2),
('2025-07-03', 4500000, 'Pending', 3),
('2025-07-04', 12000000, 'Completed', 4),
('2025-07-05', 15000000, 'Refunded', 5),
('2025-07-06', 11000000, 'Completed', 6),
('2025-07-07', 18000000, 'Pending', 7),
('2025-07-08', 3500000, 'Completed', 8),
('2025-07-09', 7500000, 'Completed', 9),
('2025-07-10', 20000000, 'Pending', 10);

-- =====================================================
-- INSERT INTO user_transaction
-- =====================================================
INSERT INTO user_transaction (user_id, transaction_id) VALUES
(1, 1), (4, 2), (6, 3), (8, 4), (10, 5),
(1, 6), (4, 7), (6, 8), (8, 9), (10, 10);

-- =====================================================
-- INSERT INTO property_amenities
-- =====================================================
INSERT INTO property_amenities (name, type, property_id) VALUES
('Swimming Pool', 'Luxury', 1),
('Gym', 'Health', 2),
('Garden', 'Outdoor', 3),
('Lift', 'Convenience', 4),
('Parking', 'Utility', 5),
('Solar Power', 'Sustainability', 6),
('Club House', 'Recreation', 7),
('24x7 Security', 'Safety', 8),
('Play Area', 'Recreation', 9),
('Backup Power', 'Utility', 10);

-- =====================================================
-- INSERT INTO images
-- =====================================================
INSERT INTO images (image_url, file_type, upload_date, property_id) VALUES
('src/propsrc/prop_img/property1.jpg', 'jpg', '2025-05-01', 1),
('src/prop_img/property2.png', 'jpg', '2025-05-02', 2),
('src/prop_img/property3.jpg', 'jpg', '2025-05-03', 3),
('src/prop_img/property4.jpg', 'jpg', '2025-05-04', 4),
('src/prop_img/property5.png', 'jpg', '2025-05-05', 5),
('src/prop_img/property6.jpg', 'jpg', '2025-05-06', 6),
('src/prop_img/property7.png', 'jpg', '2025-05-07', 7),
('src/prop_img/property8.jpg', 'jpg', '2025-05-08', 8),
('src/prop_img/property9.jpg', 'jpg', '2025-05-09', 9),
('src/prop_img/property10.png', 'jpg', '2025-05-10', 10);
