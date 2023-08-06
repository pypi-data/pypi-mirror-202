# django-admin-tool-button

Custom tool buttons for Django admin

## Rationale

Define extra actions buttons for Django admin.

## Support

Supports: Python 3.9.

Supports Django Versions: 3.2.

## Installation

```shell
$ pip install https://github.com/bboogaard/admin_tool_button/archive/refs/heads/main.zip
```

## Usage

Add `admin_tool_button` to `INSTALLED_APPS`. In your `admin.py` add your custom actions like so:

```python
from admin_tool_button.contrib.admin import ButtonActionAdmin


class MyAdmin(ButtonActionAdmin):

    button_actions = ['my_action']

    def my_action(self, request):
        # Perform your custom action
```