import os


# 처리 가능한 값보다 큰 값이 나왔을 때
class OverFlow(Exception):
    def __init__(self, args):
        self.message = f'{args} is overflow'

    def __str__(self):
        return self.message
    

# 처리 가능한 값보다 작은 값이 나왔을 때
class UnderFlow(Exception):
    def __init__(self, args):
        self.message = f'{args} is underflow'

    def __str__(self):
        return self.message


# 변수가 올바르지 않을 때
class InvalidArgs(Exception):
    def __init__(self, args):
        self.message = f'{args} is Invalid Arguments'

    def __str__(self):
        return self.message


# 카테고리가 올바르지 않을 때
class InvalidCategory(Exception):
    def __init__(self, category):
        self.message = f'{category} is Invalid Category.'

    def __str__(self):
        return self.message


# 실행시간이 너무 길어서 데이터를 얻을 수 없을 때
class ResponseTimeout(Exception):
    def __init__(self):
        self.message = "Couldn't get the data"

    def __str__(self):
        return self.message


# 존재하는 파일
class ExistFile(Exception):
    def __init__(self, path):
        absolute_path = os.path.abspath(path)
        self.message = f'{absolute_path} already exist'

    def __str__(self):
        return self.message
