"""Simple Web Crawler"""
import re
import pprint
import requests
from string import digits


class HayStack:
    """Haystack class"""
    def __init__(self, url, search_depth=3):
        """Constructor"""
        self.url = url
        self.search_depth = search_depth
        self.ranks = {}
        self.index = {}
        self.graph = {}
        self.current_level = 0
        self.visited = set()
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                          " Chrome/51.0.2704.103 Safari/537.36"
        self.test()

    def test(self):
        """Function to start the crawling process"""
        r = requests.get(self.url, headers={"User-Agent": self.user_agent}, timeout=5)
        self.crawl(self.url, self.search_depth)

    def lookup(self, keyword):
        """Lookup method"""
        keyword_lower = keyword.lower()
        url_list = []
        if keyword_lower in self.index:
            for url in self.index[keyword_lower]:
                url_list.append(url)
        url_list = sorted(url_list, key=self.ranks.get, reverse=True)
        return url_list

    def get_page_content(self, url):
        """Function to get the html content from url"""
        html = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=5)
        html_content = html.content.decode('latin-1')
        non_tag_list = re.sub('<.*?>|\n|\t|\.|\(|\)|&|"|,|:|-|;', ' ', html_content)
        digits_check = non_tag_list.maketrans('', '', digits)
        non_tag_list = non_tag_list.translate(digits_check)
        non_tag_list = non_tag_list.lower().split(' ')
        word_list = [i for i in non_tag_list if i]
        for w in word_list:
            try:
                self.index[w].add(url)
            except KeyError:
                self.index[w] = {url}
        return html_content

    def crawl(self, url, depth):
        """Function to crawl the child pages"""
        for link in self.get_child_links(url):
            if link in self.visited:
                continue
            self.visited.add(link)
            if self.current_level > depth:
                break
            self.crawl(link, depth)
            self.current_level += 1
        self.compute_ranks(self.graph)

    def get_child_links(self, url):
        """Function to get the links from the page"""
        html = self.get_page_content(url)
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href\s*=\s*"([^"]*)"''', html)
        for i, link in enumerate(links):
            try:
                self.graph[url].add(link)
            except KeyError:
                self.graph[url] = {link}
        return self.graph[url]

    def compute_ranks(self, graph):
        """Function to calculate ranks for pages"""
        d = 0.85  # probability that surfer will bail
        num_loops = 10
        ranks = {}
        n_pages = len(graph)
        for page in graph:
            ranks[page] = 1.0 / n_pages
        for i in range(0, num_loops):
            new_ranks = {}
            for page in graph:
                new_rank = (1 - d) / n_pages
                for url in graph:
                    if page in graph[url]:
                        new_rank += d * ranks[url] / len(graph[url])
                new_ranks[page] = new_rank
            ranks = new_ranks
        self.ranks = ranks


"""Driver code"""
if __name__ == '__main__':
    engine = HayStack('http://freshsources.com/page1.html', 4)
    for w in ['pages', 'links', 'you', 'have', 'I']:
        print(w)
        pprint.pprint(engine.lookup(w))
    print()
    print('index:')
    pprint.pprint(engine.index)
    print()
    print('graph:')
    pprint.pprint(engine.graph)
    print()
    print('ranks:')
    pprint.pprint(engine.ranks)
