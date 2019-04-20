import urllib.parse
import urllib.request
import http.cookiejar
from selenium import webdriver
from urllib.request import urlopen 
from bs4 import BeautifulSoup

from . import helper

# Global variables
CACHE       = 3 # minutes
url_tnw      = 'https://thenextweb.com/artificial-intelligence/'
url_bb      = 'https://www.bloomberg.com/topics/artificial-intelligence'

raw_html_tnw    = 'tmp/tnw.html'
raw_html_bb    = 'tmp/bb.html'
source_html = 'html/source.html'
dest_html = 'html/index.html'


def write_webpage_as_html(source = source_html, dest = dest_html, data=''):
    if data is '':
         data = ''
    
    helper.write_webpage_as_html(source = source_html, dest = dest_html, data = data)


class Tnw:
    _url   = ''
    _data  = ''
    _log  = None
    _soup  = None 
    
    def __init__(self, url, log):
        self._url  = url 
        self._log = log 
    
    def retrieve_webpage(self):
        try:
            html = urlopen(self._url)
        except Exception as e:
            print (e)
            self._log.report(str(e))
        else:
            self._data = html.read()
            if len(self._data) > 0:
                print ("Thenextweb Retrieved successfully")
            
    def read_webpage_from_html(self, filepath=raw_html_tnw):
        self._data = helper.read_webpage_from_html(filepath)
            
    def change_url(self, url):
        self._url = url
            
    def print_data(self):
        print (self._data)
    
    def convert_data_to_bs4(self):
        self._soup = BeautifulSoup(self._data, "html.parser")
        
    def parse_soup_to_simple_html(self):
        news_list = self._soup.find_all(['h2', 'h4']) # h1
        
        #print (news_list)
        
        htmltext = '''
        		<!-- One -->
			<section id="one" class="wrapper style2">
				<div class="inner">
					<div class="grid-style">

						<div>
							<div class="box">
								<div class="image fit">
									<img src="images/tnw-website-review.jpg" alt="" />
								</div>
								<div class="content">
									<header class="align-center">
										<p>Thenextweb</p>
										<h2>Top 10 AI-related news today</h2>
									</header>
									<p>
        {NEWS_LINKS}
        </p>
									
								</div>
							</div>
						</div>
        
        '''
        
        news_links = ''
        count = 0
        for tag in news_list:
            #print (tag.string, "    ", tag.get('href'))
            if tag.a != None:
                #print (self._url + tag.parent.get('href'), tag.string)
                #print(tag.a.string.strip(),'\n', tag.a['href'])
                if(count == 10):
                    break
                link  = tag.a['href']
                title = tag.a.string.strip()
                news_links += "<li ><a href='{}' target='_blank'>{}</a></li>\n".format(link, title)
                count+=1
        htmltext = htmltext.format(NEWS_LINKS=news_links)
        
        return htmltext
        # print(htmltext)
        #self.write_webpage_as_html(filepath=output_html, data=htmltext.encode())
  


class Bb:
    _url   = ''
    _data  = ''
    _log  = None
    _soup  = None 
    
    def __init__(self, url, log):
        self._url  = url 
        self._log = log 
    
    def retrieve_webpage(self):
        try:
            browser = webdriver.Chrome()
            proxy = webdriver.Proxy()
            proxy.http_proxy = '127.0.0.1:1080'
            proxy.add_to_capabilities(webdriver.DesiredCapabilities.CHROME)
            browser.start_session(webdriver.DesiredCapabilities.CHROME)
            browser.get(self._url)
            with open(raw_html_bb, 'w', encoding='UTF-8') as fobj:
                fobj.write(browser.page_source)
            #html = urlopen(browser.page_source)
            print ("Bloomberg Retrieved successfully")
        except Exception as e:
            print (e)
            self._log.report(str(e))
        # else:
        #     self._data = html.read()
        #     if len(self._data) > 0:
        #         print ("Retrieved successfully")
            
            
    def read_webpage_from_html(self, filepath=raw_html_bb):
        self._data = helper.read_webpage_from_html(filepath)
            
    def change_url(self, url):
        self._url = url
            
    def print_data(self):
        print (self._data)
    
    def convert_data_to_bs4(self):
        self._soup = BeautifulSoup(self._data, "html.parser")
        
    def parse_soup_to_simple_html(self):
        news_list = self._soup.find_all(['h2', 'h4']) # h1
        
        #print (news_list)
        
        htmltext = '''
        <div>
							<div class="box">
								<div class="image fit">
									<img src="images/bloomberg-technology-logo.png" alt="" />
								</div>
								<div class="content">
									<header class="align-center">
										<p>Bloomberg</p>
										<h2>Top 10 AI-related news today</h2>
									</header>
									<p>
        {NEWS_LINKS}
        </p>
									
								</div>
							</div>
						</div>

					</div>
				</div>
			</section>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>
        '''
        
        news_links = ''
        count = 0
        for tag in news_list:
            #print (tag.string, "    ", tag.get('href'))
            if tag.parent.get('href'):
                if(count == 10):
                    break
                #print (self._url + tag.parent.get('href'), tag.string)
                #print(tag.a.string.strip(),'\n', tag.a['href'])
                link  = "https://www.bloomberg.com" + tag.parent.get('href')
                title = tag.string
                news_links += "<li ><a href='{}' target='_blank'>{}</a></li>\n".format(link, title)
                count+=1
                
        htmltext = htmltext.format(NEWS_LINKS=news_links)
        
        return htmltext


  