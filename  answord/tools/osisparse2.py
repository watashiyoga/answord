from xml.dom import pulldom
from pysqlite2 import dbapi2 as sqlite
#This is used to parse osis files that use the <verse sID=""/> <verse eID=""/>
#because each tag is recognized as its own rather than an open and close tag parsing 
#is a bit harder
filename = raw_input('Enter the file to be converted(xxx.osis)')
dbname = filename.split(".")[0]+".db"
connection = sqlite.connect(dbname)
cursor = connection.cursor()
bf = open(filename)
events = pulldom.parse(bf)

count = 0 #tracks what verse the program is at(used for debugging)
in_verse = 0 #use to get nodes inside a verse. answers the question Is the parse in a verse?
tag_open=0 #used to see if a tag is open in side a verse so as not to store it in the passage
versestack = [] #used to hold test for the passage
passage="" #used to hold 
for (event, node) in events:
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
            cursor.execute(query,("note","SQlite bible made from a WEB Osis File, may contain errors"))              
        if node.tagName == "verse":
            events.expandNode(node)
            sid = node.getAttribute("sID")
            if sid != "":
                in_verse = sid
                #print "In Verse ",sid
                count+=1
                
            eid = node.getAttribute("eID")
            if eid == in_verse:
                in_verse = 0
                #print "Out of Verse ",eid,
                while len(versestack) >0: 
                    cnode = versestack.pop(0)
                    #events.expandNode(cnode)
                    if not hasattr(cnode,"tagName"):
                        passage += cnode.nodeValue
                passage = passage.replace("\n", " ")
                print eid,passage
                book,chapter,verse = eid.split(".")
                query = "INSERT INTO bible VALUES (null,?,?,?,?)"
                cursor.execute(query,(book,chapter,verse,passage))
                #insert passage in to database
                passage = ""
            print count
        elif node.tagName == "note":
            tag_open = 1
    elif event == pulldom.CHARACTERS:
        if in_verse != 0 and tag_open == 0:
            versestack.append(node)
    elif event == pulldom.END_ELEMENT:
        if node.tagName == "note":
            tag_open = 0
connection.commit()
connection.close() 