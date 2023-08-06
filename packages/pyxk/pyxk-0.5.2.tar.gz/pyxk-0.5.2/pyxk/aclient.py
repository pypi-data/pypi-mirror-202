import re
import sys
import types
import typing
import asyncio
from itertools import zip_longest
from multidict import CIMultiDict
from asyncio import AbstractEventLoop as EventLoop

from yarl import URL
from lxml import etree
from aiohttp import (
    ClientTimeout,
    TCPConnector,
    ClientSession as Session
)
import aiohttp.client_exceptions
import rich.live as rich_live
import rich.console as rich_console
import rich.progress as rich_progress
from aiohttp.client_reqrep import ClientResponse as Response

from pyxk.utils import get_user_agent
from pyxk.lazy_loader import LazyLoader

rich_box = LazyLoader("rich_box", globals(), "rich.box")
rich_panel = LazyLoader("rich_panel", globals(), "rich.panel")
rich_table = LazyLoader("rich_table", globals(), "rich.table")



class AsyncSession:

    limit: int = 16
    timeout: typing.Union[int, float, dict] = {
        "total": 8,
        "connect": None,
        "sock_read": None,
        "sock_connect": None
    }
    headers: typing.Union[dict, CIMultiDict] = {}
    start_urls: list = []
    user_agent: str = get_user_agent("android")
    aiohttp_kwargs: dict = {}

    def __init__(
        self,
        *,
        loop: EventLoop=None,
        session: Session=None
    ):
        self._loop: EventLoop = loop
        self._session: Session = session

    async def start(self):
        """运行开始之前调用"""

    async def stop(self):
        """运行完成之后调用"""

    @classmethod
    def run(cls, **kwargs) -> typing.Union[object, list]:
        """类方法: 协程入口 run, 应该从这里开始

        Return: ClientSession, [..., ...]
        返回值: 当前类的实例化, 协程运行结果列表
        """
        # Event loop
        if not isinstance(kwargs.get("loop", None), EventLoop):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            kwargs["loop"] = loop
        # Instance
        self = cls(**kwargs)
        result: list = self._loop.run_until_complete(self.async_start())
        # close event loop
        if isinstance(self._loop, EventLoop):
            self._loop.close()
        return self, result

    async def async_start(self):
        try:
            # event loop
            if (
                not isinstance(self._loop, EventLoop)
                or self._loop.is_closed() is True
            ):
                self._loop = asyncio.get_event_loop()
                asyncio.set_event_loop(self._loop)
            # create aiohttp.ClientSession
            if not (
                isinstance(self._session, Session)
                and self._session.closed is False
            ):
                self._session = await self.create_client_session()

            # run - self.open
            await self.start()
            result: list = await self.start_request()
        finally:
            await self.async_close()
        return result

    async def async_close(self):
        await self.stop()
        # close aiohttp.ClientSession
        if isinstance(self._session, Session):
            await self._session.close()

    async def create_client_session(self):
        "创建 aiohttp.ClientSession"
        return Session(loop=self._loop, headers=self.merge_headers(), **self.merge_aiohttp_kwargs())

    @property
    def loop(self) -> EventLoop:
        return self._loop

    def merge_headers(self) -> CIMultiDict:
        """aiohttp.ClientSession Headers"""
        user_agent = self.user_agent if isinstance(self.user_agent, str) else get_user_agent("android")
        headers = CIMultiDict(self.headers or {})
        headers.setdefault("User-Agent", user_agent)
        return headers

    def merge_aiohttp_kwargs(self) -> dict:
        """aiohttp.ClientSession aiohttp_kwargs"""
        aiohttp_kwargs = self.aiohttp_kwargs.copy()
        timeout_kwargs = dict(
            total=100,
            connect=None,
            sock_read=None,
            sock_connect=None
        )
        if isinstance(self.timeout, (int, float)):
            timeout_kwargs["total"] = self.timeout
        elif isinstance(self.timeout, dict):
            timeout_kwargs.update(self.timeout)

        timeout = ClientTimeout(**timeout_kwargs)
        connector = TCPConnector(limit=self.limit)
        aiohttp_kwargs.setdefault("timeout", timeout)
        aiohttp_kwargs.setdefault("connector", connector)
        return aiohttp_kwargs

    async def request(
        self,
        url: str,
        callback: callable=None,
        method: str="GET",
        cb_kwargs: dict=None,
        **kwargs
    ):
        """异步Request方法

        :params: url
        :params: callback: 回调函数
        :params: method: 请求方法
        :params: cb_kwargs: 回调函数关键词参数
        :params: **kwargs: 异步请求参数
        """
        cb_kwargs = cb_kwargs if isinstance(cb_kwargs, dict) else {}
        while True:
            try:
                async with self._session.request(method=method, url=url, **kwargs) as response:
                    response = add_response_method(response)
                    if callable(callback):
                        result = await callback(response=response, **cb_kwargs)
                        return result
                    return response
            # 请求超时 重试
            except asyncio.exceptions.TimeoutError:
                await asyncio.sleep(1)
            # 连接错误 重试
            except (
                aiohttp.client_exceptions.ClientOSError,
                aiohttp.client_exceptions.ClientPayloadError,
                aiohttp.client_exceptions.ClientConnectorError,
            ):
                await asyncio.sleep(2)
            # 服务器拒绝连接
            except aiohttp.client_exceptions.ServerDisconnectedError:
                await asyncio.sleep(2)

    async def gather_urls(
        self,
        *urls,
        callback: callable=None,
        method: str="GET",
        cb_kwargs_list: typing.List[dict]=None,
        return_exceptions: bool=False,
        **kwargs
    ):
        """异步Request gather方法 异步发送大量url

        :params: *urls: url列表
        :params: callback: 回调函数
        :params: method: 请求方法
        :params: cb_kwargs_list: 回调函数关键词参数 列表
        :params: return_exceptions: 异常传递 若为真,异常将不抛出 传递值返回结果中
        :params: **kwargs: 异步请求参数
        """
        if isinstance(cb_kwargs_list, dict):
            cb_kwargs_list = [cb_kwargs_list]
        elif not isinstance(cb_kwargs_list, list):
            cb_kwargs_list = []
        tasks = [
            self.request(
                url=url,
                callback=callback,
                method=method,
                cb_kwargs=dict(cb_kwargs),
                **kwargs
            )
            for url, cb_kwargs in zip_longest(urls, cb_kwargs_list, fillvalue={})
        ]
        return await asyncio.gather(*tasks, return_exceptions=return_exceptions)

    async def start_request(self):
        """异步请求入口方法"""
        if not self.start_urls:
            raise NotImplementedError(f"{self.__class__.__name__}.start_urls is empty(Must be a 'list')")
        tasks = [
            self.request(url, callback=self.parse)
            for url in self.start_urls
        ]
        result = await asyncio.gather(*tasks)
        return result

    async def parse(self, response: Response):
        """默认解析方法

        :params: response: 异步请求响应
        :参数传递可以使用 cb_kwargs
        """
        raise NotImplementedError(f"'{self.__class__.__name__}.parse' not implemented")

    async def sleep(self, delay: typing.Union[int, float]=0, result: any=None):
        return await asyncio.sleep(delay, result=result)


def add_response_method(response: Response) -> Response:
    # 为 Response 添加 xpath解析方法
    async def _xpath(self, _xpath, *, encoding=None, errors="strict", **kwargs):
        _htmlparse = etree.HTML(await self.text(encoding=encoding, errors=errors))
        class XpathList(list):
            def get(self, default=None):
                if not self:
                    return default
                return self[0]
        return XpathList(_htmlparse.xpath(_xpath, **kwargs))

    # 为 Response 添加 regular 方法
    async def _regular(self, pattern, flags=0):
        string = await self.text()
        return re.search(pattern, string, flags)

    # 为 Response 添加 urljoin 方法
    def _urljoin(self, _url: typing.Union[str, URL], /) -> str:
        if isinstance(_url, str):
            _url = URL(_url)
        elif not isinstance(_url, URL):
            return _url

        if _url.is_absolute():
            return _url.human_repr()
        return self.url.join(_url)

    response.xpath = types.MethodType(_xpath, response)
    response.re = types.MethodType(_regular, response)
    response.urljoin = types.MethodType(_urljoin, response)
    return response


default_progress_columns = (
    rich_progress.SpinnerColumn("line"),
    rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
    rich_progress.BarColumn(),
    rich_progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
    # rich_progress.DownloadColumn(),
    # rich_progress.TransferSpeedColumn(),
    rich_progress.TimeElapsedColumn()
)


default_download_progress_columns = (
    rich_progress.SpinnerColumn("line"),
    rich_progress.TaskProgressColumn("[progress.percentage]{task.percentage:>6.2f}%"),
    rich_progress.BarColumn(),
    #rich_progress.TextColumn("[progress.description]{task.completed}/{task.total}"),
    rich_progress.DownloadColumn(),
    # rich_progress.TransferSpeedColumn(),
    rich_progress.TimeElapsedColumn()
)


def default_live(
    *,
    total: int=None,
    renderable: list=None,
    progress_column: typing.Union[list, tuple]=None,
    transient: bool=False,
    console: rich_console.Console=None,
    refresh_per_second: int=4,
    title: str=None,
    title_align: str=None,
) -> typing.Tuple[rich_live.Live, rich_progress.Progress, rich_progress.Task]:
    # total
    if not isinstance(total, int) or total <= 0:
        total = None
    # progress column
    progress_column = progress_column or default_progress_columns
    progress = rich_progress.Progress(*progress_column)
    progress_task = progress.add_task(description="", total=total)
    # console
    console = console or rich_console.Console()
    # transient
    transient = bool(transient)
    # renderable
    if not renderable:
        live = progress
    else:
        # 创建表单
        live = rich_table.Table(
            box=rich_box.SIMPLE_HEAD, expand=True, show_header=False
        )
        live.add_column(no_wrap=False, justify="center")
        for item in renderable:
            live.add_row(f"{item}")
        live.add_section()
        live.add_row(progress)

        # 将表单装入板块(panel)中
        live = rich_panel.Panel(
            live,
            border_style="bright_blue",
            subtitle=f"[dim]Total: {total or 0}[/]",
            subtitle_align="right",
            title=title,
            title_align=title_align,
        )

    # 装入 live 中进行实时更新
    live = rich_live.Live(
        live,
        transient=transient,
        console=console,
        refresh_per_second=refresh_per_second
    )
    return live, progress, progress_task


class NovelSpiderTemplate(AsyncSession):
    """小说爬虫模板文件

    :params: keyword: 爬虫搜索值
    """

    name: str = None
    store: str = None
    start_urls: str = None
    user_agent: str = get_user_agent("windows")

    def __init__(self, *, keyword: str=None, **kwargs):
        super().__init__(**kwargs)
        self._console = rich_console.Console()
        self._keyword = keyword
        self.book, self.author = None, None

    async def start_request(self):
        """异步请求入口方法"""
        if not self.start_urls:
            raise NotImplementedError(f"{self.__class__.__name__}.start_urls is empty(Must be a 'str')")
        if not self.name:
            raise NotImplementedError(f"{self.__class__.__name__}.name is empty(Must be a 'str')")
        if not self.store:
            raise NotImplementedError(f"{self.__class__.__name__}.store is empty(Must be a 'str')")
        self._console.print(f"[magenta b]{self.name}[/] < {self.start_urls} >\n", justify="center")
        return await self.request(self.start_urls, self.parse)

    @property
    def keyword(self) -> str:
        """搜索 keyword"""
        while not(self._keyword and isinstance(self._keyword, str)):
            self._keyword = self._console.input("[yellow b]搜索书名或作者[/][Exit]: ").strip()
            if self._keyword.lower() in ("e", "exit"):
                self._console.print("[red]Exit[/]")
                sys.exit()
        return self._keyword

    def default_print_search_result(self, *col_names: typing.Tuple[str], books_info: typing.Dict[str, dict]):
        """使用 rich.table 打印搜索结果

        :params: *colv_names: table表头 - 表头每列名称
        :params: books_info: table内容
        """
        table = rich_table.Table(
            caption=f"[dim]< {self._keyword} > Total: {len(books_info)}[/]",
            caption_justify="right",
            box=rich_box.ASCII_DOUBLE_HEAD
        )
        # table 添加列
        table.add_column("", no_wrap=False, style="cyan", justify="center")
        for item in col_names:
            table.add_column(str(item), justify="center")
        # table 添加行
        for index, book in books_info.items():
            table.add_row(str(index), *[book.get(item, "") for item in col_names])
        self._console.print(table)

    def default_print_novel_detail(self, *args: typing.Tuple[str]):
        """使用 rich.panel 打印小说详情页

        :params: *args: 每行内容
        """
        renderable = rich_table.Table(show_header=False, box=rich_box.SIMPLE_HEAD)
        renderable.add_column(justify="left", overflow="fold",)
        for item in args:
            renderable.add_row(item)
        panel = rich_panel.Panel(renderable, border_style="bright_blue")
        self._console.print(panel)

    def select_form_items(
        self,
        *items: typing.Tuple[str],
        description: str=None,
        exception: typing.List[str]=None,
        arbitrary: bool=False
    ):
        """选择器

        :params: *items: input选择范围
        :params: description: 说明，介绍
        :params: exception: 额外的选择范围, 当input输入在其中是返回
        :params: arbitrary: 任意值返回

        注意: 输入 'e' 或者 'exit' 将使用 sys.exit() 关闭程序
        """
        # 需要额外处理的参数
        exception = [str(e).lower() for e in exception or []]
        exception = set(exception)
        items = [str(item) for item in items]
        items.extend(exception)
        description = description or "[yellow b]请选择: [/]"
        while True:
            select = self._console.input(description).strip()
            if select.lower() in ("e", "exit"):
                self._console.print("[red]Exit[/]")
                sys.exit()
            if select in items or arbitrary:
                break
        return select
