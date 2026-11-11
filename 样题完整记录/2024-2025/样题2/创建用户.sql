create user 'eduadmin'@'%' identified by '123456';
grant select on education.* to 'eduadmin'@'%';
flush privileges;