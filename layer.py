from rivescript import RiveScript
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
#from spell import check
import re, collections
import math
from pymongo import MongoClient
import datetime
def words(text):
        return re.findall('[a-z]+', text.lower())

def train(features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
                model[f] += 1
        return model

NWORDS = train(words(file('big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
        s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in s if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
        inserts    = [a + c + b     for a, b in s for c in alphabet]
        return set(deletes + transposes + replaces + inserts)
      
def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
    
def known(words):
        return set(w for w in words if w in NWORDS)
    
def correct(word): 
        candidates = known([word]) or known(edits1(word)) or    known_edits2(word) or [word]
        return max(candidates, key=NWORDS.get)

def formstring(message):
        word = ""
        string = ""
        for ch in message:
                if ch!=' ':
                        word+=ch
                else:
                        string+=correct(word)+' '
                        word=""
        return string


class EchoLayer(YowInterfaceLayer):
    session = []
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over
	client = MongoClient()
	db = client.data
        if True:

            rs=RiveScript()
            rs.load_directory("./brain")
            rs.sort_replies()
		
            messageOut = ""
            #print(messageProtocolEntity.getType() )
            if messageProtocolEntity.getType() == "text":
                #self.output(message.getBody(), tag = "%s [%s]"%(message.getFrom(), formattedDate))
                """
                c = check()
                para = messageProtocolEntity.getBody()                
                messageOut =c.func(para)
                """
                messageOut = messageProtocolEntity.getBody()+' '
                print(messageOut)
            elif messageProtocolEntity.getType() == "media":
                #self.getMediaMessageBody(messageProtocolEntity)
                if self.onMediaMessage(messageProtocolEntity) == 1:
                	messageOut = "location code one "
		elif self.onMediaMessage(messageProtocolEntity) == 2:
                        messageOut = "image code one "
		elif self.onMediaMessage(messageProtocolEntity) == 3:
                        messageOut = "vcard recieved  "
		else:
			messageOut = "location code zero "
            else:
                messageOut = "Unknown message type %s " % messageProtocolEntity.getType()
                print(messageOut.toProtocolTreeNode())
            
            messageOut=formstring(messageOut)
	    print(messageOut)
            reply=rs.reply("localuser",messageOut)
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())
	    result = db.session.find({"from":messageProtocolEntity.getFrom()})
	    if result.count() == 1:
	    	stime= datetime.datetime.now().hour*60+datetime.datetime.now().minute
		print(stime)
	   	if stime<=result[0]['expiry']:
		 	#Customer in citizen
			
			r = db.session.find({"from":messageProtocolEntity.getFrom()})
			qid = r[0]['qid']
			if messageProtocolEntity.getType() == "text":
				db.query.update({"_id":qid},{"$set":{"text":db.query.find({"_id":qid})[0]['text']+[messageProtocolEntity.getBody()]}})	
           		elif messageProtocolEntity.getMediaType() == "image":
				db.query.update({"_id":qid},{"$set":{"image":db.query.find({"_id":qid})[0]['image']+[messageProtocolEntity.url]}})
			
                        elif messageProtocolEntity.getMediaType() == "location":
                                db.query.update({"_id":qid},{"$set":{"location":db.query.find({"_id":qid})[0]['location']+[[messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()]]}})
			
                        elif messageProtocolEntity.getMediaType() == "vcard":
                                db.query.update({"_id":qid},{"$set":{"vcard":db.query.find({"_id":qid})[0]['vcard']+[messageProtocolEntity.getCardData()]}})
			else:
                                db.query.update({"_id":qid},{"$set":{"text":db.query.find({"_id":qid})[0]['text']+[messageProtocolEntity.getBody()]}})
			outgoingMessageProtocolEntity = TextMessageProtocolEntity(reply,
                		to = messageProtocolEntity.getFrom())
            		self.toLower(receipt)
            		self.toLower(outgoingMessageProtocolEntity)
		else:                                                                                                                                                                                         
                        r = db.session.find({"from":messageProtocolEntity.getFrom()})
                        qid = r[0]['qid']
			db.session.remove({"from":messageProtocolEntity.getFrom()})                                                                                                                                                                                    
                	outgoingMessageProtocolEntity = TextMessageProtocolEntity("Your complaint id:"+str(qid)+"\n\nYour session has been expired!!\nYou need to register again.",to = messageProtocolEntity.getFrom())                                                                                                                                             
                	self.toLower(receipt)                                                                                                                                                         
			self.toLower(outgoingMessageProtocolEntity)   
	    else:
		
		outgoingMessageProtocolEntity = TextMessageProtocolEntity("I need your location to register you",
                        to = messageProtocolEntity.getFrom())
                self.toLower(receipt)
                self.toLower(outgoingMessageProtocolEntity)
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)


    def onTextMessage(self,messageProtocolEntity):                                                                                                                
        # just print info                                                                                                                                                                                 
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))                                                       


    def onMediaMessage(self, messageProtocolEntity):                                                                                                              
        # just print info                                                                                                                                                                                 
        if messageProtocolEntity.getMediaType() == "image":
            """
	    import Image

            from PIL import Image
            import pytesseract
            import urllib

            urllib.urlretrieve(messageProtocolEntity.url, "index.jpg")
            print("Howdy,Bitch")

            print(pytesseract.image_to_string(Image.open("index.jpg")))   
	    """
	    return 2                                                      
        elif messageProtocolEntity.getMediaType() == "location":  
	    lat = float(messageProtocolEntity.getLatitude())
	    lon = float( messageProtocolEntity.getLongitude())
	    dist = math.sqrt(pow(abs(12.9714025-lat),2)+pow(abs(77.5898356-lon),2))*100
	    if dist>16:
		return 0
	    else:
		client = MongoClient()
       		db = client.data
		if db.session.find({"from":messageProtocolEntity.getFrom()}).count()==0:
			ctime = datetime.datetime.now()
			query_id = db.query.insert({"from":messageProtocolEntity.getFrom(),"time":datetime.datetime.now(),"text":[],"image":[],"location":[],"vcard":[]})
			post = {"from":messageProtocolEntity.getFrom(),"time":datetime.datetime.now(),"expiry":ctime.hour*60+ctime.minute+1,"qid":query_id}
               		r = db.session.insert(post)
			
			
		print(messageProtocolEntity.getLocationName())
                print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))
		return 1 

        elif messageProtocolEntity.getMediaType() == "vcard":                                                                                                     
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))    
	    return 3                                                                                              
