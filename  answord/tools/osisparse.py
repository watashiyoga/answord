from xml.dom import pulldom
from pysqlite2 import dbapi2 as sqlite

filename = raw_input('Enter the file to be converted(xxx.osis)')
dbname = filename.split(".")[0]+".db"
print dbname
connection = sqlite.connect(dbname)
cursor = connection.cursor()
bf = open(filename)
events = pulldom.parse(bf)
tablename = ""
count = 0
for (event, node) in events:
    if count >=0:
        if event == pulldom.START_ELEMENT:
            if node.tagName == "osisText":
                tablename = node.getAttribute("osisIDWork")
                query = "CREATE TABLE " + tablename
                query += " (id INTEGER PRIMARY KEY,book VARCHAR(50),"
                query += "chapter INTEGER,verse INTEGER,"
                query += "scripture VARCHAR(500),tags VARCHAR(100))"
                try:
                    cursor.execute(query)
                except:
                    cursor.execute("DROP TABLE "+tablename)
                    cursor.execute(query)
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
                query = "INSERT INTO "+tablename + " VALUES (null,?,?,?,?,null)"
                cursor.execute(query,(book,chapter,verse," ".join(passage)))
                if count%1000 ==0:
                    print count
    else:
        break
connection.commit()
connection.close()
