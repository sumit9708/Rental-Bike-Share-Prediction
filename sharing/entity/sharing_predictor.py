from distutils.sysconfig import PREFIX
import os,sys
from sharing.exception import SharingException
from sharing.util.util import load_object
import pandas as pd
from sharing.constant import *
from sharing.logger import logging
import boto3
import botocore
from dotenv import load_dotenv

load_dotenv()

class SharingData:
    def __init__(self,
            season: int,
            year: int,
            month: int,
            hour: int,
            holiday: int,
            weekday: int,
            workingday: int,
            weather: int,
            temp: float,
            humidity: float,
            windspeed: float) -> None:
        try:
            self.season = season
            self.year = year
            self.month = month
            self.hour = hour
            self.holiday = holiday
            self.weekday = weekday
            self.workingday = workingday
            self.weather = weather
            self.temp = temp
            self.humidity = humidity
            self.windspeed = windspeed
        except Exception as e:
            raise SharingException(e,sys) from e

    def get_housing_input_data_frame(self):
        try:
            sharing_input_dict = self.get_sharing_data_as_dict()
            return pd.DataFrame(sharing_input_dict)
        except Exception as e:
            raise SharingException(e, sys) from e
        
    def get_sharing_data_as_dict(self):
        try:
            input_data = {
                "season": [self.season],
                "year": [self.year],
                "month": [self.month],
                "hour": [self.hour],
                "holiday": [self.holiday],
                "weekday": [self.weekday],
                "workingday": [self.workingday],
                "weather": [self.weather],
                "temp": [self.temp],
                "humidity": [self.humidity],
                "windspeed": [self.windspeed],
            }
            return input_data
        except Exception as e:
            raise SharingException(e, sys)

            

class SharingPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise SharingException(e, sys) from e
        
    def s3_get_lattest_model_path(self):
        try:
            session = boto3.Session(
            aws_access_key_id= os.ACCESS_KEY,
            aws_secret_access_key=os.SECRET_KEY
            )  
            #Creating S3 Resource From the Session.
            s3 = session.resource('s3')
            bucket = s3.Bucket(S3_BUCKET_NAME)

            objs = bucket.objects.filter()
            folder_pth = []
            for obj in objs:
                path, filename = os.path.split(obj.key)
                # boto3 s3 download_file will throw exception if folder not exists
                folder_pth.append(path)
            
            # Removing hash from string and typcast string to integer
            for i in range(0, len(folder_pth)):
                folder_pth[i] = folder_pth[i].replace("-","")
            
            s3_folder_name = list(map(int, folder_pth))

            return max(s3_folder_name)  

        except Exception as e:
            raise SharingException(e,sys)
    
    def create_prefix(self):
        try:
            folder_directory = str(self.s3_get_lattest_model_path())
            year = slice(4)
            date = folder_directory[6:8]
            month = folder_directory[4:6]
            min = folder_directory[8:10]
            sec = folder_directory[10:12]
            milli_sec = folder_directory[12:14]
            download_format = folder_directory[year]+'-'+month+'-'+date+'-'+min+'-'+sec+'-'+milli_sec+'/'
            return download_format
        except Exception as e:
            raise SharingException(e,sys)
    
    def s3_download_model(self):
        try:
            session = boto3.Session(
            aws_access_key_id=os.ACCESS_KEY,
            aws_secret_access_key=os.SECRET_KEY
            )   
            #Creating S3 Resource From the Session.
            s3 = session.resource('s3')
            bucket = s3.Bucket(S3_BUCKET_NAME)

            #prefix=self.create_prefix()
            #logging.info(f"Prefix Created",{prefix})
            str='downloaded_models'
            
            for obj in bucket.objects.filter(Prefix = ""):
                path = os.path.join(str,obj.key)
                if not os.path.exists(os.path.dirname(path)):
                    os.makedirs(os.path.dirname(path))
                bucket.download_file(obj.key, path) # save to same path
            logging.info("Downloaded Model From S3")

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
    
   
    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            #print("FOLDER NAME",folder_name)
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            #print("lateset_model ", latest_model_dir)
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            #self.s3_download_model()
            return latest_model_path
        except Exception as e:
            raise SharingException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise SharingException(e, sys) from e
