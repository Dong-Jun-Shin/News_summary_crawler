import os
from datetime import date
from git import Repo, Actor
from articlecrawler import ArticleCrawler

USER_AUTHOR = 'Dongjun-Shin'
USER_EMAIL = 'tlsehdwns239@gmail.com'
SUMMARY = 'Create TodayNewsSummary'
DESCRIPTION = '- 뉴스 요약 생성'

SOURCE_REPO_PATH = os.environ['GITHUB_WORKSPACE']
# SOURCE_REPO_PATH = 'C:/Users/user/Desktop/News_summary_crawler'


def make_commit_message():
    # 커밋 메세지 생성하기
    message = SUMMARY + '_' + str(date.today()) + '\n\n' + DESCRIPTION
    return message


def push_proc(repo):
    try:
        # push 전 pull 실행
        pull_result = repo.remotes.origin.pull()[0]     # output >>> origin/main
        # push 실행
        push_result = repo.remotes.origin.push()[0]
    except Exception:
        print('error Pull or Push')
        print(str(pull_result))
        print(str(push_result))


def commit_proc(repo):
    # commit message 설정
    author = Actor(USER_AUTHOR, USER_EMAIL)        # 처음 만든 사람
    message = make_commit_message()

    # git commit 생성
    r_index = repo.index
    add_files = [item.a_path for item in repo.index.diff(None)]
    del_files = repo.untracked_files
    try:
        r_add_result, r_del_result = [], []
        if add_files:
            r_add_result = r_index.add(add_files)
        if del_files:
            r_del_result = r_index.remove(del_files)
    except Exception as e:
        print('error Staging : ' + e)
        print('add_files : ' + add_files)
        print('del_files : ' + del_files)
        return
    if r_add_result or r_del_result:
        r_index.commit(message, author=author)
    else:
        print('error Commit')
        print('r_add_result : ' + str(r_add_result))
        print('r_del_result : ' + str(r_del_result))


def auto_push():
    # repo 정의
    source_repo = Repo(SOURCE_REPO_PATH)
    # commit 실행
    commit_proc(source_repo)
    # push 실행
    push_proc(source_repo)


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category('IT과학', '경제', '사회')
    Crawler.start() 

    auto_push()
