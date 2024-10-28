import numpy as np
from typing import Optional
from pandas import Series

class Phase_shift:
    def __init__(self, ch1_data:Series|np.ndarray, ch2_data:Series|np.ndarray):
        '''
        calculate the phase shift between ch1 and ch2.
        :param ch1_data: Series|np.ndarray, the first data.
        :param ch2_data: Series|np.ndarray, the second data.
        '''
        assert type(ch1_data) is Series or type(ch1_data) is np.ndarray, 'The type of the ch1_data should be Series or np.ndarray. Not {}'.format(type(ch1_data))

        self.ch1_data=ch1_data
        self.ch2_data=ch2_data
        self.ym_y0:dict=self.find_ym_y0()

    def find_min_x_vector(self,vectors:np.ndarray[:,2])->Series:
        '''
        2차원 벡터 리스트에서 x값의 크기가 가장 작은 벡터를 찾는다.
        '''
        # 벡터 리스트를 x값 기준으로 정렬
        abs_vector_x=np.abs(vectors[:,0]) # x값의 절댓값을 구한다.
        sorted_index = np.argsort(abs_vector_x) # 입력받은 벡터를 절댓값으로 만들고 크기가 작은 순서대로 정렬 이후 원래 인덱스를 반환
        minimal_index=sorted_index[0] # x값의 크기가 가장 작은 벡터의 인덱스
        smallest_vector = vectors[minimal_index] # x값의 크기가 가장 작은 벡터 반환
        # x값의 크기가 가장 작은 벡터 반환
        return smallest_vector

    # find ym and y0
    def find_ym_y0(self)->dict[str, float]:
        '''
        Find ym and y0
        :param data1: Series, the first data.
        :param data2: Series, the second data.
        :return: tuple, the ym and y0.
        '''
        ch1_data=self.ch1_data
        ch2_data=self.ch2_data

        # chanage the data type to numpy array
        if type(ch1_data) is Series:
            ch1_data=ch1_data.values
        if type(ch2_data) is Series:
            ch2_data=ch2_data.values
        
        assert len(ch1_data)==len(ch2_data), 'The length of the data should be the same.'

        # find y0
        ## ch2가 양수일 때의 ch1값이 0일때와 ch2가 음수일 때의 ch1값이 0일 때의 ch2값을 각각 나눠서 찾아야 한다.
        combined_data:np.ndarray[:,2]=np.column_stack((ch1_data,ch2_data))
        filtered_data1:np.ndarray[:,2]=combined_data[combined_data[:,1]>0] ## ch2가 양수일 때의 데이터
        filtered_data2:np.ndarray[:,2]=combined_data[combined_data[:,1]<0] ## ch2가 음수일 때의 데이터

        assert len(filtered_data1)>0 or len(filtered_data2)>0, 'The ch2 data should have positive or negative values.'

        ## ch1가 0에 가장 가까울 때의 ch2값을 찾는다.
        upper_y0=self.find_min_x_vector(filtered_data1)
        lower_y0=self.find_min_x_vector(filtered_data2)

        ## y0 계산, y0_source 계산
        y0=np.abs(upper_y0[1])+np.abs(lower_y0[1])
        y0_source=np.array([upper_y0,lower_y0])

        # find ym: ym은 ch2의 최대값과 최솟값의 차이다.
        sorted_indices_ch2=np.argsort(ch2_data)
        max_index_ch2=sorted_indices_ch2[-1]
        min_index_ch2=sorted_indices_ch2[0]
        ym=np.abs(ch2_data.max())+np.abs(ch2_data.min())
        ym_source=np.array([[ch1_data[max_index_ch2],ch2_data.max()],
                            [ch1_data[min_index_ch2],ch2_data.min()]
        ])
        
        return {'ym':ym, 'y0':y0,'ym_source':ym_source,'y0_source':y0_source}

    def __call__(self):
        '''
        Find the phase shift between ch1 and ch2.
        '''
        ym_y0=self.ym_y0
        ym=ym_y0['ym']
        y0=ym_y0['y0']
        
        # find the phase shift
        theta=np.arcsin((y0/ym))
        deg_theta=np.rad2deg(theta)
        if deg_theta<0: # 0~360도로 변환
            deg_theta=360+deg_theta
            
        if 0<deg_theta<90 or 270<deg_theta<360:
            return theta # theta is phase shift
        else:
            phase_shift=np.pi-theta
            return phase_shift

def get_error_rate(theory:np.ndarray, experiment:np.ndarray, absolute:Optional[bool]=True) -> np.ndarray:
    '''
    오차 백분율을 계산합니다.
    :param theory: np.ndarray, 이론값
    :param experiment: np.ndarray, 실험값
    :param absolute: Optional[bool]=True, True이면 절대 오차 백분율을 반환합니다.
    :return: np.ndarray, 오차 백분율

    오차 백분율은 다음과 같이 계산됩니다.
    $$\text{Error Rate} = |\frac{\text{Theory} - \text{Experiment}}{\text{Theory}}| \times 100$$
    이 때 absolute가 True이면 절대 오차 백분율을 반환하고, False이면 위의 식에서 절댓값이 제거된 체로 오차 백분율을 반환합니다.

    Tip: You can also use skit-learn's mean_squared_error function. See https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html
    '''
    if absolute:
        return 100*np.abs(theory - experiment) / np.abs(theory)
    else:
        return 100*(theory - experiment) / np.abs(theory)