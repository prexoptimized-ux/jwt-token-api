# app.py
#━━━━━━━━━━━━━━━━━━━
#  PREX TOKEN API — v4 CLEAN BUILD
#  • India login server: loginbp.ppmainecoonghj.com
#  • Dynamic X-Ga-Sv from /Ping response
#  • bifrostAndroid anti-cheat pre-call
#  • GetLoginData post-login activation
#  • Fixed login_url scope bug (no more UnboundLocalError)
#━━━━━━━━━━━━━━━━━━━

import time
import json
import base64
import socket

import httpx
from flask import Flask, request, jsonify
from flask_cors import CORS
from Crypto.Cipher import AES

from google.protobuf import json_format
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf.message import Message


# ============================================================
#  FreeFire proto definitions
# ============================================================

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 6, 30, 0, "", "FreeFire.proto",
)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0e\x46reeFire.proto"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t'
    b'\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d '
    b'\x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t"]\n\x10\x42lacklist'
    b'InfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n'
    b'\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 '
    b'\x01(\r"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12'
    b'\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18'
    b'\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08"\xa0\x03\n\x08'
    b'LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region'
    b'\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_'
    b'region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t'
    b'\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_'
    b'regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl'
    b'\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mul'
    b'ator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.'
    b'BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueue'
    b'Info\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18'
    b'\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city'
    b'\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n'
    b'\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17'
    b'\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_'
    b'REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n'
    b'\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME'
    b'_AUTO_NEW\x10\xf6\x07\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "FreeFire_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_BANREASON"]._serialized_start = 738
    _globals["_BANREASON"]._serialized_end = 906
    _globals["_LOGINREQ"]._serialized_start = 18
    _globals["_LOGINREQ"]._serialized_end = 117
    _globals["_BLACKLISTINFORES"]._serialized_start = 119
    _globals["_BLACKLISTINFORES"]._serialized_end = 212
    _globals["_LOGINQUEUEINFO"]._serialized_start = 214
    _globals["_LOGINQUEUEINFO"]._serialized_end = 316
    _globals["_LOGINRES"]._serialized_start = 319
    _globals["_LOGINRES"]._serialized_end = 735

LoginReq = _globals["LoginReq"]
LoginRes = _globals["LoginRes"]


# ============================================================
#  Settings
# ============================================================

MAIN_KEY = base64.b64decode("WWcmdGMlREV1aDYlWmNeOA==")
MAIN_IV = base64.b64decode("Nm95WkRyMjJFM3ljaGpNJQ==")
RELEASEVERSION = "OB55"
USERAGENT = "UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)"

# Real India login servers (from mitmproxy capture)
LOGIN_URLS = [
    "https://loginbp.ppmainecoonghj.com/",
    "https://vodka.freefireind.in/",
    "https://loginbp.common.ggbluefox.com/",
    "https://loginbp.ggpolarbear.com/",
    "https://loginbp.ggblueshark.com/",
    "https://loginbp.ggwhitehawk.com/",
]

BIFROST_URL = "https://gin.freefireind.in/bifrostAndroid"
CLIENT_BASE = "https://client.ind.freefiremobile.com/"

HTTP_LIMITS = httpx.Limits(max_keepalive_connections=20, max_connections=50)
HTTP_TIMEOUT = httpx.Timeout(15.0, connect=5.0)
_http_client = httpx.Client(limits=HTTP_LIMITS, timeout=HTTP_TIMEOUT)


# ============================================================
#  Flask
# ============================================================

app = Flask(__name__)
CORS(app)


# ============================================================
#  Helpers
# ============================================================

def pad(text: bytes) -> bytes:
    padding_length = AES.block_size - (len(text) % AES.block_size)
    return text + bytes([padding_length] * padding_length)


def aes_cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plaintext))


def json_to_proto(json_data: str, proto_message: Message) -> bytes:
    json_format.ParseDict(json.loads(json_data), proto_message)
    return proto_message.SerializeToString()


def try_parse_login_res(data: bytes):
    try:
        msg = LoginRes()
        msg.ParseFromString(data)
        if msg.account_id and msg.account_id > 0:
            return json.loads(json_format.MessageToJson(msg))
    except Exception:
        pass
    return None


def extract_login_res(raw: bytes) -> dict:
    if not raw or len(raw) < 5:
        raise Exception(f"Response too short ({len(raw)} bytes): {raw.hex()}")

    parsed = try_parse_login_res(raw)
    if parsed:
        return parsed

    idx = 0
    while True:
        idx = raw.find(b"\x08", idx)
        if idx == -1:
            break
        parsed = try_parse_login_res(raw[idx:])
        if parsed:
            return parsed
        idx += 1

    jwt_marker = raw.find(b"eyJhbGciOiJIUzI1NiIs")
    if jwt_marker != -1:
        for i in range(jwt_marker - 1, max(jwt_marker - 300, -1), -1):
            if raw[i] == 0x42:
                parsed = try_parse_login_res(raw[i:])
                if parsed:
                    return parsed
                break

    raise Exception(
        f"Could not parse LoginRes. Length: {len(raw)} bytes. "
        f"Hex: {raw[:100].hex()}"
    )


def get_access_token(account: str):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    payload = (
        account
        + "&response_type=token&client_type=2"
        + "&client_secret=2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
        + "&client_id=100067"
    )
    headers = {
        "User-Agent": USERAGENT,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    resp = _http_client.post(url, data=payload, headers=headers)
    data = resp.json()
    return data.get("access_token", "0"), data.get("open_id", "0")


def filter_valid_urls(urls):
    valid = []
    for url in urls:
        host = url.replace("https://", "").replace("http://", "").rstrip("/")
        try:
            socket.gethostbyname(host)
            valid.append(url)
            print(f"  [OK] {host}")
        except Exception:
            print(f"  [--] {host} (DNS fail)")
    return valid


def _build_headers(x_ga_sv: str = "1789534056") -> dict:
    return {
        "User-Agent": USERAGENT,
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "X-Ga-Sv": x_ga_sv,
        "Authorization": "Bearer",
        "X-Ga": "v1 1",
        "Releaseversion": RELEASEVERSION,
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.12f1",
        "PlAy_VeR": "1.132.9",
        "Ob_VeR": RELEASEVERSION,
    }


def _do_ping(login_url: str, headers: dict) -> dict:
    try:
        resp = _http_client.post(f"{login_url}Ping", data=b"", headers=headers)
        print(f"  Ping Status: {resp.status_code}")
        if resp.status_code == 200 and len(resp.content) > 0:
            try:
                return resp.json()
            except Exception:
                return {}
    except Exception as e:
        print(f"  Ping failed: {e}")
    return {}


def _do_bifrost(headers: dict) -> bool:
    try:
        print(f"  [Anti-cheat] bifrostAndroid...")
        resp = _http_client.post(BIFROST_URL, data=b"", headers=headers)
        print(f"  bifrostAndroid Status: {resp.status_code}")
        return resp.status_code in (200, 900)
    except Exception as e:
        print(f"  bifrostAndroid failed: {e}")
    return False


def _do_get_login_data(token: str, headers: dict) -> bool:
    try:
        print(f"  [Activation] GetLoginData...")
        resp = _http_client.post(f"{CLIENT_BASE}GetLoginData", data=b"", headers=headers)
        print(f"  GetLoginData Status: {resp.status_code}")
        return resp.status_code == 200
    except Exception as e:
        print(f"  GetLoginData failed: {e}")
    return False


# ============================================================
#  Core: generate token
# ============================================================

def generate_jwt_token(uid: str, password: str):
    start_time = time.time()

    print(f"\n{'='*60}")
    print(f"  TOKEN GENERATION START")
    print(f"{'='*60}")
    print(f"  UID: {uid}")

    # --- Step 1: OAuth ---
    token_val, open_id = get_access_token(f"uid={uid}&password={password}")
    if token_val == "0" or open_id == "0":
        raise Exception("Invalid UID or Password")

    print(f"  [1/6] OAuth OK")
    print(f"    access_token: {token_val[:25]}...")
    print(f"    open_id: {open_id}")

    # --- Step 2: ProtoBuf encrypt ---
    body = json.dumps({
        "open_id": open_id,
        "open_id_type": "4",
        "login_token": token_val,
        "orign_platform_type": "4",
    })
    proto_bytes = json_to_proto(body, LoginReq())
    payload = aes_cbc_encrypt(MAIN_KEY, MAIN_IV, proto_bytes)
    print(f"  [2/6] ProtoBuf encrypted: {len(payload)} bytes")

    # --- Step 3: Try each login URL ---
    urls_to_try = list(LOGIN_URLS) if LOGIN_URLS else []
    if not urls_to_try:
        raise Exception("No login URLs configured")

    print(f"\n  URLs to try: {len(urls_to_try)}")

    last_error = None
    successful_url = None
    final_token = ""
    final_uid = ""

    for i, login_url in enumerate(urls_to_try, 1):
        try:
            print(f"\n  [3/6] Trying URL #{i}: {login_url}")

            # Ping + dynamic X-Ga-Sv
            base_headers = _build_headers()
            ping_data = _do_ping(login_url, base_headers)

            dynamic_sv = (
                ping_data.get("X-Ga-Sv")
                or ping_data.get("x_ga_sv")
                or ping_data.get("xGaSv")
            )
            if dynamic_sv:
                base_headers["X-Ga-Sv"] = str(dynamic_sv)
                print(f"    Dynamic X-Ga-Sv: {dynamic_sv}")
            else:
                print(f"    No dynamic X-Ga-Sv, using default")

            time.sleep(0.3)

            # Anti-cheat
            _do_bifrost(base_headers)
            time.sleep(0.3)

            # MajorLogin
            url = f"{login_url}MajorLogin"
            resp = _http_client.post(url, data=payload, headers=base_headers)

            print(f"\n    MajorLogin Status: {resp.status_code}")
            print(f"    Response Length: {len(resp.content)} bytes")

            if len(resp.content) < 500:
                try:
                    print(f"    Body: {resp.text[:400]}")
                except Exception:
                    print(f"    Body (hex): {resp.content[:200].hex()}")

            if resp.status_code != 200:
                last_error = f"HTTP {resp.status_code}"
                print(f"    Failed: {last_error}")
                continue

            if len(resp.content) < 10:
                last_error = f"Empty response ({len(resp.content)} bytes)"
                print(f"    Failed: {last_error}")
                continue

            try:
                msg = extract_login_res(resp.content)
            except Exception as e:
                last_error = f"Parse failed: {str(e)[:100]}"
                print(f"    Parse error: {e}")
                continue

            token = msg.get("token", "")
            real_uid = str(msg.get("accountId", ""))

            print(f"    Parsed accountId: {real_uid}")
            print(f"    Parsed token length: {len(token)}")

            if not token or len(token) < 50:
                last_error = f"Invalid token length: {len(token)}"
                print(f"    Failed: {last_error}")
                continue

            if not real_uid or real_uid == "1":
                last_error = f"Invalid real_uid: {real_uid}"
                print(f"    Failed: {last_error}")
                continue

            # SUCCESS
            successful_url = login_url
            final_token = token
            final_uid = real_uid
            print(f"    SUCCESS with {login_url}")

            # Activate
            activate_headers = dict(base_headers)
            activate_headers["Authorization"] = f"Bearer {token}"
            _do_get_login_data(token, activate_headers)
            break

        except Exception as e:
            last_error = str(e)
            print(f"    Exception: {e}")
            continue

    # --- Step 4: Check ---
    if not successful_url:
        print(f"\n  [4/6] ALL LOGIN URLS FAILED")
        print(f"    Last error: {last_error}")
        print(f"{'='*60}\n")
        raise Exception(f"All login URLs failed. Last error: {last_error}")

    print(f"\n  [4/6] MajorLogin OK via {successful_url}")

    elapsed = time.time() - start_time

    result = {
        "access_token": token_val,
        "open_id": open_id,
        "real_uid": final_uid,
        "status": "success",
        "time": f"{elapsed:.2f}s",
        "token": final_token,
    }

    print(f"  [6/6] DONE in {elapsed:.2f}s")
    print(f"    Real UID: {final_uid}")
    print(f"    Token length: {len(final_token)}")
    print(f"{'='*60}\n")

    return result


# ============================================================
#  Routes
# ============================================================

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "ok",
        "endpoint": "/token?uid=UID&password=PASS",
        "example": "/token?uid=18097039025&password=yourpass",
    }), 200


@app.route("/token", methods=["GET"])
def get_jwt_token():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({
            "status": "error",
            "error": "Both uid and password parameters are required"
        }), 400

    try:
        token_data = generate_jwt_token(uid, password)
        return jsonify(token_data), 200
    except Exception as e:
        print(f"  ERROR: {e}")
        return jsonify({
            "status": "error",
            "error": f"Failed to generate token: {str(e)}"
        }), 500


# ============================================================
#  Entry point
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PREX TOKEN API STARTING (v4)")
    print("=" * 60)
    print(f"Release Version: {RELEASEVERSION}")
    print(f"Testing login URLs...")

    LOGIN_URLS = filter_valid_urls(LOGIN_URLS)

    if not LOGIN_URLS:
        print("No valid login URLs found!")
        exit(1)

    print(f"\n{len(LOGIN_URLS)} valid URLs loaded")
    print("=" * 60)
    print("Server running on http://0.0.0.0:5002")
    print("=" * 60)

    app.run(host="0.0.0.0", port=5002, debug=False)
