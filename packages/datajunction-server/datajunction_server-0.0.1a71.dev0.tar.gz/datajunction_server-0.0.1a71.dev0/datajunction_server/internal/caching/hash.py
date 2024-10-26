"""Helpers for hashing"""
import hashlib

def get_hash_key(
    metrics=[],
    dimensions=[],
    filters=[],
    orderby=[],
    limit=None,
    engine_name=None,
    engine_version=None,
    use_materialized=None,
):
    return hashlib.sha256(f"{metrics}-{dimensions}-{filters}-{orderby}-{limit}-{engine_name}-{engine_version}-{use_materialized}".encode()).hexdigest()
