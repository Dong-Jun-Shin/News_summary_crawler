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
    try:
        # push 전 pull 실행
        pull_result = repo.remotes.origin.pull()[0]     # output >>> origin/main
        # push 실행
        push_result = repo.remotes.origin.push()[0]
    except Exception as e:
        print('error Pull or Push : ' + str(e))
        print('pull_result : ' + str(pull_result))
        print('push_result : ' + str(push_result))
        return 'push_proc : Success'
    return 'push_proc : Failure'


def commit_proc(repo):
    # commit message 설정
    author = Actor(USER_AUTHOR, USER_EMAIL)        # 처음 만든 사람
    message = make_commit_message()
    # git staging 생성
    add_files, del_files = get_tracked_path(repo)
    r_index = repo.index
    try:
        r_add_result, r_del_result = [], []
        if add_files:
            r_add_result = r_index.add(add_files)
        if del_files:
            r_del_result = r_index.remove(del_files)
    except Exception as e:
        print('error Staging : ' + str(e))
        print('add_files : ' + str(add_files))
        print('del_files : ' + str(del_files))
        return False
    # git commit 생성
    try:
        if r_add_result or r_del_result:
            r_index.commit(message, author=author)
    except Exception as e:
        print('error Commit : ' + str(e))
        print('r_add_result : ' + str(r_add_result))
        print('r_del_result : ' + str(r_del_result))
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
