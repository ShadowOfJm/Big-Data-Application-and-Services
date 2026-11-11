# 配置 root 用户允许任意 IP 连接
# MySQL 8 不支持在 grant 语句中设置密码，改由 update user 修改
alter user 'root'@'%' identified by '123456';
grant all privileges on *.* to 'root'@'%';
flush privileges;
