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
	menu_price VARCHAR(10) NOT NULL,
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

INSERT INTO store(store_name, category) VALUES ('두릅식당', '한식');

INSERT INTO store(store_name, category) VALUES ('조폭떡볶이', '분식');

INSERT INTO store(store_name, category) VALUES ('미쿡식당', '양식');

INSERT INTO store(store_name, category) VALUES ('내가사케', '일식');

INSERT INTO store(store_name, category) VALUES ('맛이차이나', '중식');


# menu

## 한식
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '불고기', 10000, '불고기.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '비빔밥', 9000, '비빔밥.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '칼국수', 9500, '칼국수.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '된장찌개', 9000, '된장찌개.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '냉면', 10000, '냉면.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (1, '김치찌개', 9000, '김치찌개.jpeg');


## 분식
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (2, '떡볶이', 4000, '떡볶이.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (2, '김밥', 3000, '김밥.jpeg');


## 양식
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (3, '스테이크', 13900, '스테이크.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (3, '파스타', 10900, '파스타.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (3, '햄버거', 6900, '햄버거.jpg');


## 일식
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '초밥', 12000, '초밥.jpg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '우동', 7900, '우동.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '메밀소바', 9900, '메밀소바.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (4, '돈가스', 11000, '돈가스.jpeg');


## 중식
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (5, '볶음밥', 10000, '볶음밥.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (5, '짬뽕', 9000, '짬뽕.jpeg');
INSERT INTO menu(store_id, menu_name, menu_price, menu_img) VALUES (5, '짜장면', 7000, '짜장면.jpeg');