# 游戏文档

## 1.跨服相关数据库

### mysql
game_friends #好友数据
### redis
friendReq_ 好友请求
block_ 屏蔽列表
recent_ 最近联系人列表
msg_ 消息列表，只有接受消息

## 2.搭建es服务器

```yaml
services:
  elasticsearch:
    image: m.daocloud.io/docker.elastic.co/elasticsearch/elasticsearch:7.4.0
    container_name: elasticsearch
    restart: always
    environment:
      - xpack.security.enabled=false
      - discovery.type=single-node
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    cap_add:
      - IPC_LOCK
    volumes:
      - ./elasticsearch-data:/usr/share/elasticsearch/data
      - ./plugins:/usr/share/elasticsearch/plugins
    ports:
      - 9200:9200

  kibana:
    container_name: kibana
    image: m.daocloud.io/docker.elastic.co/kibana/kibana:7.4.0
    restart: always
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200    # address of elasticsearch docker container which kibana will connect
    ports:
      - 5601:5601
    depends_on:
      - elasticsearch                                   # kibana will start when elasticsearch has started


```

使用如上docker-compose.yml

从github上下载ik并放入plugins目录下 ./plugins/ik/*

## 3.python 调试方法

1. 在需要调试的时候可以通过guiconsole来执行如下代码监听5678端口

```python
import debugpy
debugpy.listen(('0.0.0.0', 5678))
debugpy.wait_for_client()
```

2. 打开vscode安装python插件，并打开工程目录到assets
3. 点击开始调试按钮并选择 python debugger：remote attach
4. 在打开的launch.json中增加如下配置并修改其中的ip为自己虚拟机

```

    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Remote Attach",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "192.168.10.133",
                "port": 5678
            },
            "env": {
                "PYTHONPATH": "${workspaceFolder}/base"
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        }
    ]
}
```

5. 加断点并开始调试吧