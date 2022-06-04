import pandas as pd
import pymongo
import logger_Forest

class  extract_data_mongodb:
    """This class first checks whether the given username ,password,db_name ,coll_name is correct than it establishes connection , it has functions to check
    login infos and read data from mongodb"""
    def __init__(self,username,password):
            self.user_name = username
            self.pass_wd = password
            self.client = None
            self.data_base_nm = None
            self.collection_nm =None
            print("user info assigned to extract_data_mongodb class")
    def check_login_mongodb(self,data_base_name,collection_name):
        try:
            self.client = pymongo.MongoClient(f"mongodb+srv://{self.user_name}:{self.pass_wd}@forestfireprediction.weucr.mongodb.net/?retryWrites=true&w=majority")
            self.client.server_info()
            logger_Forest.logging_info("connection  established  with MONGODB" )
        except Exception as err:
            logger_Forest.logging_error("connection doesnt' established with MONGODB something wrong with username or password"+str(err))
            return False
        try:
            self.data_base_nm = self.client[data_base_name]
            self.collection_nm = self.data_base_nm[collection_name]
            if self.data_base_nm.name in self.client.list_database_names():
                logger_Forest.logging_info("the data base  exists ")
                if self.collection_nm.name in self.data_base_nm.list_collection_names():
                    logger_Forest.logging_info(f"the collection {self.collection_nm} exists in your database")
                else:
                    logger_Forest.logging_info(f"the collection {self.collection_nm} doesnt exists in your database")
                    return False
            else:
                logger_Forest.logging_info(f"the collection {self.data_base_nm} doesnt exists in your database")
                return False
        except Exception as err:
            logger_Forest.logging_info("Database or collection name entered is wrong please check that")
        return True
    def read_classi_data(self):
        l=[]
        x= self.collection_nm.find({},{'_id':0,'day':1,'month':1,'Temperature':1,' RH':1,' Ws':1,'Rain ':1,'FFMC':1,'DMC':1,'DC':1,'ISI':1})
        for data in x:
            l.append(data)
        self.data_frame = pd.DataFrame(data=l)
        #print(self.data_frame)
        return self.data_frame
    def read_regression_data(self):
        l=[]
        x = self.collection_nm.find({},{'_id': 0,'FFMC': 0, 'DMC': 0, 'DC': 0, 'ISI': 0,'Temperature':0})
        for data in x:
            l.append(data)
        self.data_frame = pd.DataFrame(data=l)
        return self.data_frame
        #print(self.data_frame)
        # username='Ineuron'
        # password='MachineAI'
        # data_base_name = 'FORESTFIRECLASSIFIER'
        # collection_name = 'Fireclassifier'

if __name__=="__main__":
    e1 = extract_data_mongodb('Ineuron', 'MachineAI')
    e1.check_login_mongodb('FORESTFIRECLASSIFIER', 'Fireclassifier')
    e1.read_classi_data()
    #e1.read_regression_data()