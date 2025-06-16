import logging
import httpx
from httpx_socks import AsyncProxyTransport
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class V2Ray:
    def __init__(self):
        # 直接从构造函数获取配置 (完全遵循 http.py 模式)
        self.proxy_url = "socks5://127.0.0.1:10808"
        self.timeout = 10.0
        
        # 创建代理传输层
        self.transport = AsyncProxyTransport.from_url(self.proxy_url)
        
        logger.info(f"V2Ray sender initialized | Proxy: {self.proxy_url} | Timeout: {self.timeout}s")

    async def send_request(self, base_request):
        """通过V2Ray代理发送请求 (完全遵循http.py的签名)"""
        try:
            async with httpx.AsyncClient(
                transport=self.transport,
                timeout=self.timeout,
                headers=base_request.headers.copy(),
                cookies=base_request.cookies
            ) as client:
                # 复用原始请求的所有参数 (与http.py完全一致)
                response = await client.request(
                    method=base_request.method,
                    url=base_request.url,
                    data=base_request.body,
                    params=base_request.params
                )
                
                # 返回与http.py相同的字典结构
                return {
                    "status_code": response.status_code,
                    "content": response.content,
                    "headers": dict(response.headers)
                }
                
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            # 使用与http.py相同的错误处理模式
            logger.error(f"V2ray proxy connection failed: {str(e)}")
            raise HTTPException(
                status_code=504,
                detail=f"代理连接失败: {str(e)}"
            )
        except Exception as e:
            logger.exception(f"V2ray request error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"代理请求错误: {str(e)}"
            )