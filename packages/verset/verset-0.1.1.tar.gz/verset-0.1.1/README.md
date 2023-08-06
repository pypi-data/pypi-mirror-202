# Verset

A handy tool to manage dependencies of your python project.
Meant to be used with poetry, but can adapt to other tools with minimal effort.

## Usage

Commands:

-  comment: (default) update comments to match versions currently in use
-  clear: clear comments
-  apply: apply versions in comment, so they are tilde (~) required version
-  relax: apply versions in comment, so they are caret (^) required version
-  up: set every version as "*"

## Example

Given those dependencies
```toml
[tool.poetry.dependencies]
docutils = ">= 0.12"
python = ">=3.8"

python-dateutil = {version="^2.8.2", optional=true}
jira = {version="^3.1.1", optional=true}
six = {version="^1.16", optional=true}
pygments = {version="^2.12.0", optional=true}
```
running `verset` in the project folder will update it to:

```toml
[tool.poetry.dependencies]
docutils = ">= 0.12" # 0.19
python = ">=3.8" # 3.10.10

python-dateutil = {version="^2.8.2", optional=true} # 2.8.2
jira = {version="^3.1.1", optional=true} # Not found
six = {version="^1.16", optional=true} # 1.16.0
pygments = {version="^2.12.0", optional=true} # 2.14.0
```

then, running `verset apply` in the project folder will update it to:

```toml
[tool.poetry.dependencies]
docutils = "~0.19" # >= 0.12
python = "~3.10.10" # >=3.8

python-dateutil = {version="~2.8.2", optional=true} # ^2.8.2
jira = {version="^3.1.1", optional=true} # Not found
six = {version="~1.16.0", optional=true} # ^1.16
pygments = {version="~2.14.0", optional=true} # ^2.12.0

```
and if you run it again, you are back to the original version (as tilde):

```toml
[tool.poetry.dependencies]
docutils = "~0.12" # ~0.19
python = "~3.8" # ~3.10.10

python-dateutil = {version="~2.8.2", optional=true} # ~2.8.2
jira = {version="^3.1.1", optional=true} # Not found
six = {version="~1.16", optional=true} # ~1.16.0
pygments = {version="~2.12.0", optional=true} # ~2.14.0
```

if you would like the more inclusive carret versions, just use `veset relax`:

```toml
[tool.poetry.dependencies]
docutils = "^0.19" # ~0.12
python = "^3.10.10" # ~3.8

python-dateutil = {version="^2.8.2", optional=true} # ~2.8.2
jira = {version="^3.1.1", optional=true} # Not found
six = {version="^1.16.0", optional=true} # ~1.16
pygments = {version="^2.14.0", optional=true} # ~2.12.0
```
