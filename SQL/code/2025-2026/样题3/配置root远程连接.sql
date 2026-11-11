# 配置 root 用户允许任意 IP 连接
use mysql;
update user set host = '%' where user = 'root';
flush privileges;
