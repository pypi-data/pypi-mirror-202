"""Implementation of the cache provider."""
# This plugin was not named "cache" to avoid conflicts with the external
# pytest-cache version.
import dataclasses
import json
import os
from pathlib import Path
from typing import Dict
from typing import Generator
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Union

from .pathlib import resolve_from_str
from .pathlib import rm_rf
from .reports import CollectReport
from _pytest import nodes
from _pytest._io import TerminalWriter
from _pytest.compat import final
from _pytest.config import Config
from _pytest.config import ExitCode
from _pytest.config import hookimpl
from _pytest.config.argparsing import Parser
from _pytest.deprecated import check_ispytest
from _pytest.fixtures import fixture
from _pytest.fixtures import FixtureRequest
from _pytest.main import Session
from _pytest.python import Module
from _pytest.python import Package
from _pytest.reports import TestReport

README_CONTENT = """\
# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
"""

CACHEDIR_TAG_CONTENT = b"""\
Signature: 8a477f597d28d172789f06886806bc55
# This file is a cache directory tag created by pytest.
# For information about cache directory tags, see:
#	https://bford.info/cachedir/spec.html
"""


@final
@dataclasses.dataclass
class Cache:
    """Instance of the `cache` fixture."""

    _cachedir: Path = dataclasses.field(repr=False)
    _config: Config = dataclasses.field(repr=False)

    # Sub-directory under cache-dir for directories created by `mkdir()`.
    _CACHE_PREFIX_DIRS = "d"

    # Sub-directory under cache-dir for values created by `set()`.
    _CACHE_PREFIX_VALUES = "v"

    def __init__(
        self, cachedir: Path, config: Config, *, _ispytest: bool = False
    ) -> None:
        check_ispytest(_ispytest)
        self._cachedir = cachedir
        self._config = config

    @classmethod
    def for_config(cls, config: Config, *, _ispytest: bool = False) -> "Cache":
        """Create the Cache instance for a Config.

        :meta private:
        """
        check_ispytest(_ispytest)
        cachedir = cls.cache_dir_from_config(config, _ispytest=True)
        if config.getoption("cacheclear") and cachedir.is_dir():
            cls.clear_cache(cachedir, _ispytest=True)
        return cls(cachedir, config, _ispytest=True)

    @classmethod
    def clear_cache(cls, cachedir: Path, _ispytest: bool = False) -> None:
        """Clear the sub-directories used to hold cached directories and values.

        :meta private:
        """
        check_ispytest(_ispytest)
        for prefix in (cls._CACHE_PREFIX_DIRS, cls._CACHE_PREFIX_VALUES):
            d = cachedir / prefix
            if d.is_dir():
                rm_rf(d)

    @staticmethod
    def cache_dir_from_config(config: Config, *, _ispytest: bool = False) -> Path:
        """Get the path to the cache directory for a Config.

        :meta private:
        """
        check_ispytest(_ispytest)
        return resolve_from_str(config.getini("cache_dir"), config.rootpath)

    def warn(self, fmt: str, *, _ispytest: bool = False, **args: object) -> None:
        """Issue a cache warning.

        :meta private:
        """
        check_ispytest(_ispytest)
        import warnings
        from _pytest.warning_types import PytestCacheWarning

        warnings.warn(
            PytestCacheWarning(fmt.format(**args) if args else fmt),
            self._config.hook,
            stacklevel=3,
        )

    def mkdir(self, name: str) -> Path:
        """Return a directory path object with the given name.

        If the directory does not yet exist, it will be created. You can use
        it to manage files to e.g. store/retrieve database dumps across test
        sessions.

        .. versionadded:: 7.0

        :param name:
            Must be a string not containing a ``/`` separator.
            Make sure the name contains your plugin or application
            identifiers to prevent clashes with other cache users.
        """
        path = Path(name)
        if len(path.parts) > 1:
            raise ValueError("name is not allowed to contain path separators")
        res = self._cachedir.joinpath(self._CACHE_PREFIX_DIRS, path)
        res.mkdir(exist_ok=True, parents=True)
        return res

    def _getvaluepath(self, key: str) -> Path:
        return self._cachedir.joinpath(self._CACHE_PREFIX_VALUES, Path(key))

    def get(self, key: str, default):
        """Return the cached value for the given key.

        If no value was yet cached or the value cannot be read, the specified
        default is returned.

        :param key:
            Must be a ``/`` separated value. Usually the first
            name is the name of your plugin or your application.
        :param default:
            The value to return in case of a cache-miss or invalid cache value.
        """
        path = self._getvaluepath(key)
        try:
            with path.open("r", encoding="UTF-8") as f:
                return json.load(f)
        except (ValueError, OSError):
            return default

    def set(self, key: str, value: object) -> None:
        """Save value for the given key.

        :param key:
            Must be a ``/`` separated value. Usually the first
            name is the name of your plugin or your application.
        :param value:
            Must be of any combination of basic python types,
            including nested types like lists of dictionaries.
        """
        path = self._getvaluepath(key)
        try:
            if path.parent.is_dir():
                cache_dir_exists_already = True
            else:
                cache_dir_exists_already = self._cachedir.exists()
                path.parent.mkdir(exist_ok=True, parents=True)
        except OSError:
            self.warn("could not create cache path {path}", path=path, _ispytest=True)
            return
        if not cache_dir_exists_already:
            self._ensure_supporting_files()
        data = json.dumps(value, ensure_ascii=False, indent=2)
        try:
            f = path.open("w", encoding="UTF-8")
        except OSError:
            self.warn("cache could not write path {path}", path=path, _ispytest=True)
        else:
            with f:
                f.write(data)

    def _ensure_supporting_files(self) -> None:
        """Create supporting files in the cache dir that are not really part of the cache."""
        readme_path = self._cachedir / "README.md"
        readme_path.write_text(README_CONTENT, encoding="UTF-8")

        gitignore_path = self._cachedir.joinpath(".gitignore")
        msg = "# Created by pytest automatically.\n*\n"
        gitignore_path.write_text(msg, encoding="UTF-8")

        cachedir_tag_path = self._cachedir.joinpath("CACHEDIR.TAG")
        cachedir_tag_path.write_bytes(CACHEDIR_TAG_CONTENT)


class LFPluginCollWrapper:
    def __init__(self, lfplugin: "LFPlugin") -> None:
        self.lfplugin = lfplugin
        self._collected_at_least_one_failure = False

    @hookimpl(hookwrapper=True)
    def pytest_make_collect_report(self, collector: nodes.Collector):
        if isinstance(collector, Session):
            out = yield
            res: CollectReport = out.get_result()

            # Sort any lf-paths to the beginning.
            lf_paths = self.lfplugin._last_failed_paths

            res.result = sorted(
                res.result,
                # use stable sort to priorize last failed
                key=lambda x: x.path in lf_paths,
                reverse=True,
            )
            return

        elif isinstance(collector, Module):
            if collector.path in self.lfplugin._last_failed_paths:
                out = yield
                res = out.get_result()
                result = res.result
                lastfailed = self.lfplugin.lastfailed

                # Only filter with known failures.
                if not self._collected_at_least_one_failure:
                    if not any(x.nodeid in lastfailed for x in result):
                        return
                    self.lfplugin.config.pluginmanager.register(
                        LFPluginCollSkipfiles(self.lfplugin), "lfplugin-collskip"
                    )
                    self._collected_at_least_one_failure = True

                session = collector.session
                result[:] = [
                    x
                    for x in result
                    if x.nodeid in lastfailed
                    # Include any passed arguments (not trivial to filter).
                    or session.isinitpath(x.path)
                    # Keep all sub-collectors.
                    or isinstance(x, nodes.Collector)
                ]
                return
        yield


class LFPluginCollSkipfiles:
    def __init__(self, lfplugin: "LFPlugin") -> None:
        self.lfplugin = lfplugin

    @hookimpl
    def pytest_make_collect_report(
        self, collector: nodes.Collector
    ) -> Optional[CollectReport]:
        # Packages are Modules, but _last_failed_paths only contains
        # test-bearing paths and doesn't try to include the paths of their
        # packages, so don't filter them.
        if isinstance(collector, Module) and not isinstance(collector, Package):
            if collector.path not in self.lfplugin._last_failed_paths:
                self.lfplugin._skipped_files += 1

                return CollectReport(
                    collector.nodeid, "passed", longrepr=None, result=[]
                )
        return None


class LFPlugin:
    """Plugin which implements the --lf (run last-failing) option."""

    def __init__(self, config: Config) -> None:
        self.config = config
        active_keys = "lf", "failedfirst"
        self.active = any(config.getoption(key) for key in active_keys)
        assert config.cache
        self.lastfailed: Dict[str, bool] = config.cache.get("cache/lastfailed", {})
        self._previously_failed_count: Optional[int] = None
        self._report_status: Optional[str] = None
        self._skipped_files = 0  # count skipped files during collection due to --lf

        if config.getoption("lf"):
            self._last_failed_paths = self.get_last_failed_paths()
            config.pluginmanager.register(
                LFPluginCollWrapper(self), "lfplugin-collwrapper"
            )

    def get_last_failed_paths(self) -> Set[Path]:
        """Return a set with all Paths()s of the previously failed nodeids."""
        rootpath = self.config.rootpath
        result = {rootpath / nodeid.split("::")[0] for nodeid in self.lastfailed}
        return {x for x in result if x.exists()}

    def pytest_report_collectionfinish(self) -> Optional[str]:
        if self.active and self.config.getoption("verbose") >= 0:
            return "run-last-failure: %s" % self._report_status
        return None

    def pytest_runtest_logreport(self, report: TestReport) -> None:
        if (report.when == "call" and report.passed) or report.skipped:
            self.lastfailed.pop(report.nodeid, None)
        elif report.failed:
            self.lastfailed[report.nodeid] = True

    def pytest_collectreport(self, report: CollectReport) -> None:
        passed = report.outcome in ("passed", "skipped")
        if passed:
            if report.nodeid in self.lastfailed:
                self.lastfailed.pop(report.nodeid)
                self.lastfailed.update((item.nodeid, True) for item in report.result)
        else:
            self.lastfailed[report.nodeid] = True

    @hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_collection_modifyitems(
        self, config: Config, items: List[nodes.Item]
    ) -> Generator[None, None, None]:
        yield

        if not self.active:
            return

        if self.lastfailed:
            previously_failed = []
            previously_passed = []
            for item in items:
                if item.nodeid in self.lastfailed:
                    previously_failed.append(item)
                else:
                    previously_passed.append(item)
            self._previously_failed_count = len(previously_failed)

            if not previously_failed:
                # Running a subset of all tests with recorded failures
                # only outside of it.
                self._report_status = "%d known failures not in selected tests" % (
                    len(self.lastfailed),
                )
            else:
                if self.config.getoption("lf"):
                    items[:] = previously_failed
                    config.hook.pytest_deselected(items=previously_passed)
                else:  # --failedfirst
                    items[:] = previously_failed + previously_passed

                noun = "failure" if self._previously_failed_count == 1 else "failures"
                suffix = " first" if self.config.getoption("failedfirst") else ""
                self._report_status = "rerun previous {count} {noun}{suffix}".format(
                    count=self._previously_failed_count, suffix=suffix, noun=noun
                )

            if self._skipped_files > 0:
                files_noun = "file" if self._skipped_files == 1 else "files"
                self._report_status += " (skipped {files} {files_noun})".format(
                    files=self._skipped_files, files_noun=files_noun
                )
        else:
            self._report_status = "no previously failed tests, "
            if self.config.getoption("last_failed_no_failures") == "none":
                self._report_status += "deselecting all items."
                config.hook.pytest_deselected(items=items[:])
                items[:] = []
            else:
                self._report_status += "not deselecting items."

    def pytest_sessionfinish(self, session: Session) -> None:
        config = self.config
        if config.getoption("cacheshow") or hasattr(config, "workerinput"):
            return

        assert config.cache is not None
        saved_lastfailed = config.cache.get("cache/lastfailed", {})
        if saved_lastfailed != self.lastfailed:
            config.cache.set("cache/lastfailed", self.lastfailed)


class NFPlugin:
    """Plugin which implements the --nf (run new-first) option."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self.active = config.option.newfirst
        assert config.cache is not None
        self.cached_nodeids = set(config.cache.get("cache/nodeids", []))

    @hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_collection_modifyitems(
        self, items: List[nodes.Item]
    ) -> Generator[None, None, None]:
        yield

        if self.active:
            new_items: Dict[str, nodes.Item] = {}
            other_items: Dict[str, nodes.Item] = {}
            for item in items:
                if item.nodeid not in self.cached_nodeids:
                    new_items[item.nodeid] = item
                else:
                    other_items[item.nodeid] = item

            items[:] = self._get_increasing_order(
                new_items.values()
            ) + self._get_increasing_order(other_items.values())
            self.cached_nodeids.update(new_items)
        else:
            self.cached_nodeids.update(item.nodeid for item in items)

    def _get_increasing_order(self, items: Iterable[nodes.Item]) -> List[nodes.Item]:
        return sorted(items, key=lambda item: item.path.stat().st_mtime, reverse=True)  # type: ignore[no-any-return]

    def pytest_sessionfinish(self) -> None:
        config = self.config
        if config.getoption("cacheshow") or hasattr(config, "workerinput"):
            return

        if config.getoption("collectonly"):
            return

        assert config.cache is not None
        config.cache.set("cache/nodeids", sorted(self.cached_nodeids))


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--lf",
        "--last-failed",
        action="store_true",
        dest="lf",
        help="Rerun only the tests that failed "
        "at the last run (or all if none failed)",
    )
    group.addoption(
        "--ff",
        "--failed-first",
        action="store_true",
        dest="failedfirst",
        help="Run all tests, but run the last failures first. "
        "This may re-order tests and thus lead to "
        "repeated fixture setup/teardown.",
    )
    group.addoption(
        "--nf",
        "--new-first",
        action="store_true",
        dest="newfirst",
        help="Run tests from new files first, then the rest of the tests "
        "sorted by file mtime",
    )
    group.addoption(
        "--cache-show",
        action="append",
        nargs="?",
        dest="cacheshow",
        help=(
            "Show cache contents, don't perform collection or tests. "
            "Optional argument: glob (default: '*')."
        ),
    )
    group.addoption(
        "--cache-clear",
        action="store_true",
        dest="cacheclear",
        help="Remove all cache contents at start of test run",
    )
    cache_dir_default = ".pytest_cache"
    if "TOX_ENV_DIR" in os.environ:
        cache_dir_default = os.path.join(os.environ["TOX_ENV_DIR"], cache_dir_default)
    parser.addini("cache_dir", default=cache_dir_default, help="Cache directory path")
    group.addoption(
        "--lfnf",
        "--last-failed-no-failures",
        action="store",
        dest="last_failed_no_failures",
        choices=("all", "none"),
        default="all",
        help="Which tests to run with no previously (known) failures",
    )


def pytest_cmdline_main(config: Config) -> Optional[Union[int, ExitCode]]:
    if config.option.cacheshow and not config.option.help:
        from _pytest.main import wrap_session

        return wrap_session(config, cacheshow)
    return None


@hookimpl(tryfirst=True)
def pytest_configure(config: Config) -> None:
    config.cache = Cache.for_config(config, _ispytest=True)
    config.pluginmanager.register(LFPlugin(config), "lfplugin")
    config.pluginmanager.register(NFPlugin(config), "nfplugin")


@fixture
def cache(request: FixtureRequest) -> Cache:
    """Return a cache object that can persist state between testing sessions.

    cache.get(key, default)
    cache.set(key, value)

    Keys must be ``/`` separated strings, where the first part is usually the
    name of your plugin or application to avoid clashes with other cache users.

    Values can be any object handled by the json stdlib module.
    """
    assert request.config.cache is not None
    return request.config.cache


def pytest_report_header(config: Config) -> Optional[str]:
    """Display cachedir with --cache-show and if non-default."""
    if config.option.verbose > 0 or config.getini("cache_dir") != ".pytest_cache":
        assert config.cache is not None
        cachedir = config.cache._cachedir
        # TODO: evaluate generating upward relative paths
        # starting with .., ../.. if sensible

        try:
            displaypath = cachedir.relative_to(config.rootpath)
        except ValueError:
            displaypath = cachedir
        return f"cachedir: {displaypath}"
    return None


def cacheshow(config: Config, session: Session) -> int:
    from pprint import pformat

    assert config.cache is not None

    tw = TerminalWriter()
    tw.line("cachedir: " + str(config.cache._cachedir))
    if not config.cache._cachedir.is_dir():
        tw.line("cache is empty")
        return 0

    glob = config.option.cacheshow[0]
    if glob is None:
        glob = "*"

    dummy = object()
    basedir = config.cache._cachedir
    vdir = basedir / Cache._CACHE_PREFIX_VALUES
    tw.sep("-", "cache values for %r" % glob)
    for valpath in sorted(x for x in vdir.rglob(glob) if x.is_file()):
        key = str(valpath.relative_to(vdir))
        val = config.cache.get(key, dummy)
        if val is dummy:
            tw.line("%s contains unreadable content, will be ignored" % key)
        else:
            tw.line("%s contains:" % key)
            for line in pformat(val).splitlines():
                tw.line("  " + line)

    ddir = basedir / Cache._CACHE_PREFIX_DIRS
    if ddir.is_dir():
        contents = sorted(ddir.rglob(glob))
        tw.sep("-", "cache directories for %r" % glob)
        for p in contents:
            # if p.is_dir():
            #    print("%s/" % p.relative_to(basedir))
            if p.is_file():
                key = str(p.relative_to(basedir))
                tw.line(f"{key} is a file of length {p.stat().st_size:d}")
    return 0
