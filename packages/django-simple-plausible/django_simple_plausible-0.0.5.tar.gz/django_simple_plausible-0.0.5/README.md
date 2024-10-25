## Django Simple Plausible

A dead simple package to add Plausible Analytics html tag to your HTML. Tested with Python 2.7 and 3.8. Tested with Django 1.11 and 3.2.

### Usage

1. Install package: `pip install django_simple_plausible`

2. Add `django_simple_plausible` to your `INSTALLED_APPS` in settings.py

3. ADD `PLAUSIBLE_SITES` and `PLAUSIBLE_SCRIPT_URL` keys and values to your settings.py. Or enter the corresponding values as template tag parameters, as shown below.
```
...

PLAUSIBLE_SITES = "example.com"
PLAUSIBLE_SCRIPT_URL = "https://example.com/js/plausible.js"

...
```

4. add the following template tags to your site html:
```
{% load plausible %}
{% plausible %}
```

---

### Configuring details

- `PLAUSIBLE_SITES` can be a comma separated list without spaces, if you want to use that feature of Plausible

```
PLAUSIBLE_SITES = "example.com,yoursite.com"
```

- `PLAUSIBLE_SCRIPT_ASYNC_TAG` is an optional setting. It can be used to render the script tag with the `async` attribute instead of `defer`

```
PLAUSIBLE_SCRIPT_ASYNC_TAG = True
```
- Systemwide settings can be overridden giving the template tag some optional parameters:

```
{% plausible plausible_sites="mysite.com" script_url="https://mysite.com/plausible.js" async_tag=True %}
```
