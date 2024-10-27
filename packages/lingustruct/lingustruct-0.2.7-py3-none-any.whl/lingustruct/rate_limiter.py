from fastapi import HTTPException, status, Request
from typing import Dict
import time
import redis.asyncio as redis

class RateLimiter:
    def __init__(self, free_calls: int = 5, period: int = 3600, redis_client: redis.Redis = None):
        self.free_calls = free_calls  # 無料ユーザーのリクエスト上限
        self.period = period  # 期間（秒単位）
        self.redis_client = redis_client  # Redisクライアント
        self.ip_request_count = {}  # 無料ユーザーのIPアドレスごとのカウント

    async def enforce_limit(self, request: Request, user: Dict):
        """ユーザーのプランに基づき、レート制限を適用する"""
        ip = request.client.host

        # 有料ユーザーは無制限アクセスを許可
        if user.get("plan") == "paid":
            print(f"Paid user: Unlimited access for IP {ip}")
            return

        # 無料ユーザーはIPアドレスごとのアクセス制限を適用
        self._check_ip_rate_limit(ip)

    def _check_ip_rate_limit(self, ip: str):
        """IPアドレスに基づく無料ユーザーのレート制限"""
        current_time = int(time.time())

        if ip not in self.ip_request_count:
            # 初回リクエストの場合、カウントを1に初期化
            self.ip_request_count[ip] = {"count": 1, "timestamp": current_time}
            return

        data = self.ip_request_count[ip]

        # 指定期間が経過した場合、カウントをリセット
        if current_time - data["timestamp"] > self.period:
            self.ip_request_count[ip] = {"count": 1, "timestamp": current_time}
            return

        # 上限を超えた場合、429エラーを返す
        if data["count"] >= self.free_calls:
            print(f"Rate limit exceeded for IP {ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later."
            )

        # リクエスト数を増加
        self.ip_request_count[ip]["count"] += 1
