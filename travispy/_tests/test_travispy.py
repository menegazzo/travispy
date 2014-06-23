from travispy import TravisPy
from travispy.entities import User
import os
import pytest



#===================================================================================================
# Test
#===================================================================================================
class Test:

    def setup_method(self, method):
        self._travis = TravisPy.github_auth(os.environ['TRAVISPY_GITHUB_ACCESS_TOKEN'])


    def test_accounts(self):
        accounts = self._travis.accounts()
        assert len(accounts) == 2

        assert accounts[0].id == 72481
        account = self._travis.account(72481)
        assert account.name == 'Fabio Menegazzo'
        assert account.login == 'menegazzo'
        assert account.type == 'user'
        assert account.repos_count == 7
        assert not hasattr(account, 'subscribed') # Only for Pro and Enterprise

        assert accounts[1].id == 17781
        account = self._travis.account(17781)
        assert account.name == 'ESSS'
        assert account.login == 'ESSS'
        assert account.type == 'organization'
        assert hasattr(account, 'repos_count')
        assert not hasattr(account, 'subscribed') # Only for Pro and Enterprise

        account = self._travis.account(123)
        assert account is None


    def test_broadcasts(self):
        broadcasts = self._travis.broadcasts()
        assert len(broadcasts) == 0


    def test_builds(self):
        pytest.raises(RuntimeError, self._travis.builds)

        builds = self._travis.builds(repository_id=2298605)
        assert len(builds) == 25
        assert builds[0].repository_id == 2298605
        assert builds[-1].repository_id == 2298605

        build = self._travis.build(25718103) # menegazzo/watchsubs #52
        assert build.id == 25718103
        assert build.repository_id == 2298605
        assert build.commit_id == 7430235
        assert build.number == '52'
        assert build.pull_request == False
        assert build.pull_request_title == None
        assert build.pull_request_number == None
        assert build.config == {
            '.result': 'configured',
            'os': 'linux',
            'language': 'python',
            'python': [
                '2.7'
            ],
            'before_install': [
                'sudo apt-get install rar',
                'sudo apt-get install unrar',
                'sudo apt-get install python-pyside'
            ],
            'install': [
                'pip install -r requirements.txt'
            ],
            'before_script': [
                'export PYTHONPATH="$PYTHONPATH:/usr/lib/python2.7/dist-packages/"'
            ],
            'script': 'py.test',
            'cache': 'apt',
        }
        assert hasattr(build, 'state')
        assert hasattr(build, 'started_at')
        assert hasattr(build, 'finished_at')
        assert hasattr(build, 'duration')
        assert build.job_ids == [25718104]

        assert build.restart() == True
        assert build.cancel() == True


    def test_hooks(self):
        hooks = self._travis.hooks()
        assert len(hooks) == 7


    def test_jobs(self):
        jobs = self._travis.jobs(ids=[25718104])
        assert len(jobs) == 1

        job = self._travis.job(25718104)
        assert job.build_id == 25718103
        assert job.repository_id == 2298605
        assert job.commit_id == 7430235
        assert job.log_id == 15928905
        assert job.number == '52.1'
        assert job.config == {
            '.result': 'configured',
            'language': 'python',
            'python': '2.7',
            'before_install': [
                'sudo apt-get install rar',
                'sudo apt-get install unrar',
                'sudo apt-get install python-pyside'
            ],
            'install': [
                'pip install -r requirements.txt'
            ],
            'before_script': [
                'export PYTHONPATH="$PYTHONPATH:/usr/lib/python2.7/dist-packages/"'
            ],
            'script': 'py.test',
            'cache': 'apt',
        }
        assert hasattr(job, 'state')
        assert hasattr(job, 'started_at')
        assert hasattr(job, 'finished_at')
        assert job.queue == 'builds.linux'
        assert job.allow_failure == False
        assert job.annotation_ids == []

        assert job.restart() == True
        assert job.cancel() == True


    def test_log(self):
        log = self._travis.log(15928905)
        assert log.id == 15928905
        assert log.job_id == 25718104
        assert hasattr(log, 'body')


    def test_repos(self):
        repos = self._travis.repos()
        assert len(repos) == 25

        repos = self._travis.repos(member='menegazzo')
        assert len(repos) == 5

        repos = self._travis.repos(owner_name='menegazzo')
        assert len(repos) == 3

        assert repos[0].id == 2298605
        repo = self._travis.repo(repos[0].id)
        assert repo.id == 2298605
        assert repo.slug == 'menegazzo/watchsubs'
        assert repo.description == 'You get the videos, it gets the subtitles.'
        assert repo.github_language == 'Python'
        assert hasattr(repo, 'last_build_id')
        assert hasattr(repo, 'last_build_number')
        assert hasattr(repo, 'last_build_state')
        assert hasattr(repo, 'last_build_duration')
        assert hasattr(repo, 'last_build_started_at')
        assert hasattr(repo, 'last_build_finished_at')
        assert repo.id == self._travis.repo(repos[0].slug).id


    def test_user(self):
        user = self._travis.user()
        assert isinstance(user, User) == True

        assert user.login == 'menegazzo'
        assert user.name == 'Fabio Menegazzo'
        assert user.email == 'menegazzo@gmail.com'
