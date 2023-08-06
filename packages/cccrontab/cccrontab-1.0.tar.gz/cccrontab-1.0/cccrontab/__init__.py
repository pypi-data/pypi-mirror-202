#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

import sys
import subprocess
import time


def work(seconds: int, args: [str]):
    print('Running script: "' + ' '.join(args) + '"')
    while True:
        subprocess.run(args)
        time.sleep(seconds)


def main():
    args = sys.argv
    real_args = args[1:]
    if len(real_args) < 2:
        print("Usage: python3 -m cccrontab.install [seconds] [command] [arg1] [arg2] ...")
        return
    seconds = int(real_args[0])
    command_args = real_args[1:]
    work(seconds, command_args)


if __name__ == '__main__':
    main()
