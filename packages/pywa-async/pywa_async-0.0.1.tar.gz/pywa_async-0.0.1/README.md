# pywa_async

Installing this package will only install the latest version of pywa, which already includes the async support. This package is just a placeholder to prevent takeovers of the name.
Avoid using this package because if pywa gets updated, you will not get the latest version.

## Installation

```sh
pip3 install pywa # not pywa_async!
```

```python

from pywa_async import WhatsApp, types, filters

wa = WhatsApp(...)

async def main():
    await wa.send_message(...)

@wa.on_message(filters.text)
async def hello(_: WhatsApp, msg: types.Message):
    await msg.react("👋")
    await msg.reply(...)
```

