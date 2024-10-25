import argparse
import ftplib
import socket
import urllib.request
from clear import clear

CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RED = "\033[1;31m"

def pycobra():
    clear()
    parser = argparse.ArgumentParser()
    parser.add_argument("-host", required = True)
    args = parser.parse_args()

    hits = []
    methods = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "TRACE"]

    print(f"{CYAN}checking: {args.host}")

    dns = socket.getfqdn(args.host)
    hits.append(dns)

    try:
        ftp_client = ftplib.FTP(args.host, timeout = 10)
        ftp_client.login()
        ftp_client.quit()
        hits.append("ANONYMOUS FTP ALLOWED")

    except:
        pass

    try:
        ftp_client = ftplib.FTP_TLS(args.host, timeout = 10)
        ftp_client.login()
        ftp_client.quit()
        hits.append("ANONYMOUS FTP TLS ALLOWED")

    except:
        pass

    ssl_support = False
    try:
        my_request = urllib.request.Request(f"https://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "GET")
        my_request = urllib.request.urlopen(my_request, timeout = 10)
        ssl_support = True

    except:
        pass

    if ssl_support:
        try:
            my_request = urllib.request.Request(f"https://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "GET")
            my_request = urllib.request.urlopen(my_request, timeout = 10).headers
            banner = my_request["server"]
            hits.append(f"WEB BANNER {banner}")

        except:
            pass

    else:
        try:
            my_request = urllib.request.Request(f"http://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "GET")
            my_request = urllib.request.urlopen(my_request, timeout = 10).headers
            banner = my_request["server"]
            hits.append(f"WEB BANNER {banner}")

        except:
            pass

    for i in methods:
        if ssl_support:
            try:
                my_request = urllib.request.Request(f"https://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = i)
                my_request = urllib.request.urlopen(my_request, timeout = 10)
                hits.append(f"{i} METHOD ALLOWED")

            except:
                pass

        else:
            try:
                my_request = urllib.request.Request(f"http://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = i)
                my_request = urllib.request.urlopen(my_request, timeout = 10)
                hits.append(f"{i} METHOD ALLOWED")

            except:
                pass

    if ssl_support:
        try:
            my_request = urllib.request.Request(f"https://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "*")
            my_request = urllib.request.urlopen(my_request, timeout = 10)
            hits.append("ANY METHOD ALLOWED")

        except:
            pass

    else:
        try:
            my_request = urllib.request.Request(f"http://{args.host}", headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}, unverifiable = True, method = "*")
            my_request = urllib.request.urlopen(my_request, timeout = 10)
            hits.append("ANY METHOD ALLOWED")

        except:
            pass

    clear()
    
    if len(hits) > 0:
        for hit in hits:
            print(f"{RED}{hit}")

    else:
        print(f"{GREEN}We didn't find anything interesting!")

if __name__ == "__main__":
    pycobra()
