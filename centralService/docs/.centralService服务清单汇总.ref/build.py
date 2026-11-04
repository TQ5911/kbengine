# -*- coding: utf-8 -*-
"""centralService 服务清单汇总 xlsx 生成脚本（记录型清单表，商务蓝）"""
import math
from datetime import date

try:
    import openpyxl
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "openpyxl>=3.1.0"])
    import openpyxl

from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = "F:/shsvn/h1/Dev/tools/centralService/docs/centralService服务清单汇总.xlsx"


def xl_color(css_hex: str) -> str:
    value = css_hex.removeprefix("#").upper()
    if len(value) != 6:
        raise ValueError(f"Expected #RRGGBB, got: {css_hex}")
    return "FF" + value


XL_PRIMARY = xl_color("#4472C4")   # 表头背景
XL_TITLE_BG = xl_color("#D9E2F3")  # 标题浅底
XL_TITLE_FG = xl_color("#2F5597")  # 标题深蓝字
XL_BAND = xl_color("#F2F6FC")      # 隔行浅蓝
XL_BORDER = xl_color("#BFBFBF")
XL_NOTE_FG = xl_color("#7F7F7F")

FONT_NAME = "微软雅黑"
thin_side = Side(style="thin", color=XL_BORDER)
BORDER = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

wb = openpyxl.Workbook()
wb.properties.title = "centralService 服务清单汇总"


def disp_units(s: str) -> int:
    """估算显示宽度：CJK 记 2，ASCII 记 1"""
    return sum(2 if ord(c) > 127 else 1 for c in s)


def est_height(pairs, min_h=22.0):
    """pairs: [(text, col_width)]，按换行后的行数估行高"""
    lines = 1
    for text, width in pairs:
        for seg in str(text).split("\n"):
            lines = max(lines, math.ceil(disp_units(seg) / max(1, width - 2)))
    return max(min_h, lines * 15.0 + 5.0)


def style_title(ws, ncols, text, row=1):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name=FONT_NAME, size=14, bold=True, color=XL_TITLE_FG)
    c.fill = PatternFill("solid", fgColor=XL_TITLE_BG)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[row].height = 30


def style_header(ws, headers, row=2):
    for i, h in enumerate(headers, start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(name=FONT_NAME, size=10, bold=True, color="FFFFFFFF")
        c.fill = PatternFill("solid", fgColor=XL_PRIMARY)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    ws.row_dimensions[row].height = 24


# ============================================================
# Sheet 1: 服务总览
# ============================================================
ws1 = wb.active
ws1.title = "服务总览"

HEADERS1 = ["序号", "服务名", "功能说明", "监听端口及用途", "调试端口",
            "MySQL（地址/库名）", "Redis", "下游依赖", "探活端口",
            "systemd 单元", "日志文件", "备注"]
WIDTHS1 = [6, 16, 34, 40, 13, 24, 20, 28, 15, 32, 15, 36]
for i, w in enumerate(WIDTHS1, start=1):
    ws1.column_dimensions[get_column_letter(i)].width = w

style_title(ws1, len(HEADERS1), "centralService 服务清单总览（12 个服务，均为 Go 静态二进制）")
style_header(ws1, HEADERS1)

SERVICES = [
    # (服务名, 功能, 监听端口, 调试, MySQL, Redis, 下游, 探活, 日志, 备注)
    ("centralLogin", "登录网关：客户端接入、对游戏服指令转发、IDIP 接口",
     "2020 客户端接入（clientServiceAddr）\n2030 游戏服指令（gameServerServiceAddr）\n8999 IDIP HTTP（idipHttpServer）",
     "8989", "127.0.0.1:3306 / login", "192.168.10.12:6379",
     "游戏服（serverList.json，如 192.168.11.118:20013）\nqueueServer（192.168.11.118:7999）",
     "2020,2030,8999", "login.log",
     "serverList.json 维护游戏服/排队服列表；fakeSDKServer 为联调测试工具，非服务进程"),
    ("queueServer", "排队与限流：登录排队、在线人数与请求限流",
     "4396 HTTP（httpServer）", "8989", "无", "192.168.10.12:6379",
     "—", "4396", "queue.log",
     "serverList.json：maxOnlineNum=3000，limitPerSecond=11"),
    ("router", "路由与集群同步：游戏服接入、router 集群服务发现",
     "2060 游戏服接入（gameServerServiceAddr）\n2061 集群同步（routerClusterAddr，advertise 192.168.10.133:2061）",
     "8989", "无", "192.168.10.12:6379",
     "—", "2060,2061", "router.log",
     "集群化改造见 src/router/router集群化改造PRD.md"),
    ("maple", "大区/分区（zone）基础数据服务：游戏服/分区列表、KV、合服映射，对外 HTTP JSON API",
     "9527 HTTP API（httpAddr）", "8989", "127.0.0.1:3306 / maple",
     "无", "—", "9527", "maple.log",
     "表：maple/maple_zone/maple_kv/maple_merge_server；写接口需 HMAC-SHA256 签名；被 admin/auction/dropServer/leaseServer 经 mapleHttpAddr 调用；API 文档 src/maple/docs/maple_api.md"),
    ("auction", "拍卖行：挂单、成交、拍卖行聊天与公示",
     "2010 游戏服接入（gameServerServiceAddr）", "8989",
     "127.0.0.1:3306 / auction", "127.0.0.1:6379",
     "maple（HTTP 127.0.0.1:9527）", "2010", "auction.log",
     "gmLogServerId=10001；gmBuyInterception=0"),
    ("orderService", "订单与支付：游戏内购订单、支付回调、订单数据加密",
     "2011 游戏服接入（gameServerServiceAddr）\n8888 HTTP API（httpAddr）",
     "无", "127.0.0.1:3306 / transaction", "127.0.0.1:6379",
     "—", "2011,8888", "orderService.log",
     "HTTP 接口需 apiSecret 签名；payNotifyApi 支付回调；orderDataSecret 数据加密"),
    ("allianceService", "公会（联盟）服务：公会数据、成员与日志",
     "2150 服务端口（allianceServiceAddr）", "9900",
     "127.0.0.1:3306 / allianceDB", "无", "—", "2150", "alliance.log", "—"),
    ("leaseServer", "装备租赁：租赁挂单、状态流转与超时清理",
     "2015 游戏服接入（GameServerServiceAddr）", "9393",
     "127.0.0.1:3306 / lease", "127.0.0.1:6379",
     "maple（HTTP 192.168.10.13:9527）", "2015", "lease.log",
     "RateLimit r=50/b=80；PendingStatusTimeout=60s；CleanIntervalHours=6"),
    ("dropServer", "掉落结算：怪物/宝箱掉落计算与发放",
     "2120 服务端口（dropServerAddr）", "8989",
     "127.0.0.1:3306 / dropDB", "无",
     "maple（HTTP 127.0.0.1:9527）", "2120", "drop.log", "—"),
    ("crossDataServer", "跨服数据：跨服玩法数据存储与同步",
     "2140 服务端口（crossDataServerAddr）", "8989",
     "127.0.0.1:3306 / crossDataDB", "无", "—", "2140", "crossData.log", "—"),
    ("crossTeamServer", "跨服队伍：跨服组队、crusade 并发控制",
     "2016 服务端口（crossTeamServerAddr）", "8990",
     "无", "127.0.0.1:6379", "—", "2016", "crossTeam.log",
     "workerNum=16，crusadeMaxConcurrent=100；reportAddr=22016 疑似配置异常（其余服务为企业微信 webhook）"),
    ("admin", "GMT 后台：GM 工具、HTTP API/SDK、grpc-web、游戏服与机器管理",
     "8080 HTTP API（httpAPIAddress）\n8081 HTTP SDK（httpSDKAddress）\n2040 游戏服管理（addressForGameServer）\n2050 GMT grpc-web 入口（addressForGMT）\n2051 gRPC（AddreesForGRPC）\n20099 机器管理（MachinePort）",
     "9292", "无", "192.168.10.12:6379",
     "maple（HTTP 192.168.10.13:9527）\ncentralLogin IDIP（localhost:8999）",
     "8080,8081,2040,2050,2051", "admin.log",
     "启动顺序最后；MachinePort 用于 TCP 探测游戏服机器"),
]

r = 3
for idx, (name, func, ports, debug, mysql, redis, dep, probe, log, note) in enumerate(SERVICES, start=1):
    unit = f"centralsvc-{name}.service"
    vals = [idx, name, func, ports, debug, mysql, redis, dep, probe, unit, log, note]
    for col, v in enumerate(vals, start=1):
        c = ws1.cell(row=r, column=col, value=v)
        c.font = Font(name=FONT_NAME, size=10)
        c.border = BORDER
        if col in (1, 5, 9):  # 序号/调试/探活居中
            c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        elif col in (2,):
            c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            c.font = Font(name=FONT_NAME, size=10, bold=True)
        else:
            c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        if idx % 2 == 0:
            c.fill = PatternFill("solid", fgColor=XL_BAND)
    ws1.row_dimensions[r].height = est_height(
        [(func, WIDTHS1[2]), (ports, WIDTHS1[3]), (mysql, WIDTHS1[5]),
         (redis, WIDTHS1[6]), (dep, WIDTHS1[7]), (note, WIDTHS1[11])])
    r += 1

note_row = r
ws1.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=len(HEADERS1))
nc = ws1.cell(row=note_row, column=1,
              value=f"数据来源：bin/<服务名>/<服务名>.json、deploy/instances.conf、src/ 源码；生成日期 {date.today().isoformat()}；"
                    f"安装与部署详见「说明」页")
nc.font = Font(name=FONT_NAME, size=9, italic=True, color=XL_NOTE_FG)
nc.alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[note_row].height = 18

ws1.freeze_panes = "C3"
ws1.auto_filter.ref = f"A2:{get_column_letter(len(HEADERS1))}{note_row - 1}"
ws1.page_setup.orientation = "landscape"
ws1.page_setup.fitToWidth = 1
ws1.page_setup.fitToHeight = 0
ws1.sheet_properties.pageSetUpPr.fitToPage = True

# ============================================================
# Sheet 2: 端口速查
# ============================================================
ws2 = wb.create_sheet("端口速查")
HEADERS2 = ["端口", "服务", "用途", "绑定地址", "协议/说明"]
WIDTHS2 = [8, 18, 46, 16, 16]
for i, w in enumerate(WIDTHS2, start=1):
    ws2.column_dimensions[get_column_letter(i)].width = w

style_title(ws2, len(HEADERS2), "端口速查（按端口号排序，含对端地址）")
style_header(ws2, HEADERS2)

PORTS = [
    (20013, "游戏服（外部对端）", "centralLogin serverList.json 配置的游戏服", "192.168.11.118", "TCP/外部"),
    (20099, "admin", "机器管理端口（TCP 探测游戏服机器）", "0.0.0.0", "TCP"),
    (2010, "auction", "游戏服接入（gameServerServiceAddr）", "0.0.0.0", "TCP"),
    (2011, "orderService", "游戏服接入（gameServerServiceAddr）", "0.0.0.0", "TCP"),
    (2015, "leaseServer", "游戏服接入（GameServerServiceAddr）", "0.0.0.0", "TCP"),
    (2016, "crossTeamServer", "跨服队伍服务（crossTeamServerAddr）", "0.0.0.0", "TCP"),
    (2020, "centralLogin", "客户端接入（clientServiceAddr）", "0.0.0.0", "TCP"),
    (2030, "centralLogin", "游戏服指令通道（gameServerServiceAddr）", "0.0.0.0", "TCP"),
    (2040, "admin", "游戏服管理通道（addressForGameServer）", "0.0.0.0", "TCP"),
    (2050, "admin", "GMT grpc-web 入口（addressForGMT）", "0.0.0.0", "gRPC-web"),
    (2051, "admin", "gRPC 服务（AddreesForGRPC）", "0.0.0.0", "gRPC"),
    (2060, "router", "游戏服接入（gameServerServiceAddr）", "0.0.0.0", "TCP"),
    (2061, "router", "集群同步（routerClusterAddr，advertise 192.168.10.133:2061）", "0.0.0.0", "TCP"),
    (2120, "dropServer", "掉落结算服务（dropServerAddr）", "0.0.0.0", "TCP"),
    (2140, "crossDataServer", "跨服数据服务（crossDataServerAddr）", "0.0.0.0", "TCP"),
    (2150, "allianceService", "公会服务（allianceServiceAddr）", "0.0.0.0", "TCP"),
    (4396, "queueServer", "排队/限流 HTTP（httpServer）", "0.0.0.0", "HTTP"),
    (7999, "queueServer（外部对端）", "centralLogin serverList.json 配置的排队服", "192.168.11.118", "HTTP/外部"),
    (8080, "admin", "GMT HTTP API（httpAPIAddress）", "0.0.0.0", "HTTP"),
    (8081, "admin", "HTTP SDK（httpSDKAddress）", "0.0.0.0", "HTTP"),
    (8888, "orderService", "订单 HTTP API（httpAddr，需 apiSecret 签名）", "0.0.0.0", "HTTP"),
    (8989, "多服务", "调试端口（maple/centralLogin/router/auction/dropServer/crossDataServer/queueServer）", "localhost", "调试"),
    (8990, "crossTeamServer", "调试端口（addressForDebug）", "localhost", "调试"),
    (8999, "centralLogin", "IDIP HTTP（idipHttpServer）", "0.0.0.0", "HTTP"),
    (9292, "admin", "调试端口（addressForDebug）", "localhost", "调试"),
    (9393, "leaseServer", "调试端口（AddressForDebug）", "localhost", "调试"),
    (9527, "maple", "HTTP JSON API（httpAddr，写接口需 HMAC-SHA256 签名）", "0.0.0.0", "HTTP"),
    (9900, "allianceService", "调试端口（addressForDebug）", "localhost", "调试"),
]
PORTS.sort(key=lambda x: x[0])

r = 3
for port, svc, use, bind, proto in PORTS:
    vals = [port, svc, use, bind, proto]
    for col, v in enumerate(vals, start=1):
        c = ws2.cell(row=r, column=col, value=v)
        c.font = Font(name=FONT_NAME, size=10)
        c.border = BORDER
        if col == 1:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = "0"
        else:
            c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=(col == 3))
        if (r - 3) % 2 == 1:
            c.fill = PatternFill("solid", fgColor=XL_BAND)
    ws2.row_dimensions[r].height = est_height([(use, WIDTHS2[2])], min_h=20)
    r += 1

ws2.freeze_panes = "A3"
ws2.auto_filter.ref = f"A2:{get_column_letter(len(HEADERS2))}{r - 1}"

# ============================================================
# Sheet 3: 说明
# ============================================================
ws3 = wb.create_sheet("说明")
HEADERS3 = ["项目", "说明"]
WIDTHS3 = [22, 96]
for i, w in enumerate(WIDTHS3, start=1):
    ws3.column_dimensions[get_column_letter(i)].width = w

style_title(ws3, len(HEADERS3), "部署与配置说明")
style_header(ws3, HEADERS3)

NOTES = [
    ("数据来源", "bin/<服务名>/<服务名>.json（端口/MySQL/Redis 配置）、deploy/instances.conf（服务清单/探活端口/启动顺序）、src/<服务名>/ 源码"),
    ("技术栈", "12 个服务均为 Go 1.21+ 静态二进制；构建脚本 build_all.sh / bin/build_all_server.sh / deploy/build_linux.sh"),
    ("安装根目录", "/home/fengyan/Server/centralService/bin/<服务名>/：可执行文件、<服务名>.json 与目录同名同目录（src/common/utils.go 按可执行所在目录名推导配置文件名）"),
    ("共享数据目录", "<安装根>/bin/data，各服务内以 ../data 访问"),
    ("systemd 单元", "centralsvc-<服务名>.service（UNIT_PREFIX=centralsvc）；Restart=always，RestartSec=3，StartLimitIntervalSec=0；运行用户 fengyan"),
    ("日志", "<服务名>.log（业务日志）+ <服务名>.out.log（stdout/stderr），均在服务自己目录；logrotate 配置 /etc/logrotate.d/centralsvc（copytruncate）"),
    ("告警上报", "各服务 reportAddr 为企业微信 webhook（crossTeamServer 的 reportAddr=22016 疑似配置异常）"),
    ("数据库账号", "MySQL 用户 fengyan、Redis 无口令（开发基线）；生产口令以 deploy.env（MYSQL_PASSWD 等）为准，本表不含口令"),
    ("建库导表", "db_init=yes 的服务（centralLogin/maple/auction/orderService/allianceService/leaseServer/dropServer/crossDataServer）由 install.sh 自动执行 up.sh + <服务>.sql"),
    ("部署方式", "远程：bash install.sh --ansible（inventory 组 tmp，目标机 172.16.41.49，SSH 用户 fengyan，需免密 sudo）；仅重装单元：./deploy/install-systemd.sh --only <服务名>"),
    ("启动顺序", "centralLogin → queueServer → router → maple → auction → orderService → allianceService → leaseServer → dropServer → crossDataServer → crossTeamServer → admin"),
    ("探活端口", "install.sh / healthcheck.sh 按 instances.conf 的 probe_ports 做 TCP 探活；改端口需同步改 instances.conf"),
]

r = 3
for i, (k, v) in enumerate(NOTES):
    ck = ws3.cell(row=r, column=1, value=k)
    ck.font = Font(name=FONT_NAME, size=10, bold=True)
    ck.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ck.border = BORDER
    cv = ws3.cell(row=r, column=2, value=v)
    cv.font = Font(name=FONT_NAME, size=10)
    cv.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    cv.border = BORDER
    if i % 2 == 1:
        ck.fill = PatternFill("solid", fgColor=XL_BAND)
        cv.fill = PatternFill("solid", fgColor=XL_BAND)
    ws3.row_dimensions[r].height = est_height([(v, WIDTHS3[1])], min_h=22)
    r += 1

ws3.freeze_panes = "A3"

wb.save(OUT)
print("saved:", OUT)
