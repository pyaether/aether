# Aether

Build HTML user interfaces in Python.

## Introduction

Aether is a DSL that lets you build HTML components as Python objects, offering a clean, component-based approach that avoids the complexities of traditional templating engines. Create reusable components that generate HTML fragments to build complex views, pages, or even entire web applications, all within your Python workflow.


## Getting Started

**Installation:**

```bash
pip install pyaether  
```

**Simple Example:**

```python
from aether.tags.html import H1, Div, P
from aether import render

page = Div(_class="container")(
    H1()("My Awesome Page"),
    P()("This is a paragraph of text.")
)

print(render(page))
```

This will output neatly formatted HTML.

**Advanced Example 1: Dynamic Content and Components**

```python
from aether.tags.html import Li, Span, Ul
from aether import render

items = ["apple", "banana", "cherry"]
item_list = Ul()(Li()(item) for item in items)

name = "Alice"
greeting = Span()(f"Hello, {name}!")

print(render(Div()(greeting, item_list)))
```

This demonstrates creating dynamic content and nesting components.  The output will be an HTML `<div>` containing a greeting and the unordered list of fruits.

**Advanced Example 2: HTMX Support**

```python
from aether.tags.html import Div, Button, Img
from aether import render

click_to_load = Div(id="replace_me")(
    Button(
        _class="btn primary",
        hx_get="/example/?data=1",
        hx_target="#replace_me",
        hx_swap="outerHTML",
    )(
        "Load More Data...",
        Img(_class="htmx-indicator", src="/img/bars.svg", alt="Loading..."),
    )
)

print(render(click_to_load))
```

## Backwards Compatibility Note

This project is under active development and has not yet reached `v1.0.0`. This means that while we are working hard to build the best possible package, we may need to make changes that affect how your code works.

**Version Stability:**

- **Minor Version Updates (e.g., 0.1.x -> 0.2.x)**: These updates **may introduce breaking changes** as we refine and improve the package's functionality and APIs.
- **Patch Version Updates (e.g., 0.1.1 -> 0.1.2):** These updates will maintain compatibility within the same minor version and generally include bug fixes or small enhancements.


To avoid unexpected disruptions, it is recommended to pin your dependency to a specific minor version (v0.x) and carefully review release notes before upgrading to a new minor version.

We appreciate your understanding and welcome feedback as we work towards a stable and robust v1.0.0!


## License

This project is licensed under the [BSD-2-Clause License](LICENCE.md)
