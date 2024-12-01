# PyTempl

Build HTML user interfaces in Python.

## Introduction

PyTempl is a DSL that lets you build HTML components as Python objects, offering a clean, component-based approach that avoids the complexities of traditional templating engines. Create reusable components that generate HTML fragments to build complex views, pages, or even entire web applications, all within your Python workflow.


## Getting Started

**Installation:**

```bash
pip install pytempl  
```

**Simple Example:**

```python
from pytempl.tags import H1, Div, P
from pytempl import render

page = Div(_class="container")(
    H1()("My Awesome Page"),
    P()("This is a paragraph of text.")
)

print(render(page))
```

This will output neatly formatted HTML.

**Advanced Example: Dynamic Content and Components**

```python
from pytempl.tags import Li, Span, Ul
from pytempl import render

items = ["apple", "banana", "cherry"]
item_list = Ul()(Li()(item) for item in items)

name = "Alice"
greeting = Span()(f"Hello, {name}!")

print(render(Div()(greeting, item_list)))
```

This demonstrates creating dynamic content and nesting components.  The output will be an HTML `<div>` containing a greeting and the unordered list of fruits.

## License

This project is licensed under the [BSD-2-Clause License](LICENCE.md)
