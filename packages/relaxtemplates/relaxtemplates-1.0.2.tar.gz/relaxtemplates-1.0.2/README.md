![RelaxTemplates Banner](https://ravikisha.github.io/assets/relaxtemplates.jpg)

# Relaxtemplates

<p float="left">
<img src="https://img.shields.io/badge/Python-3.6%2B-blue" alt="Python 3.6+"> 
<img src="https://img.shields.io/badge/PyPI-v24.2-blue" alt="PyPI v24.2">
<img src="https://img.shields.io/badge/Version-1.0.0-blue" alt="Version 1.0.0">
<img src="https://img.shields.io/badge/License-MIT-green" alt="MIT License"> 
<img src="https://img.shields.io/badge/Status-Active-green" alt="Active Status">
</p>

Relaxtemplates is a simplified, educational template engine designed to help developers understand the inner workings of template rendering. This project is not production-ready but instead serves as a hands-on exploration of template rendering with fundamental features commonly found in templating systems, such as variable substitution, control flow with conditionals, loops, callable functions, template inheritance, and includes.

## Why Relaxtemplates?

Relaxtemplates was created to provide a playground for experimenting with templating features and to gain insight into template engine design. It showcases key templating principles and techniques while allowing flexibility for customizations and feature expansions.

## Features

Relaxtemplates supports the following features:

1. **Variable Substitution**: Dynamically replace variables with values from the context.
2. **Control Flow (Conditionals)**: Use `if` conditions to control the flow of template content.
3. **Loops**: Use `each` to iterate over lists and collections.
4. **Callable Functions**: Pass and invoke callable functions within templates.
5. **Template Inheritance**: Extend base templates with `extend` and `block` to achieve layout inheritance.
6. **Includes**: Insert reusable template snippets with `include`.

## Getting Started

To use Relaxtemplates, include the files in your project and create a simple template. Templates are HTML files with special syntax for variables, blocks, and includes.

### Template Syntax

Relaxtemplates uses three main syntaxes: `{{ variable }}`, `{% block %}...{% endblock %}`, and `{% include %}`. These enable flexible, structured templates.

### Variables

Variables are enclosed in `{{ }}` and are replaced by corresponding values in the provided context.

```html
<div>Hello, {{ user_name }}!</div>
```

### Blocks

Blocks are enclosed in `{% %}` tags, allowing for control structures like conditionals and loops. 

#### Conditionals

Relaxtemplates supports conditionals for control flow with operators such as `>`, `<`, `>=`, `<=`, `==`, and `!=`. For instance:

```html
{% if user_age > 18 %}
    <p>Welcome, adult user!</p>
{% else %}
    <p>Welcome, young user!</p>
{% end %}
```

#### Loops

The `{% each %}` block allows you to iterate over a collection. The `it` variable represents each item in the iteration, and `..` accesses attributes from the outer scope.

```html
{% each items %}
    <p>{{ it }}</p>
{% end %}
```

Example of referencing the outer context within a loop:

```html
{% each items %}
    <p>Outer name: {{ ..name }}</p>
    <p>Item: {{ it }}</p>
{% end %}
```

#### Callable Functions

The `{% call %}` block allows for invoking functions with both positional and keyword arguments:

```html
<p>{% call format_date date_created %}</p>
<p>{% call log 'Event logged' level='debug' %}</p>
```

### Template Inheritance

Templates can extend a base template, providing a layout structure that child templates can override within defined blocks.

Base template (`base.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
</head>
<body>
    <div id="content">
        {% block content %}Default content.{% endblock %}
    </div>
</body>
</html>
```

Child template (`child.html`):
```html
{% extend 'base' %}
{% block title %}Custom Page Title{% endblock %}
{% block content %}
    <p>This is custom content for the child template.</p>
{% endblock %}
```

### Includes

Relaxtemplates supports includes for inserting reusable template snippets, such as headers and footers, using `{% include 'template_name' %}`.

```html
{% include 'header' %}
<p>Welcome to the page!</p>
{% include 'footer' %}
```

### Example Usage

1. **Define Template and Context**:
   Create a template file, e.g., `my_template.html` with variables, loops, and conditionals.

   ```html
   <h1>Welcome, {{ user_name }}!</h1>
   {% if is_member %}
       <p>Thanks for being a member!</p>
   {% else %}
       <p>Please sign up to become a member.</p>
   {% end %}
   ```

2. **Rendering**:
   Use the `Template` class to load, compile, and render the template with a given context.

   ```python
   template = Template('my_template', {'user_name': 'Alice', 'is_member': True})
   print(template.render())
   ```

## Performance

While Relaxtemplates is a simple engine, benchmarks indicate it performs efficiently. However, it lacks the optimization layers present in more mature engines like Django or Jinja2, so it is best suited for educational use and smaller projects.

| Template                | Runs       | Time Taken (ms) |
|------------------------|------------|-----------------|
| relaxtemplates         | 10,000     | 0.19            |
| django                 | 10,000     | 0.39            |
| django_default_loader  | 10,000     | 0.22            |
| jinja2                 | 10,000     | 3.28            |
| jinja2_env             | 10,000     | 0.10            |


## Contribution

Feel free to fork and explore the code. Improvements and experiments are welcome, as this project is meant for exploration and learning in template engine design.

Happy templating with Relaxtemplates!