# UserAgent Generator

This project aims to create a simple user-agent generator that can be used to mimic different browsers and devices. This can be particularly useful for web scraping and testing purposes.

## Getting Started v1.0

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- pip

### Installation

Follow these steps to set up the project:

```bash
$ pip install GenUserAgent

```
### Generate User-Agent Facebook
```Python

from Gen import UserAgentGenerator

headers = {
'User-agent': UserAgentGenerator().generate_user_agent(),
'X-Tigon-Is-Retry': 'False',
'X-Fb-Device-Group': '7948',
'X-Graphql-Request-Purpose': 'fetch',
'X-Fb-Privacy-Context': '3643298472347298',
'X-Fb-Friendly-Name': 'FbBloksActionRootQuery-com.bloks.www.bloks.caa.login.async.send_login_request',
}

```
### Show message status
```Python

from Gen import *
