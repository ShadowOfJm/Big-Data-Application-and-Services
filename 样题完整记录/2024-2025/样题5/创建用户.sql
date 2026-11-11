use bigdata;

create user 'hadoop'@'%' identified by 'Hadoop@2025';
grant select,insert,update on bigdata.* to 'hadoop'@'%';

# 监控专用用户：仅授予 PROCESS 和 SHOW DATABASES 权限
create user 'monitor'@'%' identified by '123456';
grant process on *.* to 'monitor'@'%';
grant show databases on *.* to 'monitor'@'%';

flush privileges;
