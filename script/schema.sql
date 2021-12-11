CREATE TABLE test.covid(
    id int primary key auto_increment,
	province_state varchar(100),
	country_region varchar(100),
	lat real,
	lon real,
	date datetime,
	count int,
	category varchar(100)
);
