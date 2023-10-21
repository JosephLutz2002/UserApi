DROP TABLE IF EXISTS users;

CREATE TABLE users(
	userid uuid NOT NULL,
	usern VARCHAR,
	pass VARCHAR,
	email VARCHAR,
	PRIMARY KEY (userid)
);

CREATE TABLE token_tbl (
	refresh_token VARCHAR NOT NULL
);