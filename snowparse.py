#from html.parser import HTMLParser
from HTMLParser import HTMLParser
class SnowHTMLParser(HTMLParser): 
    def __init__(self): 
        HTMLParser.__init__(self) 
        self.links = [] 
        self.istext = False
        self.texts = []
        
    def handle_starttag(self, tag, attrs): 
        print "Encountered the beginning of a %s tag" % tag 
        self.istext = True 
        if tag == "a": 
            if len(attrs) == 0: 
                pass 
            else: 
                for (variable, value) in attrs: 
                    if variable == "href": 
                        self.links.append(value) 
                   
              
    def handle_endtag(self,tag):  
        if tag == 'a':  
            self.istext = False  
              
    def handle_data(self,data):  
        if self.istext:  
            #print (data) 
            self.texts.append(data) 
            
if __name__ == "__main__": 
    html_code = """ <a href="www.google.com"> google.com</a> <A Href="www.pythonclub.org"> PythonClub </a> <A HREF = "www.sina.com.cn"> Sina </a> """ 
    hp = SnowHTMLParser() 
    hp.feed(html_code) 
    hp.close() 
    print(hp.links)
    print(hp.texts)
