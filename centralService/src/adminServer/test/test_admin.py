#!/usr/bin/env python3
import requests
import json
import base64
import hashlib
import time
import datetime

def generate_sign(body: bytes, sign_key: str) -> str:
    """Generate MD5 signature for request body"""
    if not sign_key:
        return ""

    h = hashlib.md5()
    h.update(body)
    h.update(sign_key.encode('utf-8'))
    return h.hexdigest().lower()

def send_mail():
# title base 64 encode
    _cmd = '$sendglobalmail'

    _mail_id = 37001003
    _itemId_num = '30000236,1'
    _deps = ''
    _title = base64.b64encode('Test Title2'.encode('utf-8')).decode('utf-8')
    _content = base64.b64encode('Test Content'.encode('utf-8')).decode('utf-8')
    _start_time = '2022-01-01 00:00:00'
    # _start_time is int
    _start_time = int(datetime.datetime.strptime(_start_time, '%Y-%m-%d %H:%M:%S').timestamp())

    _end_time = '2026-01-01 01:00:00'
    # _end_time is int
    _end_time = int(datetime.datetime.strptime(_end_time, '%Y-%m-%d %H:%M:%S').timestamp())

    _min_level = 1
    _max_level = 99

    _channel = 1

    _args = f"{_mail_id} {_itemId_num} {_deps} {_title} {_content} {_start_time} {_end_time} {_min_level} {_max_level} {_channel}"                             # Command arguments

    return _cmd, _args

def official_msg():
    _cmd = '$gmPublishMarquee'
    _mid = 1
    _content = 'test'
    _startTime = int(time.time())
    _endTime = int(time.time()) + 3600
    _tick = 60
    _priority = 0
    _channels = 1
    _args = f"{_mid} {_content} {_startTime} {_endTime} {_tick} {_priority} {_channels}"                             # Command arguments
    return _cmd, _args

def ban_avatar():
    _cmd = '$banAvatar'
    #_gbId = '5692323899933458433'
    _gbId = '5692323864546954445'
    #_gbId = '5692323558839235377'
    _endTime = '1766284329'
    _args = f"{_gbId} {_endTime}"                             # Command arguments
    return _cmd, _args

def disban_avatar():
    _cmd = '$disbanAvatar'
    _gbId = '5692323864546954445'
    _args = f"{_gbId}"                             # Command arguments
    return _cmd, _args

def ban_chat():
    _cmd = '$setChatForbidden'
    _gbId = '5692323694627310797'
    _endTime = '180'
    _args = f"{_gbId} {_endTime}"                             # Command arguments
    return _cmd, _args

def add_buff():
    # $addbuff 0 64000002 1
    _cmd = '$addbuff'
    _id = 10058
    _buff_id = 64000002
    _num = 1
    _args = f"{_id} {_buff_id} {_num}"                             # Command arguments
    return _cmd, _args

def test_docmd():
    # -------------------------- CONFIGURATION --------------------------
    # Edit these parameters directly in the file:

    _cmd, _args = add_buff()
    print(f'{_cmd} {_args}')
    URL = "http://192.168.10.13:8080/docmd"           # Admin server docmd URL
    PARTITION = 20223                                  # Partition ID (0 for broadcast to all servers)
    COMMAND = _cmd
    ARGS = _args
    SEQID = int(time.time())                       # Sequence ID (current timestamp by default)
    SERIALNO = ""                                  # Serial number (optional)
    SIGN_KEY = "3Pi0ZsIoRha8h0MG6jfHdxG1WLcE7XplB0kzhFitVIZzUNIbKc871DMEZnHGygno"                                  # Signature key (if server requires signatures)
    TIMEOUT = 15                                   # Request timeout in seconds
    # -------------------------------------------------------------------

    # Use configured values
    url = URL
    partition = PARTITION
    command = COMMAND
    args = ARGS
    seqid = SEQID
    serialno = SERIALNO
    sign_key = SIGN_KEY
    timeout = TIMEOUT

    # Prepare request body - args need hex encoding as server uses bytes.fromhex(request.args).decode('utf-8')
    request_data = {
        "Partition": partition,
        "Command": command,
        "Args": args.encode('utf-8').hex(),
        "Seqid": seqid,
        "SerialNo": serialno
    }

    # Convert to JSON bytes
    body_str = json.dumps(request_data)
    body_bytes = body_str.encode('utf-8')

    # Generate signature if sign key provided
    sign = generate_sign(body_bytes, sign_key)
    params = {"sign": sign} if sign else {}

    print(f"Testing docmd interface:")
    print(f"URL: {url}")
    print(f"Request Body: {body_str}")
    if sign:
        print(f"Sign: {sign}")
    print("-" * 50)

    try:
        # Send POST request
        response = requests.post(
            url,
            params=params,
            data=body_bytes,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )

        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")

        # Try to parse JSON response
        if response.headers.get("Content-Type", "").startswith("application/json"):
            try:
                response_json = response.json()
                print(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                print("Warning: Failed to parse response as JSON")

    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to {url}. Is the admin server running?")
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {timeout} seconds")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_docmd()
