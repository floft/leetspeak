#for everything
import sqlite3
#for creating the database
import xml.sax,time
#for webserver
import pickle,os,re
from Dictionary import Dictionary
from urllib.parse import unquote_plus
from http.server import HTTPServer, BaseHTTPRequestHandler

#another example which completely skips the DTD, thus working w/o internet (taken from: http://silveiraneto.net/2009/12/25/python-fast-xml-parsing/)
#import xml.parsers.expat

# 3 handler functions
#def start_element(name, attrs):
#    print 'Start element:', name, attrs
#def end_element(name):
#    print 'End element:', name
#def char_data(data):
#    print 'Character data:', repr(data)

#p = xml.parsers.expat.ParserCreate()

#p.StartElementHandler = start_element
#p.EndElementHandler = end_element
#p.CharacterDataHandler = char_data

#p.Parse("""<?xml version="1.0"?>
#<parent id="top"><child1 name="paul">Text goes here</child1>
#<child2 name="fred">More text</child2>
#</parent>""", 1)

articles=[]
currentpage=0
dblocation="/home/garrett/Downloads/Websites/wikipedia.db"

def save_articles(connection):
    global articles,currentpage
    
    if len(articles) > 0:
        percent=currentpage/10610374*100
        print(percent,"%      ",articles[0][2])
        connection.executemany("insert into wikiarticles(id,timestamp,title,content) values (?,?,?,?)",articles)
        connection.commit()
    
    articles=[]

#xpath: http://w3schools.com/xpath/xpath_syntax.asp (used with "import lxml.etree"... see wopto.net/stuff/pydive)
#help from: http://www.devshed.com/c/a/Python/Working-with-XML-Documents-and-Python/1/
class HandleCollection(xml.sax.ContentHandler):
    def __init__(self,dbconnection):
        self.pageid=""
        self.pagetitle=""
        self.pagetext=""
        self.pagetime=""
        self.id=False
        self.title=False
        self.text=False
        self.time=False
        self.connection=dbconnection
            
    def ValidTitle(self):
        """
        Quickly scan the title of the article to make sure it isn't one of the useless pages.
        """
        skip_pages=["Media","Special","Talk","User","User talk","Wikipedia","Wikipedia talk","File","File talk","MediaWiki","MediaWiki talk","Template","Template talk","Help","Help talk","Category","Category talk","Portal","Portal talk","Book","Book talk"]
        title_elements=self.pagetitle.split(":")
        
        if len(title_elements) > 1 and title_elements[0].strip() in skip_pages:
            return False
        else:
            return True
    
    def ValidPage(self):
        """
        Verify that the page isn't just a redirect.
        """
        if self.pagetext[0:9] == "#REDIRECT" or len(self.pagetext) == 0:
            return False
        else:
            return True
    
    def startElement(self,name,attributes):
        if name=='id':
            self.id=True
        elif name=='title':
            self.title=True
        elif name=='text':
            self.text=True
        elif name=='timestamp':
            self.time=True
            
        #if name=='track':
        #   self.artist=attributes.getValue('artist')
    
    def endElement(self,name):
        global articles,currentpage
        
        if name=='page':
            currentpage+=1
            
            #strip extra stuff from the text
            self.pagetext=self.pagetext.strip()
            
            #see if this is a page I want to add to the database; if it is, convert the timestamp to unix time
            if self.ValidTitle() and self.ValidPage() and len(self.pageid) > 0:
                article_time=int(time.mktime(time.strptime(self.pagetime,"%Y-%m-%dT%H:%M:%SZ")))
                
                if article_time > 0:
                    articles.append((self.pageid,article_time,self.pagetitle,self.pagetext))
            
            self.pageid=""
            self.pagetitle=""
            self.pagetext=""
            self.pagetime=""
            
            #save to the database every certian number of articles
            if currentpage%5000==0:
                save_articles(self.connection)
        elif name=='id':
            self.id=False
        elif name=='title':
            self.title=False
        elif name=='text':
            self.text=False
        elif name=='timestamp':
            self.time=False
        
    def characters(self,content):
        if self.id:
            self.pageid+=content.strip()
        elif self.title:
            self.pagetitle+=content.strip()
        elif self.text:
            self.pagetext+=content
        elif self.time:
            self.pagetime+=content.strip()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global wikipedia
        
        page=unquote_plus(self.path[1:])
        response=wikipedia.GetPage(page)
        
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

class Wikipedia:
    def __init__(self,db="data/fulltext.db",titles_txt="data/wikipedia_titles.txt",titles_pickled="data/wikipedia_titles.pickle"):
        self.xml=""
        self.database=db
        self.connection=False
        self.titles=[]
        self.titles_txt=titles_txt
        self.titles_pickled=titles_pickled
        self.Load()
        self.LoadTitles()
        
    def create_database():
        self.connection.execute("create table if not exists wikiarticles(id int,timestamp int,title text,content text)")
    
        #parse the wikipedia document
        parser=xml.sax.make_parser()
        parser.setContentHandler(HandleCollection(self.connection))
        parser.parse('/home/garrett/Downloads/Websites/enwiki-latest-pages-articles-20101220.xml')
        
        #save the last few to the database
        save_articles(self.connection)
        
    def create_fulltextsearch():
        #create full-text database
        insert=[]
        fulltext=sqlite3.connect("data/fulltext.db")
        wikipedia=sqlite3.connect("data/wikipedia.db")
        fulltext.execute("create virtual table wikiarticles using fts4(id int,timestamp int,title text,content text)")
        
        i=0
        for row in wikipedia.execute("select id,timestamp,title,content from wikiarticles"):
            insert.append((row[0],row[1],row[2],row[3]))
            
            #print cool message
            i+=1
            if i%20000==0:
                addit()
                print(i/3992949*100,"%    ",row[2])
        
        wikipedia.close()
        fulltext.close()
        
    def GetPage(self,title):
        page=""
        
        if title in self.titles:
        #for i in self.connection.execute("select content from wikiarticles where title match '\"?\"' limit 1", (title,)):
            #for i in self.connection.execute("select content from wikiarticles where title in (select title from wikiarticles where title match ? limit 1) and title = ? limit 1",(title,title)):
            for i in self.connection.execute("select content from wikiarticles where title match ? limit 1",(title,)):
                page+=i[0]
        
        if page=="":
            page="<html><head><title>Page Not Found</title></head><body><h1>Page Not Found</h1><p>The page you have requested was not found in the Wikipedia database.</p></body></html>"
        else:
            #remove excess line returns
            page=bytes(page,'utf-8').decode('ascii', 'ignore').strip()
            #remove junk
            page=re.sub(r"==External links==(.|\n)*","",page)
            page=re.sub(r"\{\{?[^\}\{]*\}\}?","",page)
            page=re.sub(r"\{\{?[^\}\{]*\}\}?","",page)
            page=re.sub(r"\</?ref\>","",page)
            page=re.sub(r"\<\!\-\-[^\>]*\-\-\>","",page)
            #links
            page=re.sub(r"\[\[([^\]]*?)\|(.*?)\]\]","<a href='\\1'>\\2</a>",page)
            page=re.sub(r"\[\[(.*?)\]\]","<a href='\\1'>\\1</a>",page)
            #formating
            page=re.sub(r"'''(.*?)'''","<b>\\1</b>",page)
            page=re.sub(r"''(.*?)''","<i>\\1</i>",page)
            page=re.sub(r"====([^\<\>]*?)====","<h4>\\1</h4>",page)
            page=re.sub(r"===([^\<\>]*?)===","<h3>\\1</h3>",page)
            page=re.sub(r"==([^\<\>]*?)==","<h2>\\1</h2>",page)
            #sources
            page=re.sub(r"\[([^\] ]*) ([^\]]*)\]"," <sup><small>[<a href='\\1'>\\2</a>]</small></sup> ",page)
            
            #line returns
            #old way: page=re.sub(r"\n+","<br />",page)
            new_page=""
            
            for part in page.split("\n\n"):
                line=part.strip()
                if len(line) > 0:
                    new_page+="<p>"+line+"</p>"
            
            page="<html><head><title>"+title+"</title></head><body><h1>"+title+"</h1>"+new_page+"</body></html>"
        
        return page
    
    def Load(self):
        self.connection=sqlite3.connect(self.database)
    
    def LoadTitles(self):
        #load them from disk
        if os.path.exists(self.titles_pickled):
            print("Loading from pickle.")
            with open(self.titles_pickled, 'rb') as infile:
                self.titles=pickle.load(infile)
        else:
            print("Creating the pickle.")
            #load them
            with open(self.titles_txt) as infile:
                for line in infile:
                    self.titles.append(line.strip())
            
            #save to disk
            if len(self.titles) > 0:
                with open(self.titles_pickled, 'wb') as outfile:
                        pickle.dump(self.titles, outfile)
    
    def Close(self):
        self.connection.close()
    
    def SaveSentences(self):
        pass
    
    
def addit():
    global insert,i,fulltext
    
    fulltext.executemany("insert into wikiarticles(id,timestamp,title,content) values (?,?,?,?)",insert)
    fulltext.commit()
    insert=[]

if __name__ == '__main__':
    wikipedia=Wikipedia()
    httpd=HTTPServer(('',42781),RequestHandler)
    print("Ready to serve.")
    httpd.serve_forever()
    wikipedia.close()
    
    #con=sqlite3.connect("data/wikipedia.db")
    #for i in con.execute("select title from wikiarticles"):
    #    print(i[0])
    #con.close()
