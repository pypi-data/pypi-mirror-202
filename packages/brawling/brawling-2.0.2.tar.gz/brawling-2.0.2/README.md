# Brawling 2.0

Sync + async wrapper for the Brawl Stars API (additionally via an unofficial proxy) and BrawlAPI by Brawlify

## Installation

To install normally (only sync, no cache)

```
pip install brawling
```

There are three additional extras you can install: `async`, `cache`, `acache`

To install with caching support (only sync, installs `requests-cache`)

```
pip install brawling[cache]
```

To install with async support (will install `aiohttp`)

```
pip install brawling[async]
```

To install with async caching support (will also install `aiohttp`, `aiohttp-client-cache` and `aiosqlite`)

```
pip install brawling[acache]
```

## Usage

Usage is fairly simple and straightforward:

```py
import brawling

# either a token, or a path to the file with it
TOKEN = "..."

client = brawling.Client(TOKEN)
player = client.get_player("#YOURTAG")
print(f"Hi, {player.tag}")

# or, asynchronously

client = brawling.AsyncClient(TOKEN)
player = await client.get_player("#YOURTAG")
print(f"Hi, {player.tag}")
```

If you only need to make one or few calls, you can use a context manager:

```py
with brawling.Client(TOKEN) as client:
    player = client.get_player("#YOURTAG")

# or, asynchronously
async with brawling.AsyncClient(TOKEN) as client:
    player = await client.get_player("#YOURTAG")
```

If you want to paginate over data, there are also paginator functions available to do exactly that:

```py
pages = client.page_brawler_rankings(
    brawling.BrawlerID.SHELLY,
    per_page=10, region='us', max=200
)

# ^ this operation was immediate, no data was fetched yet

for page in pages:
    # prints a list of 10 items
    print(page)

# if asynchronous, use 'await client.page_xx()' and 'async for'
```

When initializing a client, there are additional options:

```py
Client(token: str,
       proxy = False,
       strict_errors = True,
       cache = False)
```

`proxy` - uses the Royale API proxy (read [Special thanks](#special-thanks) before using!) to make requests, useful if you don't have a static IP.

`strict_errors` - throw an error if the API returned one, if set to `False`, will return an `ErrorResponse` object instead.

`cache` - enables caching of responses, caching period is determined by either the API, or a fallback default value of 10 minutes.

## Common issues

If you are having troubles with getting the `AsyncClient` to work, make sure that you initialize it inside an asynchronous function, like so:

```py
client = None

# correct
async def init():
    client = brawling.AsyncClient("...")

asyncio.run(init())

# wrong
client = brawling.AsyncClient("...")
```

## Special thanks

Thanks to [brawlify](https://brawlify.com) for the amazing project [BrawlAPI](https://brawlapi.com)

Thanks to [Royale API](https://royaleapi.com/) for providing a [proxy service](https://docs.royaleapi.com/proxy.html#how-to-use-with-the-clash-royale-api) to bypass the static IP limitation

NOTE: These two tools were made by neither me nor Supercell. They have been included in this module just because of their convenience, I am not responsible for any use of them and cannot guarantee that they are, and will continue complying with Supercell's Terms of Service, and therefore it's not my fault if they turn out to be malicious in any way.

## Disclaimer

This content is not affiliated with, endorsed, sponsored, or specifically approved by Supercell and Supercell is not responsible for it. For more information see Supercell’s Fan Content Policy: [www.supercell.com/fan-content-policy.](https://supercell.com/en/fan-content-policy/)