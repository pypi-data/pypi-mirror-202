#!/usr/bin/env python3

import sys
import argparse
from smobot_api import smobot_api
import asyncio

async def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pull Smobot Temperatures")
    parser.add_argument('-u', '--user',
                        metavar='user_id',
                        required=True,
                        help="Account user id")
    parser.add_argument('-p', '--password',
                        metavar='password',
                        required=True,
                        help="Account password")

    args = parser.parse_args()
    smobot = smobot_api(args.user, args.password)
    await smobot.login()
    for serial in await smobot.serials:
        print(await smobot.status(serial))

    await smobot.close()
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))