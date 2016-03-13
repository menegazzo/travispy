from travispy import TravisPy
from travispy.entities import Build, Job, Log, Repo
from travispy.errors import TravisError
import pytest
import sys


@pytest.fixture(scope='module')
def travis():
    return TravisPy()


def test_github_auth():
    with pytest.raises(TravisError) as exception_info:
        TravisPy.github_auth('invalid')
    assert str(exception_info.value) == '[403] not a Travis user'


def test_branch(travis, test_settings, repo_slug):
    expected = test_settings.get('branch')
    if not expected:
        pytest.skip('TRAVISPY_TEST_SETTINGS has no "branch" value')

    pytest.raises(RuntimeError, travis.branches)

    branches = travis.branches(slug=repo_slug)
    assert len(branches) == expected['count']

    branch = travis.branch('master', repo_slug)
    assert branch.id == expected['id']
    assert branch.repository_id == expected['repository_id']
    assert branch.number == expected['number']
    assert branch.pull_request == expected['pull_request']
    assert branch.config == expected['config']

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


def test_build(travis, test_settings, repo_slug):
    expected = test_settings.get('build')
    if not expected:
        pytest.skip('TRAVISPY_TEST_SETTINGS has no "build" value')

    pytest.raises(RuntimeError, travis.builds)

    builds = travis.builds(slug=repo_slug)
    assert len(builds) == expected['count']

    build = travis.build(builds[0].id)
    assert build.id == expected['id']
    assert build.repository_id == expected['repository_id']
    assert build.number == expected['number']
    assert build.pull_request == expected['pull_request']
    assert build.pull_request_title == expected['pull_request_title']
    assert build.pull_request_number == expected['pull_request_number']
    assert build.config == expected['config']

    assert hasattr(build, 'commit_id')
    assert hasattr(build, 'state')
    assert hasattr(build, 'started_at')
    assert hasattr(build, 'finished_at')
    assert hasattr(build, 'duration')
    assert hasattr(build, 'job_ids')
    assert hasattr(build, 'commit')

    assert build.commit_id == build.commit.id

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


def test_commit(travis, test_settings, repo_slug):
    expected = test_settings.get('commit')
    if not expected:
        pytest.skip('TRAVISPY_TEST_SETTINGS has no "commit" value')

    builds = travis.builds(slug=repo_slug)
    assert len(builds) == expected['count']

    build = builds[0]
    assert hasattr(build, 'commit')

    commit = build.commit
    assert commit.id == expected['id']
    assert commit.sha == expected['sha']
    assert commit.branch == expected['branch']
    assert commit.message == expected['message']
    assert commit.committed_at == expected['committed_at']
    assert commit.author_name == expected['author_name']
    assert commit.author_email == expected['author_email']
    assert commit.committer_name == expected['commiter_name']
    assert commit.committer_email == expected['commiter_email']
    assert commit.compare_url == expected['compare_url']
    assert commit.pull_request_number == expected['pull_request_number']


def test_job(travis, test_settings, repo_slug):
    expected = test_settings.get('job')
    if not expected:
        pytest.skip('TRAVISPY_TEST_SETTINGS has no "job" value')

    pytest.raises(RuntimeError, travis.jobs)

    builds = travis.builds(slug=repo_slug)
    build_id = builds[0].id
    build = travis.build(build_id)

    jobs = travis.jobs(ids=build.job_ids)
    assert len(jobs) == expected['count']

    job = travis.job(build.job_ids[0])
    assert job.build_id == expected['build_id']
    assert job.repository_id == expected['repository_id']
    assert job.number == expected['number']
    assert job.config == expected['config']
    assert job.queue == expected['queue']
    assert job.allow_failure == expected['allow_failure']
    assert job.annotation_ids == expected['annotation_ids']

    assert hasattr(job, 'commit_id')
    assert hasattr(job, 'log_id')
    assert hasattr(job, 'state')
    assert hasattr(job, 'started_at')
    assert hasattr(job, 'finished_at')
    assert hasattr(job, 'commit')
    assert hasattr(job, 'duration')

    assert job.commit_id == job.commit.id


def test_job_negative_ids(travis):
    job = travis.job(81966565)

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


def test_archived_log(travis):
    log = travis.log(15928905)
    assert log.id == 15928905
    assert log.job_id == 25718104

    # Initial Log body is empty
    assert log._body is None

    # Dynamically fetch the log
    assert log.body
    unicode_type = unicode if sys.version_info[0] == 2 else str
    assert isinstance(log.body, unicode_type)

    job = log.job
    assert isinstance(job, Job)
    assert log.job_id == job.id
    assert job == log.job

    log.job_id = -1
    with pytest.raises(TravisError) as exception_info:
        log.job
    assert str(exception_info.value) == "[404] The job(-1) couldn't be found"


def test_incomplete_log(travis):
    jobs = travis.jobs(state='started')
    log = jobs[0].log
    assert log._body is not None
    assert log.body is not None


@pytest.mark.flaky(reruns=5)
def test_recent_passed_log(travis):
    jobs = travis.jobs(state='passed')
    log = jobs[0].log
    assert log._body is None
    assert log.body is not None
    assert log._body is not None


def test_empty_archived_log(travis):
    job = travis.job(81891594)
    assert job.build.id == 81891579
    assert job.log.job_id == 81891594

    log = job.log
    assert log._body is None
    assert log.body == ''
    assert log._body == ''


def test_repo(travis, test_settings, repo_slug):
    expected = test_settings.get('repo')
    if not expected:
        pytest.skip('TRAVISPY_TEST_SETTINGS has no "repo" value')

    repos = travis.repos()
    assert len(repos) == expected['public_count']

    repos = travis.repos(member='travispy')
    assert len(repos) == expected['member_count']

    repos = travis.repos(owner_name='travispy')
    assert len(repos) == expected['owner_count']

    repo = travis.repo(repo_slug)
    assert repo.slug == repo_slug
    assert repo.github_language == expected['github_language']
    assert repo.id == expected['id']
    assert repo.description == expected['description']
    assert repo.active == expected['active']

    assert hasattr(repo, 'last_build_id')
    assert hasattr(repo, 'last_build_number')
    assert hasattr(repo, 'last_build_state')
    assert hasattr(repo, 'last_build_duration')
    assert hasattr(repo, 'last_build_started_at')
    assert hasattr(repo, 'last_build_finished_at')
    assert hasattr(repo, 'state')

    last_build = repo.last_build
    assert isinstance(last_build, Build)
    assert last_build.repository_id == repo.id
    assert last_build == repo.last_build

    repo.last_build_id = -1
    with pytest.raises(TravisError) as exception_info:
        repo.last_build
    assert str(exception_info.value) == '[404] not found'
