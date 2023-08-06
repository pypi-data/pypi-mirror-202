import re
import time
import requests
from TheSilent.clear import clear
from TheSilent.link_scanner import link_scanner
from TheSilent.return_user_agent import return_user_agent

CYAN = "\033[1;36m"
RED = "\033[1;31m"

# create html sessions object
web_session = requests.Session()

tor_proxy = {
    "http": "socks5h://localhost:9050",
    "https": "socks5h://localhost:9050"}

# increased security
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

# increased security
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"

except AttributeError:
    pass

def html_lint(url, secure=True, crawl="all", delay=1, tor=False, parse=""):
    clear()

    linted = []
    
    crawler = link_scanner(url, secure=secure, crawl=crawl, delay=delay, tor=tor, parse=parse)

    for crawl in crawler:
        print(CYAN + "checking: " + crawl)
        # prevent dos attacks
        time.sleep(delay)

        try:
            if tor:
                result = web_session.get(crawl, verify=False, headers={"User-Agent": return_user_agent()}, proxies=tor_proxy, timeout=(60,120)).text.lower()

            else:
                result = web_session.get(crawl, verify=False, headers={"User-Agent": return_user_agent()}, timeout=(5,30)).text.lower()

            image_tag = re.findall("<img.+>", result)

            for image in image_tag:
                if "alt" not in image:
                    print(RED + f"no alt in img tag detected on {crawl}. Consider using alt (accessibility).")
                    linted.append(f"no alt in img tag detected on {crawl}. Consider using alt (accessibility).")

            if "<b>" in result:
                print(RED + f"<b> detected on {crawl}. Consider using <strong> (accessibility).")
                linted.append(f"<b> detected on {crawl}. Consider using <strong> (accessibility).")

            if "document.write" in result:
                print(RED + f"document.write detected on {crawl}. This has weird behavior (weird).")
                linted.append(f"document.write detected on {crawl}. This has weird behavior (weird).")

            if "<i>" in result:
                print(RED + f"<i> detected on {crawl}. Consider using <em> (accessibility).")
                linted.append(f"<i> detected on {crawl}. Consider using <em> (accessibility).")

            if "innerhtml" in result:
                print(RED + f"innerhtml detected on {crawl}. This could lead to a security vulnerability (security).")
                linted.append(f"innerhtml detected on {crawl}. This could lead to a security vulnerability (security).")

        except:
            continue

    linted = list(set(linted))
    linted.sort()
    clear()

    if len(linted) == 0:
        print(CYAN + "No problems deteced!")

    else:
        for lint in linted:
            print(RED + lint)
