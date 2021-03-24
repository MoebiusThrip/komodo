# komodos.py for monitoring website comments

# import reload
from importlib import reload

# import requests
import requests

# import beautiful soup
from bs4 import BeautifulSoup as Soup


# create class Komodo for monitoring a website
class Komodo(list):
    """Komodo class to monitor website comments.

    Inherits from:
        list
    """

    def __init__(self, url):
        """Initialize a Komodo instance with a root url.

        Arguments:
            url: str
        """

        # set url
        self.url = url

        # cook soup
        self.soup = None
        self._cook()

        return None

    def _cook(self, word='comments'):
        """Cook the soup from the main url and get all links.

        Arguments:
            word: str, keyword for links

        Returns:
            None

        Populates:
            self.soup
        """

        # print status
        print('scraping {} for comments...'.format(self.url))

        # make soup from request
        request = requests.get(self.url)
        soup = Soup(request.content, features='html.parser')
        self.soup = soup

        # get all comment links
        links = soup.find_all('a', href=True)
        comments = [link for link in links if word in link.text.lower()]

        # get text from all comments
        for comment in comments:

            # make url
            url = self.url + comment['href']

            # get text from requests
            requestii = requests.get(url)
            soupii = Soup(requestii.content, features='html.parser')
            text = soupii.get_text().replace('\n', '')

            # populate
            self.append(text)

        return None

    def monitor(self, search):
        """Check for instances of a word.

        Arguments:
            search: str

        Returns:
            None
        """

        # get subset of texts with word
        posts = [post for post in self if search.lower() in post.lower()]

        # reverse to get most recent last
        posts.reverse()

        # begin grand comment total
        grand = 0

        # print each post, highlighting word
        for index, post in enumerate(posts):

            # delimiter is not unicode!  (not plain hyphen)
            delimiter = '[–]'

            # split the post into comments and go through each
            comments = post.split(delimiter)
            total = len([comment for comment in comments if search.lower() in comment.lower()])
            grand += total
            for indexii, comment in enumerate(comments):

                # check for presence of word
                if search.lower() in comment:

                    # highlight the word
                    highlighting = lambda word: '\n\n[!!!  *** {} ***   !!!]\n\n'.format(word) if search.lower() in word.lower() else word
                    highlights = [highlighting(word) for word in comment.split(' ')]
                    text = ' '.join(highlights)

                    # print
                    print('\n\n\n\ncomment {} of {} in post {} of {}...\n'.format(indexii, len(comments), index, len(posts)))
                    print(text)

        # print grand total total
        print('\n{} total comments with -{}- over {} posts'.format(grand, search, len(posts)))

        return None


# set up instance
# import komodos as kom; komo = kom.komodo;
komodo = Komodo('https://ovarit.com')





