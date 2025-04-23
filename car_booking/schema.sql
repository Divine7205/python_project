DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS vehicle;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS queries;
DROP TABLE IF EXISTS subscription;
DROP TABLE IF EXISTS testimonial;


CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    isAdmin TEXT NOT NULL,
    username TEXT NOT Null,
    address TEXT NOT NULL,
    img TEXT,
    mimetype TEXT,
    date_of_birth TEXT NOT NULL,
    security_question TEXT NOT NULL,
    security_answer TEXT NOT NULL
);

CREATE TABLE vehicle (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    'image' TEXT NOT NULL,
    mimetype TEXT NOT NULL,
    rent_price INTEGER NOT NULL,
    description TEXT NOT NULL,
    brands TEXT NOT NULL
);

CREATE TABLE brands(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_name TEXT UNIQUE NOT NULL
);

CREATE TABLE booking(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    register TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_use TEXT NOT NULL,
    'status' TEXT NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (id)
);

CREATE TABLE queries(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL
);

CREATE TABLE subscription (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    registered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE testimonial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    body TEXT NOT NULL
);

INSERT INTO user (email, 'password', isAdmin , username, 'address', 'date_of_birth','security_question', 'security_answer') VALUES ("adediv12@gmail.com","scrypt:32768:8:1$NrgtousFLExFVEq3$4498ab2f80672238344741d7d1f05a11232ca824f23802a2d2374c8491de95a2c50ef13e3b254b9192c5afceec19af8ee75425a99152d5e05ddbbd7e63acbcb4","True", "Adegoke Divine","21,samuel road", "02-07-2005", "favorite team", "Barcelona");
