# PushX  
One-Stop Python Push Solution.
## Introduction
Python-based Aggregate Push Module

## Supported Push Providers
- [x] Ntfy
- [x] ServerChan3
- [x] ServerChanTurbo 
- [ ] And more...

## Install

```bash
pip install pushx
```

## Usage
The docs is [here](https://illustar0.github.io/PushX), you can also refer to the Examples below.  

## Examples
### Example 1
```python
from pushx import Notifier, providers

n = Notifier(providers.ServerChan3, sendkey="666",uid=2233)
n.notify(title="test title",desp="test content")
# content/message=("content") is also fine
```
### Example 2
```python
from pushx import Notifier, providers

n = Notifier(providers.Ntfy, topic="233233233")
p = providers.Ntfy.NotifyParams(
    title="test title",
    message=("test message"), # content=("test message") is also fine
    tags=["tag1", "tag2"],
    priority=5,
    markdown=True,
    actions=[
        {
            "action": "view",
            "label": "Open portal",
            "url": "https://home.nest.com/",
            "clear": True,
        },
        {
            "action": "http",
            "label": "Turn down",
            "url": "https://api.nest.com/",
            "body": '{"temperature": 65}',
        },
    ],
    click="https://illustar0.com",
)
n.notify(p)
```