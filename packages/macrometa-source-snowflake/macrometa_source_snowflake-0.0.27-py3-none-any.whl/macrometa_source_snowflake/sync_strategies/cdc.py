import singer
import macrometa_source_snowflake.sync_strategies.common as common

LOGGER = singer.get_logger('macrometa_source_snowflake')

BOOKMARK_KEYS = {'replication_key', 'replication_key_value', 'version'}


def sync_table(snowflake_conn, catalog_entry, state, columns, replication_method):
    """Sync table using CDC-like approach"""
    common.whitelist_bookmark_keys(
        BOOKMARK_KEYS, catalog_entry.tap_stream_id, state)

    stream_version = common.get_stream_version(
        catalog_entry.tap_stream_id, state)
    state = singer.write_bookmark(state,
                                  catalog_entry.tap_stream_id,
                                  'version',
                                  stream_version)

    activate_version_message = singer.ActivateVersionMessage(
        stream=catalog_entry.stream,
        version=stream_version
    )

    singer.write_message(activate_version_message)

    # Call generate_dynamic_create_stream_query to get the query and stream_name
    create_stream_query, stream_name = common.create_stream(catalog_entry)

    # Execute the create_stream_query before defining insert_sql
    with snowflake_conn.connect_with_backoff() as open_conn:
        with open_conn.cursor() as cur:
            cur.execute(create_stream_query)

    # Replace table name with stream name
    insert_sql = common.insert_into_stream_sql(catalog_entry, stream_name, columns)

    params = {}
    with snowflake_conn.connect_with_backoff() as open_conn:
        while True:
            with open_conn.cursor() as cur:
                common.sync_query(cur,
                                catalog_entry,
                                state,
                                insert_sql,
                                columns,
                                stream_version,
                                params,
                                replication_method)
