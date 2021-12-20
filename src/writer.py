import platform
from exceptions import *


class Writer(object):
    def __init__(self, category, article_category, today):
        self.date = today

        self.file = None
        self.initialize_file(category, article_category)

    def initialize_file(self, category, article_category):
        output_path = f'../output/{self.date}'
        if os.path.exists(output_path) is not True:
            os.makedirs(output_path)

        file_name = f'{output_path}/{category}_{article_category}_{self.date}.md'

        user_os = str(platform.system())
        if user_os == "Windows":
            self.file = open(file_name, 'w', encoding='utf-8', newline='')
        # Other OS uses utf-8
        else:
            self.file = open(file_name, 'w', encoding='utf-8', newline='')

    # 템플릿
    def write_title(self, text_headline):
        row_string = '<!-- 타이틀 -->  \n'
        row_string += f'# {text_headline}  \n'
        self.file.write(row_string)

    def write_info(self, time, text_company, content_url):
        row_string = '<!-- 기사 정보 -->  \n'
        row_string += f'> Date : {time}  \n'
        row_string += f'> Author : {text_company}  \n'
        row_string += f'> Original : [원문기사]({content_url})  \n'
        row_string += '<br/>  \n'
        self.file.write(row_string)

    def write_img(self, img_content):
        row_string = '<!-- 대표 이미지 -->  \n'
        row_string += f'{img_content}  \n'
        row_string += '<br/><br/>  \n'
        self.file.write(row_string)

    def write_sentence(self, text_sentence):
        row_string = '<!-- 기사 본문 -->  \n'
        row_string += f'{text_sentence}  \n'
        row_string += '<br/><br/><br/>  \n\n'
        self.file.write(row_string)

    # 파일 커넥션 종료
    def close(self):
        self.file.close()
