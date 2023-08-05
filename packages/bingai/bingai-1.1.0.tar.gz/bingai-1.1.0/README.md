# BingAI (ChatGPT)

## Bing AI API for ChatGPT

### Installation

```
pip install bingai --upgrade
```

### Requirements
```
selenium (Edge browser opens up and automatically fetches tokens, no manual intervention required)
```

### Usage
```
from bingai import BingSession
session = BingSession(email, password)
session.run()
```

Microsoft credentials for the account which has access to the Bing Chat feature
