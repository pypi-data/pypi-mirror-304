# exceptions.py
class DataDirectoryEmptyError(Exception):
    """'data' 디렉토리가 비어 있을 때 발생하는 예외"""
    def __init__(self, message="오류: 'data' 디렉토리에 파일이 없습니다. 실험 데이터를 'data' 디렉토리에 넣어주세요."):
        self.message = message
        super().__init__(self.message)