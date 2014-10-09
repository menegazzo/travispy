from .account import Account
from .branch import Branch
from .broadcast import Broadcast
from .build import Build
from .commit import Commit
from .hook import Hook
from .job import Job
from .log import Log
from .repo import Repo
from .session import Session
from .user import User


COMMAND_TO_ENTITY = {
    Account.many(): Account,
    Account.one(): Account,

    Branch.many(): Branch,
    Branch.one(): Branch,

    Broadcast.many(): Broadcast,
    Broadcast.one(): Broadcast,

    Build.many(): Build,
    Build.one(): Build,

    Commit.many(): Commit,
    Commit.one(): Commit,

    Hook.many(): Hook,
    Hook.one(): Hook,

    Job.many(): Job,
    Job.one(): Job,

    Log.many(): Log,
    Log.one(): Log,

    Repo.many(): Repo,
    Repo.one(): Repo,

    User.many(): User,
    User.one(): User,
}
