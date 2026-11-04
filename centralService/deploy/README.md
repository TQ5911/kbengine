# 使用方法
先修改下 /etc/ansible/hosts
使其中的tmp可访问
最好测试下
ansible tmp -m ping
然后修改下deploy.env中的数据库和redis
然后执行下面这个命令

```
bash install.sh --ansible --skip-build
```
