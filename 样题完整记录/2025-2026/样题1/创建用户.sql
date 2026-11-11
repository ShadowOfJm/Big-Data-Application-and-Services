use tree_statistics;

#查看当前 MySQL 服务器状态和版本信息
status;
select version();

#创建两个用户账号：tree_admin（具有所有权限）和 tree_viewer（只具有查询权限）
create user 'tree_admin'@'%' identified by '123456';
grant all privileges on tree_statistics.* to 'tree_admin'@'%';

create user 'tree_viewer'@'%' identified by '123456';
grant select on tree_statistics.* to 'tree_viewer'@'%';

#创建 backup_operator 用户，只授予备份相关的权限（BACKUP_ADMIN 和 RELOAD）
#注：BACKUP_ADMIN 为全局权限，必须授予到 *.*
create user 'backup_operator'@'%' identified by '123456';
grant BACKUP_ADMIN,RELOAD on *.* to 'backup_operator'@'%';

flush privileges;
