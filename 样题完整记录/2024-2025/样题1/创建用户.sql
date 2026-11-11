create user 'house_admin'@'%' identified by '123456';
grant all privileges on house_market.* to 'house_admin'@'%';

create user  'house_viewer'@'%' identified by '123456';
grant select on house_market.* to 'house_viewer'@'%';

create user 'backup_user'@'%' identified by '123456';
# BACKUP_ADMIN 与 RELOAD 均为全局权限，必须授予到 *.*
grant BACKUP_ADMIN,RELOAD on *.* to 'backup_user'@'%';