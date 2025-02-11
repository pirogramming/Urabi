# asgi_adapter.py
import asyncio

class ASGI3toASGI2Adapter:
    def __init__(self, app):
        self.app = app

    def __call__(self, scope):
        # 이 함수는 scope만 받고, receive와 send를 받는 callable(코루틴)을 반환합니다.
        async def asgi3_app(receive, send):
            await self.app(scope, receive, send)
        return asgi3_app

