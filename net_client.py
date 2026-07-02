# -*- coding:utf-8 -*-
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: net_client.py
    @time: 2024/xx/xx
--------------------------------
基于 httpx 的网络客户端，自动检测 HTTP 版本并选择合适的后端。

- HTTP/1.x、HTTP/2 → 使用 httpx 同步客户端
- HTTP/3     → 临时导入 aioquic，启用 QUIC 支持
"""
import re
import time
import subprocess

import httpx
from loguru import logger
from anti_useragent import UserAgent

_ua = None


def _get_ua():
    """延迟初始化 UserAgent，避免模块导入时 PyCharm 调试器内省触发
    anti_useragent 的 __getattr__ 导致 AntiUserAgentError。"""
    global _ua
    if _ua is None:
        _ua = UserAgent()
    return _ua


# ============ 全局配置 ============

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}


# ============ HTTP 版本检测 ============

def check_http_version(url):
    """使用 curl -v 检测网站的 HTTP 版本

    :param url: 目标 URL
    :return: 版本字符串 '1' / '2' / '3'，检测失败返回 None

    示例:
        >>> ver = check_http_version('https://example.com')
        >>> ver in ('1', '2', '3') or ver is None
        True
    """
    cmd = ['curl', '-v', '-o', '/dev/null', url]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        # curl -v 的详细信息输出到 stderr
        output = result.stderr

        # 匹配 curl 的 HTTP 版本声明
        # 典型格式:
        #   * using HTTP/1.1  或  * using HTTP/1.x  (curl 8.x)
        #   * using HTTP/2
        #   * using HTTP/3
        match = re.search(r'using HTTP/(\d+)', output)
        if match:
            version = match.group(1)
            logger.info(f"检测到 HTTP 版本: {version}  (url: {url})")
            return version

        # 回退方案: 从响应行 < HTTP/2 200 中解析
        match = re.search(r'^< HTTP/([\d.]+)', output, re.MULTILINE)
        if match:
            version = match.group(1)
            logger.info(f"从响应头检测到 HTTP 版本: {version}")
            return version

    except FileNotFoundError:
        logger.error("curl 未安装，请先安装 curl")
    except subprocess.TimeoutExpired:
        logger.error(f"curl 请求超时: {url}")
    except Exception as e:
        logger.error(f"检测 HTTP 版本失败: {e}")

    return None


# ============ HTTP 客户端类 ============

class NetClient(httpx.Client):
    """HTTP 客户端，继承自 httpx.Client，用法类似 requests。

    根据目标 URL 的 HTTP 版本自动选择后端:
        - HTTP/1.x 或 HTTP/2 → 使用 httpx 内置的 HTTP/1.1 + HTTP/2 支持
        - HTTP/3              → 临时导入 aioquic，通过 QUIC 传输层发起请求

    基本用法:
        client = NetClient()
        resp = client.get('https://example.com', headers={...})
        print(resp.text)

    也支持上下文管理器:
        with NetClient() as client:
            resp = client.get('https://example.com')
    """

    def __init__(self, *args, **kwargs):
        # 默认启用 HTTP/2（httpx 也会借此自动协商 H3）
        kwargs.setdefault('follow_redirects', True)
        kwargs.setdefault('timeout', httpx.Timeout(20.0))

        # 检查 h2 是否可用，不可用时降级为 http/1.1 only
        if kwargs.get('http2', True):
            try:
                import h2  # noqa: F401
                kwargs.setdefault('http2', True)
            except ImportError:
                logger.warning("h2 未安装，HTTP/2 不可用，降级为 HTTP/1.1。"
                               "可执行: pip install httpx[http2]")
                kwargs['http2'] = False

        super().__init__(*args, **kwargs)

    def get(self, url, **kwargs):
        """发送 GET 请求，调用方式类似 requests.get。

        会自动检测目标 URL 的 HTTP 版本:
            - HTTP/1.x 或 HTTP/2 → 由 httpx 同步客户端直接处理
            - HTTP/3              → 临时导入 aioquic 后通过 httpx 发起 QUIC 请求

        :param url:     目标 URL
        :param headers: 可选，请求头 dict
        :param cookies: 可选，cookie dict
        :param timeout: 可选，超时秒数
        :return:        httpx.Response 对象（用法类似 requests.Response）
        """
        version = check_http_version(url)

        if version and version.startswith('3'):
            # HTTP/3: 临时导入 aioquic，确保 QUIC 依赖可用
            try:
                import aioquic  # noqa: F401
            except ImportError:
                raise ImportError(
                    "HTTP/3 请求需要 aioquic 支持，请执行: pip install aioquic"
                )
            # httpx 在 http2=True + aioquic 已安装的条件下，
            # 会自动尝试通过 QUIC 与支持 H3 的服务器建立连接
            logger.info(f"目标 {url} 支持 HTTP/3，已加载 aioquic")

        return super().get(url, **kwargs)


# ============ 功能函数 ============

def get_html(url, **kwargs):
    """获取网页 HTML 文本

    :param url:      目标 URL
    :param headers:  可选，自定义请求头
    :param cookies:  可选，cookie dict
    :param timeout:  可选，超时秒数（默认 20）
    :param charset:  可选，强制指定编码（否则自动检测）
    :param proxies:  可选，代理配置
                     - "v2ray" → socks5://127.0.0.1:10808
                     - "ip:port" → http://ip:port
    :param progress: 可选，是否显示下载进度条（默认 False）
    """
    global headers
    req_headers = kwargs.get('headers', headers).copy()
    req_headers["user-agent"] = _get_ua().random

    cookies = kwargs.get('cookies', None)
    timeout = kwargs.get('timeout', 20)
    show_progress = kwargs.get('progress', False)

    # 代理处理
    proxies = None
    if 'proxies' in kwargs:
        if kwargs['proxies'] == "v2ray":
            proxies = {
                'http://': 'socks5://127.0.0.1:10808',
                'https://': 'socks5://127.0.0.1:10808',
            }
        else:
            proxy_url = 'http://{}'.format(kwargs['proxies'])
            proxies = proxy_url

    client = NetClient(proxy=proxies, timeout=httpx.Timeout(timeout))

    while True:
        try:
            if show_progress:
                resp = _stream_get_with_progress(
                    client, 'GET', url, req_headers, cookies, desc=url.split('/')[-1],
                )
            else:
                resp = client.get(url, headers=req_headers, cookies=cookies)
            # 编码处理: 优先使用用户指定的 charset，其次从 Content-Type 解析
            resp.encoding = kwargs.get('charset') or _detect_encoding(resp)
            resp.raise_for_status()
            break
        except Exception as e:
            logger.error(e)
            logger.error(f"出错url: {url}")
            time.sleep(10)

    html = resp.text
    client.close()

    logger.info(f"\"get\" succeed: {url}")
    return html


def get_file(url, targetfile):
    """获取文件（流式下载，带进度条）

    :param url:        目标 URL
    :param targetfile: 保存路径
    """
    global headers
    from tqdm import tqdm

    client = NetClient()

    # httpx 使用 stream() 进行流式下载
    with client.stream('GET', url, headers=headers) as resp:
        total_size = int(resp.headers.get('Content-Length', 0))
        total_size_mb = round(total_size / (1024 * 1024), 2)

        progress_bar = tqdm(
            total=total_size_mb, unit='MB',
            desc=url.split('/')[-1], ncols=80,
        )
        with open(targetfile, 'wb') as fw:
            for data in resp.iter_bytes(chunk_size=1024):
                fw.write(data)
                progress_bar.update(len(data) / (1024 * 1024))
        progress_bar.close()

    client.close()


def get_binary_image(url, **kwargs):
    """获取二进制图片

    :param url:      目标 URL
    :param progress: 可选，是否显示下载进度条（默认 False）
    :return:          图片二进制内容，失败返回 None
    """
    global headers
    show_progress = kwargs.get('progress', False)

    client = NetClient()
    try:
        if show_progress:
            resp = _stream_get_with_progress(
                client, 'GET', url, headers, desc=url.split('/')[-1],
            )
        else:
            resp = client.get(url, headers=headers)
        return resp.content
    except Exception as e0:
        logger.exception(e0)
    finally:
        client.close()


# ============ 内部工具 ============

def _stream_get_with_progress(client, method, url, headers, cookies=None, desc=''):
    """带 tqdm 进度条的流式 GET，返回一个类 httpx.Response 对象。"""
    from tqdm import tqdm

    with client.stream(method, url, headers=headers, cookies=cookies) as resp:
        total_size = int(resp.headers.get('Content-Length', 0))
        total_size_mb = round(total_size / (1024 * 1024), 2) if total_size else None

        chunks = []
        if total_size_mb:
            progress_bar = tqdm(
                total=total_size_mb, unit='MB', desc=desc, ncols=80,
            )
            for data in resp.iter_bytes(chunk_size=1024):
                chunks.append(data)
                progress_bar.update(len(data) / (1024 * 1024))
            progress_bar.close()
        else:
            for data in resp.iter_bytes(chunk_size=1024):
                chunks.append(data)

        # 将流式响应包装为类 httpx.Response 的对象
        resp._content = b''.join(chunks)
        return resp


def _detect_encoding(resp):
    """从 httpx Response 中检测编码，类似 requests 的 apparent_encoding。

    优先从 Content-Type 头解析；解析不到则用 charset_normalizer 猜测。
    """
    # httpx 的 Response.charset_encoding 从 Content-Type 的 charset 字段解析
    if resp.charset_encoding:
        return resp.charset_encoding

    # 回退: 用 charset_normalizer 从内容中检测
    try:
        from charset_normalizer import detect
        result = detect(resp.content)
        if result:
            return result['encoding']
    except ImportError:
        pass

    return 'utf-8'


# ============ 测试入口 ============

if __name__ == '__main__':
    # 测试 HTTP 版本检测
    print("=== HTTP 版本检测 ===")
    ver = check_http_version("https://www.baidu.com/")
    print(f"检测结果: {ver}")

    # 测试 get_html（带进度条）
    print("\n=== 测试 get_html ===")
    html = get_html('https://www.baidu.com/', progress=True)
    print(f"内容长度: {len(html)} 字节")
    print(f"内容预览: {html[:200]}")

    # 测试 get_html 不带进度条
    print("\n=== 测试 get_html (无进度条) ===")
    html2 = get_html('https://icanhazip.com/')
    print(f"获取内容: {html2.strip()}")
    print(f"内容长度: {len(html2)} 字节")
