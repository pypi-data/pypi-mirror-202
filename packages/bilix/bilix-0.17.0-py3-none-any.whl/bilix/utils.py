import asyncio
import html
import json
import os
import re
import random
import errno
from pathlib import Path
from urllib.parse import quote_plus
from typing import Union, Sequence, Coroutine, List, Tuple, Optional
import aiofiles
import browser_cookie3
import httpx
import time

from bilix.log import logger


def cors_slice(cors: Sequence[Coroutine], p_range: Sequence[int]):
    h, t = p_range[0] - 1, p_range[1]
    assert 0 <= h <= t
    [cor.close() for idx, cor in enumerate(cors) if idx < h or idx >= t]  # avoid runtime warning
    cors = cors[h:t]
    return cors


async def req_retry(client: httpx.AsyncClient, url_or_urls: Union[str, Sequence[str]], method='GET',
                    follow_redirects=False, retry=5, **kwargs) -> httpx.Response:
    """Client request with multiple backup urls and retry"""
    pre_exc = None  # predefine to avoid warning
    for times in range(1 + retry):
        url = url_or_urls if type(url_or_urls) is str else random.choice(url_or_urls)
        try:
            res = await client.request(method, url, follow_redirects=follow_redirects, **kwargs)
            res.raise_for_status()
        except httpx.TransportError as e:
            msg = f'{method} {e.__class__.__name__} url: {url}'
            logger.warning(msg) if times > 0 else logger.debug(msg)
            pre_exc = e
            await asyncio.sleep(.1 * (times + 1))
        except httpx.HTTPStatusError as e:
            logger.warning(f'{method} {e.response.status_code} {url}')
            pre_exc = e
            await asyncio.sleep(1. * (times + 1))
        except Exception as e:
            logger.warning(f'{method} {e.__class__.__name__} 未知异常 url: {url}')
            raise e
        else:
            return res
    logger.error(f"{method} 超过重复次数 {url_or_urls}")
    raise pre_exc


async def merge_files(file_list: List[Path], new_path: Path):
    first_file = file_list[0]
    async with aiofiles.open(first_file, 'ab') as f:
        for idx in range(1, len(file_list)):
            async with aiofiles.open(file_list[idx], 'rb') as fa:
                await f.write(await fa.read())
            os.remove(file_list[idx])
    os.rename(first_file, new_path)


def legal_title(*parts: str, join_str: str = '-'):
    """
    join several string parts to os illegal file/dir name (no illegal character and not too long).
    auto skip empty.

    :param parts:
    :param join_str: the string to join each part
    :return:
    """
    return join_str.join(filter(lambda x: len(x) > 0, map(replace_illegal, parts)))


def replace_illegal(s: str):
    """strip, unescape html and replace os illegal character in s"""
    s = s.strip()
    s = html.unescape(s)  # handel & "...
    s = re.sub(r"[/\\:*?\"<>|\n]", '', s)  # replace illegal filename character
    return s


def parse_bilibili_url(url: str):
    if re.match(r'https://space\.bilibili\.com/\d+/favlist\?fid=\d+', url):
        return 'fav'
    elif re.match(r'https://space\.bilibili\.com/\d+/channel/seriesdetail\?sid=\d+', url):
        return 'list'
    elif re.match(r'https://space\.bilibili\.com/\d+/channel/collectiondetail\?sid=\d+', url):
        return 'col'
    elif re.match(r'https://space\.bilibili\.com/\d+', url):  # up space url
        return 'up'
    elif re.search(r'www\.bilibili\.com', url):
        return 'video'
    raise ValueError(f'{url} no match for bilibili')


def convert_size(total_bytes: int) -> str:
    unit, suffix = pick_unit_and_suffix(
        total_bytes, ["bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"], 1000
    )
    return f"{total_bytes / unit:,.2f}{suffix}"


def pick_unit_and_suffix(size: int, suffixes: List[str], base: int) -> Tuple[int, str]:
    """Borrowed from rich.filesize. Pick a suffix and base for the given size."""
    for i, suffix in enumerate(suffixes):
        unit = base ** i
        if size < unit * base:
            break
    else:
        raise ValueError('Invalid input')
    return unit, suffix


def parse_bytes_str(s: str) -> float:
    """"Parse a string byte quantity into an integer"""
    units_map = {unit: i for i, unit in enumerate(['', *'KMGTPEZY'])}
    units_re = '|'.join(units_map.keys())
    m = re.fullmatch(rf'(?P<num>\d+(?:\.\d+)?)\s*(?P<unit>{units_re})B?', s)
    if not m:
        raise ValueError(f"Invalid bytes str {s} to parse to number")
    num = float(m.group('num'))
    mult = 1000 ** units_map[m.group('unit')]
    return num * mult


def valid_sess_data(sess_data: Optional[str]) -> str:
    """check and encode sess_data"""
    # url-encoding sess_data if it's not encoded
    # https://github.com/HFrost0/bilix/pull/114https://github.com/HFrost0/bilix/pull/114
    if sess_data and not re.search(r'(%[0-9A-Fa-f]{2})|(\+)', sess_data):
        sess_data = quote_plus(sess_data)
        logger.debug(f"sess_data encoded: {sess_data}")
    return sess_data


def update_cookies_from_browser(client: httpx.AsyncClient, browser: str, domain: str = ""):
    try:
        f = getattr(browser_cookie3, browser.lower())
        a = time.time()
        logger.debug(f"trying to load cookies from {browser}: {domain}, may need auth")
        client.cookies.update(f(domain_name=domain))
        logger.debug(f"load complete, consumed time: {time.time() - a} s")
    except AttributeError:
        raise AttributeError(f"Invalid Browser {browser}")


def t2s(t: int) -> str:
    return str(t)


def s2t(s: str) -> int:
    """
    :param s: hour:minute:second or xx(s) format input
    :return:
    """
    if ':' not in s:
        return int(s)
    h, m, s = map(int, s.split(':'))
    return h * 60 * 60 + m * 60 + s


def json2srt(data: Union[bytes, str, dict]):
    b = False
    if type(data) is bytes:
        data = data.decode('utf-8')
        b = True
    if type(data) is str:
        data = json.loads(data)

    def t2str(t):
        ms = int(round(t % 1, 3) * 1000)
        s = int(t)
        m = s // 60
        h = m // 60
        m, s = m % 60, s % 60
        t_str = f'{h:0>2}:{m:0>2}:{s:0>2},{ms:0>3}'
        return t_str

    res = ''
    for idx, i in enumerate(data['body']):
        from_time, to_time = t2str(i['from']), t2str(i['to'])
        content = i['content']
        res += f"{idx + 1}\n{from_time} --> {to_time}\n{content}\n\n"
    return res.encode('utf-8') if b else res


def eclipse_str(s: str, max_len: int = 100):
    if len(s) <= max_len:
        return s
    else:
        half_len = (max_len - 1) // 2
        return f"{s[:half_len]}…{s[-half_len:]}"


def path_check(path: Path, retry: int = 100) -> Tuple[bool, Path]:
    """
    check whether path exist, if filename too long, truncate and return valid path

    :param path: path to check
    :param retry: max retry times
    :return: exist, path
    """
    for times in range(retry):
        try:
            exist = path.exists()
            return exist, path
        except OSError as e:
            if e.errno == errno.ENAMETOOLONG:  # filename too long for os
                if times == 0:
                    logger.warning(f"filename too long for os, truncate will be applied. filename: {path.name}")
                else:
                    logger.debug(f"filename too long for os {path.name}")
                path = path.with_stem(eclipse_str(path.stem, int(len(path.stem) * .8)))
            else:
                raise e
    raise OSError(f"filename too long for os {path.name}")
