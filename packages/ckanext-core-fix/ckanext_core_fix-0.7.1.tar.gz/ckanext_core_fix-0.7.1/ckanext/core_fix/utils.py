from __future__ import annotations

import logging

import ckan.plugins.toolkit as tk

import ckanext.core_fix.config as conf
from ckanext.core_fix.exceptions import CoreFixException

log = logging.getLogger(__name__)


def notify() -> None:
    """Notify about disabled/enabled fixes on startup"""
    enabled: list[str] = []
    disabled: list[str] = []

    for fix in conf.Fixes:
        disabled.append(fix.name) if is_fix_disabled(fix) else enabled.append(fix.name)

    log.info(
        f"List of enabled fixes: {', '.join(enabled)}. "
        f"List of disabled fixes: {', '.join(disabled)}"
    )


def check_disabled_fixes() -> None:
    """Check if all fixes listed as disabled are actually exists"""
    available_fixes: list[str] = conf.Fixes._member_names_

    for fix in conf.get_disabled_fixes():
        if is_fix_exist(fix):
            continue

        raise CoreFixException(
            f"The fix `{fix}` doesn't exists. List of available fixes: {available_fixes}"
        )


def is_fix_disabled(fix: conf.Fixes | str) -> bool:
    """Check if fix is disabled"""
    fix_name: str = fix.name if isinstance(fix, conf.Fixes) else fix
    available_fixes: list[str] = conf.Fixes._member_names_

    if fix_name not in available_fixes:
        raise CoreFixException(
            f"The fix `{fix}` doesn't exists. List of available fixes: {available_fixes}"
        )

    return fix_name in conf.get_disabled_fixes()


def is_fix_exist(fix: str) -> bool:
    return fix in conf.Fixes._member_names_


def register_fix_templates(config_: tk.CKANConfig) -> None:
    """Register templates for fixes with custom templates"""
    for fix in conf.FIXES_WITH_TEMPLATES:
        if is_fix_disabled(fix):
            continue

        tk.add_template_directory(config_, f"template_fix/{fix.name}")
