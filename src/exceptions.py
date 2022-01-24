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

# Git err_log 출력
class GitErrLog():
    prt_list = {'staging' : ['error Staging : ', 'add_files : ', 'del_files : '] \
                , 'commit' : ['error Commit : ', 'r_add_result : ', 'r_del_result : '] \
                , 'push' : ['error Pull or Push : ', 'pull_result : ', 'push_result : ']}
    exp_data, log_data_1, log_data_2 = '', '', ''

    def __init__(self, type, exp_data, log_data_1, log_data_2):
        prt_str = self.prt_list[type]
        self.prt_err_log(prt_str, exp_data, log_data_1, log_data_2)

    def prt_err_log(self, prt_str, exp_data, log_data_1, log_data_2):
        print('----------------------------------')
        print(prt_str[0] + str(exp_data))
        print(prt_str[1] + str(log_data_1))
        print(prt_str[2] + str(log_data_2))
        print('----------------------------------')
