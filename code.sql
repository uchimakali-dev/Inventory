-- Inventory schema (generated from inventory.drawio)
-- MySQL 8.0+


USE inventory;

-- ---------------------------------------------------------
-- users
-- ---------------------------------------------------------
CREATE TABLE users (
    id             INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    username       VARCHAR(50)   NOT NULL,
    email          VARCHAR(255)  NOT NULL,
    phone          VARCHAR(20)   NULL,
    hash_password  VARCHAR(255)  NOT NULL,
    user_role      VARCHAR(20)   NOT NULL DEFAULT 'staff',
    created_at     TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_username (username),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- dealers  (one user -> many dealers)
-- ---------------------------------------------------------
CREATE TABLE dealers (
    id           INT UNSIGNED  NOT NULL AUTO_INCREMENT,
    user_id      INT UNSIGNED  NOT NULL,
    dealer_name  VARCHAR(100)  NOT NULL,
    contact_no   VARCHAR(20)   NULL,
    PRIMARY KEY (id),
    KEY idx_dealers_user_id (user_id),
    CONSTRAINT fk_dealers_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------
-- products  (one user -> many products, one dealer -> many products)
-- ---------------------------------------------------------
CREATE TABLE products (
    id             INT UNSIGNED   NOT NULL AUTO_INCREMENT,
    user_id        INT UNSIGNED   NOT NULL,
    dealer_id      INT UNSIGNED   NULL,
    product_name   VARCHAR(150)   NOT NULL,
    quantity       INT UNSIGNED   NOT NULL DEFAULT 0,
    threshold      INT UNSIGNED   NOT NULL DEFAULT 0,   -- low-stock alert level
    cost_price     DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    selling_price  DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    updated_at     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP
                                  ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_products_user_id (user_id),
    KEY idx_products_dealer_id (dealer_id),
    CONSTRAINT fk_products_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT fk_products_dealer
        FOREIGN KEY (dealer_id) REFERENCES dealers (id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB;


-- in dealers
ALTER TABLE dealers
  ADD UNIQUE KEY uq_dealer_owner (id, user_id),
  ADD UNIQUE KEY uq_dealer_name_per_owner (user_id, dealer_name);

ALTER TABLE products
  DROP FOREIGN KEY fk_products_dealer;

ALTER TABLE products
  ADD CONSTRAINT fk_products_dealer
    FOREIGN KEY (dealer_id, user_id) REFERENCES dealers (id, user_id)
    ON UPDATE RESTRICT
    ON DELETE RESTRICT;
-- Optional: list products at or below their low-stock threshold
-- SELECT p.product_name, p.quantity, p.threshold, d.dealer_name
-- FROM products p
-- LEFT JOIN dealers d ON d.id = p.dealer_id
-- WHERE p.quantity <= p.threshold;