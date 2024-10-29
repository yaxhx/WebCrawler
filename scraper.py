import requests
import argparse
from termcolor import colored
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin

class WebCrawler:
    def __init__(self, url, max_depth):
        self.url = url
        self.max_depth = max_depth
        self.subdomains = set()
        self.links = set()
        self.jsfiles = set()

    def start_crawling(self):
        self.crawl(self.url, depth=1)

    def crawl(self, url, depth):
        if depth > self.max_depth: # if true
            return                 # the program exits with "return"
        try:
            response = requests.get(url, timeout=3, allow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')

        except requests.exceptions.RequestException as err:
            print(f"[-] A fuckin error occured: {err}")
            return                          #similarly here if err occurs, it exits
        
        subdomain_query = fr"https?://([a-zA-Z0-9.-]+)"
        for link in soup.find_all('a'):
            link_text = link.get('href')
            if link_text:
                if re.match(subdomain_query, link_text) and link_text not in self.subdomains:
                    self.subdomains.add(link_text)
                else:
                    full_link = urljoin(url, link_text)
                    if full_link != url and full_link not in self.links:
                        self.links.add(full_link)
                        self.crawl(full_link, depth + 1)

        for file in soup.find_all('script'):
            script_src = file.get('src')
            if script_src:
                self.jsfiles.add(script_src)




    def print_banner(self):
        print("-" * 80)
        print(colored(f"Recursive Spider starting at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", "cyan", attrs=['bold']))
        print("-" * 80)
        print(f"[*] URL".ljust(20, " "), ":", self.url)
        print(f"[*] Max Depth".ljust(20, " "), ":", self.max_depth)
        print("-" * 80)

    def print_results(self):
        if self.subdomains:
            for subdomain in self.subdomains:
                print(f"[+] Subdomains : {subdomain}")
        print()

        if self.links:
            for link in self.links:
                print(f"[+] Links : {link}")
        print()

        if self.jsfiles:
            for file in self.jsfiles:
                print(f"[+] JsFiles : {file}")


def get_args():
        parser = argparse.ArgumentParser()

        # -u accepts a url, which the user wants to scan
        parser.add_argument('-u', '--url', dest='url', help="Specify the url, provide it along http or https", required=True)

        # -d to define the recursive limit
        parser.add_argument('--d', '--depth', dest='depth', type=int, default=1, help="Specify the recursion depth limit")

        return parser.parse_args()    



#indentation is the key!!!!!!!!


if __name__ == "__main__":
    args = get_args()
    web_crawler = WebCrawler(args.url, args.depth)
    web_crawler.print_banner()
    web_crawler.start_crawling()
    web_crawler.print_results()