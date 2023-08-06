#!/bin/env python
import sys
from importlib.metadata import version as get_version

import tomlkit
import tomlkit.container
import tomlkit.items
from tomlkit import dumps, parse

PYPROJECT_FILE = "pyproject.toml"

def get_dependencies(doc: tomlkit.TOMLDocument) -> tomlkit.items.Table:
    d = doc['tool']['poetry']['dependencies']
    assert isinstance(d, tomlkit.items.Table)
    return d

def comment(deps):
    for dep in deps:
        if dep == 'python':
            version = sys.version.split(None, 1)[0].strip()
        else:
            try:
                version = get_version(dep)
            except Exception:
                version = "Not found"
        deps[dep].comment(version)

def clear(deps):
    for dep in deps:
        deps[dep]._trivia.comment = ''

def extract_version(txt):
    i = 0
    for i, c in enumerate(txt):
        if c not in '^~>=< ':
            break
    v = txt[i:]
    if v[0].isdigit():
        return v
    

def _apply(deps, prefix):
    for dep in deps:
        _comment = deps[dep]._trivia.comment
        if not _comment:
            continue
        version = extract_version(deps[dep]._trivia.comment.split('#', 1)[1].strip())

        if version:
            d = deps[dep]
            if isinstance(d, tomlkit.items.InlineTable):
                old_version = str(deps[dep]['version'])
                deps[dep]['version'] = prefix + version
            else:
                old_version = str(deps[dep])
                deps[dep] = prefix + version
            deps[dep].comment(old_version)

def apply(deps):
    return _apply(deps, "~")

def relax(deps):
    return _apply(deps, "^")

def upgrade(deps):
    for dep in deps:
        d = deps[dep]
        if isinstance(d, tomlkit.items.InlineTable):
            d.comment(d['version'])
            d['version'] = '*'
        else:
            d.comment(d)
            deps[dep] = "*"

def main():
    try:
        cmd = sys.argv[1]
    except IndexError:
        cmd = 'comment'
    doc = parse(open(PYPROJECT_FILE).read())
    deps = get_dependencies(doc)
    update_file = True

    if cmd.startswith('co'):
        comment(deps)
    elif cmd.startswith('cl'):
        clear(deps)
    elif cmd.startswith('a'):
        apply(deps)
    elif cmd.startswith('r'):
        relax(deps)
    elif cmd.startswith('u'):
        upgrade(deps)
    else:
        update_file = False
        print(f"""Syntax: {sys.argv[0]} [command]

Commands:
  comment: (default) update comments to match versions currently in use
  clear: clear comments in dependencies
  apply: apply versions in comment, so they are tilde (~) required version
  relax: apply versions in comment, so they are caret (^) required version
  up: set every version as "*"
""")

    if update_file:
        open(PYPROJECT_FILE, 'w').write(dumps(doc))
        print(dumps(doc))

if __name__ == "__main__":
    main()
