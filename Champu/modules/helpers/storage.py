import random
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
CHAAT_STORAGE = [
    "mongodb+srv://yash:shivanshudeo@yk.6bvcjqp.mongodb.net/?retryWrites=true&w=majority&appName=yk",
]

CHAT_STORAGE = [
    "mongodb+srv://yash:shivanshudeo@yk.6bvcjqp.mongodb.net/?retryWrites=true&w=majority&appName=yk"
    "mongodb+srv://chutiyapa:bihar@cluster0.bph5t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    "mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Bikash:Bikash@bikash.yl2nhcy.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://hnyx:wywyw2@cluster0.9dxlslv.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://ravi:ravi12345@cluster0.hndinhj.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://userbot:userbot@cluster0.iweqz.mongodb.net/test?retryWrites=true&w=majority",
    "mongodb+srv://Alisha:Alisha123@cluster0.yqcpftw.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://vikashgup87:EDRIe3bdEq85Pdpl@cluster0.pvoygcu.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Sarkar123:GAUTAMMISHRA@sarkar.1uiwqkd.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://kuldiprathod2003:kuldiprathod2003@cluster0.wxqpikp.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Alisha:Alisha123@cluster0.yqcpftw.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://Krishna:pss968048@cluster0.4rfuzro.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://rahul:rahulkr@cluster0.szdpcp6.mongodb.net/?retryWrites=true&w=majority",
    "mongodb+srv://knight_rider:GODGURU12345@knight.jm59gu9.mongodb.net/?retryWrites=true&w=majority",
    
]


THECHAMPU = MongoCli(random.choice(CHAAT_STORAGE))
chatai = THECHAMPU.Anonymous.Word.WordDb
storeai = THECHAMPU.Anonymous.Word.NewWordDb  
