# smobot_api
Python package to interface with the Smobot device.
You will need to have previously registered and set up your smobot on the smobot website.

# Installation
`pip install smobot_api`

Description
===========

```
import asyncio
from smobot_api import smobot_api

async def main():
    smobot = smobot_api('<username>', '<password>')
    print(await smobot.login())
    for serial in await smobot.serials:
    print(serial)
    print(await smobot.status(serial))
    print(await smobot.setpoint(serial, 276))
    await smobot.close()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```