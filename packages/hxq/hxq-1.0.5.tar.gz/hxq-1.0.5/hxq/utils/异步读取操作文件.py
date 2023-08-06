# -*- coding: utf-8 -*-
# @Time    : 2023/4/9 2:27
# @Author  : hxq
# @Software: PyCharm
# @File    : qwwe.py

import asyncio
from functools import wraps

import aiofiles as aiofiles


def run_event_loop(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))

    return wrapped


@run_event_loop
async def read_file(file_path):
    async with aiofiles.open(file_path, mode='r') as file:
        contents = await file.read()
        print(contents)


@run_event_loop
async def write_file(file_path, contents):
    async with aiofiles.open(file_path, mode='a+') as file:
        await file.write(contents + '\n')


def main():
    write_file('file.txt', 'Hello, world!123')
    read_file('file.txt')


# asyncio.run(main())  # This line of code is required to run the async functions.
if __name__ == '__main__':
    main()
