# i3pystatus-elisaroaming
Module for [i3pystatus](https://github.com/enkore/i3pystatus) for showing roaming quota information from OmaElisa.

Requires PyPI package `requests`

![Screenshot](https://i.imgur.com/eDtOJCn.png)

## Usage
Install from PyPI
```
pip install i3pystatuscontrib.elisaroaming
```

Add module to your configuration file
```python
from i3pystatuscontrib.elisaroaming import ElisaRoaming

status.register(ElisaRoaming, 
                email="",
                password="",
                number="")
```

### Module settings
* format
* color
* color_warning: Color when data usage over warning_percentage threshold. Optional
* warning_percentage: Percentage threshold for data usage, 0.0 - 1. Optional
* email: OmaElisa email/username
* password: OmaElisa password
* number: Target phone number

### Available formatters
* `{used}` amount of quota used in gigabytes
* `{total}` amount of total quota in gigabytes
* `{free}` amount of data left in gigabytes
* `{used_percentage}` percentage of data used

