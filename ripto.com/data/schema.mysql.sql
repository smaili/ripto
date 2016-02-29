-- RT DB & Tables
-- To run:  mysql> \. /<path_to_sql_folder>/schema.mysql.sql

DROP DATABASE IF EXISTS rt;
CREATE DATABASE rt;
USE rt;


-- Users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name TEXT, /* Full name */
    username TEXT, /* Username */
    password TEXT, /* Password */
    email TEXT, /* Email address */
    status INTEGER NOT NULL, /* User's current account status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Memorials
-- Status types: new 1, new 2, new 3, new 4, active, deactive
DROP TABLE IF EXISTS memorials;
CREATE TABLE memorials (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL, /* Who created this memorial */
    name TEXT, /* Full name of the person */
    dob DATETIME, /* Date of birth */
    dod DATETIME, /* Date of death */
    cause INTEGER NOT NULL, /* Cause of death */
    epitaph TEXT, /* Epitaph */
    funeral_type INTEGER, /* Type of funeral */
    funeral_date DATETIME, /* Date of funeral */
    funeral_loc TEXT, /* Location of funeral */
    url TEXT, /* URL */
    condolences INTEGER NOT NULL, /* Total condolences count */
    remembers INTEGER NOT NULL, /* Total remembered count */
    views INTEGER NOT NULL, /* Total view count */
    status INTEGER NOT NULL, /* Memorial's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Media
DROP TABLE IF EXISTS media;
CREATE TABLE media (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    memorial_id INTEGER NOT NULL, /* Which memorial this media file is for */
    media_type INTEGER NOT NULL, /* What type of media file is this */
    filename TEXT, /* The filename of the media */
    status INTEGER NOT NULL, /* Media's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Comments
DROP TABLE IF EXISTS comments;
CREATE TABLE comments (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    memorial_id INTEGER NOT NULL, /* Which memorial this comment is for */
    user_id INTEGER NOT NULL, /* Which user is this comment from */
    text TEXT, /* The comment */
    parent_id INTEGER NOT NULL, /* Implies it is a reply to a comment if > 0 */
    likes INTEGER NOT NULL, /* Total likes count */
    dislikes INTEGER NOT NULL, /* Total dislikes count */
    status INTEGER NOT NULL, /* Comment's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Viewed
DROP TABLE IF EXISTS viewed;
CREATE TABLE viewed (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL, /* Which user viewed */
    ip_addr TEXT, /* IP Address (useful if viewer is not logged in) */
    memorial_id INTEGER NOT NULL, /* Which memorial was viewed */
    status INTEGER NOT NULL, /* Viewed's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Remembered
-- Status types: remembered, unremembered
DROP TABLE IF EXISTS remembered;
CREATE TABLE remembered (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL, /* Which user remembered */
    memorial_id INTEGER NOT NULL, /* Which memorial was remembered */
    status INTEGER NOT NULL, /* Remembered's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Liked
-- Status types: dislike, undo, like
DROP TABLE IF EXISTS liked;
CREATE TABLE liked (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL, /* Which user liked */
    comment_id INTEGER NOT NULL, /* Which comment was liked */
    status INTEGER NOT NULL, /* Liked's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Codes
DROP TABLE IF EXISTS codes;
CREATE TABLE codes (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL, /* Which user this code was created for */
    code_type INTEGER NOT NULL, /* What type of code is this */
    code TEXT, /* The actual code */
    used BOOLEAN, /* Whether or not the code has been used */
    status INTEGER NOT NULL, /* Code's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



-- Flags
-- Flag types: user, comment, memorial, wrong email
DROP TABLE IF EXISTS flags;
CREATE TABLE flags (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    flag_type INTEGER NOT NULL, /* What type of thing was flagged */
    accused_id INTEGER NOT NULL, /* Which thing is being flagged */
    reporter_id INTEGER NOT NULL, /* Which user reported it */
    status INTEGER NOT NULL, /* Flag's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




-- Mail
-- Mail types: invite friend, share memorial, reset password, deactivate user, ban user, confirm email, memorial notification
DROP TABLE IF EXISTS mail;
CREATE TABLE mail (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    mail_type INTEGER NOT NULL, /* What type of mail is it */
    user_id INTEGER NOT NULL, /* Who is it from */
    address INTEGER NOT NULL, /* Where is this mail going */
    status INTEGER NOT NULL, /* Mail's current status */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




-- RTimg
-- Page types: css, js
DROP TABLE IF EXISTS rtimg;
CREATE TABLE rtimg (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    page TEXT, /* Which page */
    css INTEGER NOT NULL, /* CSS file version */
    js INTEGER NOT NULL, /* JS file version */
    created TIMESTAMP DEFAULT '0000-00-00 00:00:00',
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
