create user 'hadoop'@'%' identified by 'qwER12#$';
grant select,insert,delete on *.* to 'hadoop'@'%';
flush privileges;

create user 'hdadmin'@'%' identified by 'qwER12#$';
grant all privileges on hddb.* to 'hdadmin'@'%';
flush privileges;

#查看 hdadmin 用户的权限信息
show grants for 'hdadmin'@'%';
