from scipy.optimize import curve_fit
import numpy as np
from typing import Callable, Optional
from pandas import DataFrame

# regression
class Regression:
    @staticmethod
    def cosine_regression(x_data:np.ndarray, y_data:np.ndarray, freq:Optional[str]=None)->dict:
        pure_model=lambda x,A,f,phi,offset: A*np.cos(2*np.pi*f*x+phi)+offset

        if freq: # freq is given
            freq_model:Callable=lambda x,A,phi,offset: pure_model(x,A,freq,phi,offset)
            freq_parms, _ = curve_fit(freq_model, x_data, y_data)
            fitted_func:Callable= lambda x: freq_model(x, *freq_parms)
            result:dict={'fitted_func':fitted_func,'parms':freq_parms}
            return result
        
        # freq is not given
        parms, _ = curve_fit(pure_model, x_data, y_data, maxfev=10000)
        fitted_func:callable= lambda x: pure_model(x, *parms)
        result:dict={'fitted_func':fitted_func,'parms':parms}
        return result

class Delate_offset(Regression):
    '''
    Regression을 사용해 offset을 데이터에서 제거합니다.
    '''
    def __init__(self, data:DataFrame, data_column:Optional[list[str]]=['Time','Voltage'],is_use_regression:Optional[bool]=False):
        '''
        Delate the offset from the data.
        :param data: DataFrame
        :param data_column: list[str], the column names of the data.
        :param is_use_regression: bool, if True, use the regression to find the offset. If False, use the mean value of the data.
        '''
        assert type(data) is DataFrame, 'The type of the data should be Dataframe. Not {}'.format(type(data))

        self.data=data
        self.is_use_regression=is_use_regression
        self.column_x:str=data_column[0]
        self.column_y:str=data_column[1]
        self.data_x=data[self.column_x]
        self.data_y=data[self.column_y]
        if self.is_use_regression:
            self.offset:float=self.cosine_regression(self.data_x,self.data_y)['parms'][3] # offset 값 찾기
        else:
            self.offset:float=self.data_y.mean()
    
    def __call__(self)->DataFrame:
        '''
        Delate the offset from the data.
        '''
        offset=self.offset
        data_x=self.data_x
        data_y=self.data_y
        data_y=data_y-offset
        results={self.column_x:data_x,self.column_y:data_y}
        return DataFrame(results)