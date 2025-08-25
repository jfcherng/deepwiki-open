from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class GerritUrlInfo:
    base_url: str
    """E.g., `https://release-git.rtkbf.com/gerrit`"""
    project: str
    """E.g., `sdlc/realtek_release`"""
    owner: str = "gerrit-owner"

    # ----------------- #
    # not always in URL #
    # ----------------- #

    branch: str | None = None
    revision: str | None = None

    @property
    def project_safe_path(self) -> str:
        """
        A safe version of the project name for use in file paths.

        A Gerrit project name usually contains slashes, which are not safe for file paths.

        E.g., `sdlc__realtek_release`
        """
        return self.project.replace("/", "__")

    @property
    def project_safe_url(self) -> str:
        """
        A safe version of the project name for use in url.

        A Gerrit project name usually contains slashes, which are not safe for file paths.

        E.g., `sdlc%2Frealtek_release`
        """
        return self.project.replace("/", "%2F")


class Gerrit(ABC):
    PROVIDER = "gerrit"

    @classmethod
    @abstractmethod
    def is_supported(cls, url: str) -> bool:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def parse_url(cls, url: str) -> GerritUrlInfo | None:
        raise NotImplementedError


class RealtekGerrit(Gerrit):
    PROVIDER = "realtek-gerrit"

    URL_RE = re.compile(
        r"""^
            (?P<base_url>https?://[^/]+\.(?:rtkbf|realtek)\.com/gerrit)
            (?:/admin/repos)?
            /(?P<project>[^,]+)
        """,
        re.VERBOSE,
    )
    """
    Some URL formats...

    - git clone "https://release-git.rtkbf.com/gerrit/sdlc/realtek_release"
    - https://release-git.rtkbf.com/gerrit/admin/repos/sdlc/realtek_release,general
    """

    @classmethod
    @abstractmethod
    def is_supported(cls, url: str) -> bool:
        return cls.URL_RE.match(url) is not None

    @classmethod
    @abstractmethod
    def parse_url(cls, url: str) -> GerritUrlInfo | None:
        if m := cls.URL_RE.match(url):
            return GerritUrlInfo(
                base_url=m.group("base_url"),
                project=m.group("project").replace("%2F", "/").removesuffix(".git"),
                owner="realtek",
            )
        return None
