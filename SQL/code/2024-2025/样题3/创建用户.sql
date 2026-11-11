create user 'bike_admin'@'%' identified by '123456';
grant select,insert on bike_data.* to 'bike_admin'@'%';
flush privileges ;