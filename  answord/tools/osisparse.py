from xml.dom import pulldom
from pysqlite2 import dbapi2 as sqlite
#used to convert sword bible osis  for osis files that use the <verse> </verse> convention
filename = raw_input('Enter the file to be converted(xxx.osis)')
dbname = filename.split(".")[0]+".db"
connection = sqlite.connect(dbname)
cursor = connection.cursor()
bf = open(filename)
events = pulldom.parse(bf)
tablename = ""
count = 0
for (event, node) in events:
    if count >=0:
        if event == pulldom.START_ELEMENT:
            #create table
            if node.tagName == "work" and node.getAttribute("osisWork"):
                bibleversion = ""
                events.expandNode(node)
                for cnode in node.childNodes:
                    if hasattr(cnode,"tagName"):
                        if cnode.tagName =="title":
                            bibleversion = cnode.childNodes[0].nodeValue
                            break 
                query = "CREATE TABLE bible" 
                query += " (id INTEGER PRIMARY KEY,book VARCHAR(50),"
                query += "chapter INTEGER,verse INTEGER,"
                query += "scripture VARCHAR(500))"
                try:
                    cursor.execute(query)
                except:
                    cursor.execute("DROP TABLE bible")
                    cursor.execute(query)
                #define what bible version
                query = "INSERT INTO bible VALUES(null,?,'','',?)"
                print bibleversion
                cursor.execute(query,("version",bibleversion))
                cursor.execute(query,("note","SQlite bible made from a Sword Bible Module, may contain errors"))
            
            if node.tagName == "verse":
                count+=1
                events.expandNode(node)
                book,chapter,verse = node.getAttribute("osisID").split(".")           
                passage= []
                #grabs the text in verse nodes
                for cnode in node.childNodes:
                    if not hasattr(cnode,"tagName"):
                        passage.append(cnode.nodeValue)
                    elif cnode.tagName =="q": 
                        #Fix this so that we can tell who said this and make it 
                        #recursive(only goes 2 deep right now)
                        passage.append("\"")#begin quote
                        if len(cnode.childNodes) >0:
                            for gcnode in cnode.childNodes:
                                if not hasattr(gcnode,"tagName"):
                                    passage.append(gcnode.nodeValue)
                                elif gcnode.tagName =="q":
                                    passage.append("\"")
                            passage.append("\"")#finish the quote
                query = "INSERT INTO bible VALUES (null,?,?,?,?)"
                cursor.execute(query,(book,chapter,verse," ".join(passage)))
                if count%1000 ==0:
                    print count
    else:
        break
connection.commit()
connection.close()
