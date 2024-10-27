from ast import Global
import pandas as pd
from pandas import DataFrame
from typing import Optional
import os
import re
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def pairwise_to_2d_list(flat_list:list)->list[any]:
    # 2개씩 묶어서 2차원 배열로 변환
    return [flat_list[i:i + 2] for i in range(0, len(flat_list), 2)]

def get_sorted_folders_dir_by_number(directory) -> list[str]:
    """
    주어진 디렉토리 내의 모든 폴더 이름에서 숫자를 추출하여, 숫자 기준으로 오름차순 정렬된 폴더 이름 목록을 반환합니다.
    
    :param directory: str, 디렉토리 경로
    :return: list, 숫자 기준으로 정렬된 폴더 이름 목록
    """
    folder_names:list[str] = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    
    # 폴더 이름에서 숫자를 추출하고, 숫자가 없는 경우 0으로 간주
    folder_numbers:list[str] = [(folder, int(re.search(r'\d+', folder).group()) if re.search(r'\d+', folder) else 0) for folder in folder_names]
    
    # 숫자 기준으로 폴더 이름 정렬
    sorted_folders:list = sorted(folder_numbers, key=lambda x: x[1])
    
    # 정렬된 폴더 이름만 반환
    return [directory+'/'+folder[0] for folder in sorted_folders]

def get_channel_csv_files(directory) -> dict[str,str]:
    """
    주어진 디렉토리 내의 CSV 파일 중 파일 이름에 'CH1', 'CH2' 등이 포함된 파일을 채널별로 딕셔너리로 반환합니다.
    
    :param directory: str, 디렉토리 경로
    :return: dict, 채널별 CSV 파일 경로 딕셔너리

    > Tektronix는 CSV 파일 이름에 'CH1', 'CH2' 등 채널 정보가 포함되어 있습니다. 또한 확장자가 csv가 아닌 CSV로 되어 있으니 주의하세요.
    """
    csv_files = [file for file in os.listdir(directory) if file.endswith('.CSV')] # csv가 아니라 CSV로 되어 있음.

    assert len(csv_files) > 0, 'No CSV files in the directory.'

    channel_files:defaultdict = defaultdict(list)
    
    for file in csv_files:
        match = re.search(r'CH\d+', file)
        if match:
            channel = match.group()
            channel_files[channel].append(os.path.join(directory, file))
    
    return dict(channel_files)

# Read the data from the CSV file
def read_csv_Tektronix(file_path:str,columns_name:Optional[str]=['Time', 'Voltage'], exclude_columns:Optional[list]=[0,1,2,5], metadata_lows:Optional[int]=18, name:Optional[str]=None) -> dict[str, DataFrame]:
    '''
    Read Tektronix's CSV file and return the data and metadata.
    :param file_path: str, the path of the CSV file.
    :param exclude_columns: list, the index of the columns to be excluded.
    :param metadata_lows: int, the number of rows to be extracted as metadata.
    :return: dict, the data and metadata.
    '''
    # CSV 파일에서 데이터 읽기
    data = pd.read_csv(file_path)
    
    # extract metadata
    metadata = data.iloc[:metadata_lows]

    # 제외할 열 이름 계산
    exclude_column_names = [data.columns[i] for i in exclude_columns]
    
    # 제외할 열 이름을 제외한 나머지 열 이름 선택
    usecols = [column for column in data.columns if column not in exclude_column_names]
    
    # CSV 파일 다시 읽기, 특정 열 제외
    data = pd.read_csv(file_path, usecols=usecols)

    # set the name of the data
    if name is not None:
        data.name=name

    # data 열 이름 지정
    if len(columns_name) == len(data.columns):
        data.columns = columns_name
    else:
        raise ValueError('The number of columns_name is not same as the number of columns in the data.: columns_name={}, data.columns={}'.format(len(columns_name), len(data.columns)))

    # results
    result = {
        'metadata': metadata,
        'data': data
    }
    return result

class get_all_csv_paths:
    def __init__(self, flatten:Optional[bool]=False, custom_dir_name:Optional[list[str]]=None):
        '''
        :param flatten: bool, 만약 True이면, 실험 번호대로 시험 데이터를 묶는 게 아닌(2차원 배열), 1차원 배열로 변환합니다.
        :param custom_dir_name: Optional[list[str]], 실험 데이터 내의 폴더 이름들을 설정합니다. 예를 들어, ['data1', 'data2']로 설정하면, data1, data2 폴더 내의 데이터만 가져옵니다. 만약 None이면, 모든 실험 순서대로 데이터를 가져옵니다.
        '''
        self.directory = 'data'
        self.flatten = flatten
        self.custom_dir_name = custom_dir_name
        self.all_csv_list = self.__call__()

    def __rough_get_all_csv_paths(self, experi_dir:list)->np.ndarray:
        '''
        flatten이나 custom_dir_name을 고려하지 않고, 모든 csv 파일을 가져옵니다.

        > 코드 가독성을 위해 본 함수를 만들었기에 private 함수로 만들었습니다.
        '''
        rough_all_csv_list = []
        # get all the csv files in the directory
        for dir in experi_dir:
            temp_list=[get_channel_csv_files(dir)['CH1'][0],get_channel_csv_files(dir)['CH2'][0]]
            csv_list=temp_list
            rough_all_csv_list.append(csv_list)
        rough_all_csv_list:np.ndarray=np.array(rough_all_csv_list)
        return rough_all_csv_list

    def __call__(self)->np.ndarray:
        '''
        주어진 조건에 따라 모든 csv 파일을 가져옵니다.
        :return: np.ndarray, the list of the csv files.
        '''
        directory=self.directory
        flatten=self.flatten
        custom_dir_name=self.custom_dir_name
        experi_dir= get_sorted_folders_dir_by_number(directory)
        if custom_dir_name is not None:
            # no custom_dir_name
            experi_dir=custom_dir_name

        all_csv_list=self.__rough_get_all_csv_paths(experi_dir)

        # flatten
        if flatten:
            all_csv_list=all_csv_list.flatten()
        return all_csv_list