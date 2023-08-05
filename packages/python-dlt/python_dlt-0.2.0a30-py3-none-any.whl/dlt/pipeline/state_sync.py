import base64
import binascii
from typing import Any, Optional, cast
import zlib

import pendulum

import dlt

from dlt.common import json
from dlt.common.pipeline import TPipelineState
from dlt.common.typing import DictStrAny
from dlt.common.schema.typing import LOADS_TABLE_NAME, TTableSchemaColumns

from dlt.destinations.sql_client import SqlClientBase
from dlt.extract.source import DltResource

from dlt.pipeline.exceptions import PipelineStateEngineNoUpgradePathException


# allows to upgrade state when restored with a new version of state logic/schema
STATE_ENGINE_VERSION = 2
# state table name
STATE_TABLE_NAME = "_dlt_pipeline_state"
# state table columns
STATE_TABLE_COLUMNS: TTableSchemaColumns = {
    "version": {
        "name": "version",
        "data_type": "bigint",
        "nullable": False
    },
    "engine_version": {
        "name": "engine_version",
        "data_type": "bigint",
        "nullable": False
    },
    "pipeline_name": {
        "name": "pipeline_name",
        "data_type": "text",
        "nullable": False
    },
    "state": {
        "name": "state",
        "data_type": "text",
        "nullable": False
    },
    "created_at": {
        "name": "created_at",
        "data_type": "timestamp",
        "nullable": False
    }
}


def merge_state_if_changed(old_state: TPipelineState, new_state: TPipelineState, increase_version: bool = True) -> Optional[TPipelineState]:
    # we may want to compare hashes like we do with schemas
    if json.dumps(old_state, sort_keys=True) == json.dumps(new_state, sort_keys=True):
        return None
    # TODO: we should probably update smarter ie. recursively
    old_state.update(new_state)
    if increase_version:
        old_state["_state_version"] += 1
    return old_state


def state_resource(state: TPipelineState) -> DltResource:
    state_str = json.dumps(state)
    state_doc = {
        "version": state["_state_version"],
        "engine_version": state["_state_engine_version"],
        "pipeline_name": state["pipeline_name"],
        "state": base64.b64encode(zlib.compress(state_str.encode("utf-8"), level=9)).decode("ascii"),
        "created_at": pendulum.now()
    }

    return dlt.resource([state_doc], name=STATE_TABLE_NAME, write_disposition="append", columns=STATE_TABLE_COLUMNS)


def load_state_from_destination(pipeline_name: str, sql_client: SqlClientBase[Any]) -> TPipelineState:
    # NOTE: if dataset or table holding state does not exist, the sql_client will rise DatabaseUndefinedRelation. caller must handle this
    query = f"SELECT state FROM {STATE_TABLE_NAME} AS s JOIN {LOADS_TABLE_NAME} AS l ON l.load_id = s._dlt_load_id WHERE pipeline_name = %s AND l.status = 0 ORDER BY created_at DESC"
    with sql_client.execute_query(query, pipeline_name) as cur:
        row = cur.fetchone()
    if not row:
        return None
    state_str = row[0]
    try:
        state_bytes = base64.b64decode(state_str, validate=True)
        state_str = zlib.decompress(state_bytes).decode("utf-8")
    except binascii.Error:
        pass
    s = json.loads(state_str)
    return migrate_state(pipeline_name, s, s["_state_engine_version"], STATE_ENGINE_VERSION)


def migrate_state(pipeline_name: str, state: DictStrAny, from_engine: int, to_engine: int) -> TPipelineState:
    if from_engine == to_engine:
        return cast(TPipelineState, state)
    if from_engine == 1 and to_engine > 1:
        state["_local"] = {}
        from_engine = 2

    # check state engine
    state["_state_engine_version"] = from_engine
    if from_engine != to_engine:
        raise PipelineStateEngineNoUpgradePathException(pipeline_name, state["_state_engine_version"], from_engine, to_engine)

    return cast(TPipelineState, state)
