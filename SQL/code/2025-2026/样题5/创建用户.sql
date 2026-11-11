create user 'hadoop'@'%' identified by 'Hadoop@2025';
grant select,insert,update on bigdata.* to 'hadoop'@'%';

#注：PROCESS 与 SHOW DATABASES 均为全局权限，必须授予到 *.*
create user 'monitor'@'%' identified by 'Monitor@2025';
grant PROCESS,SHOW DATABASES on *.* to 'monitor'@'%';

flush privileges;
show grants for 'hadoop'@'%';
show grants for 'monitor'@'%';
