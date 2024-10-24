"""
Asyncio Crawler Support
"""

import asyncio

from asyncio.queues import Queue
from collections import deque
from datetime import datetime, timezone, tzinfo
import queue
from itertools import chain
import hashlib
import pickle
import re
import os
import sys
import traceback
from typing import Dict, List, Any, Tuple
import time
import types
from datetime import datetime, timedelta
from functools import partial
import itertools
import functools

# from pprint import pformat
import yaml

from jinja2 import Template, StrictUndefined

# import requests
import aiohttp
from pydantic import BaseModel as _BaseModel
from shapely.geometry.base import BaseGeometry as _BaseGeometry


from agptools.helpers import (
    expandpath,
    I,
    DATE,
    parse_uri,
    build_uri,
    parse_xuri,
    build_fstring,
    replace,
)

# from agptools.progress import Progress
from agptools.containers import (
    walk,
    myassign,
    rebuild,
    SEP,
    list_of,
    overlap,
    soft,
    build_paths,
    combine_uri,
    json_compatible,
    # expand_expression,
)

# from agptools.calls import scall

from agptools.logs import logger
from syncmodels import __version__
from syncmodels.definitions import (
    # DURI,
    # JSON,
    # MONOTONIC_SINCE,
    # MONOTONIC_SINCE_KEY,
    # MONOTONIC_SINCE_VALUE,
    # REG_SPLIT_PATH,
    # URI,
    BOT_KEY,
    CALLABLE_KEY,
    CRAWLER_KEY,
    DATETIME_KEY,
    EXTRA_ENV_KEY,
    FUNC_KEY,
    GEOJSON_KEY,
    GEOMETRY_COMP_KEY,
    GEOMETRY_KEY,
    GEOMETRY_SHAPE_KEY,
    GEOQUERY_COMP_KEY,
    GEOQUERY_KEY,
    ID_KEY,
    KIND_KEY,
    MAPPER_KEY,
    META_KEY,
    METHOD_KEY,
    MONOTONIC_KEY,
    monotonic_wave,
    ORG_KEY,
    ORG_URL,
    PARAMS_KEY,
    PATH_KEY,
    PREFIX_KEY,
    PREFIX_URL,
    REG_PRIVATE_KEY,
    REVERSE_SORT_KEY,
    SORT_KEY,
    STREAM_KEY,
    WAVE_FIRST_KEY,
    WAVE_INFO_KEY,
    WAVE_LAST_KEY,
    WAVE_RESUMING_KEY,
)
from syncmodels.model.geojson import (
    BaseGeometry,
    shape,
    to_geojson,
    Point,
    MultiPolygon,
)

from syncmodels.mapper import Mapper
from syncmodels.model import Enum, BaseModel, Field


from syncmodels.http import (
    # guess_content_type,
    # AUTHORIZATION,
    # AUTH_USER,
    # AUTH_SECRET,
    # AUTH_URL,
    # AUTH_KEY,
    # AUTH_VALUE,
    # AUTH_METHOD,
    # AUTH_PAYLOAD,
    # METHOD_BASIC,
    # METHOD_JSON,
    CONTENT_TYPE,
    USER_AGENT,
    APPLICATION_JSON,
    # APPLICATION_ZIP,
    # BASIC_HEADERS,
    extract_result,
)

# from syncmodels.model import BaseModel
# from syncmodels.registry import iRegistry
from syncmodels.auth import iAuthenticator
from syncmodels.storage import WaveStorage
from syncmodels.exceptions import NonRecoverable
from syncmodels.syncmodels import SyncModel, COPY
from .crud import parse_duri, DEFAULT_DATABASE, DEFAULT_NAMESPACE, tf


# from syncmodels.syncmodels import Transformer


# from .helpers import analyze_url
# from .context import iContext
# from .requests import iResponse
from .runner import iRunner

from .session import iSession
from .helpers.crawler import SortKeyFinder, GeojsonManager

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------
log = logger(__name__)

DEFAULT = "__default__"
UNKNOWN = "__unknown__"

SINGLE = "single"  # single stream sub-type element, not a list
REG_KIND = r"(?P<parent>[^-]*)(-(?P<sub>.*))?$"


# ---------------------------------------------------------
# SQL Bots
# ---------------------------------------------------------


# ---------------------------------------------------------
# Agent
# ---------------------------------------------------------


class JSONVerter:
    @classmethod
    def to_json(cls, params: Dict) -> Dict:
        _env = rebuild([(k, cls._to_json(v)) for k, v in walk(params)])
        return _env

    @classmethod
    def from_json(cls, params: Dict) -> Dict:
        _env = rebuild([(k, cls._from_json(v)) for k, v in walk(params)])
        return _env

    @classmethod
    def _to_json(cls, value: Any) -> Any:
        if isinstance(value, datetime):
            value = value.strftime("%FT%T.%f%Z")
        return value

    @classmethod
    def _from_json(cls, value: Any) -> Any:
        for func in [
            DATE,
        ]:
            _value = func(value)
            if _value != value:
                value = _value
                break
        return value


TJ = JSONVerter.to_json
FJ = JSONVerter.from_json


class iAgent(iRunner):
    "the minimal interface for an agent in crawler module"
    CREDENTIALS = {}

    # CURSOR = {}

    @classmethod
    def clean(cls):
        "clean shared (classmethod) data"

    def __init__(
        self,
        config_path=None,
        include=None,
        exclude=None,
        credentials=None,
        prefix=None,
        *args,
        **kw,
    ):
        super().__init__(*args, **kw)

        # tasks to be included or excluded
        self.include = include or [".*"]
        self.exclude = exclude or []

        # credentials
        self.credentials = {
            **self.CREDENTIALS,
            **(credentials or {}),
        }

        # prefix template
        if prefix:
            if isinstance(prefix, str):
                _uri = parse_duri(prefix)
                if not _uri["_path"] and (
                    m := re.match(r"/?(?P<prefix>.*?)/?$", prefix)
                ):
                    d = m.groupdict()
                    if d["prefix"]:
                        prefix = "/{{{prefix}}}".format_map(d)
                prefix_template = Template(prefix)
            assert isinstance(prefix_template, Template)
            self.prefix = prefix_template
            self.prefix_url = prefix

        # config file
        if not config_path:
            config_path = "config.yaml"
        config_path = expandpath(config_path)
        self.root = os.path.dirname(config_path)
        self.stats_path = os.path.join(self.root, "stats.yaml")

        if not config_path:
            config_path = "config.yaml"
        config_path = expandpath(config_path)

        try:
            with open(config_path, "rt", encoding="utf-8") as f:
                self.cfg = yaml.load(f, Loader=yaml.Loader)
        except Exception:
            self.cfg = {}

        self.cfg.update(kw)

    async def _bootstrap(self):
        "Add the initial tasks to be executed by agent"
        log.info(">> [%s] entering bootstrap()", self.name)

        # get iWave storages (if any) to get the starting
        # point of the synchronization
        _tasks = self.bootstrap
        if not isinstance(_tasks, list):
            _tasks = [_tasks]

        tasks = []
        for _ in _tasks:
            if _ is None:
                tasks.extend(self.default_bootstrap())
            else:
                tasks.append(_)

        i = 0

        for task in tasks:
            task = json_compatible(task)

            # set some default params
            task.setdefault(FUNC_KEY, "get_data")

            extra_meta = {
                # TODO: is an example of built-in default parmeters
                "foo": "bar",
            }
            extra_meta.update(task.get(META_KEY, {}))
            task[META_KEY] = extra_meta

            task[PREFIX_KEY] = self.prefix
            task[PREFIX_URL] = self.prefix_url

            wave0 = await self._get_initial_wave(task)
            if not wave0:
                log.warning(
                    "Can't find initial sync wave for task: [%s]",
                    task,
                )
            else:
                task.setdefault(WAVE_LAST_KEY, wave0)

            env = self.build_env()
            resuming_wave = task.get(WAVE_RESUMING_KEY, {})
            first_wave = task.get(WAVE_FIRST_KEY, {})
            extra_env = task.get(EXTRA_ENV_KEY, {})
            # overlap dicts in order to provide the best
            # resuming context before try to evaluate it

            expressions = [resuming_wave, first_wave]
            env0, par0 = {}, {}
            wave0 = FJ(wave0)

            for w in wave0:
                for _ in w["items"]:
                    env0.update(_)
                par0.update(w["wave"][PARAMS_KEY])
                _fquid = parse_duri(env0[ORG_KEY])
                env0[ID_KEY] = _fquid[ID_KEY]

            environments = [extra_env, env0]
            ctx = self.eval_params(
                expressions,
                environments,
                **env,
            )
            # obtain the values that seems to be the
            # input parameters of the call
            # params must be provided by last item stored
            # in resumeing case, or bootstrap initial wave
            # as fallback on 1st historical call to the provider
            params = {
                key: ctx[key]
                for key in functools.reduce(
                    set.intersection,
                    [set(_) for _ in [set(_) for _ in expressions]],
                )
            }
            # max_param = max(params.values())
            # min_param = min(params.values())
            # delta = max_param - min_param

            # kind = task[KIND_KEY]
            # par0 = self.CURSOR.get(kind)
            if par0:
                assert set(par0.keys()) == set(params.keys())
                # params: data from last item in storage
                # par0: next params propossed for next iteration
                max_param = max(params.values())
                min_param = min(params.values())

                max_par0 = max(par0.values())
                min_par0 = min(par0.values())

                if max_param > max_par0:
                    pass  #  ok
                else:
                    delta = max_par0 - max_param
                    for k, v in list(params.items()):
                        params[k] = par0[k] + delta
                    foo = 1
            else:
                # self.CURSOR[kind] = params
                foo = 1

            # recalculate ctx with (possibly) new call parameters
            # but forgetting resuming_wave as it has been taken
            # into account
            environments = [params, extra_env, env0]
            ctx = {}
            for _ in reversed(environments):
                ctx.update(_)

            # CHECK HERE: ------------------------------------------
            task = self._render_dict(
                task,
                **ctx,
            )
            task[PARAMS_KEY] = TJ(params)

            if self.add_task(task):
                log.info("+ [%s]: [%s] %s", i, self.name, task)
                i += 1
            else:
                log.info("- SKIP: [%s]: [%s] %s", i, self.name, task)

        if i <= 0:
            log.error("[%s] no task provided by bootstrap()", self.name)

        log.info("<< [%s] exit bootstrap()", self.name)

    # async def bootstrap(self):
    # "Add the initial tasks to be executed by crawler"

    def build_env(self):
        """Build an environment for rendering using jinja2."""
        now = datetime.now(tz=timezone.utc)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        oneday = timedelta(days=1)
        yesterday = today - oneday
        from agptools.helpers import (
            DATE,
        )  # TODO: generalize this type of variables

        env = {
            "now": now,
            "today": today,
            "yesterday": yesterday,
            "oneday": oneday,
            "DATE": DATE,  # TODO: generalize this type of variables
        }

        return env

    def eval_params(self, expressions, environments, result__=None, **kw):
        globalns = dict(globals())
        globalns.update(kw)
        # to avoid dependency problems we need to evaluate
        # all expressions that yields an error until the
        # remains expressions are the same from the last iteration
        result__ = {} if result__ is None else result__
        for params in expressions:
            for env in environments:
                last_n = -1
                remain = dict(params)
                soft(globalns, env)
                while remain:
                    for key, source in list(remain.items()):
                        try:
                            value = eval(source, globalns, result__)
                            if key not in result__:
                                globalns[key] = result__[key] = value
                            remain.pop(key)
                        except Exception as why:
                            log.warning("eval: [%s]", why)
                    new_n = len(remain)
                    if last_n == new_n:
                        break
                    last_n = new_n

        return result__

    def _render_dict(self, data: Dict, **kw):
        # prepare render context
        frame = sys._getframe(1)

        kw.update(data)
        soft(kw, self.__dict__)
        soft(kw, frame.f_locals)

        loops = 0
        while loops < 2:
            for key, value in list(data.items()):
                if isinstance(value, str):
                    try:
                        old = data[key]
                        new = Template(
                            value, undefined=StrictUndefined
                        ).render(kw)
                        if new != old:
                            data[key] = kw[key] = new
                            loops = 0
                    except Exception as why:
                        foo = 1
            loops += 1

        return data

    async def idle(self):
        "default implementation when loop has nothing to do"
        if self.remain_tasks() < 1:
            log.info("[%s] hasn't more pending tasks", self)
            # self.running = False
            await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(0.1)

    async def _get_initial_wave(self, *args, **kw):
        return 0

    def default_bootstrap(self):
        """Provide the initial tasks to ignite the process

        yield a tuple with:
          - function to be executed | name of the function (to be located in any iBot instance)
          - args (call args, if any)
          - kwargs (call kwargs, if any)

        Note: KIND_KEY is the name of the item kind to be synced
              Must match the mapper name in MAPPERS
        """
        return []

    def add_task(self, task, expire=0):
        "add a new pending task to be executed by this iAgent"
        raise NotImplementedError()


# ---------------------------------------------------------
# iPlugin
# ---------------------------------------------------------
class iPlugin:
    "A plugin that manipulate received data before giving to main crawler"

    # TODO: chage score by dependences between plugins? (by name, not instance)
    SCORE = 500  # 0..1000
    SPECS = {}

    MAX_RECORDS = int(sys.float_info.max)

    def __init__(self, bot=None, specs=None):
        self.bot = bot
        specs = {} if specs is None else specs
        self.specs = overlap(specs, self.SPECS, overwrite=True)
        self.stats = {}

    async def handle(self, stream: List[Dict], context: Dict):
        """TBD"""

    @classmethod
    def matches(self, serie, *patterns):
        for string in serie:
            string = str(string)
            for pattern in patterns:
                if re.match(pattern, string):
                    yield string

    def geofilter(self, geospecs, context: Dict) -> bool:
        """Helpr to determine if a single item pass a geojson filter (is any)

        Prerequisites:
        - bounding: must be pre-computed
        - geometry: must be pre-computed (geospecs)
        """
        bounding = context.get(GEOQUERY_COMP_KEY)
        geometry = geospecs.get(GEOMETRY_SHAPE_KEY)
        if all([bounding, geometry]):
            assert all(
                [
                    isinstance(bounding, _BaseGeometry),
                    isinstance(geometry, _BaseGeometry),
                ]
            )
            return bounding.intersects(geometry) or bounding.contains(
                geometry
            )

        return True


class iStreamPlugin(iPlugin):
    """Plugins that received the whole stream instead single data"""

    async def handle(
        self, stream: List[Dict], context: Dict
    ) -> Tuple[List[Dict], Dict]:
        return stream, context


class RenameKeys(iPlugin):
    """Rename some keys"""

    NEED_KEYS = {
        "result": r"data",
        "meta": r"info",
    }

    async def handle(self, stream: List[Dict], context: Dict):
        for data in stream:
            if isinstance(data, dict):
                for key, pattern in self.NEED_KEYS.items():
                    for k, v in data.items():
                        if re.match(pattern, k):
                            data[key] = v
                            break


class UnwrapResponse(iPlugin):
    """Unwrap and expand sobre responses that comes in
    'result', and 'meta' format
    """

    NEED_KEYS = {
        "result",
        "meta",
    }

    async def handle(self, stream: List[Dict], context: Dict):
        # TODO: review with josega Multimedia Stats crawler
        assert isinstance(stream, list)
        for data in list(stream):
            if isinstance(data, dict) and self.NEED_KEYS.issubset(data):
                _data = data["result"]
                if isinstance(_data, list):
                    stream.remove(data)
                    stream.extend(_data)
                    soft(context, data["meta"])


# ---------------------------------------------------------
# Bot
# ---------------------------------------------------------


class iBot(iAgent):
    "Interface for a bot"

    MAX_RETRIES = 15
    RETRY_DELAY = 1.0
    DEFAULT_PARAMS = {}
    ALLOWED_PARAMS = [".*"]
    # allowed params from context to build the query

    EXCLUDED_PARAMS = list(parse_uri(""))

    MAX_QUEUE = 200
    ALREADY = {}  # TODO: review faster method

    @classmethod
    def blueprint(cls, **params):
        keys = list(params)
        keys.sort()
        blueprint = [(k, params[k]) for k in keys]
        blueprint = str(blueprint)
        blueprint = hashlib.md5(blueprint.encode("utf-8")).hexdigest()
        return blueprint

    def __init__(
        self,
        *args,
        parent=None,
        context=None,
        headers=None,
        preauth=False,
        **kw,
    ):
        super().__init__(*args, **kw)
        self.fiber = None
        self.plugins = []
        self.parent = parent

        context = context or {}
        self.headers = headers or {}
        self.context = {
            **context,
            **self.headers,
            **kw,
        }
        self.preauth = preauth
        self._sessions: Dict[str, iSession] = {}

        self._add_plugins()

    @classmethod
    def clean(cls):
        "clean shared (classmethod) data"
        # cls.ALREADY.clear()

    def add_plugin(self, plugin: iPlugin):
        "add a new plugin to be executed by this iBot grouped by some PLUGIN_FAMILIES"
        assert isinstance(
            plugin, iPlugin
        ), f"{plugin} is not a subclass of iPlugin!"
        plugins = self.plugins
        plugins.append(plugin)
        plugins.sort(key=lambda x: x.SCORE)
        if not plugin.bot:
            plugin.bot = self

    def can_handle(self, task):
        "return if the function can be handled by this iBot"
        return True

    def old_process(self, klass, data: Dict | List[Dict], context):
        "chain execution for all plugins of the given `klass` or transforming the data"
        # check the data received with the kind of pluggin
        if issubclass(klass, iStreamPlugin):
            if not isinstance(data, list):
                raise RuntimeError(
                    f"for plugins [{klass}], data must be a list of dict"
                )
        elif issubclass(klass, iEachPlugin):
            if not isinstance(data, dict):
                raise RuntimeError(
                    f"for plugins [{klass}], data must be a dict"
                )

        for plugin in self.plugins.get(klass, []):
            # TODO: agp: simplufy if and call in one sentence
            r = plugin.handle(data, context)
            assert r is None, f"plugin {plugin} is not 100% modified yet!"
            if r:
                break
        return data, context

    async def process(self, stream: List[Dict], context):
        """chain execution for all plugins to process the entire stream"""
        for i, plugin in enumerate(self.plugins):
            log.debug(
                "[%s]:%s %s", i, plugin.SCORE, plugin.__class__.__name__
            )

        for i, plugin in enumerate(self.plugins):

            t0 = time.time()
            if await plugin.handle(stream, context):
                # abort responsability chain
                break
            elapsed = time.time() - t0
            log.debug(
                "[%s]:%s (%.4f secs) %s",
                i,
                plugin.SCORE,
                elapsed,
                plugin.__class__.__name__,
            )
            await asyncio.sleep(0)

        foo = 1

    def add_task(self, task, expire=0):
        "add a new pending task to be executed by this iBot"
        # universe = list(kw.values()) + list(args)

        # def check():
        #     "check if this task must be considered or ignored"
        #     return True
        #     # for string in universe:
        #     #     string = str(string)
        #     #     for pattern in self.include:
        #     #         if re.match(pattern, string):
        #     #             return True
        #     #     for pattern in self.exclude:
        #     #         if re.match(pattern, string):
        #     #             return False
        if CALLABLE_KEY in task:
            # process itself
            self.input_queue.push(task, expire)
            return True
        else:
            # assert isinstance(task[FUNC_KEY], str)
            # must be processed by parent for round_robin
            if self.parent:
                return self.parent.add_task(task, expire=expire)
            else:
                log.warning(
                    "[%s] hasn't parent trying to process: %s",
                    self.name,
                    task,
                )
        return False

    def _add_plugins(self):
        # add plugins
        self.add_plugin(NormalizePlugin())
        self.add_plugin(SortPlugin())
        self.add_plugin(HashStreamPlugin())

        self.add_plugin(GeoquerySetupPlugin())
        self.add_plugin(GeospecsFilterPlugin())
        self.add_plugin(MetaExtractPlugin())
        self.add_plugin(PutPlugin())

        self.add_plugin(SetURIPlugin())
        self.add_plugin(Cleaner())

        # self.add_plugin(TubeMetadataPlugin())

    async def get_task(self, timeout=2) -> dict:
        "get the next task or raise a timeout exception"
        while (pending := self.output_queue.qsize()) > self.MAX_QUEUE:
            now = time.time()
            if now - self._last_announce > 10:
                print(
                    f"Pause worker due too much results pending in queue: {pending}"
                )
            self._last_announce = now
            await asyncio.sleep(1)

        return await super().get_task(timeout=timeout)

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        return len(self._wip) + self.input_queue.qsize()

    async def stop(self):
        await super().stop()
        await self.parent.remove_bot(self)

    async def _get_session(self, url, **context) -> iSession:
        uri = parse_uri(url)
        session = self._sessions.get(uri["xhost"])
        if session is None:
            context.update(
                {
                    "url": url,
                    "bot": self,
                }
            )
            session = self._sessions[uri["xhost"]] = await iSession.new(
                **context
            )
        return session

    async def get_data(self, **task):
        """
        Example a crawling function for recommender crawler.

        Get data related to the given kind and path.
        May add more tasks to be done by crawler.
        """
        context = {}
        # context.update(self.parent.cfg)
        # context.update(self.context)
        # filter non-convenient context values
        # context = {
        #     key: value
        #     for key, value in context.items()
        #     if isinstance(value, (int, float, str, bool))
        # }

        wave_keys = task.get(WAVE_INFO_KEY, [])
        wave_keys = [wave_keys] if isinstance(wave_keys, str) else wave_keys
        assert isinstance(wave_keys, list)

        context.update(
            {
                CRAWLER_KEY: self.parent,
                BOT_KEY: self,
                # "limit": 50,
                # "offset": 0,
                WAVE_INFO_KEY: wave_keys,
                **task,
            }
        )
        # method to gather the information from 3rd system
        stream, meta = await self._get_data(**context)
        meta = {replace(k): v for k, v in meta.items()}

        if stream:
            context.setdefault(META_KEY, {}).update(meta)
            self.add_task(
                {
                    CALLABLE_KEY: self.process_stream,
                    "stream": stream,
                    # META_KEY: meta,
                    "context": context,
                    **task,
                }
            )
        else:
            log.info("No data received from source: %s", context)

    async def process_stream(self, stream, context, **task):
        """TBD"""
        if not isinstance(stream, (list, types.GeneratorType)):
            stream = [stream]

        log.info(
            "received (%s) items of type '%s'",
            len(stream),
            context[KIND_KEY],
        )

        context = {
            **context,
            **task,
        }

        # TODO: use generators to try to free memory ASAP when data has been saved into storage
        await self.process(stream, context)

    async def _get_data(self, **context):
        "A helper method to get the data from external system"

        soft(context, self.DEFAULT_PARAMS)
        # TODO: MONOTONIC_KEY context must be passed to iSession
        params = self._build_params(**context)

        path = context.get(PATH_KEY) or ""
        path = path.format_map(context)
        _local = parse_duri(path)

        app_url = self.parent.app_url.format_map(context)
        _source = parse_duri(app_url)
        _uri = combine_uri(
            _source,
            _local,
        )
        url = build_uri(**_uri)

        exception_raised = None
        # get the session related to this url
        proxy = await self._get_session(url, **context)

        # provide extra params to the proxy before calling EP
        call_kw = await proxy.update_params(url, params, context)

        timeout = self.parent.cache_timeout
        assert "url" in call_kw
        if self._set_already(
            timeout=timeout, **call_kw
        ):  # TODO: remove debug
            # self._set_already(url, **params)
            try:
                for tries in range(1, self.MAX_RETRIES):
                    try:
                        exception_raised = None
                        # authenticate when is needed
                        # await proxy.authenticate(url, params)
                        # a chance to create a more specific instance in a context
                        # to deal with the real get() method
                        async with proxy as session:
                            # log.debug(
                            # "[%s][%s/%s] %s : %s", self.name, tries, self.MAX_RETRIES, url, params
                            # )
                            # merge headers without key conflicts
                            soft(call_kw["headers"], self.headers)
                            method = getattr(
                                session, context.get(METHOD_KEY, "get")
                            )

                            if self.preauth:
                                await iAuthenticator.auth(url, params, proxy)

                            # response = requests.get(**call_kw)
                            response = await method(**call_kw)

                            async with response:
                                if 200 <= response.status < 300:
                                    stream, meta = (
                                        await proxy._process_response(
                                            response
                                        )
                                    )
                                    soft(meta, params)
                                    return stream, meta
                                #  https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses
                                elif response.status in (
                                    401,
                                    403,
                                    404,
                                    405,
                                    407,
                                ):
                                    # forbidden
                                    result = await extract_result(response)
                                    # result = await response.text()
                                    log.error(
                                        "[%s] server sent: %s",
                                        response.status,
                                        result,
                                    )
                                    await iAuthenticator.auth(
                                        url, params, proxy
                                    )
                                    await asyncio.sleep(self.RETRY_DELAY)
                                    continue
                                elif 400 <= response.status < 500:
                                    log.warning(
                                        "Status: %s, ABORT, not recoverable error",
                                        response.status,
                                    )
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    # result = await response.json()
                                    result = await extract_result(response)

                                    log.error("server sent: %s", result)
                                    raise NonRecoverable(result)
                                elif 500 <= response.status < 600:
                                    log.warning(
                                        "Status: %s, RETRY", response.status
                                    )
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    # result = await response.json()
                                    # log.error("server sent: %s", result)
                                else:
                                    log.error("Status: %s", response.status)
                    except NonRecoverable:
                        break
                    except Exception as why:  # pragma: nocover
                        log.error(why)
                        msg = "".join(
                            traceback.format_exception(*sys.exc_info())
                        )
                        log.error(msg)
                        exception_raised = why

                    log.warning("retry: %s: %s, %s", tries, call_kw, params)
                    await asyncio.sleep(self.RETRY_DELAY)
            except Exception as why:  # pragma: nocover
                log.error(why)
                msg = "".join(traceback.format_exception(*sys.exc_info()))
                log.error(msg)
                exception_raised = why

            finally:
                # self._set_already(url)
                if exception_raised:
                    raise exception_raised
        else:
            log.info("[%s] SKIPPING %s : %s", self.name, url, params)

        return None, {}

    def _build_params(self, **context):
        params = {}

        def match(text) -> bool:
            if re.match(REG_PRIVATE_KEY, text):
                return False

            if text in self.EXCLUDED_PARAMS:
                return False

            for pattern in self.ALLOWED_PARAMS:
                if re.match(pattern, text):
                    return True

            return False

        # TODO: remove / deprecated
        if "kind" in context:
            log.warning(
                "['%s'] key is deprecated, use KIND_KEY instead", "kind"
            )
            context[KIND_KEY] = context.pop("kind")

        for k, v in context.items():
            if match(k) and isinstance(v, (int, str, float)):
                params[k] = v

        return params

    def _is_already(self, timeout=600, type_="task", **params):
        blueprint = self.blueprint(**params)
        universe = self.ALREADY.setdefault(type_, {})
        last = universe.get(blueprint, 0)
        return time.time() - last < timeout

    def _set_already(self, timeout=600, type_="task", **params):
        # TODO: I need to clean really old cache entries
        # TODO: in order to control any excesive memory compsumption
        try:

            if not self._is_already(timeout=timeout, type_=type_, **params):
                blueprint = self.blueprint(**params)
                universe = self.ALREADY.setdefault(type_, {})
                universe[blueprint] = time.time()
                return True
            return False
        finally:
            self._purge_already()

    def _purge_already(self, timeout=3600 * 4, max_records=10):
        for type_, universe in self.ALREADY.items():
            for blueprint, last in list(universe.items()):
                elapsed = time.time() - last
                if elapsed > timeout:
                    universe.pop(blueprint)
            if len(universe) > max_records:
                timestamps = list(universe.values())
                timestamps.sort()
                cut = timestamps[max_records]
                for blueprint, last in list(universe.items()):
                    if last < cut:
                        universe.pop(blueprint)

    @classmethod
    def _clean_already(cls):
        cls.ALREADY.clear()


# ---------------------------------------------------------
# Helper Plugins
# ---------------------------------------------------------
class Cleaner(iPlugin):
    "strip text values"

    async def handle(self, stream: List[Dict], context: Dict):
        for data in stream:
            for k, v in data.items():
                if isinstance(v, str):
                    data[k] = v.strip()


class RegExtractor(iPlugin):

    async def handle(self, stream: List[Dict], context: Dict):
        # TODO: review
        # TODO: create a reveal + regexp + SEP ?
        for data in stream:

            aux = {**data, **context}
            values = list([aux[x] for x in self.matches(aux, "path")])

            # for key in self.matches(aux, KIND_KEY):
            # kind = aux[key]
            for regexp in self.specs:
                for value in values:
                    m = re.match(regexp, value)
                    if m:
                        data.update(m.groupdict())


class Restructer(iPlugin):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.__mask_restruct_data()

    def __mask_restruct_data(self):
        for container in self.specs.values():
            for k in list(container):
                if SEP in k:
                    continue
                v = container.pop(k)
                k = k.replace("/", SEP)
                v = tuple([v[0].replace("/", SEP), *v[1:]])
                container[k] = v

    async def handle(self, stream: List[Dict], context: Dict):
        for data in stream:
            restruct = {}
            kind = context.get(KIND_KEY, UNKNOWN)
            info = self.specs.get("default", {})
            info.update(self.specs.get(kind, {}))
            reveal = build_paths(data)
            for path, value in reveal.items():
                for pattern, (new_path, new_value) in info.items():
                    m = re.match(pattern, path)
                    if m:
                        d = m.groupdict()
                        d["value"] = value
                        key = tuple(new_path.format_map(d).split(SEP))
                        _value = (
                            value
                            if new_value == COPY
                            else new_value.format_map(d)
                        )
                        restruct[key] = _value

            restruct = rebuild(restruct, result={})
            data = {**data, **restruct}


class FQIUD(iPlugin):
    SPECS = {
        **iPlugin.SPECS,
        "root": ("{url}", I, "url"),
        # 'groups': ("{id}", int, 'id'),
    }

    async def handle(self, stream: List[Dict], context: Dict):
        for data in stream:
            patterns = context.get("kind_key", KIND_KEY)
            for key in self.matches(data, patterns):
                kind = data[key]
                for specs in self.specs.get(kind, []):
                    if not specs:
                        continue
                    uid_key, func, id_key = specs
                    try:
                        uid = uid_key.format_map(data)
                        fquid = func(uid)
                        data[id_key] = fquid
                        data["_fquid"] = fquid
                        data["_uid"] = uid
                        return data
                    except Exception as why:  # pragma: nocover
                        # TODO: remove, just debugging
                        log.error(why)
                        log.error(
                            "".join(
                                traceback.format_exception(*sys.exc_info())
                            )
                        )


class Tagger(iPlugin):

    async def handle(self, stream: List[Dict], context: Dict):
        pass


class DeepSearch(iPlugin):

    async def handle(self, stream: List[Dict], context: Dict):
        for data in stream:
            aux = {**data, **context}
            patterns = aux.get("kind_key", KIND_KEY)

            for key in self.matches(aux, patterns):
                kind = aux.get(key)
                for specs in self.specs.get(kind, []):
                    if not specs:
                        continue
                    try:
                        task = dict(aux)
                        sub_kind, sub_url = specs
                        sub_url = sub_url.format_map(task)
                        task[key] = sub_kind
                        task[PATH_KEY] = sub_url

                        self.bot.add_task(task)
                    except Exception as why:  # pragma: nocover
                        # TODO: remove, just debugging
                        log.error(why)
                        log.error(
                            "".join(
                                traceback.format_exception(*sys.exc_info())
                            )
                        )


class PaginationDisabled:
    "represent no pagination for an item"


class iPaginationPlugin(iPlugin):
    PER_PAGE = "per_page"

    MAX_PAGES = "max_pages"
    FIRST_PAGE = "first_page"
    AHEAD_PAGES = "ahead_pages"
    PAGE = "page"

    FIRST_ITEM = "first_item"
    MAX_ITEMS = "max_items"
    OFFSET = "offset"


class GenericPagination(iPaginationPlugin):

    SPECS = {
        **iPlugin.SPECS,
        **{
            DEFAULT: {
                iPaginationPlugin.MAX_ITEMS: "count",
                iPaginationPlugin.MAX_PAGES: "max_pages",
                iPaginationPlugin.OFFSET: "offset",
                iPaginationPlugin.PER_PAGE: "limit",
                iPaginationPlugin.FIRST_ITEM: 0,
            },
            "gitlab": {
                iPaginationPlugin.PAGE: "page",
                iPaginationPlugin.PER_PAGE: "per_page",
                iPaginationPlugin.FIRST_PAGE: 1,
                iPaginationPlugin.AHEAD_PAGES: 1,
            },
        },
    }

    async def handle(self, stream: List[Dict], context: Dict):
        "Request the next pagination (just the next one!)"

        for name, spec in self.specs.items():
            page = int(context.get(spec[self.PAGE], -1))
            per_page = int(context.get(spec[self.PER_PAGE], 50))
            if context.get(spec.get(self.MAX_ITEMS), -1) < page * per_page:
                page = max(page, spec.get(self.FIRST_PAGE, 0))
                for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                    context[spec[self.PAGE]] = page + 1
                    ##log.debug("> request: %s", context)
                    self.bot.add_task(
                        func="get_data",  # TODO: extract from context
                        # **data,
                        **context,
                    )
                break


class SimplePagination(iPaginationPlugin):
    """
    kind: specs_for_this_kind

    used: kind: [] to explicit avoid pagination
    DEFAULT: a default pagination when no other is defined
    """

    SPECS = {
        # **iPlugin.SPECS, # don't use base class
        **{
            DEFAULT: {
                iPaginationPlugin.PAGE: "page",
                iPaginationPlugin.PER_PAGE: "per_page",
                iPaginationPlugin.FIRST_PAGE: 1,
                iPaginationPlugin.AHEAD_PAGES: 1,
            },
            # "groups": {},
            # "projects": {},
            # "users": {},
            # "wikis": {},
            # "issues": {},
            # "milestones": {},
            # "notes": {},
        },
    }

    async def handle(self, stream: List[Dict], context: Dict):
        "Request the next pagination"
        kind = context.get(KIND_KEY, UNKNOWN)
        spec = self.specs.get(kind, self.specs.get(DEFAULT))

        # poi and poi-single
        d = re.match(REG_KIND, kind).groupdict()
        if spec == PaginationDisabled or d["sub"] in (SINGLE,):
            # single items doesn't use pagination
            ##log.debug("skip pagination for '%s'", kind)
            # remove parent pagination context
            kind = d["parent"]
            spec = self.specs.get(kind, self.specs.get(DEFAULT))
            if spec:
                foo = 1
            for k in spec.values():
                context.pop(k, None)
            foo = 1
        else:
            ##log.debug("for '%s' use pagination: %s", kind, spec)
            ##log.debug("page: %s, per_page: %s", page, per_page)

            # we have 2 options: pagination based on pages or based on num items
            per_page = int(context.get(spec.get(self.PER_PAGE), 20))
            max_items = context.get(spec.get(self.MAX_ITEMS))
            page = context.get(spec.get(self.PAGE))
            offset = int(context.get(spec.get(self.OFFSET), -1))
            offset = max(offset, spec.get(self.FIRST_ITEM, 0))
            if max_items is not None:
                if max_items > offset:
                    for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                        context[spec[self.OFFSET]] = offset + per_page
                        ##log.debug("> request page: [%s]:%s", kind, context.get(spec[self.PAGE], -1))

                        # use name instead callable so crawler can assign the
                        # request to another bot apartt current one
                        # using calleable will always assign the task to itself
                        func_name = context[FUNC_KEY].__name__

                        self.bot.add_task(
                            func=func_name,
                            # **data,
                            **context,
                        )
            elif page is not None:
                page = max(offset, spec.get(self.FIRST_PAGE, 0))
                max_pages = max(
                    page, spec.get(self.MAX_PAGES, sys.float_info.max)
                )
                if max_pages >= page:
                    for batch in range(spec.get(self.AHEAD_PAGES, 1)):
                        context[spec[self.PAGE]] = page + per_page
                        ##log.debug("> request page: [%s]:%s", kind, context.get(spec[self.PAGE], -1))
                        self.bot.add_task(context)
            else:
                log.debug("no pagination info found")


class NormalizePlugin(iPlugin):
    """
    Normalize data based on mappers

    Example:

    TODO: TBD
    """

    SCORE = 950  # before SetURIPlugin

    async def handle(self, stream: List[Dict], context: Dict):
        for data in stream:
            kind = context[KIND_KEY]
            crawler = context[CRAWLER_KEY]
            MAPPERS = crawler.MAPPERS
            d = re.match(REG_KIND, kind).groupdict()
            real_kind = d["parent"]
            klass = MAPPERS.get(real_kind)
            if not klass:
                log.warning(
                    "missing MAPPERS[%s] class!", kind
                )  # TODO: remove debug
                return

            _data = crawler.convert_into_references(data)
            context.update(_data)
            _data = klass.transform(_data)
            data.update(_data)


class SortPlugin(iPlugin):
    """
    Sort data stream based on *future* wave parameter
    in order to resume later

    Example:

    TODO: TBD
    """

    SCORE = max([NormalizePlugin.SCORE]) + 1

    async def handle(self, stream: List[Dict], context: Dict):
        if not stream:
            return
        sort_key = context.get(SORT_KEY)
        if not sort_key:
            # figure out the sort_key
            sort_key = SortKeyFinder.find_sort_key(stream)
            context[SORT_KEY] = sort_key
            sample = stream[-1]
            reverse = []
            for key in sort_key:
                value = sample[key]
                candidates = {
                    k: v
                    for k, v in sample.items()
                    if k != key and sample[k] == value
                }
                if candidates:
                    _key, _ = candidates.popitem()
                    reverse.append(_key)
                else:
                    log.warning(
                        "can't find the reverse key of '%s' in %s",
                        sort_key,
                        sample,
                    )
            context[REVERSE_SORT_KEY] = reverse

            foo = 1
        if sort_key:

            def order(data, accessor):
                result = data
                for key in accessor:
                    try:
                        result = result[key]
                    except Exception as why:
                        pass

                return result

            stream.sort(key=partial(order, accessor=sort_key))
        else:
            msg = "ABORT: Can't find any key for sorting the stream!"
            log.error(msg)
            raise RuntimeError(msg)


class ApplyDatePlugin(iPlugin):
    """
    *Bless* the data with some kind of datetime for sorting
    """

    SCORE = max([SortPlugin.SCORE]) - 1
    KEY = DATETIME_KEY
    ROUND_SECONDS = 600

    async def handle(self, stream: List[Dict], context: Dict):
        now = datetime.now(tz=timezone.utc)
        for data in stream:
            data.setdefault(self.KEY, now)


class HashStreamPlugin(iPlugin):
    """
    Get a hash value for the whole stream

    Example:

    TODO: TBD
    """

    SCORE = 50  # before SortPlugin

    async def handle(self, stream: List[Dict], context: Dict):
        blueprint = hashlib.sha1(b"")
        for data in stream:
            new = hashlib.sha1(pickle.dumps(data))
            blueprint = hashlib.sha1(blueprint.digest() + new.digest())

        blueprint = blueprint.hexdigest()
        context["stream_blueprint"] = blueprint
        if not self.bot._set_already(
            timeout=3600,
            type_="response",
            blueprint=blueprint,
        ):
            log.info(
                f"this reponse is already seen: ['%s'], ignoring the whole response ...",
                blueprint,
            )
            stream.clear()


class PutPlugin(iPlugin):
    """
    Put items into storage
    TODO: pending (plugins are not async)
    """

    SCORE = 5000  # the last one

    async def handle(self, stream: List[Dict], context: Dict):
        crawler = self.bot.parent
        for data in stream:
            await crawler.inject(data, context)
            await asyncio.sleep(0)
        foo = 1


class GeoquerySetupPlugin(iPlugin):
    """
    Compile Geo queries for late filtering and place them in context

    # Note: stream must be modified in place
    # Note: example: stream[:] = selected_items
    """

    SCORE = 100

    async def handle(self, stream: List[Dict], context: Dict):

        geoquery = context.get(GEOQUERY_KEY)
        geoquery_comp = context.get(GEOQUERY_COMP_KEY)

        if geoquery and not geoquery_comp:
            if isinstance(geoquery, dict):
                geoquery_comp = shape(geoquery)
            elif isinstance(geoquery, BaseModel):
                geoquery_comp = shape(geoquery.model_dump())
            else:
                raise RuntimeError(
                    f"I don't know how to handle geoquery: {geoquery}"
                )

        context[GEOQUERY_COMP_KEY] = geoquery_comp


# class TubeMetadataPlugin(iPlugin):
#     """
#     Filter point not contained into GeoFeature
#     """
#
#     SCORE = 1000
#
#     def handle(self, data: Dict, context: Dict) -> Tuple[Dict, Dict]:
#
#         if data:
#             sample = data[0]
#             sid = sample[ID_KEY]  # must exists!
#             _sid = parse_duri(sid)
#
#             tube = "{fscheme}://{xhost}/{_path}".format_map(_sid)
#             meta = context.get(META_KEY, {})
#
#             await self.bot.parent.update_meta(tube, meta)
#
#         return data, context


class GeospecsFilterPlugin(iPlugin):
    """
    Check that all entities provides Geo Specification
    Check if data has been filtered or not as well
    """

    SCORE = 925  # before NormalizePlugin

    async def handle(self, stream: List[Dict], context: Dict):
        warnings = set()
        bounding = context.get(GEOQUERY_COMP_KEY)
        if bounding:
            _stream = []
            for data in stream:
                geometry = data.get(GEOMETRY_SHAPE_KEY)
                if geometry:
                    if bounding.intersects(geometry) or bounding.contains(
                        geometry
                    ):
                        _stream.append(data)
                else:
                    warnings.add(
                        f"[{context[ORG_URL]} : {context}] stream doesn't provide bounding geoquery: {GEOMETRY_SHAPE_KEY}"
                    )
                    _stream.append(data)
            stream[:] = _stream
        else:
            warnings.add(
                f"[{context[ORG_URL]} : {context}] stream doesn't provide bounding geoquery: {GEOQUERY_COMP_KEY}"
            )

        for msg in warnings:
            log.warning(msg)


class GeoPoint(BaseModel):
    id: str
    geojson: Point


class GeoMultipolygon(BaseModel):
    id: str
    geojson: MultiPolygon


class PointMapper(Mapper):
    PYDANTIC = GeoPoint


class MultipolygonMapper(Mapper):
    PYDANTIC = GeoMultipolygon


GEO_MAPPER = {
    "Point": PointMapper,
    # "LineString": LineString,
    # "Polygon": Polygon,
    # "MultiPoint": MultiPoint,
    # "MultiLineString": MultiLineString,
    "MultiPolygon": GeoMultipolygon,
    # "GeometryCollection": GeometryCollection,
    # "Feature": Feature,
    # "FeatureCollection": FeatureCollection,
}


class GeoJsonEnum(Enum):
    """TBD"""

    # TODO: use 'geojson.Point' as KIND?
    POINT = {
        KIND_KEY: "Point",
        MAPPER_KEY: PointMapper,
    }

    MULTIPOLYGON = {
        KIND_KEY: "MultiPolygon",
        MAPPER_KEY: MultipolygonMapper,
    }


class MetaAddPlugin(iPlugin):
    """
    Add metainfo to the items in stream
    """

    async def handle(self, stream: List[Dict], context: Dict):
        pass


class MetaExtractPlugin(iPlugin):
    """
    Split data into multiples related families: geojson, etc
    """

    SCORE = 1000  # before NormalizePlugin

    async def handle(self, stream: List[Dict], context: Dict):
        stream[:] = stream[: iPlugin.MAX_RECORDS]  # debug code

        # Note: using a dict to check all different geojson
        # that we can associate to the same fquid, no matter
        # of the value of the item data
        # this will provent mistakes of assuming that each geojson
        # relate to the same fquid changs within the stream live
        geoids = dict()

        for data in list(stream):
            # bless data with kind
            monotonic = monotonic_wave()
            data[KIND_KEY] = context[KIND_KEY]
            data[MONOTONIC_KEY] = monotonic
            # -------------------------------------------------
            # extract goespecs info data and add to stream
            # -------------------------------------------------
            # assert isinstance(geojson, BaseGeometry)
            MAP = self.bot.parent.MAPPERS
            geojson = data.get(GEOJSON_KEY)  # TODO: fix, coords are tuples!
            if geojson is None:
                log.warning("no geojson info: [%s]", data)
                continue
            kind = geojson["type"]
            # TODO: use (slower) more general jinja render?

            # preserve this order
            # _sid = parse_duri(data[ID_KEY])
            # _sid['path'] = "/{thing}/geo".format_map(_sid)
            # fquid = build_uri(**_sid)
            fquid = GeojsonManager.geo_uri(data)

            # don't assume geojson are the same
            # maybe in the future for some EndPoints
            # that we trust, this restriction can be relaxed
            if fquid:  #  fquid not in geoids:
                # TODO: use a new dict (item) and kind
                # TODO: or share same dict (data) and provide multiples { id, kind }
                # TODO: letting pydantic takes only the data needed for each kind/mapper

                # Note: we `stich` all items belongs to the same wave
                # Note: with the same monotonic value
                item = {
                    **data,
                    "id": fquid,
                    KIND_KEY: kind,
                    # MONOTONIC_KEY: monotonic, # not needed (data has)
                }
                # >> debug
                # klass = MAP[kind]
                # item = klass.item(item)
                # item = self.bot.parent.new(kind, item)

                # assert item.model_dump()[GEOJSON_KEY] == geojson
                # << debug

                # add the related geojson item

                holder = geoids.setdefault(fquid, [])
                if not holder:
                    # only add
                    # stream.insert(0, item)
                    stream.append(item)

                # don't trust the EndPoint and check geojson
                # related to the same fquid
                _new = item[GEOJSON_KEY]
                for _existing in holder:
                    assert (
                        _new == _existing
                    ), f"GeoJSON related to {fquid} doesn't match, you need to review fqui and geojson association"
                holder.append(_new)
            else:
                log.error("can't build geo_uri from [%s]", data)
                log.error(
                    "maybe '%s' or '%s' isn't propertly set?",
                    ID_KEY,
                    ORG_KEY,
                )
                foo = 1
            # >> debug()
            # else:
            #     assert geoids[fquid] == item.geojson.model_dump_json()
            #     foo = 1
            # << debug

            # -------------------------------------------------
            # TODO: add any other extra family related entity
            # -------------------------------------------------

            foo = 1

            # extract metadata info

        foo = 1
        #  check


class SetURIPlugin(iPlugin):
    """
    Build fquid based on the data and context info

    Example:

    self.bot.parent.prefix
    'transport://aena/flights/flows'

    data
    {
     'cia': 'EZY',
     'aeropuerto': 'AGP',
     'asientos': '156',
     'fecha_prevista': '13-06-2024 16:10:00',
     'numero_vuelo': '8071',
     'origen': 'LGW',
     'kind__': 'arrival',
     'departure': False,
     'id': 'transport://aena/flights/flows/arrival/arrival_EZY8071',
     'id__': 'arrival_EZY8071'
    }
    """

    SCORE = 990  # at the end of the resposability chain

    # self.RENDER_FORMAT: '{prefix}/{kind__}/{id}'
    RENDER_FORMAT = build_fstring("prefix", KIND_KEY, ID_KEY, sep="/")

    async def handle(self, stream: List[Dict], context: Dict):
        template = context[PREFIX_KEY]

        for data in stream:
            # preserve original ID
            data[ORG_KEY] = data.get(ID_KEY)

            # calculate new one
            context.update(data)
            fquid = template.render(context)
            data[ID_KEY] = fquid

    def hide_handle(self, data: Dict, context: Dict) -> Tuple[Dict, Dict]:

        sid = data[ID_KEY]
        assert (
            sid
        ), "items must provide an `id` member. Maybe you need to set an `id` attribute in Pytantic or create a SetIDPlugin plugin?"
        kind = context[KIND_KEY]

        prefix = self.bot.parent.prefix  # or kind
        prefix = prefix.format_map(context)
        _prefix = parse_duri(prefix)

        sid = str(sid)
        sid = sid.format_map(context)
        _uri = parse_xuri(sid)

        if _uri["fscheme"]:
            subpath = _uri.get("path", "").split(_prefix.get("path", ""))[-1]
            raise RuntimeError(
                f"Absolute id: {sid} is not allowed. You need to use an id that can be combined with crawler prefix: {prefix}, i.e. {subpath}"
            )
        elif _uri["_path"] == _uri["id"]:
            # id = 'TNXY08247528421523'
            _uri = {"id": sid}
        elif not sid.startswith("/"):
            # a relative path?: "a/2:22"
            _uri = parse_xuri(f"/{sid}")

        # elif not _uri["host"]:
        #     _uri = {"id": sid}

        template = "{{ xhost }}/{{ kind__ }}"
        template = Template(template)
        ctx = dict(context)
        ctx.update(data)
        out = template.render(ctx)

        #
        _fquid = combine_uri(
            _prefix,
            _uri,
            # context,
        )
        fquid = build_uri(**_fquid)
        data[ID_KEY] = fquid

        return data, context


# ---------------------------------------------------------
# HTTP Bots
# ---------------------------------------------------------


class HTTPBot(iBot):
    "Basic HTTPBot"

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.headers = {
            # USER_AGENT: f"python-{self.__class__.__name__.lower()}/{__version__}",
            USER_AGENT: "Mozilla/5.0 (X11; Linux i686; rv:125.0) Gecko/20100101 Firefox/125.0",
            CONTENT_TYPE: APPLICATION_JSON,
            # "Authorization": f"Bearer {personal_access_token}",
        }

    def _add_plugins(self):
        super()._add_plugins()
        self.add_plugin(RenameKeys())
        self.add_plugin(UnwrapResponse())

        # self.add_plugin(RegExtractor())
        # self.add_plugin(Cleaner())
        # self.add_plugin(FQIUD())
        # self.add_plugin(DeepSearch())
        # self.add_plugin(SimplePagination())


# ---------------------------------------------------------
# SQL Bots
# ---------------------------------------------------------


class SQLBot(iBot):
    "Basic SQLBot"

    # RESPONSE_META = ["headers", "links", "real_url"]
    TABLE_NAME = {
        DEFAULT: "{name}",
    }
    "syncmodel table for a particular database schema"
    WAVE_COLUMN_NAME = {
        DEFAULT: MONOTONIC_KEY,
    }
    "wave column for a particular table"

    #
    MAX_RETRIES = 15
    DEFAULT_PARAMS = {}
    ALLOWED_PARAMS = [".*"]
    # allowed params from context to build the query

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # self.add_plugin(RegExtractor())
        # self.add_plugin(Cleaner())
        # self.add_plugin(FQIUD())
        # self.add_plugin(DeepSearch())
        # self.add_plugin(SimplePagination())
        # self.headers = {
        # "User-Agent": "python-httpbot/0.1.0",
        # "Content-type": "application/json",
        ## "Authorization": f"Bearer {personal_access_token}",
        # }

    async def get_rows(self, **context):
        """
        Example a crawling function for recommender crawler.

        Get data related to the given kind and path.
        May add more tasks to be done by crawler.
        """
        context = {
            # "limit": 50,
            # "offset": 0,
            **context,
        }
        # method to gather the information from 3rd system
        stream, meta = await self._get_rows(**context)
        if not stream:
            return

        if isinstance(stream, list):
            ##log.debug("received (%s) items of type '%s'", len(stream), context['kind'])
            pass
        else:
            ##log.debug("received a single items of type: '%s'", context['kind'])
            stream = [stream]

        context.update(meta)
        for _, org in enumerate(stream):
            # data = {**data, **org}
            data = {**org}
            data, ctx = self.process(iEachPlugin, data, **context)

            yield data, (ctx, org)
            # if random.random() < 0.05:
            # await asyncio.sleep(0.25)  # to be nice with other fibers
            ##log.debug("[%s]:[%s]#%s: processed", i, context['kind'], data.get('id', '-'))

        # params['offset'] = (page := page + len(result))
        data, context = self.process(iPostPlugin, data, **context)

    async def _get_rows(self, path, **context):
        "A helper method to get the data from external system"

        soft(context, self.DEFAULT_PARAMS)
        params = self._build_params(**context)

        uri = parse_uri(path)
        if not uri["host"]:
            uri2 = self.context["app_url"]  # must exists!
            uri2 = parse_uri(uri2)
            uri["path"] = uri2["path"] = (uri2["path"] or "") + uri["path"]
            uri = overlap(uri2, uri, overwrite=True)
        uri["query_"] = params

        #
        url = build_uri(**uri)
        # print(url)
        if self._is_already(url):
            ##log.info("[%s] SKIPING %s : %s", self.name, url, params)
            foo = 1
        else:
            self._set_already(url)
            try:
                for tries in range(1, self.MAX_RETRIES):
                    try:
                        session = self._get_session()

                        async with aiohttp.ClientSession() as session:
                            # log.debug(
                            # "[%s][%s/%s] %s : %s", self.name, tries, self.MAX_RETRIES, url, params
                            # )
                            async with session.get(
                                url, headers=self.headers, params=params
                            ) as response:
                                if response.status in (200,):
                                    stream, meta = (
                                        await proxy._process_response(
                                            response
                                        )
                                    )
                                    soft(meta, params)
                                    return stream, meta
                                elif response.status in (400, 404):
                                    log.warning(
                                        "Status: %s, RETRY", response.status
                                    )
                                    ##log.debug("%s: %s: %s", response.status, path, params)
                                    # result = await response.json()
                                    # log.error("server sent: %s", result)
                                elif response.status in (403,):
                                    log.error(
                                        "Status: %s, SKIPPING",
                                        response.status,
                                    )
                                else:
                                    log.error("Status: %s", response.status)
                    except Exception as why:  # pragma: nocover
                        log.error(why)
                        log.error(
                            "".join(
                                traceback.format_exception(*sys.exc_info())
                            )
                        )
                    log.warning("retry: %s: %s, %s", tries, path, params)
                    await asyncio.sleep(self.RETRY_DELAY)
            finally:
                # self._set_already(url)
                pass
        return None, None


#     def _is_already(self, url):
#         return url in self.ALREADY
#
#     def _set_already(self, url):
#         if not self._is_already(url):
#             self.ALREADY[url] = time.time()
#             return True
#         return False


# ---------------------------------------------------------
# Crawler
# ---------------------------------------------------------
class iCrawler(iAgent):
    "Interface for a crawler"
    bots: Dict[Any, iBot]

    # governance data
    MAPPERS = {}

    @classmethod
    def unwarp_mappers(cls, *enums):
        result = {}
        # collect any parent mapper definition
        for klass in cls.mro():
            if issubclass(klass, cls):
                result.update(klass.MAPPERS)

        # unwarp emums
        for enum in enums:
            result.update(
                {e.value[KIND_KEY]: e.value[MAPPER_KEY] for e in enum}
            )

        # cls.MAPPERS = result
        return result

    def __init__(
        self,
        syncmodel: SyncModel = None,
        raw_storage=None,
        app_url=None,
        task_filters=None,
        *args,
        **kw,
    ):
        super().__init__(*args, **kw)
        self.bot: Dict[str, iBot] = {}
        self.round_robin: deque[iBot] = deque()

        if task_filters:
            if isinstance(task_filters, str):
                task_filters = {
                    KIND_KEY: task_filters,
                }
            if not isinstance(task_filters, list):
                task_filters = [task_filters]

        self.task_filters = task_filters

        self.stats = {}
        self.show_stats = True
        self.syncmodel = list_of(syncmodel, SyncModel)
        self.raw_storage = raw_storage

        self.app_url = app_url or self.cfg.get("app_url") or ""
        # self.app_url = (
        # self.cfg["app_url_dev"] if app_url else self.cfg["app_url"]
        # )
        self._app_uri = parse_uri(self.app_url)

    def _storages(self, klass):
        "get storages that match some class"
        result = []
        for syncmodel in self.syncmodel:
            for storage in syncmodel.storage:
                if isinstance(storage, klass):
                    result.append(storage)
        return result

    def add_task(self, task, expire=0) -> bool:
        "add a new pending task to be executed by a bot that match the profile"
        if self.task_filters:
            for _filter in self.task_filters:
                assert isinstance(_filter, dict)
                for key, pattern in _filter.items():
                    string = str(task.get(key))
                    if not re.search(pattern, string, re.I):
                        break
                else:
                    break  # all patterns matches
            else:
                return False  # no patterns has been found

        # func = task[FUNC_KEY]
        func = task.setdefault(FUNC_KEY, "get_data")

        assert isinstance(
            func, str
        ), f"'func' must be a function name, not {func}"

        # overlap(kw, self._app_uri)
        candidates = self.round_robin
        for _ in range(len(candidates)):
            candidates.rotate(-1)
            bot = candidates[-1]
            if call := getattr(bot, func):
                if bot.can_handle(task):
                    # replace for a direct callable
                    task[CALLABLE_KEY] = call
                    bot.add_task(task, expire=expire)
                    return True
        else:
            log.warning(
                "can't find a callable for `%s` in (%s) bots",
                task,
                len(candidates),
            )
        return False

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        n = super().remain_tasks()
        for bot in self.bot.values():
            n += bot.remain_tasks()
        return n


class iAsyncCrawler(iCrawler):
    """A crawler that uses asyncio"""

    DEFAULT_APP_URL = ""
    DEFAULT_PREFIX = ""

    # need to be redefined by subclass
    # MODEL = None
    BOTS = [HTTPBot]

    MAPPERS = iCrawler.unwarp_mappers(
        GeoJsonEnum,
    )
    RESTRUCT_DATA = {}
    RETAG_DATA = {}
    REFERENCE_MATCHES = []
    KINDS_UID = {}

    def __init__(
        self,
        *args,
        app_url=None,
        prefix=None,
        fibers=1,
        restart=None,
        cycles=1,
        cache_timeout=600,
        **kw,
    ):
        super().__init__(
            app_url=app_url or self.DEFAULT_APP_URL,
            prefix=prefix or self.DEFAULT_PREFIX,
            *args,
            **kw,
        )
        self.fibers = fibers

        self.restart = restart
        self.cycles = cycles
        self.cache_timeout = cache_timeout

        # self.model = self.MODEL() if self.MODEL else None

    def _get_mapper_from_uri(self, uri):
        _uri = parse_duri(uri)
        for key in ("uri", "thing", "path", "basename", "table"):
            candidate = _uri.get(key)
            klass = self.MAPPERS.get(candidate)
            if klass:
                return key, candidate, klass
        raise RuntimeError(f"uri: {uri} hasn't any associated mapper")

    async def _get_initial_wave(self, task):
        """Get the initial waves from storage"""
        waves = []
        storage = None
        task[ORG_URL] = self.app_url

        # have sense to require the initial wave for this uri
        # as they have a mapper to handle it
        for storage in self._storages(klass=WaveStorage):
            # last_waves(self, sources: List, uid: UID) -> Dict[str, WAVE]:
            waves.extend(await storage.last_wave(task))
            # must break here as only one wave storage
            # should be used, but just in case ...
            if waves:
                break
        else:
            log.warning("can't find initial wave for [%s]", task)

        if not storage:
            log.warning(
                "[%s] doesn't use any WaveStorage (needed for getting initial waves)",
                self,
            )
        if waves:
            # takes the minimal wave object for resuming the process
            waves.sort(key=lambda x: x["wave"].get(MONOTONIC_KEY, 0))
            # if the same wave contains multiples objects, we need to return them all
            # because the resuming information can be in any of them.
            early_wave = waves[0]["wave"][MONOTONIC_KEY]  # must exists
            waves = [
                x for x in waves if x["wave"][MONOTONIC_KEY] == early_wave
            ]
            # TODO: REVIEW: always is a single value (len==1), why not return waves[0]
        return waves

    async def hide_run(self) -> bool:
        """Execute a full crawling loop"""
        result = True

        while self.cycles != 0:
            self.cycles -= 1

            await super().run()
            await self.start()
            await self._bootstrap()

            # wait until all work is done
            while remain := self.remain_tasks():
                try:
                    result = await asyncio.wait_for(
                        self.input_queue.get(), timeout=2
                    )
                    res = await self.dispatch(*result)
                    if not res:
                        # log.warning(
                        # "Can't save item in storage: %s", result[0][2]
                        # )
                        # log.warning("%s", pformat(result[1]))
                        self.stats["failed"] = (
                            self.stats.get("failed", 0) + 1
                        )
                        self.progress.closer()
                except queue.Empty:
                    pass
                except asyncio.exceptions.TimeoutError:
                    pass
                except Exception as why:  # pragma: nocover
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )

                self.progress.update(
                    remain=remain,
                    stats=self.stats,
                    force=False,
                )

            await self.stop()

            # end of the cycle
            if self.cycles != 0:
                restart = self.restart or 1
                log.info(
                    "remaining cycles: [%s] : restart crawling in [%s] secs",
                    self.cycles,
                    restart,
                )
                await asyncio.sleep(restart)

        # result = all([await sync.save(wait=True) for sync in self.syncmodel])
        result = await self.save()
        if result:
            log.info("all storages have been saved")
        else:
            log.error("some storages have NOT been SAVED")

        return result

    async def start(self):
        "start runner"
        await super().start()
        await self._bootstrap()

    async def idle(self):
        "default implementation when loop has nothing to do"
        # check running bots
        await asyncio.sleep(0.1)
        for bot in self.bot.values():
            if not bot.remain_tasks():
                # wait until bot exit loop
                # TODO: decide where to add and remove bots
                if bot.fiber.done():
                    pass
                else:
                    log.info(
                        "from [%s]: [%s] has not remaining tasks, request stopping",
                        self,
                        bot,
                    )
                    # direct low level put, to overpass bot.add_task() checkings
                    bot.input_queue.push(None)
                    break
        else:
            if self.remain_tasks():
                # check if having not bots,
                # we have something in the input_queue
                await super().idle()
            else:
                log.info(
                    "[%s] hasn't more pending tasks, request stopping myself",
                    self,
                )
                self.input_queue.push(None)

    async def run(self) -> bool:
        """Execute a full crawling loop"""
        result = True

        while self.cycles != 0:
            self.cycles -= 1

            await super().run()

            # wait until all work is done
            while remain := self.remain_tasks():
                try:
                    result = await asyncio.wait_for(
                        self.input_queue.get(), timeout=2
                    )
                    res = await self.dispatch(*result)
                    if not res:
                        # log.warning(
                        # "Can't save item in storage: %s", result[0][2]
                        # )
                        # log.warning("%s", pformat(result[1]))
                        self.stats["failed"] = (
                            self.stats.get("failed", 0) + 1
                        )
                        self.progress.closer()
                except queue.Empty:
                    pass
                except asyncio.exceptions.TimeoutError:
                    pass
                except Exception as why:  # pragma: nocover
                    log.error(why)
                    log.error(
                        "".join(traceback.format_exception(*sys.exc_info()))
                    )

                self.progress.update(
                    remain=remain,
                    stats=self.stats,
                    force=False,
                )

            # end of the cycle
            if self.cycles != 0:
                restart = self.restart or 1
                log.info(
                    "[%s]: remaining cycles: [%s] : restart crawling in [%s] secs",
                    self,
                    self.cycles,
                    restart,
                )
                await asyncio.sleep(restart)

        result = await self.save()
        if result:
            log.info("all storages have been saved")
        else:
            log.error("some storages have NOT been SAVED")

        return result

    async def inject(self, data, context):
        "create an item from data and try to update into storage"

        # processed data, (execution context, original data)
        if isinstance(data, dict):
            kind = data[KIND_KEY]
            # task.pop(CALLABLE_KEY)  # don't propagate
            # kind = context[KIND_KEY] # equivalent

            # inject item into models
            item = self.new(kind, data, **context)
        else:
            item = data

        if item:
            assert isinstance(item, _BaseModel)
            # result = await self.syncmodel.put(item)
            context.update(data)
            result = all(
                [await sync.put(item, **context) for sync in self.syncmodel]
            )
            # save original item if a raw storage has been specified
            if self.raw_storage:
                fqid = item.id
                await self.raw_storage.put(fqid, data)

            # check if we need to do something from time to time
            t1 = time.time()
            if t1 > self.t1:
                self.t1 = t1 + self.nice
                await self.save(nice=True)
        else:
            foo = 1

    async def update_meta(self, tube, meta: Dict) -> bool:
        meta = json_compatible(meta)
        log.info("Updating Meta: [%s]", meta)
        result = all(
            [
                await sync.update_meta(tube=tube, meta=meta)
                for sync in self.syncmodel
            ]
        )
        return result

    async def save(self, nice=False, wait=False):
        log.info("[%s] Saving models ...", self)
        result = all(
            [
                await sync.save(nice=nice, wait=wait)
                for sync in self.syncmodel
            ]
        )
        if self.raw_storage:
            res = await self.raw_storage.save(nice=nice, wait=wait)
            result = result and res
        return result

    async def _create_resources(self):
        """Try to adjust needed resources in every restart"""
        BOTS = deque(self.BOTS)

        for n in range(self.fibers):

            # BOTS.rotate()
            # klass = BOTS[-1]
            for klass in BOTS:
                name = f"{klass.__name__.lower()}-{n}"

                klass.clean()
                if name not in self.bot:
                    bot = klass(
                        output_queue=self.input_queue,
                        name=name,
                        parent=self,
                        context=self.__dict__,
                    )
                    await self.add_bot(bot)

    async def _stop_resources(self):
        # Add sentinel values to signal worker threads to exit
        while self.bot:
            for bot in self.bot.values():
                await self.remove_bot(bot)
                break

    async def add_bot(self, bot: iBot):
        self.bot[bot.name] = bot
        self.round_robin.append(bot)
        loop = asyncio.get_running_loop()
        bot.fiber = loop.create_task(bot.run())

    async def remove_bot(self, bot: iBot):
        assert bot.name in self.bot

        # request bot to finish
        # bot.input_queue.put_nowait(None)

        # remove bot for more assignations
        self.round_robin.remove(bot)
        self.bot.pop(bot.name)

    def remain_tasks(self):
        "compute how many pending tasks still remains"
        n = sum([sync.running() for sync in self.syncmodel])
        if self.raw_storage:
            n += self.raw_storage.running()
        n += super().remain_tasks()
        # x = 1
        # n += x
        return n

    def _clean(self, kind, data):
        for k, v in data.items():
            if isinstance(v, str):
                data[k] = v.strip()
        return data

    # Transformer

    def convert_into_references(self, data):
        """Search for nested objects in `value` and convert them into references"""
        if self.REFERENCE_MATCHES:
            id_keys = list(
                walk(
                    data,
                    keys_included=self.REFERENCE_MATCHES,
                    include_struct=False,
                )
            )
            for idkey, idval in id_keys:
                # myassign(value, myget(value, idkey), idkey[:-1])
                myassign(data, idval, idkey[:-1])

        return data

    def new(self, kind, data, **context):
        """Try to create / update an item of `type_` class from raw data

        - convert nested data into references
        - convert data to suit pydantic schema
        - get the pydantic item

        """
        if not data:
            return
        d = re.match(REG_KIND, kind).groupdict()
        real_kind = d["parent"]
        klass = self.MAPPERS.get(real_kind)
        if not klass:
            log.warning(
                "missing MAPPERS[%s] class!", kind
            )  # TODO: remove debug
            return

        data2 = self.convert_into_references(data)
        context.update(data2)

        # use item() as context is already transformed
        item = klass.item(context)

        # agp: TODO: delete check
        if item:
            sid = item.id
            _sid = parse_uri(sid)
            assert _sid["fscheme"]
            assert _sid["xhost"]

        return item

    def _restruct(self, kind, data, reveal):
        """Restructure internal data according to `RESTRUCT_DATA` structure info.

        Finally the result is the overlay of the original `data` and the restructured one.
        """
        restruct = {}
        info = self.RESTRUCT_DATA.get("default", {})
        info.update(self.RESTRUCT_DATA.get(kind, {}))
        for path, value in reveal.items():
            for pattern, (new_path, new_value) in info.items():
                m = re.match(pattern, path)
                if m:
                    d = m.groupdict()
                    d["value"] = value
                    key = tuple(new_path.format_map(d).split(SEP))
                    _value = (
                        value
                        if new_value == COPY
                        else new_value.format_map(d)
                    )
                    restruct[key] = _value

        # build the restructured data
        restruct = rebuild(restruct, result={})
        # create the overlay of both data to be used (possibly) by pydantic
        data = {**data, **restruct}

        return data

    def _transform(self, kind, data):
        return data
