from ming import Session, create_datastore
from ming import Document, Field, schema
import json

bind = create_datastore('mongodb://114.34.79.27:27017/paperMiningTest')
session = Session(bind)

class Paper(Document):

    class __mongometa__:
        session = session
        name = 'paperRefRelationSimple2'
    firstRef = Field(str)
    secRef = Field(str) 
    intersectionArray = Field([])

class PaperName(Document):
    class __mongometa__:
        session = session
        name = 'paperName2'
    IndexId = Field(str)
    title = Field(str)

if __name__ == '__main__':
    papers = Paper.m.find().all()
    papersName = PaperName.m.find().all()
    nodeArray = []
    nodeDicArray = []
    linkArray = []
    nodeUse = []
    nodes = []
    for doc in papers:
    	if doc['firstRef'] not in nodeArray:
    		nodeArray.append(doc['firstRef'])
    	if doc['secRef'] not in nodeArray:
    		nodeArray.append(doc['secRef'])
    for doc in papers:
    	dic = {"source": nodeArray.index(doc['firstRef']),"target":nodeArray.index(doc['secRef']), "value":len(doc['intersectionArray']), "cocitepaper": doc['intersectionArray']}
        for p in doc['intersectionArray']:
            if p not in nodeUse:
                nodeUse.append(p)
    	linkArray.append(dic)
    for x in nodeArray:
        print x
        nodes.append(x)
    	nodeDicArray.append({"name":x, "group":1})
    dicFinal = {"nodes": nodeDicArray, "links": linkArray}
    # for x in nodeUse:
    #     print x
    # with open('/Users/man27382210/Desktop/d3_exmaple/nodes3.json', 'w') as outfile:
    # 	json.dump(dicFinal, outfile)
    dicName = {}
    for pN in papersName:
        dicName[pN["IndexId"]] = pN["title"]
    # with open('/Users/man27382210/Desktop/d3_exmaple/nodesName3.json', 'w') as outfile:
    #   json.dump(dicName, outfile)
    for i in nodes:
        print (i+" "+dicName[i])