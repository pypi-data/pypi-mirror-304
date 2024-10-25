from __future__ import annotations

import json
from typing import Any, Optional
from sqlalchemy import or_


import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df
import ckan.model as model
from ckan.logic.converters import convert_to_json_if_string
from ckan.logic.validators import name_validator
from ckan.types import Context, FlattenDataDict, FlattenErrorDict, FlattenKey


import ckanext.alias.utils as alias_utils


def alias_unique(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    """Ensures that the alias unique and not occupied by another dataset"""
    aliases: list[str] = convert_to_json_if_string(data[key], context)
    pkg_id: str = _get_package_id_from_data(data)

    if not aliases:
        return

    if len(aliases) != len(set(aliases)):
        raise tk.Invalid("Alias must be unique. Remove duplicates.")

    for alias in aliases:
        pkg_dict = alias_utils.get_package_by_alias(alias)

        if not pkg_dict:
            continue

        if pkg_dict["id"] == pkg_id:
            continue

        raise tk.Invalid(f"Alias '{alias}' is already occupied.")

    data[key] = json.dumps(aliases)


def alias_doesnt_conflict_with_name(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    """Ensures that the alias doesn't point to an existing* dataset.
    * We have to skip validation for a current dataset, otherwise the automatic
    alias won't work"""
    aliases = alias_utils.parse_alias_field(data[key])
    pkg_id: str = _get_package_id_from_data(data)

    for alias in aliases:
        if not _alias_point_to_an_existing_dataset(alias, pkg_id):
            continue

        raise tk.Invalid(tk._("Alias points to an existing dataset name or ID"))


def _alias_point_to_an_existing_dataset(alias: str, current_pkg_id: str) -> bool:
    query = (
        model.Session.query(model.Package.id)
        .filter(or_(model.Package.name == alias, model.Package.id == alias))
        .filter(model.Package.id != current_pkg_id)
        .filter(model.Package.state != model.State.DELETED)
    )

    return query.count() >= 1


def name_doesnt_conflict_with_alias(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    """Ensures that the name doesn't conflict with existing aliases"""

    pkg_dict = alias_utils.get_package_by_alias(data[key])

    if not pkg_dict:
        return

    pkg_id: str = _get_package_id_from_data(data)

    if pkg_dict["id"] == pkg_id:
        return

    raise tk.Invalid(f"Name '{data[key]}' is already occupied by an alias.")


def alias_valid(v: str, context) -> Any:
    """Check if each alias is a valid URL slug"""
    aliases = alias_utils.parse_alias_field(v)

    for alias in aliases:
        try:
            name_validator(alias, context)
        except tk.Invalid as e:
            raise tk.Invalid(str(e))

    return v


def _get_package_id_from_data(data: FlattenDataDict) -> str:
    pkg_id: str | df.Missing | None = data.get(("id",))

    if not pkg_id or pkg_id is df.missing:
        return ""

    return pkg_id  # type: ignore


def aliases_to_string(
    key: FlattenKey, data: FlattenDataDict, errors: FlattenErrorDict, context: Context
) -> Any:
    aliases = alias_utils.parse_alias_field(data[key])

    data[key] = ",".join(aliases)


def aliases_from_string(value: str | list[str], context) -> list[str]:
    if isinstance(value, list):
        return value

    return value.split(",") if value else []
