import logging
from dataclasses import dataclass
from pathlib import Path

from git import Repo, Tag
from git.objects import Commit

from uv_version.collectors.base import BaseCollector

logger = logging.getLogger('uv-version')


@dataclass()
class GitCommitStatus(object):
    tag_name: str | None
    hash: str

    @property
    def short_hash(self):
        return self.hash[:7]


@dataclass()
class GitStatus(object):
    is_dirty: bool
    branch: str

    tag: GitCommitStatus | None
    commit: GitCommitStatus

    distance: int


class GitService(object):
    repo: Repo

    def __init__(self) -> None:
        path = Path.cwd()
        self.repo = Repo(path, search_parent_directories=True)

    @property
    def commits(self) -> list[Commit]:
        return list(self.repo.iter_commits())

    @property
    def tags(self) -> list[Tag]:
        return list(self.repo.tags)[::-1]

    def get_last_tag(self) -> Tag | None:
        """Получение последнего тега нынешней ветки."""
        tag_dict = {tag.commit: tag for tag in self.tags}

        for commit in self.commits:
            if commit in tag_dict:
                return tag_dict[commit]

        return None

    def get_distance(self, from_commit: Commit, to_commit: Commit) -> int:
        return len(list(self.repo.iter_commits(f'{from_commit}..{to_commit}')))

    def get_status(self) -> GitStatus:
        tag = self.get_last_tag()
        commit = self.repo.head.commit

        if tag is None:
            return GitStatus(
                self.repo.is_dirty(),
                self.repo.active_branch.name,
                None,
                GitCommitStatus(
                    None,
                    commit.hexsha,
                ),
                0,
            )

        is_current_tag = tag.commit.hexsha == commit.hexsha
        distance = self.get_distance(tag.commit, commit)

        return GitStatus(
            self.repo.is_dirty(),
            self.repo.active_branch.name,
            GitCommitStatus(tag.name, tag.commit.hexsha),
            GitCommitStatus(tag.name if is_current_tag else None, commit.hexsha),
            distance,
        )


class GitCollector(BaseCollector):
    def __init__(self) -> None:
        super().__init__()
        self._git_service = GitService()

    def collect(self) -> str | None:
        status = self._git_service.get_status()

        if status.tag is not None and status.distance == 0:
            return status.tag.tag_name

        if status.tag is not None:
            return f'{status.tag.tag_name}.post{status.distance}+{status.commit.short_hash}'

        return f'0.0.0.post{status.distance}+{status.commit.short_hash}'
