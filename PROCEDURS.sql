USE comics_store_db;
select comics.comics_id from user_order inner join comics on comics.comics_id = user_order.comics_id where user_order.user_ord_id = 12; 
 
delimiter $$  

CREATE PROCEDURE update_status_order(in id INT , IN st_id TINYINT )
	BEGIN 
		DECLARE com_id int UNSIGNED DEFAULT null ; 
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL;
			END ;
		START TRANSACTION ; 
			IF (st_id = 3) THEN 
				set com_id = (select comics.comics_id from user_order inner join comics on comics.comics_id = user_order.comics_id where user_order.user_ord_id = id);
                        update order_history set status_id = st_id where order_id = id ; 
                        update order_line set status_id = st_id where order_id = id  ; 
                        update comics set comics_amount = comics_amount + 1 where comics_id = com_id ; 
			ELSE 
				update order_history set status_id = st_id where order_id = id  ; 
                        update order_line set status_id = st_id where order_id = id  ; 
			end if ; 
                  COMMIT; 
	end $$

CREATE PROCEDURE update_COMICS(IN id INT, IN comics_title VARCHAR(50), IN about VARCHAR(1000), IN public DATE,
								IN PRICE DECIMAL(10, 5), in amount int ) 
	BEGIN
      DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL;
			END ; 
                  
	START TRANSACTION ; 
		IF EXISTS(SELECT * FROM comics_store_db.comics WHERE comics_id = id AND title != UPPER(comics_title) )then 
				update comics_store_db.comics set title = UPPER(comics_title), about = about, date_public = public,
								price = PRICE, comics_amount = amount  WHERE comics.comics_id = id;
		ELSEIF EXISTS(SELECT * FROM comics_store_db.comics WHERE comics_id = id) then 
			update comics_store_db.comics set about = about, date_public = public,
								price = PRICE, comics_amount = amount WHERE comics.comics_id = id;
            END IF;
	COMMIT; 
    END$$

   CREATE PROCEDURE update_publisher(IN id INT , IN _name_ VARCHAR(50), IN about VARCHAR(1000)) 
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL; 
			END ; 
		START TRANSACTION ; 
		IF EXISTS(SELECT * FROM comics_store_db.publisher WHERE publisher_id = ID )then 
			update comics_store_db.publisher set about_pub = about, publisher_name = _name_ WHERE publisher_id = id   ;
            END IF; 
            COMMIT; 
    END$$
  CREATE PROCEDURE update_author(IN id INT, IN _name_ VARCHAR(50), IN lastname VARCHAR(50), IN about VARCHAR(1000), IN birth DATE) 
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
					BEGIN 
						ROLLBACK; 
                                    RESIGNAL; 
					END ; 
		START TRANSACTION ; 
			IF EXISTS(SELECT * FROM comics_store_db.author WHERE author_id = id )then 
				update comics_store_db.author set author_name = capitalize(_name_),  author_lastname = capitalize(lastname) , author_birth = birth , about_author = capitalize(about) where author_id = id  ; 
			END IF;
		COMMIT; 
    END$$

    
CREATE PROCEDURE insert_comics_author( in comics_id int UNSIGNED, in author_id int unsigned) 
	BEGIN
		 DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL;
			END ; 
                  
		START TRANSACTION ;
			INSERT INTO comics_author(comics_id, author_id) VALUE (comics_id , author_id) ; 
		COMMIT ;
END $$
		
CREATE PROCEDURE insert_COMICS(IN comics_title VARCHAR(50), IN comics_path TEXT, IN about VARCHAR(1000), IN public DATE,
								IN PRICE DECIMAL(10, 5), IN PUB_ID INT unsigned, in amount int) 
	BEGIN
      DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL;
			END ; 
                  
	START TRANSACTION ; 
		IF NOT EXISTS(SELECT * FROM comics_store_db.comics WHERE title = comics_title )then 
			 INSERT INTO comics_store_db.comics(about, title, path_image, price,date_public, comics_amount)
					VALUE(about, comics_title, comics_path, price, public, amount);
			insert into comics_store_db.comics_publisher(comics_id, publisher_id) value ((select comics_id from comics_store_db.comics where title = comics_title),PUB_ID);
		END IF; 
	COMMIT; 
    END$$
    
CREATE PROCEDURE delete_publisher(IN id INT)
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
				BEGIN 
					ROLLBACK;
                              RESIGNAL; 
				END ; 
		START TRANSACTION ; 
			IF EXISTS(SELECT * FROM comics_store_db.publisher WHERE publisher_id = id)then 
				DELETE FROM comics_store_db.comics_publisher WHERE publisher_id = id ; 
				DELETE FROM comics_store_db.publisher WHERE publisher_id = id; 	
			END IF;
            COMMIT ; 
    END$$

    
CREATE PROCEDURE delete_COMICS(IN id INT)
	BEGIN 
      DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL; 
			END ; 
	START TRANSACTION ; 
		IF EXISTS(SELECT * FROM comics_store_db.comics WHERE comics_id = id)then 
			DELETE FROM comics_store_db.comics_author WHERE comics_id = id ;
                  DELETE FROM comics_store_db.comics_publisher WHERE comics_id = id ;
                  DELETE FROM comics_store_db.comics WHERE comics_id = id ;
		END IF;
	COMMIT;
	END $$

CREATE PROCEDURE delete_author(IN id INT)
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
				BEGIN 
					ROLLBACK; 
                              RESIGNAL; 
				END ; 
		START TRANSACTION ; 
			IF EXISTS(SELECT * FROM comics_store_db.author WHERE author_id = id)then 
				IF EXISTS(SELECT * FROM comics_store_db.comics_author WHERE author_id = id)then 
					delete from comics_store_db.comics_author where author_id = id ; 
                        END IF ;
				DELETE FROM comics_store_db.author WHERE author_id = id;
			END IF;
		COMMIT; 
    END$$
    
CREATE PROCEDURE update_USER(IN old_log VARCHAR(50),IN new_name VARCHAR(50), IN new_lastname VARCHAR(50), IN new_login VARCHAR(50),
							 IN new_email VARCHAR(320), IN new_numb VARCHAR(15), IN new_pass VARCHAR(320))
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL; 
			END ; 
                  
		START TRANSACTION ; 
			IF EXISTS(SELECT * FROM comics_store_db.users WHERE  login = old_log )then 
				UPDATE users set users.user_name = new_name, users.user_lastname = new_lastname, users.login = new_login, users.email = new_email,
					users.user_password = SHA2(new_pass,224), users.user_mobile_phone = new_numb where login = old_log ; 
	
			END IF;
            COMMIT ; 
    END$$

    
CREATE PROCEDURE insert_USER(IN _name_ VARCHAR(50), IN lastname VARCHAR(50), IN user_login VARCHAR(50),
							 IN user_email VARCHAR(320), IN numb VARCHAR(15), IN pass VARCHAR(320)) 
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
            BEGIN 
			ROLLBACK;
                  resignal; 
            END ; 
		START TRANSACTION; 
		IF NOT EXISTS(SELECT * FROM comics_store_db.users WHERE login = user_login)then 
			 insert into comics_store_db.users(user_name, user_lastname, login, email, user_password, user_mobile_phone) 
						value (_name_, lastname, user_login, user_email, SHA2(pass, 224), numb);
			INSERT INTO comics_store_db.user_role value ((SELECT user_id FROM comics_store_db.users WHERE login = user_login ),
										    (select role_id from comics_store_db.roles where role_name = "USER"  ));
		END IF;
            COMMIT; 
    END$$


CREATE PROCEDURE insert_author(IN _name_ VARCHAR(50), IN lastname VARCHAR(50), IN about VARCHAR(1000), IN birth DATE) 
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
					BEGIN 
						ROLLBACK;
                                    RESIGNAL; 
					END ; 
		START TRANSACTION ; 
			IF NOT EXISTS(SELECT * FROM comics_store_db.author WHERE author_name = _name_ AND author_lastname = lastname )then 
				insert into comics_store_db.author(author_name, author_lastname, author_birth, about_author) 
					value (_name_, lastname, birth, about);
			END IF;
		COMMIT; 
    END$$

CREATE PROCEDURE insert_publisher(IN _name_ VARCHAR(50), IN about VARCHAR(1000)) 
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL; 
			END ; 
		START TRANSACTION ; 
		IF NOT EXISTS(SELECT * FROM comics_store_db.publisher WHERE publisher_name = _name_)then 
			INSERT INTO comics_store_db.publisher(publisher_name, about_pub) VALUE (_name_,  about);
            END IF; 
            COMMIT; 
    END$$


CREATE PROCEDURE delete_USER(IN id INT)
	BEGIN
		DECLARE EXIT HANDLER FOR SQLEXCEPTION 
			BEGIN 
				ROLLBACK; 
                        RESIGNAL; 
			END ; 
                  
		START TRANSACTION ; 
			IF EXISTS(SELECT * FROM comics_store_db.users WHERE  user_id = id)then 
				DELETE FROM comics_store_db.users WHERE  user_id = id;
                        DELETE FROM comics_store_db.user_role WHERE  user_id = id;
			END IF;
            COMMIT ; 
    END$$
delimiter ;
    
    
    
 

