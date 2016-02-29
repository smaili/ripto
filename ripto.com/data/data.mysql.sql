-- RT Data
-- To run:  mysql> \. /<path_to_sql_folder>/data.mysql.sql


-- Users
-- id name username password email status created modified
INSERT INTO users VALUES (1, '', '', '', '', 2, NOW(), NOW());



-- Memorials
-- id user_id name dob dod cause epitaph funeral_type funeral_date funeral_loc url condolences remembers views status created modified
INSERT INTO memorials VALUES (1, 1, '', NOW(), NOW(), 1, '', 1, NOW(), '', '', 0, 0, 0, 3, NOW(), NOW());



-- Media
-- id memorial_id media_type filename created modified
INSERT INTO media VALUES (1, 1, 1, '', NOW(), NOW());



-- Comments
-- id memorial_id user_id text parent_id likes dislikes created modified
INSERT INTO comments VALUES (1, 1, 1, '', 0, 0, 0, NOW(), NOW());
