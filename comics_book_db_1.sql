
use comics_store_db;
CREATE TABLE comics_publisher(
	comics_id int UNSIGNED DEFAULT null , 
      publisher_id int UNSIGNED DEFAULT NULL, 
	FOREIGN KEY (comics_id) REFERENCES comics(comics_id), 
      FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id)); 
      
CREATE TABLE users(
	user_id  INT UNSIGNED NOT NULL AUTO_INCREMENT, 
	user_name VARCHAR(50), 
	user_lastname VARCHAR(50), 
	login VARCHAR(50), 
	email VARCHAR(320), 
	user_password varchar(224),
	user_mobile_phone varchar(15),
	PRIMARY KEY (user_id)); 

CREATE TABLE roles ( 
  role_id TINYINT NOT NULL AUTO_INCREMENT, 
  role_name VARCHAR(50),
  PRIMARY KEY (role_id)); 
  
    
CREATE TABLE user_role (
	user_id INT UNSIGNED, 
	role_id TINYINT , 
    FOREIGN KEY (user_id) REFERENCES users(user_id), 
    FOREIGN KEY (role_id) REFERENCES roles(role_id));     
 
 CREATE TABLE author(
    author_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    author_name VARCHAR(50),
    author_lastname VARCHAR(50), 
    author_birth DATE, 
    about_author VARCHAR(1000), 
    PRIMARY KEY (author_id)); 
    
 CREATE TABLE publisher( 
    publisher_id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    publisher_name VARCHAR(50), 
    about_pub VARCHAR(1000), 
    PRIMARY KEY (publisher_id)); 
    
CREATE TABLE comics(
    comics_id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    publisher_id INT UNSIGNED,
    date_public DATE, 
    price DECIMAL(10, 5), 
    title VARCHAR(50),
    about VARCHAR(1000),
    path_image TEXT DEFAULT NULL,
    FOREIGN KEY (publisher_id) REFERENCES publisher(publisher_id), 
    PRIMARY KEY (comics_id)); 
    
CREATE TABLE comics_author(
    comics_id INT UNSIGNED, 
    author_id INT UNSIGNED, 
    FOREIGN KEY (comics_id) REFERENCES comics(comics_id), 
    FOREIGN KEY (author_id) REFERENCES author(author_id)); 
    

CREATE TABLE user_order( 
    user_ord_id INT UNSIGNED NOT NULL AUTO_INCREMENT, 
    user_id INT UNSIGNED, 
    order_date DATE , 
    user_address varchar(500),
    PRIMARY KEY (user_ord_id) , 
    FOREIGN KEY (user_id) REFERENCES users(user_id)); 
    
CREATE TABLE status_order(
	status_id TINYINT UNSIGNED NOT NULL , 
      _status_ VARCHAR(40), 
	PRIMARY KEY (status_id));
      
CREATE TABLE order_line( 
    line_id INT NOT NULL AUTO_INCREMENT , 
    order_id INT UNSIGNED, 
    comics_id INT UNSIGNED, 
    price DECIMAL(10, 5), 
    status_id TINYINT UNSIGNED ,  
    PRIMARY KEY (line_id), 
    FOREIGN KEY (comics_id) REFERENCES comics(comics_id),
    FOREIGN KEY (order_id) REFERENCES user_order(user_ord_id),
    FOREIGN KEY (status_id) REFERENCES status_order(status_id)); 
    
CREATE TABLE order_history(
	history_id INT UNSIGNED NOT NULL AUTO_INCREMENT , 
    order_id INT UNSIGNED, 
    status_id TINYINT UNSIGNED , 
    PRIMARY KEY(history_id),
    foreign key (order_id) references user_order(user_ord_id),
    foreign key (status_id) references status_order(status_id));
	
    


	
	
    
    
    
	
    













