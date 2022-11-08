import os, time
from datetime import date
from git import Repo, Actor
from articlecrawler import ArticleCrawler
from exceptions import GitErrLog

USER_AUTHOR = 'Dongjun-Shin'
USER_EMAIL = 'tlsehdwns239@gmail.com'
SUMMARY = 'Create TodayNewsSummary'
DESCRIPTION = '- 뉴스 요약 생성'

SOURCE_REPO_PATH = os.environ['GITHUB_WORKSPACE']
# SOURCE_REPO_PATH = 'C:/Users/user/Desktop/Repo/News_summary_crawler'
# SOURCE_REPO_PATH = 'C:/Users/tlseh/Desktop/News_summary_crawler'

RETRY_COUNT = 0


def get_tracked_path(repo):
    # 추가, 수정, 삭제된 파일을 트래킹
    add_index = repo.untracked_files
    update_index = repo.index.diff(None).iter_change_type('M')
    delete_index = repo.index.diff(None).iter_change_type('D')
    # 트래킹한 파일의 path 리스트 추출
    add_files = add_index + [item.a_path for item in update_index]
    del_files = [item.a_path for item in delete_index]
    return add_files, del_files


def make_commit_message():
    # 커밋 메세지 생성하기
    message = SUMMARY + '_' + str(date.today()) + '\n\n' + DESCRIPTION
    return message


def push_proc(repo):
    global RETRY_COUNT

    try:
        if not repo.remotes.origin:
            raise Exception

        # push 전 pull 실행
        pulled_branches = repo.remotes.origin.pull()
        # push 실행
        pushed_branch = repo.remotes.origin.push().raise_if_error()

        return 'push_proc : Success'
    except Exception as push_err:
        GitErrLog(push_err=push_err, pull_result=pulled_branches, push_result=pushed_branch)
        if RETRY_COUNT < 5:
            RETRY_COUNT += 1
            time.sleep(5)
            push_proc(repo)
        else:
            return 'push_proc : Failure'


def commit_proc(repo):
    # commit message 설정
    author = Actor(USER_AUTHOR, USER_EMAIL)        # commit을 처음 만든 사람
    message = make_commit_message()
    # git staging 생성
    add_files, del_files = get_tracked_path(repo)
    r_index = repo.index

    try:
        stg_add, stg_del = [], []
        if add_files:
            stg_add = r_index.add(add_files)
        if del_files:
            stg_del = r_index.remove(del_files)
    except Exception as stg_err:
        GitErrLog(stg_err=stg_err, add_files=add_files, del_files=del_files)
        return False
    # git commit 생성
    try:
        if stg_add or stg_del:
            r_index.commit(message, author=author)
    except Exception as cmt_err:
        GitErrLog(cmt_err=cmt_err, stg_add=stg_add, stg_del=stg_del)
        return False
    return True


def auto_push():
    # repo 정의
    source_repo = Repo(SOURCE_REPO_PATH)
    # commit 실행
    if source_repo:
        commit_result = commit_proc(source_repo)
    # push 실행
    if commit_result:
        push_result = push_proc(source_repo)
    # push 결과 출력
    print(push_result)


if __name__ == "__main__":
    Crawler = ArticleCrawler()
    Crawler.set_category('IT과학', '경제', '사회')
    Crawler.start()
    auto_push()
