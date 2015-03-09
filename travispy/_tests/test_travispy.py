from travispy import TravisPy
from travispy.entities import Build, Job, Log, Repo, User
from travispy.errors import AuthenticationError, TravisError
import os
import pytest
import time


class Test:

    def setup_method(self, method):
        self._travis = TravisPy.github_auth(os.environ['TRAVISPY_GITHUB_ACCESS_TOKEN'])

    @pytest.fixture
    def python_version(self):
        try:
            import __pypy__
            return 'pypy'
        except ImportError:
            import sys
            return '%d.%d' % (
                sys.version_info[0],
                sys.version_info[1],
            )

    @pytest.fixture
    def repo_slug(self):
        try:
            import __pypy__
            return 'travispy/on_pypy'
        except ImportError:
            import sys
            return 'travispy/on_py%d%d' % (
                sys.version_info[0],
                sys.version_info[1],
            )

    def test_github_auth(self):
        with pytest.raises(AuthenticationError) as exception_info:
            TravisPy.github_auth('invalid')
        assert str(exception_info.value) == '[500] error while authenticating against GitHub'

    def test_accounts(self):
        accounts = self._travis.accounts()
        assert len(accounts) == 1

        assert accounts[0].id == 84789
        account = self._travis.account(84789)
        assert account.name == 'TravisPy'
        assert account.login == 'travispy'
        assert account.type == 'user'
        assert account.repos_count == 6
        assert not hasattr(account, 'subscribed')  # Only for Pro and Enterprise

        account = self._travis.account(123)
        assert account is None

    def test_branches(self, python_version, repo_slug):
        pytest.raises(RuntimeError, self._travis.branches)

        branches = self._travis.branches(slug=repo_slug)
        assert len(branches) == 2

        repo = self._travis.repo(repo_slug)
        branch = self._travis.branch('master', repo_slug)
        assert branch.id == branches[0].id
        assert branch.repository_id == repo.id
        assert branch.number == '3'
        assert branch.pull_request is False
        assert branch.config == {
            'sudo': False,
            '.result': 'configured',
            'os': 'linux',
            'language': 'python',
            'python': [python_version],
            'script': ['py.test'],
        }
        assert hasattr(branch, 'commit_id')
        assert hasattr(branch, 'state')
        assert hasattr(branch, 'started_at')
        assert hasattr(branch, 'finished_at')
        assert hasattr(branch, 'duration')
        assert hasattr(branch, 'job_ids')
        assert hasattr(branch, 'commit')

        assert branch.commit_id == branch.commit.id

        repository = branch.repository
        assert isinstance(repository, Repo)
        assert branch.repository_id == repository.id
        assert repository == branch.repository

        branch.repository_id = -1
        assert branch.repository is None

        jobs = branch.jobs
        assert isinstance(jobs, list)

        job_ids = []
        for job in jobs:
            assert isinstance(job, Job)
            job_ids.append(job.id)

        assert branch.job_ids == job_ids
        assert jobs == branch.jobs

    def test_broadcasts(self):
        broadcasts = self._travis.broadcasts()
        assert isinstance(broadcasts, list)

    def test_builds(self, python_version, repo_slug):
        pytest.raises(RuntimeError, self._travis.builds)

        builds = self._travis.builds(slug=repo_slug)
        assert len(builds) == 3

        repo = self._travis.repo(repo_slug)
        build_id = builds[0].id
        build = self._travis.build(build_id)
        assert build.id == build_id
        assert build.repository_id == repo.id
        assert build.number == '3'
        assert build.pull_request is False
        assert build.pull_request_title is None
        assert build.pull_request_number is None
        assert build.config == {
            'sudo': False,
            '.result': 'configured',
            'os': 'linux',
            'language': 'python',
            'python': [python_version],
            'script': ['py.test'],
        }
        assert hasattr(build, 'commit_id')
        assert hasattr(build, 'state')
        assert hasattr(build, 'started_at')
        assert hasattr(build, 'finished_at')
        assert hasattr(build, 'duration')
        assert hasattr(build, 'job_ids')
        assert hasattr(build, 'commit')

        assert build.commit_id == build.commit.id

        count = 0
        while not build.restart():
            if count >= 10:
                assert False
            time.sleep(1)
            count += 1

        count = 0
        while not build.cancel():
            if count >= 10:
                assert False
            time.sleep(1)
            count += 1

        repository = build.repository
        assert isinstance(repository, Repo)
        assert build.repository_id == repository.id
        assert repository == build.repository

        build.repository_id = -1
        assert build.repository is None

        jobs = build.jobs
        assert isinstance(jobs, list)

        job_ids = []
        for job in jobs:
            assert isinstance(job, Job)
            job_ids.append(job.id)

        assert build.job_ids == job_ids
        assert jobs == build.jobs

    def test_commit(self, repo_slug):
        builds = self._travis.builds(slug=repo_slug)

        build = builds[0]
        assert hasattr(build, 'commit')

        commit = build.commit
        assert hasattr(commit, 'id')
        assert hasattr(commit, 'sha')
        assert hasattr(commit, 'branch')
        assert hasattr(commit, 'message')
        assert hasattr(commit, 'committed_at')
        assert hasattr(commit, 'author_name')
        assert hasattr(commit, 'author_email')
        assert hasattr(commit, 'committer_name')
        assert hasattr(commit, 'committer_email')
        assert hasattr(commit, 'compare_url')
        assert hasattr(commit, 'pull_request_number')

    def test_hooks(self):
        hooks = self._travis.hooks()
        assert len(hooks) == 6

    def test_jobs(self, python_version, repo_slug):
        pytest.raises(RuntimeError, self._travis.jobs)

        repo = self._travis.repo(repo_slug)

        builds = self._travis.builds(slug=repo_slug)
        build_id = builds[0].id
        build = self._travis.build(build_id)

        jobs = self._travis.jobs(ids=build.job_ids)
        assert len(jobs) == 1

        job = self._travis.job(build.job_ids[0])
        assert job.build_id == build_id
        assert job.repository_id == repo.id
        assert job.number == '3.1'
        assert job.config == {
            'sudo': False,
            'os': 'linux',
            '.result': 'configured',
            'language': 'python',
            'python': python_version,
            'script': ['py.test'],
        }
        assert hasattr(job, 'commit_id')
        assert hasattr(job, 'log_id')
        assert hasattr(job, 'state')
        assert hasattr(job, 'started_at')
        assert hasattr(job, 'finished_at')
        assert job.queue == 'builds.docker'
        assert job.allow_failure is False
        assert job.annotation_ids == []
        assert hasattr(job, 'commit')
        assert hasattr(job, 'duration')

        assert job.commit_id == job.commit.id

        count = 0
        while not job.restart():
            if count >= 10:
                assert False
            time.sleep(1)
            count += 1

        count = 0
        while not job.cancel():
            if count >= 10:
                assert False
            time.sleep(1)
            count += 1

        build = job.build
        assert isinstance(build, Build)
        assert job.build_id == build.id
        assert build == job.build

        job.build_id = -1
        with pytest.raises(TravisError) as exception_info:
            job.build
        assert str(exception_info.value) == "[404] not found"

        repository = job.repository
        assert isinstance(repository, Repo)
        assert job.repository_id == repository.id
        assert repository == job.repository

        job.repository_id = -1
        assert job.repository is None

        log = job.log
        assert isinstance(log, Log)
        assert job.log_id == log.id
        assert log == job.log

        job.log_id = -1
        with pytest.raises(TravisError) as exception_info:
            job.log
        assert str(exception_info.value) == "[404] not found"

    def test_log(self):
        log = self._travis.log(15928905)
        assert log.id == 15928905
        assert log.job_id == 25718104
        assert hasattr(log, 'body')

        job = log.job
        assert isinstance(job, Job)
        assert log.job_id == job.id
        assert job == log.job

        log.job_id = -1
        with pytest.raises(TravisError) as exception_info:
            log.job
        assert str(exception_info.value) == "[404] The job(-1) couldn't be found"

    def test_repos(self, repo_slug):
        repos = self._travis.repos()
        assert len(repos) == 25

        repos = self._travis.repos(member='travispy')
        assert len(repos) == 7

        repos = self._travis.repos(owner_name='travispy')
        assert len(repos) == 6

        repo = self._travis.repo(repo_slug)
        assert repo.slug == repo_slug
        assert repo.github_language == 'Python'
        assert hasattr(repo, 'id')
        assert hasattr(repo, 'description')
        assert hasattr(repo, 'last_build_id')
        assert hasattr(repo, 'last_build_number')
        assert hasattr(repo, 'last_build_state')
        assert hasattr(repo, 'last_build_duration')
        assert hasattr(repo, 'last_build_started_at')
        assert hasattr(repo, 'last_build_finished_at')
        assert repo.active is True
        assert repo.state == repo.last_build_state

        last_build = repo.last_build
        assert isinstance(last_build, Build)
        assert last_build.repository_id == repo.id
        assert last_build == repo.last_build

        repo.last_build_id = -1
        with pytest.raises(TravisError) as exception_info:
            repo.last_build
        assert str(exception_info.value) == '[404] not found'

    def test_user(self):
        user = self._travis.user()
        assert isinstance(user, User) is True

        # Accessing values using __getitem__
        assert user['login'] == 'travispy'
        assert user['name'] == 'TravisPy'
        assert user['email'] == 'menegazzo+travispy@gmail.com'
