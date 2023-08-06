from TheSilent.clear import clear
from TheSilent.sql_injection_scanner import sql_injection_scanner
from TheSilent.xss_scanner import xss_scanner

CYAN = "\033[1;36m"

# scans for all security flaws


def security_scanner(url, secure=True, tor=False, my_file=" ", crawl="0", parse=" ", delay=1):
    clear()

    my_sql_injection_scanner = sql_injection_scanner(
        url=url,
        secure=secure,
        tor=tor,
        my_file=my_file,
        crawl=crawl,
        parse=parse,
        delay=delay)
    my_xss_scanner = xss_scanner(
        url=url,
        secure=secure,
        tor=tor,
        my_file=my_file,
        crawl=crawl,
        parse=parse,
        delay=delay)

    clear()

    print(CYAN + "sql injection:")

    for i in my_sql_injection_scanner:
        print(CYAN + i)

    print("")
    print(CYAN + "xss:")

    for i in my_xss_scanner:
        print(CYAN + i)
