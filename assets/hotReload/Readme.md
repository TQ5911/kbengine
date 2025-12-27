# 插件使用方法

## 安装

1.打开vscode 或者cursor或者类似编辑器

2.ctrl+shift+p 打开命令面板

3.输入并选择 **“Extensions: Install from VSIX...”**。
  回到hotreload目录安装 vsix插件

## 配置

1.打开config.yaml

```
ServerAddr: "192.168.10.133:20099"
Verbose: true
UDPMode: true
ConfigFile: "config.yaml"
ScriptFile: "temp.py"
ComponentNum: 2
Uid: 1001
```

主要修改服务器为你自己的
ComponentNum配置为你的cell数量+base数量

还有Uid大部分人都是1001

## python环境

执行
```
python -m pip install astor
```

