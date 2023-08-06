# cbmc.py

Unofficial 麥塊匿名發文平台 API Wrapper for Python

## Installation

```sh
pip install cbmc
```

## Usage

```py
# Import the library
from cbmc import AsyncCbmc, SyncCbmc

# Obtain post with post id, raise cbmc.NotFound if not found
SyncCbmc.get_post(1)

# List recent posts, maximum 300 posts.
SyncCbmc.get_posts()

# Also available in async
async def main():
    await AsyncCbmc.get_post(1)
    await AsyncCbmc.get_posts()
```
