# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['boolean_expression']
setup_kwargs = {
    'name': 'boolean-expression',
    'version': '0.1.0',
    'description': 'A simple library for constructing nested boolean expressions and rendering them in various dialects.',
    'long_description': '# boolean_expression\n\nThis is a simple library for creating nested boolean expressions and rendering them in a variety of dialects. It is provided as a single file so that it can be vendored into other projects where an external dependency is not possible or desirable. It is not assumed to be universally useful, but might be handy to someone out there.\n\n## Getting started\n\nYou can use this library out-of-the-box as a miniature DSL to construct boolean expressions in your library, which can later be converted to a search expression, query language, or the like. For example:\n\n```python\nfrom boolean_expression import AND, OR, EQ, NOT\n\ncondition = AND(\n    EQ("id", record_id),\n    OR(\n        NOT(EQ("status", "private")),\n        EQ("status", "private") & EQ("owner", searching_user),\n    )\n)\n```\n\nThere are a few built-in renderers, like one that creates LDAP expressions. Given the above, the following code...\n\n```python\nfrom boolean_expression import LdapRenderer\nprint(LdapRenderer().to_str(condition))\n```\n\n...produces the following output:\n\n```\n(&(id=theRecordId)(|(!(status=private))(&(status=private)(owner=theUser))))\n```\n\nIn most cases, however, it is likely that if you\'re using this library you have your own particular needs and will need to implement your own renderer.\n\n## Usage\n\nDevelopers considering this library are encouraged to read the docstring tests, because they demonstrate 100% of the functionality of the library. Basics are reproduced below.\n\n### Equality\n\nComparisons express an lval and an rval which are not interpreted at all during construction (but which you could choose to interpret during rendering, if appropriate to your use case).\n\nTo specify a comparison where some name or expression is expected to match a value:\n\n```python\nEQ("some_name", expected_value)\n```\n\n### Less Than / Greater Than\n\nThere are convenience methods for these common types of comparisons:\n\n```python\nLT("some_name", 0)\nGT("some_name", 0)\nLTE("some_name", 0)\nGTE("some_name", 0)\n```\n\n### And / Or\n\nThese can be constructed in one of a few ways. The most straightforward is the "Excel style":\n\n```python\nAND(\n    GT("total", 0),\n    OR(\n        EQ("alpha", "A"),\n        EQ("bravo", "B")\n    )\n)\n```\n\n...which can be made more tersely by using `&` and `|` operators:\n\n```python\nGT("total", 0) & (EQ("alpha", "A") | EQ("bravo", "B"))\n```\n\nThe `AND()` and `OR()` functions also accept keyword arguments (which are all interpreted as `EQ`):\n\n```python\nGT("total", 0) & OR(alpha="A", bravo="B")\n```\n\n### Negation\n\nThere are two ways of negating an expression. One is an atomic condition, equivalent to `X != Y`:\n\n```python\nNE("some_name", "some_value")\n```\n\nThe other way to construct "not equal" is with a compound condition. The following Python expressions all produce the same data structure:\n\n```python\n~EQ("some_name", "some_value")\nNOT(EQ("some_name", "some_value"))\nCompound("NOT", [EQ("some_name", "some_value")])\n```\n\n### Raw Expressions\n\nShould your use case require it, the library also allows for inserting raw expressions into the data structure:\n\n```python\nAND(\n    NOT(OR(Role="Admin", Role="Owner")),\n    Expression("AttemptedDelete")\n)\n```\n',
    'author': 'Alex Levy',
    'author_email': 'mesozoic@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
