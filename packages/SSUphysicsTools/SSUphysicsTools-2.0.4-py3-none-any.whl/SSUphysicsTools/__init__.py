# 주요 모듈 임포트
from .data_analysis import *
from .data_processing import *
from .getting_data import *
from .Plots import *
from .exceptions import DataDirectoryEmptyError

# 필요한 디렉토리가 있는 지 확인 후 생성
directory_list = ['fig','data']
for directory in directory_list:
    if not os.path.exists(directory):
        os.makedirs(directory)

# 'data' 디렉토리에 파일이 없는 경우 경고 문구 출력
data_directory = directory_list[1]
if os.path.exists(data_directory) and not os.listdir(data_directory):
    raise DataDirectoryEmptyError()