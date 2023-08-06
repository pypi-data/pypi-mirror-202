from neosekai_api.novel import Novel
import requests
from bs4 import BeautifulSoup


class NovelChapter:
    '''
    NovelChapter object

    :params _url : The Mangadex Chapter URL
    '''

    def __init__(self, _url: str) -> None:
        self.url = self.__urlformatter(_url)
        self.__response_object = requests.get(self.url, timeout=10)
        self.details = self.chapter_details()
        self.volume = self.details['volume']
        self.name = self.details['chapter_name']
        self.release_date = self.details['release_date']

    def __urlformatter(self, _url):
        """
        formats url to standard form to be used in the program
        """
        __url = ''
        if 'https://' not in _url:
            _url == 'https://' + _url
        else:
            return _url

    def chapter_details(self):
        """
        returns chapter details : 

        - chapter volume
        - chapter name
        - url
        - chapter release date

        In the given order in JSON format

        """
        novel_url = self.url[:self.url.index('/', 43)]
        novel = Novel(novel_url)
        index_page = novel.get_index_page()
        for i in index_page:
            if index_page[i]['url'] == self.url:
                return index_page[i]

    def get_chapter_content(self):
        """
        returns main chapter content in JSON format

        JSON format:
        ```json
            {
                "1" : {
                    "type" : '...', "content" : '...'
                }
            }
        ```
        - each key will be a paragraph
        - ```type```  can have a value of ```text``` for textual content
        - ```type``` can have a value of ```img``` if the content is an image. link to the image will be provided in ```content```

        """
        soup = BeautifulSoup(self.__response_object.text, 'lxml')
        div = soup.find('div', attrs={'class': 'text-left'})
        paras = div.find_all('p')
        content = {}
        n = 1
        for i in paras:
            if i.span != None:
                content[str(n)] = {'type': 'text',
                                   'content': i.span.text.strip()}
                n += 1
            elif i.img != None:
                content[str(n)] = {'type': 'img', 'content': i.img['src']}
                n += 1
            else:
                continue
        return content
