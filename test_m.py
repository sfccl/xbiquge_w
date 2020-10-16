from pymongo import MongoClient
conn = MongoClient('localhost',27017)
db = conn.novels #Mongodb不需要提前创建好数据库，而是直接使用，如果发现没有则自动创建
id = 3
url = "www.sina.com.cn"
content = "铜锣坝旅游开发有限公司_景区"
date1={}
date1["ID"] = id
date1["URL"] = url
date1["CONTENT"] = content

collection_novel = "tlb"
exec('db.' + collection_novel + '.insert_one(date1)')


