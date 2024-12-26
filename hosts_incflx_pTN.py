import asyncio
import time
import requests
from bs4 import BeautifulSoup
from base64 import b64decode
from urllib.error import HTTPError
import aiofiles as aiofiles


def gethtml(url="https://www.incestflix.com/", r=requests.Session()):
    H = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    r.headers = H
    print("User-Agent Sent:%s" % (H['User-Agent']))
    with r.get(url) as response:
        return response.content


def incflx_ads_urls(url="https://www.incestflix.com/", indx=0, r=requests.Session()):
    arr_script = BeautifulSoup(gethtml(url), 'html.parser').find_all('script')
    arr_script = arr_script[indx]
    q = arr_script.string.split("+atob(")
    if len(q) > 1:
        q = q[1]
    else:
        return exit("no atob found")
    var_containing_atobs = q.split('[')[0]
    st = arr_script.string.split('],' + var_containing_atobs + '=[')
    st = st[1] if len(st) > 1 else st[0]
    atobs = st.split(']')[0].split(",")
    S = set()
    for x in atobs:
        t = str(b64decode(x)).split('/')[0]
        if t[0] == 'b' and t[1] == "'":
            t = t[2:len(t)]
        tt = t.split("www.")
        tt = tt[1] if isinstance(tt, list) and len(tt) > 1 else tt[0]
        S.add(str(tt))
    return S


async def print_waiting():
    for i in range(100000):
        if i % 2:
            print(f"\r... Waiting for download to start\t", end='\r')
        else:
            print(f"\r. Waiting for download to start  \t", end='\r')
        await asyncio.sleep(0.27387)
    return


def _print_progressbar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (atob.g. "\r", "\r\n") (Str)
    """
    try:
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    except ZeroDivisionError:
        print('tried dividing by zero, made total 100')
        total = 100
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def wait(_ttl=1):
    print(f"waiting {_ttl} seconds.")
    _print_progressbar(0, _ttl, prefix='Progress:', suffix='Complete', length=50, fill='>')
    for i in range(_ttl):
        time.sleep(1)
        _print_progressbar(i + 1, _ttl, prefix='Progress:', suffix='Complete', length=50, fill='>')


def write_to_hosts(s="", filename="C:\\Windows\\System32\\drivers\\etc\\hosts"):
    while True:
        try:
            with open(filename, 'a') as f:  # append sorted_set STR to file
                r = f.write(s)
                bool_written = True if r > 1 else False
                if bool_written:
                    print(f"\t written to {filename} : {r:10} chars")
                    return bool_written
                else:
                    print('nothing written for some reason, trying again')
                    wait(3)
        except PermissionError as err:
            print('no Permission; \terror code: ' + str(err.errno))
            wait(15)
            print("trying again")


async def tail(_file, lines=100):
    async with aiofiles.open(_file, 'rb') as x:
        total_lines_wanted = lines
        block_size = 1024
        await x.seek(0, 2)
        block_end_byte = await x.tell()
        lines_to_go = total_lines_wanted
        block_number = -1
        blocks = []
        while lines_to_go > 0 and block_end_byte > 0:
            if block_end_byte - block_size > 0:
                await x.seek(block_number * block_size, 2)
                blocks.append(await x.read(block_size))
            else:
                await x.seek(0, 0)
                blocks.append(await x.read(block_end_byte))
            lines_found = blocks[-1].count(b'\n')
            lines_to_go -= lines_found
            block_end_byte -= block_size
            block_number -= 1  #
        all_read_text = b''.join(reversed(blocks))
        return b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:])


async def set_tail_from_hosts(_filename="C:\\Windows\\System32\\drivers\\etc\\hosts",
                              _number_of_lines=250000, split_char='\n'):
    tail_split_by_enter = await tail(_filename, _number_of_lines)
    tail_split_by_enter = set(tail_split_by_enter.decode('utf-8').split(split_char))
    successful_split = set()
    rejected = set()
    g = set()
    print('\n>>>> Building unique array from last %d from HOSTS°:' % _number_of_lines)
    for x in tail_split_by_enter:
        for xx in set(filter(None, x.split('#'))):
            if '0.0.0.0 ' in xx:
                for split_by_ip in set(filter(None, xx.split('0.0.0.0 '))):
                    for split_by_www in set(filter(None, split_by_ip.split("www."))):
                        if len(split_by_www) > 1:
                            successful_split.add(split_by_www)
                        else:
                            rejected.add(split_by_www)
            else:
                rejected.add(xx)
    if len(rejected) > 0:
        print("\nREJECTED: \n" + str(rejected) + "\nlenght of rejected items= " + str(len(rejected)))
    else:
        print('No Rejected lines. #succes: ' + str(len(successful_split)))
    return [successful_split, rejected]


def main():
    global_tail_set = set()
    try:
        loop = asyncio.get_event_loop()
        _waiting = asyncio.ensure_future(print_waiting())
        result_urls = loop.run_until_complete(set_tail_from_hosts())
        set_from_tail = result_urls[0]
        print("\n" + str(_waiting.cancel()))
        strwth = ''
        with requests.Session() as req:
            incflxSet = incflx_ads_urls('https://www.incestflix.com', 0, req)
            incflxSet = incflxSet | incflx_ads_urls('https://porntn.com', 1, req)
            for v in incflxSet:
                if v not in set_from_tail:
                    strwth += "\n0.0.0.0 " + v
                    global_tail_set = global_tail_set | set(v)
        if strwth is not '':
            write_to_hosts(strwth)
            print("written to hosts: " + strwth)
        else:
            print('nothing new found')
        exit('TRIAL; only add these 4')
    except HTTPError as err:
        exit("HTTP.error...122")
    except OSError:
        print('error reading file')
        exit("420")


main()
