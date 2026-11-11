use tourism;

# 备份账户：每天凌晨2点自动备份 tourism 数据库
create user 'tourism_backup'@'localhost' identified by '123456';
# LOCK TABLES / RELOAD / PROCESS 属于全局权限，需授予到 *.*；SELECT 授予到库级
grant select on tourism.* to 'tourism_backup'@'localhost';
grant LOCK TABLES,RELOAD,PROCESS on *.* to 'tourism_backup'@'localhost';
flush privileges;
