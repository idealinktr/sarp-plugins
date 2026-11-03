#!/usr/bin/env python3
"""Strict schema check for plugin.json and marketplace.json.

Used when `claude plugin validate --strict` is not installable. Unknown
fields fail. Required fields and value shapes follow the Claude Code
manifest and marketplace references.
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]

PLUGIN_KEYS = {
    "$schema",
    "name",
    "displayName",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "metadata",
    "icon",
    "documentationUrl",
    "supportUrl",
    "privacyPolicyUrl",
    "termsOfServiceUrl",
    "defaultEnabled",
    "dependencies",
    "settings",
    "userConfig",
    "types",
    "channels",
    "skills",
    "commands",
    "agents",
    "hooks",
    "mcpServers",
    "lspServers",
    "outputStyles",
    "workflows",
    "experimental",
}

MARKETPLACE_KEYS = {
    "$schema",
    "name",
    "owner",
    "plugins",
    "description",
    "version",
    "metadata",
    "forceRemoveDeletedPlugins",
    "allowCrossMarketplaceDependenciesOn",
    "renames",
}

ENTRY_KEYS = PLUGIN_KEYS | {
    "source",
    "category",
    "tags",
    "strict",
    "relevance",
    "headers",
    "headersHelper",
}

IDENTIFIER = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?$")
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$")
SPDX = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.+-]*$")


def fail(message):
    print(message, file=sys.stderr)
    return 1


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def unknown(label, value, allowed):
    extra = sorted(set(value) - allowed)
    if extra:
        return fail(f"{label}: unknown fields {extra}")
    return 0


def require_string(label, value, key):
    if not isinstance(value.get(key), str) or not value[key].strip():
        return fail(f"{label}: {key} must be a non-empty string")
    return 0


def check_identifier(label, value):
    if IDENTIFIER.fullmatch(value) is None or ".." in value:
        return fail(f"{label}: invalid identifier {value!r}")
    return 0


def check_url(label, value):
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return fail(f"{label}: expected an absolute http(s) URL")
    return 0


def check_author(label, author):
    if not isinstance(author, dict):
        return fail(f"{label}: author must be an object")
    status = unknown(f"{label} author", author, {"name", "email", "url"})
    status |= require_string(f"{label} author", author, "name")
    if "email" in author:
        email = author["email"]
        if not isinstance(email, str) or "@" not in email or " " in email:
            status |= fail(f"{label}: author.email is not an email address")
    if "url" in author:
        if not isinstance(author["url"], str):
            status |= fail(f"{label}: author.url must be a string")
        else:
            status |= check_url(f"{label} author.url", author["url"])
    return status


def check_plugin(label, plugin, require_contact):
    status = unknown(label, plugin, PLUGIN_KEYS)
    name = plugin.get("name")
    if not isinstance(name, str):
        status |= fail(f"{label}: name is required")
    else:
        status |= check_identifier(label, name)
    status |= require_string(label, plugin, "description")
    version = plugin.get("version")
    if not isinstance(version, str) or SEMVER.fullmatch(version) is None:
        status |= fail(f"{label}: version must be semver")
    author = plugin.get("author")
    if not isinstance(author, dict):
        status |= fail(f"{label}: author object is required")
    else:
        status |= check_author(label, author)
        if require_contact and "email" not in author:
            status |= fail(f"{label}: author.email is required")
    homepage = plugin.get("homepage")
    if not isinstance(homepage, str):
        status |= fail(f"{label}: homepage is required")
    else:
        status |= check_url(f"{label} homepage", homepage)
    repository = plugin.get("repository")
    if not isinstance(repository, str):
        status |= fail(f"{label}: repository is required")
    else:
        status |= check_url(f"{label} repository", repository)
    license_id = plugin.get("license")
    if not isinstance(license_id, str) or SPDX.fullmatch(license_id) is None:
        status |= fail(f"{label}: license must be an SPDX identifier")
    for key in ("privacyPolicyUrl", "termsOfServiceUrl"):
        if key not in plugin:
            continue
        if not isinstance(plugin[key], str):
            status |= fail(f"{label}: {key} must be a string")
        else:
            status |= check_url(f"{label} {key}", plugin[key])
    keywords = plugin.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        status |= fail(f"{label}: keywords must be a non-empty array")
    elif any(not isinstance(item, str) or not item.strip() for item in keywords):
        status |= fail(f"{label}: every keyword must be a non-empty string")
    elif len(keywords) != len(set(keywords)):
        status |= fail(f"{label}: keywords must be unique")
    return status


def check_source(label, source):
    if not isinstance(source, str) or not source.startswith("./") or ".." in source:
        return fail(f"{label}: source must be a relative path inside the marketplace")
    path = ROOT / source[2:]
    if not path.is_dir():
        return fail(f"{label}: source directory does not exist: {source}")
    return 0


def check_marketplace(marketplace):
    status = unknown("marketplace.json", marketplace, MARKETPLACE_KEYS)
    name = marketplace.get("name")
    if not isinstance(name, str):
        status |= fail("marketplace.json: name is required")
    else:
        status |= check_identifier("marketplace.json", name)
    status |= require_string("marketplace.json", marketplace, "description")
    owner = marketplace.get("owner")
    if not isinstance(owner, dict):
        status |= fail("marketplace.json: owner object is required")
    else:
        status |= unknown("marketplace.json owner", owner, {"name", "email", "url"})
        status |= require_string("marketplace.json owner", owner, "name")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        return status | fail("marketplace.json: plugins must be a non-empty array")
    seen = set()
    for index, entry in enumerate(plugins):
        label = f"marketplace.json plugins[{index}]"
        if not isinstance(entry, dict):
            status |= fail(f"{label}: must be an object")
            continue
        status |= unknown(label, entry, ENTRY_KEYS)
        entry_name = entry.get("name")
        if not isinstance(entry_name, str):
            status |= fail(f"{label}: name is required")
        else:
            status |= check_identifier(label, entry_name)
            if entry_name in seen:
                status |= fail(f"{label}: duplicate plugin name {entry_name}")
            seen.add(entry_name)
        status |= require_string(label, entry, "description")
        status |= check_source(label, entry.get("source"))
        if isinstance(entry.get("source"), str) and entry["source"].startswith("./"):
            manifest = ROOT / entry["source"][2:] / ".claude-plugin" / "plugin.json"
            if not manifest.is_file():
                status |= fail(f"{label}: missing {manifest.relative_to(ROOT)}")
            elif isinstance(entry_name, str):
                plugin_name = load(manifest).get("name")
                if plugin_name != entry_name:
                    status |= fail(
                        f"{label}: name {entry_name!r} does not match "
                        f"plugin.json name {plugin_name!r}"
                    )
    return status


def main():
    plugin_path = (
        ROOT
        / "plugins"
        / "sarp-organizational-memory"
        / ".claude-plugin"
        / "plugin.json"
    )
    marketplace_path = ROOT / ".claude-plugin" / "marketplace.json"
    status = check_plugin(str(plugin_path.relative_to(ROOT)), load(plugin_path), True)
    status |= check_marketplace(load(marketplace_path))
    if status:
        return 1
    print("ok plugin.json")
    print("ok marketplace.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
