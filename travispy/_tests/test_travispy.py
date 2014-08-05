from travispy import TravisPy
from travispy.entities import Build, Job, Log, Repo, User
import os
import pytest



#===================================================================================================
# Test
#===================================================================================================
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
        assert TravisPy.github_auth('invalid') is None


    def test_accounts(self):
        accounts = self._travis.accounts()
        assert len(accounts) == 1

        assert accounts[0].id == 84789
        account = self._travis.account(84789)
        assert account.name == 'TravisPy'
        assert account.login == 'travispy'
        assert account.type == 'user'
        assert account.repos_count == 6
        assert not hasattr(account, 'subscribed') # Only for Pro and Enterprise

        account = self._travis.account(123)
        assert account is None


    def test_broadcasts(self):
        broadcasts = self._travis.broadcasts()
        assert len(broadcasts) == 0


    def test_builds(self, python_version, repo_slug):
        pytest.raises(RuntimeError, self._travis.builds)

        builds = self._travis.builds(slug=repo_slug)
        assert len(builds) == 1

        repo = self._travis.repo(repo_slug)
        build_id = builds[0].id
        build = self._travis.build(build_id)
        assert build.id == build_id
        assert build.repository_id == repo.id
        assert build.number == '1'
        assert build.pull_request == False
        assert build.pull_request_title == None
        assert build.pull_request_number == None
        assert build.config == {
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

        assert build.restart() == True
        assert build.cancel() == True

        repository = build.repository
        assert isinstance(repository, Repo)
        assert build.repository_id == repository.id
        assert repository == build.repository

        build.repository_id = -1
        assert build.repository == None

        jobs = build.jobs
        assert isinstance(jobs, list)

        job_ids = []
        for job in jobs:
            assert isinstance(job, Job)
            job_ids.append(job.id)

        assert build.job_ids == job_ids
        assert jobs == build.jobs

        build.job_ids = [-1]
        assert build.jobs == []


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
        assert job.number == '1.1'
        assert job.config == {
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
        assert job.queue == 'builds.linux'
        assert job.allow_failure == False
        assert job.annotation_ids == []

        assert job.restart() == True
        assert job.cancel() == True

        build = job.build
        assert isinstance(build, Build)
        assert job.build_id == build.id
        assert build == job.build

        job.build_id = -1
        assert job.build == None

        repository = job.repository
        assert isinstance(repository, Repo)
        assert job.repository_id == repository.id
        assert repository == job.repository

        job.repository_id = -1
        assert job.repository == None

        log = job.log
        assert isinstance(log, Log)
        assert job.log_id == log.id
        assert log == job.log

        job.log_id = -1
        assert job.log == None


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
        assert log.job == None


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
        assert repo.state == repo.last_build_state

        last_build = repo.last_build
        assert isinstance(last_build, Build)
        assert last_build.repository_id == repo.id
        assert last_build == repo.last_build

        repo.last_build_id = -1
        assert repo.last_build == None


    def test_user(self):
        user = self._travis.user()
        assert isinstance(user, User) == True

        # Accessing values using __getitem__
        assert user['login'] == 'travispy'
        assert user['name'] == 'TravisPy'
        assert user['email'] == 'menegazzo+travispy@gmail.com'
