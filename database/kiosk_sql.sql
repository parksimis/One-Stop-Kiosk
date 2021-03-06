# CREATE TABLE
CREATE TABLE if NOT EXISTS user(
	user_id INT(20) AUTO_INCREMENT,
	age_segment INT(4) NULL, 
	emotion INT(4) NULL,
	sex INT(4) NULL,
	capture_chk CHAR(2) NOT NULL DEFAULT 'Y',
	last_modify DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (user_id)
) ENGINE=InnoDB DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;


CREATE TABLE if NOT EXISTS store(
	store_id INT(20) AUTO_INCREMENT,
	store_name VARCHAR(20) NOT NULL, 
	category VARCHAR(20) NOT NULL,
	last_modify DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (store_id)
) ENGINE=InnoDB DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;


CREATE TABLE menu (
	menu_id INT(20) NOT NULL AUTO_INCREMENT,
	store_id INT(20) NOT NULL,
	menu_name VARCHAR(20) NOT NULL,
	menu_price INT(30) NOT NULL,
	menu_img VARCHAR(50) NOT NULL,
	last_modify DATETIME NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
	created_at DATETIME NULL DEFAULT current_timestamp(),
	PRIMARY KEY (menu_id),
	FOREIGN KEY (store_id) REFERENCES store(store_id) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;


CREATE TABLE if NOT EXISTS orders(
	order_id INT(20) AUTO_INCREMENT,
	user_id INT(20) NOT NULL,
	total_qty INT(10) NOT NULL,
	total_price INT(30) NOT NULL,
	last_modify DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (order_id),
	FOREIGN KEY(user_id) REFERENCES user(user_id) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;


CREATE TABLE if NOT EXISTS order_details(
	order_detail_id INT(10) AUTO_INCREMENT,
	order_id INT(20) NOT NULL,
	user_id INT(20) NOT NULL,
	menu_id INT(20) NOT NULL,
	store_id INT(20) NOT NULL,
	food_qty INT(10) NOT NULL,
	food_price INT(30) NOT NULL,
	last_modify DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (order_detail_id),
	FOREIGN KEY (order_id) REFERENCES orders(order_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES orders(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (store_id) REFERENCES store(store_id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;


CREATE TABLE if NOT EXISTS cart(
	cart_id INT(10) AUTO_INCREMENT,
	user_id INT(20) NOT NULL,
	store_id INT(20) NOT NULL,
	menu_id INT(20) NOT NULL,
	menu_name VARCHAR(20) NOT NULL,
	menu_qty INT(10) NOT NULL,
	menu_price INT(30) NOT NULL,
	last_modify DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP(),
	PRIMARY KEY (cart_id)
) ENGINE=InnoDB DEFAULT CHARACTER SET UTF8 COLLATE UTF8_GENERAL_CI;



# store
## INSERT 

INSERT INTO store(store_name, category) VALUES ('????????????', '??????');

INSERT INTO store(store_name, category) VALUES ('???????????????', '??????');

INSERT INTO store(store_name, category) VALUES ('????????????', '??????');

INSERT INTO store(store_name, category) VALUES ('????????????', '??????');

INSERT INTO store(store_name, category) VALUES ('???????????????', '??????');


# menu

## ??????
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '?????????', 10000, '?????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '?????????', 9000, '?????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '?????????', 9500, '?????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '????????????', 9000, '????????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '??????', 10000, '??????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '????????????', 9000, '????????????.jpeg');


## ??????
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (2, '?????????', 4000, '?????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (2, '??????', 3000, '??????.jpeg');


## ??????
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (3, '????????????', 13900, '????????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (3, '?????????', 10900, '?????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (3, '?????????', 6900, '?????????.jpg');


## ??????
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '??????', 12000, '??????.jpg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '??????', 7900, '??????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '????????????', 9900, '????????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '?????????', 11000, '?????????.jpeg');


## ??????
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (5, '?????????', 10000, '?????????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (5, '??????', 9000, '??????.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (5, '?????????', 7000, '?????????.jpeg');