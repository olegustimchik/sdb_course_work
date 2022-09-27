use comics_store_db; 
 
delimiter $$ 
CREATE TRIGGER before_update_publisher before update on comics_store_db.publisher for each row 
	begin 
		SET new.publisher_name = capitalize(new.publisher_name);
            set new.about_pub = capitalize(new.about_pub) ; 
      end $$ 
CREATE trigger before_UPDATE_user BEFORE update on comics_store_db.users for each row 
BEGIN 
	SET NEW.user_name = CONCAT(UPPER(LEFT(TRIM(NEW.user_name), 1)), LOWER(SUBSTRING(TRIM(NEW.user_name), 2)));
        SET NEW.user_lastname = CONCAT(UPPER(LEFT(TRIM(NEW.user_lastname), 1)), LOWER(SUBSTRING(NEW.user_lastname, 2)));
        SET NEW.login = TRIM(NEW.login); 
        SET NEW.email = TRIM(NEW.email); 
        SET NEW.user_mobile_phone = TRIM(NEW.user_mobile_phone); 
end $$ 
CREATE TRIGGER before_insert_order 
	BEFORE INSERT ON comics_store_db.user_order FOR EACH ROW 
		BEGIN 
			 SET NEW.customer_name = CONCAT(UPPER(LEFT(TRIM(NEW.customer_name),1)),LOWER(SUBSTRING(TRIM(NEW.				customer_name),2)));
			 SET NEW.customer_lastname = CONCAT(UPPER(LEFT(TRIM(NEW.customer_lastname),1)),LOWER(SUBSTRING(NEW.					customer_lastname,2)));
                   SET NEW.user_address = trim(NEW.user_address);
		END $$ 
CREATE TRIGGER before_insert_comics 
	BEFORE INSERT ON comics_store_db.comics FOR EACH ROW 
      BEGIN 
        SET NEW.title = UPPER(TRIM(NEW.title) );
        SET NEW.about = TRIM(NEW.about);
        SET NEW.path_image = TRIM(NEW.path_image);
	END$$

CREATE TRIGGER before_insert_author
	BEFORE INSERT ON comics_store_db.author FOR EACH ROW 
      BEGIN 
        SET NEW.author_name = CONCAT(UPPER(LEFT(TRIM(NEW.author_name),1)),LOWER(SUBSTRING(TRIM(NEW.author_name),2)));
        SET NEW.author_lastname = CONCAT(UPPER(LEFT(TRIM(NEW.author_lastname),1)),LOWER(SUBSTRING(NEW.author_lastname,2)));
        SET NEW.about_author = TRIM(NEW.about_author);
	END $$

CREATE TRIGGER before_insert_users 
	BEFORE INSERT ON comics_store_db.users FOR EACH ROW 
      BEGIN 
        SET NEW.user_name = CONCAT(UPPER(LEFT(TRIM(NEW.user_name), 1)), LOWER(SUBSTRING(TRIM(NEW.user_name), 2)));
        SET NEW.user_lastname = CONCAT(UPPER(LEFT(TRIM(NEW.user_lastname), 1)), LOWER(SUBSTRING(NEW.user_lastname, 2)));
        SET NEW.login = TRIM(NEW.login); 
        SET NEW.email = TRIM(NEW.email); 
        SET NEW.user_mobile_phone = TRIM(NEW.user_mobile_phone); 
	END$$
 
CREATE TRIGGER before_insert_publisher 
	BEFORE INSERT ON comics_store_db.publisher FOR EACH ROW 
      BEGIN 
		SET NEW.publisher_name = TRIM(NEW.publisher_name) ;
		SET NEW.about_pub = TRIM(NEW.about_pub);
	END$$
delimiter ; 