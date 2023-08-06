import os
import sys


def execute(command: str):
    print(">", command)
    os.system(command)


def info(*message: str):
    print("ℹ", " ".join(message))


def warn(*message: str):
    print("⚠️", " ".join(message))


def err(*message: str):
    print("❌", " ".join(message))


def critical(exit_code: int, *message: str):
    err(*message)
    sys.exit(exit_code)