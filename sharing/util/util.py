import yaml
from sharing.exception import SharingException
from sharing.logger import logging
import os,sys
import numpy as np
import dill
import pandas as pd
from sharing.constant import *
import boto3
from dotenv import load_dotenv
load_dotenv()

def upload_model_s3(model_path:str):
    try:
        session = boto3.Session(
        aws_access_key_id= os.ACCESS_KEY,
        aws_secret_access_key=os.SECRET_KEY
        )   

        #Creating S3 Resource From the Session.
        s3 = session.resource('s3')
        model_file_name = os.path.basename(model_path)

        object = s3.Object(S3_BUCKET_NAME, model_file_name)

        directoryname = CURRENT_TIME_STAMP

        KeyFileName = "{dirname}/{fname}".format(dirname = directoryname,fname=model_file_name) 
        
        result = object.put(Body=open(model_path, 'rb'), Key=KeyFileName)

        res = result.get('ResponseMetadata')

        if res.get('HTTPStatusCode') == 200:
            print('File Uploaded Successfully')
            logging.info('File Uploaded Successfully')

        else:
            print('File Not Uploaded')
            logging.info('File Not Uploaded')
    except Exception as e:
        raise SharingException(e,sys)

def write_yaml_file(file_path:str,data:dict=None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise SharingException(e,sys)


def read_yaml_file(file_path:str)->dict:
    """
    Reads a YAML file and returns the contents as a dictionary.
    file_path: str
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise SharingException(e,sys) from e


def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise SharingException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SharingException(e, sys) from e


def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise SharingException(e,sys) from e


def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise SharingException(e,sys) from e


def load_data(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        datatset_schema = read_yaml_file(schema_file_path)

        schema = datatset_schema[DATASET_SCHEMA_COLUMNS_KEY]

        dataframe = pd.read_csv(file_path)

        error_messgae = ""


        for column in dataframe.columns:
            if column in list(schema.keys()):
                dataframe[column].astype(schema[column])
            else:
                error_messgae = f"{error_messgae} \nColumn: [{column}] is not in the schema."
        if len(error_messgae) > 0:
            raise Exception(error_messgae)
        return dataframe

    except Exception as e:
        raise SharingException(e,sys) from e
    