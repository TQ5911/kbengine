# KBE Hot Reloader 使用说明

## 插件概述

KBE Hot Reloader 是一款专为 KBE（Knowledge Based Engine）游戏服务器开发的 VS Code 插件，用于热重载 Python 脚本。

## 功能特性

- **一键热重载**: 在 Python 函数上右键即可触发热重载
- **智能代码解析**: 使用 VS Code 符号提供器 API 准确识别类和函数
- **智能路径解析**: 自动解析 assets 目录和脚本名称
- **多组件支持**: 支持 Base 和 Cell 组件的热重载
- **层级信息显示**: 显示文件→类→函数的完整层级结构
- **容错机制**: 当符号提供器不可用时自动回退到正则解析

## 使用方法

### 基础操作

1. **打开 Python 文件**: 在 VS Code 中打开 KBE 脚本文件
2. **右键点击函数**: 在函数定义行右键
3. **选择热重载类型**:
   - `Base`: Base 组件热重载
   - `Cell`: Cell 组件热重载
   - `取消`: 取消操作

### 自动检测逻辑

插件会根据文件路径自动检测组件类型：
- 文件路径包含 `cell` 目录 → 自动识别为 Cell 组件
- 文件路径包含 `base` 目录 → 自动识别为 Base 组件
- 其他情况 → 弹出选择窗口让用户选择

## 工作原理

### 路径解析示例

```
输入路径: e:\shsvn\h1_trunk\Dev\Server\kbeLinux\kbengine\assets\scripts\cell\impTask.py

解析结果:
- assetsDir: e:\shsvn\h1_trunk\Dev\Server\kbeLinux\kbengine\assets
- scriptName: impTask
```

### 命令执行

执行格式：
```
genhotfix.bat [componentType] [scriptName] [className] [functionName]
```

参数说明：
| 参数 | 值 | 说明 |
|------|-----|------|
| componentType | cellapp / baseapp | 根据热重载类型确定 |
| scriptName | impTask | 脚本名称（不含 .py 扩展名）|
| className | ImpTask / None | 类名，如果没有则为 None |
| functionName | onTimer | 函数名 |

### 执行示例

对于 `ImpTask.onTimer` 函数在 `cell` 目录下：
```
genhotfix.bat cellapp impTask ImpTask onTimer
```

## 项目结构

```
src/
├── extension.ts        # 主扩展文件，入口点
├── commandExecutor.ts  # 命令行执行模块
├── pythonParser.ts     # Python 解析模块（符号解析 + 回退正则解析）
├── types.ts            # 类型定义和上下文封装类
└── utils.ts            # 工具函数
```

## 技术实现

### 代码解析流程

1. **调用 VS Code 符号提供器**: 使用 `vscode.executeDocumentSymbolProvider` 获取文档结构
2. **定位函数位置**: 在符号树中查找光标位置对应的函数
3. **获取层级信息**: 提取文件路径、类名、函数名
4. **失败回退**: 符号提供器不可用时，使用正则表达式解析

### 符号解析优势

- 准确识别嵌套类和方法
- 支持异步处理
- 提供完整的代码结构信息

### 正则回退机制

当 VS Code 符号提供器不可用时，插件自动使用正则表达式解析：
- 匹配 `class (\w+)` 定义类
- 匹配 `def (\w+)` 定义函数
- 按行扫描定位光标位置

## 适用场景

- KBE 游戏服务器开发
- Python 脚本热更新
- 游戏逻辑调试和测试

## 安装与打包

### 开发调试

```bash
# 安装依赖
npm install

# 编译项目
npm run compile

# 启动调试 (F5)
```

### 打包发布

```bash
# 编译并打包
npm run build

# 或分步执行
npm run compile
vsce package
```

## 热重载流程图

```
┌─────────────────────────────────────┐
│      用户右键点击函数定义行           │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│   解析获取: 文件路径、类名、函数名     │
└──────────────┬──────────────────────┘
               ▼
┌─────────────────────────────────────┐
│   检查路径是否包含 cell/base 目录     │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
  ┌─────────┐    ┌─────────────┐
  │ 包含    │    │ 不包含      │
  └────┬────┘    └──────┬──────┘
       │                │
       ▼                ▼
  ┌─────────────┐  ┌─────────────────┐
  │ 自动识别    │  │ 弹出选择对话框   │
  │ cell/base  │  │ Base/Cell/取消   │
  └──────┬──────┘  └────────┬────────┘
         │                 │
         └────────┬────────┘
                  ▼
┌─────────────────────────────────────┐
│   调用 genhotfix.bat 执行热重载      │
└─────────────────────────────────────┘
```

## 注意事项

1. 确保 `genhotfix.bat` 文件位于 `{assetsDir}\hotReload\` 目录下
2. 光标需要在函数定义行上才能正确识别
3. 仅支持 Python 文件（`.py`）
4. Windows 平台使用 cmd.exe 执行命令