DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS modules;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS tests;
CREATE TABLE users(
	userid uuid NOT NULL,
	usern VARCHAR,
	pass VARCHAR,
	email VARCHAR,
	PRIMARY KEY (userid)
);

CREATE TABLE modules (
	moduleid uuid NOT NULL,
	name VARCHAR,
	year int NOT NULL,
	code VARCHAR,
	mark float,
	userid uuid NOT NULL,
	PRIMARY KEY (moduleid)
);

CREATE TABLE assignments (
    assignid uuid NOT NULL,
    name VARCHAR,
    description VARCHAR,
    duedate TIMESTAMP,
    userid UUID NOT NULL,
	moduleid UUID NOT NULL,
    mark FLOAT,
	weighting FLOAT,
    PRIMARY KEY (assignid)
);

CREATE TABLE tests(
	testid uuid NOT NULL,
	name VARCHAR,
	date TIMESTAMP,
	userid uuid NOT NULL,
	moduleid uuid NOT NULL,
	mark FLOAT,
	weighting FLOAT

);
