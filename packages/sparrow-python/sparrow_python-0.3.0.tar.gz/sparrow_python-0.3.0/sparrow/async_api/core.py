import asyncio
import time
from typing import Any, Iterable, Optional
from aiohttp import ClientSession
from contextlib import asynccontextmanager
from ..decorators.core import async_retry
from .interface import RequestResult
from .progress import ProgressTracker, ProgressBarConfig



class RateLimiter:
    """速率限制器"""

    def __init__(self, max_fps: Optional[float] = None):
        self.max_fps = max_fps
        self.min_interval = 1 / max_fps if max_fps else 0
        self.last_request_time = 0

    async def acquire(self):
        if not self.max_fps:
            return

        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.min_interval:
            # await asyncio.sleep(self.min_interval - elapsed)
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()


class ConcurrentRequester:
    """
    并发请求管理器

    Example
    -------

    requester = ConcurrentRequester(
        concurrency_limit=5,
        max_fps=10,
        timeout=0.7,
    )

    request_params = [
        {
            'json': {
                'messages': [{"role": "user", "content": "讲个笑话" }],
                'model': "qwen2.5:latest",
            },
            'headers': {'Content-Type': 'application/json'}
        } for i in range(10)
    ]

    # 执行并发请求
    results, tracker = await requester.process_requests(
        request_params=request_params,
        url='http://localhost:11434/v1/chat/completions',
        method='POST',
        show_progress=True
    )
    """

    def __init__(
            self,
            concurrency_limit: int,
            max_fps: Optional[float] = None,
            timeout: float | None = None,
    ):
        self._concurrency_limit = concurrency_limit
        self._timeout = timeout
        self._rate_limiter = RateLimiter(max_fps)
        self._semaphore = asyncio.Semaphore(concurrency_limit)

    @asynccontextmanager
    async def _get_session(self):
        async with ClientSession() as session:
            yield session

    @async_retry(retry_times=3, retry_delay=1.0)
    async def _send_single_request(
            self,
            session: ClientSession,
            request_id: int,
            url: str,
            method: str = 'POST',
            **kwargs
    ) -> RequestResult:
        """发送单个请求"""
        async with self._semaphore:
            try:
                # todo: 速率限制也许需要优化
                await self._rate_limiter.acquire()

                start_time = time.time()

                async with session.request(
                        method, url,
                        timeout=self._timeout,
                        **kwargs
                ) as response:
                    data = await response.json()
                    latency = time.time() - start_time

                    if response.status != 200:
                        error_info = {
                            'status_code': response.status,
                            'response_data': data,
                            'error': f"HTTP {response.status}"
                        }
                        return RequestResult(
                            request_id=request_id,
                            data=error_info,
                            status='error',
                            latency=latency
                        )

                    return RequestResult(
                        request_id=request_id,
                        data=data,
                        status="success",
                        latency=latency
                    )

            except asyncio.TimeoutError as e:
                return RequestResult(
                    request_id=request_id,
                    data={'error': 'Timeout error', 'detail': str(e)},
                    status='error',
                    latency=time.time() - start_time
                )
            except Exception as e:
                return RequestResult(
                    request_id=request_id,
                    data={'error': e.__class__.__name__, 'detail': str(e)},
                    status='error',
                    latency=time.time() - start_time
                )

    async def process_requests(
            self,
            request_params: Iterable[dict[str, Any]],
            url: str,
            method: str = 'POST',
            show_progress: bool = True
    ) -> tuple[list[RequestResult], Optional[ProgressTracker]]:
        """
        处理批量请求

        Returns:
            Tuple[list[RequestResult], Optional[ProgressTracker]]:
            请求结果列表和进度跟踪器（如果启用了进度显示）
        """
        request_params = list(request_params)
        requests_with_ids = list(enumerate(request_params))

        bar_config = ProgressBarConfig()
        progress = ProgressTracker(
            len(requests_with_ids),
            concurrency=self._concurrency_limit,
            config = bar_config) if show_progress else None

        async with self._get_session() as session:
            tasks = {
                asyncio.create_task(
                    self._send_single_request(
                        session=session,
                        request_id=request_id,
                        url=url,
                        method=method,
                        **params
                    )
                ): request_id
                for request_id, params in requests_with_ids
            }

            results = []
            for task in asyncio.as_completed(tasks):
                try:
                    result = await task
                except Exception as e:
                    request_id = tasks[task]
                    result = RequestResult(
                        request_id=request_id,
                        data={
                            'error': 'Task execution error',
                            'error_type': e.__class__.__name__,
                            'detail': str(e)
                        },
                        status='error',
                        latency=0
                    )

                if progress:
                    progress.update(result)
                results.append(result)

            if progress:
                progress.print_summary()

            return sorted(results, key=lambda x: x.request_id), progress