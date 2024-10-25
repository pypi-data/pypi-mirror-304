from __future__ import annotations

import logging

import ckan.model as model
import ckan.plugins.toolkit as tk
import ckan.types as types

import ckanext.alias.config as alias_config
import ckanext.alias.utils as alias_utils

log = logging.getLogger(__name__)


@tk.chained_action
def package_update(next_action, context: types.Context, data_dict: types.DataDict):
    """Create an alias for a dataset, if the `name` has been changed.
    If the automatic alias creation is disabled, skip it and call core action"""
    if not alias_config.save_alias_automatically():
        return next_action(context, data_dict)

    package = _get_package_object(data_dict)

    if not package:
        raise tk.ObjectNotFound(tk._("Package was not found."))

    package_name = package.name

    if package_name == data_dict["name"]:
        return next_action(context, data_dict)

    _save_alias(data_dict, package_name)

    return next_action(context, data_dict)


def _get_package_object(data_dict: types.DataDict) -> model.Package | None:
    name_or_id = data_dict.get("id") or data_dict.get("name")

    if name_or_id is None:
        raise tk.ValidationError({"id": tk._("Missing value")})

    return model.Package.get(name_or_id)


def _save_alias(data_dict: types.DataDict, alias: str) -> None:
    """Save a dataset name alias, store only unique ones"""
    alias_fieldname = alias_config.get_alias_fieldname()

    aliases = alias_utils.parse_alias_field(data_dict.get(alias_fieldname))

    aliases.append(alias)

    data_dict[alias_fieldname] = ",".join(set(aliases))
