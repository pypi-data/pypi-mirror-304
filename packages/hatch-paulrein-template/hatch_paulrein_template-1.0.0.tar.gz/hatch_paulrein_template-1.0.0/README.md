# hatch-paulrein-template

[![PyPI - Version](https://img.shields.io/pypi/v/hatch-paulrein-template.svg)](https://pypi.org/project/hatch-paulrein-template)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-paulrein-template.svg)](https://pypi.org/project/hatch-paulrein-template)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pipx inject hatch hatch-paulrein-template
```

## License

`hatch-paulrein-template` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Changes

This plug-in is meant to augment the default Hatch template, not replace it.

The following changes to Hatch default template are made:

- [x] Add `versioningit` as a build dependency
- [x] Make versioning use `versioningit`, including config options
- [X] Modify `__about__.py` to use the info in the project instead of hard coded values

- [x] For CLI-projects: make help a normal option and not a group.
- [x] For CLI-projects: add click-logging (needs a dependency added as well)

- [X] Add mkdocs.yml
- [X] Add stub files for a [Diátaxis](https://diataxis.fr/) based documentation.
- [x] Add `hatch-mkdocs` configuration (don't forget to make the docs-environment non-detached)

- [x] Add extended Ruff config.

### By file

`pyproject.toml`
:   Add `versioningit` to build dependencies (modify the second line)
:   Change `[tool.hatch.version]` to use `versioningit` (foreach line, find the header and modify the next line)
:   Add `[tool.hatch.env]` and  `[tool.hatch.env.collectors.mkdocs.docs]` tables
:   Add `[tool.hatch.envs.docs]` table with `detached = false` after `[tool.hatch.env.collectors.mkdocs.docs]`
:   Add `[tool.versioningit.next-version]` and `[tool.versioningit.format]` tables
:   Add `[tool.ruff.lint]` and `[tool.ruff.format]` tables

`__about__.py`
:   Modify the `__version__` definition

`cli/__init__.py`
:   make help a normal option and not a group.
:   add click-logging (needs a dependency added as well)

`mkdocs.yml`
:   Write a better configuration

`docs/`
:   Add stub files for a [Diátaxis](https://diataxis.fr/) based documentation.




## Reference info

Info that was found out regarding project template plug-ins. At the time of writing, 2024-10-24, hatch documentation does not detail the
template system. According to [the author](https://github.com/pypa/hatch/discussions/143#discussioncomment-2263137),
he is not happy with the template system and has therefore not documented it.

### Contents of `template_config`

Most of this is taken from the central `config.toml` file. Project and package names are obviously from the invocation of `hatch new`.
The `args` key shows whether the user requested a CLI-application.

````` python
template_config:
{'name': 'Paul Reinerfelt',
 'email': 'Paul.Reinerfelt@gmail.com',
 'licenses': {'headers': True, 'default': ['MIT']},
 'description': '',
 'dependencies': set(),
 'package_name': 'frasse',
 'project_name': 'frasse',
 'project_name_normalized': 'frasse',
 'args': {'cli': False},
 'readme_file_path': 'README.md',
 'package_metadata_file_path': 'src/frasse/__about__.py',
 'license_data': {'MIT': 'MIT License\n'
                         '\n'
                         'Copyright (c) <year> <copyright holders>\n'
                         '\n'
                         'Permission is hereby granted, free of charge, to any '
                         'person obtaining a copy of this software and '
                         'associated documentation files (the "Software"), to '
                         'deal in the Software without restriction, including '
                         'without limitation the rights to use, copy, modify, '
                         'merge, publish, distribute, sublicense, and/or sell '
                         'copies of the Software, and to permit persons to '
                         'whom the Software is furnished to do so, subject to '
                         'the following conditions:\n'
                         '\n'
                         'The above copyright notice and this permission '
                         'notice shall be included in all copies or '
                         'substantial portions of the Software.\n'
                         '\n'
                         'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY '
                         'OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT '
                         'LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
                         'FITNESS FOR A PARTICULAR PURPOSE AND '
                         'NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR '
                         'COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES '
                         'OR OTHER LIABILITY, WHETHER IN AN ACTION OF '
                         'CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR '
                         'IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER '
                         'DEALINGS IN THE SOFTWARE.\n'},
 'license_expression': 'MIT',
 'license_header': '# SPDX-FileCopyrightText: 2024-present Paul Reinerfelt '
                   '<Paul.Reinerfelt@gmail.com>\n'
                   '#\n'
                   '# SPDX-License-Identifier: MIT\n',
 'license_files': ''}
`````

## Contents of `plugin_conf`

The `plugin_conf` dictionary contains any keys (and their values, of course) that are defined under

`[template.plugins.paulrein-template]`

in the `config.toml` file. (I.e. the plug-in's own configuration, to be interpreted as it wants.)


