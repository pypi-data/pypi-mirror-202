import os
import shutil
from tempfile import gettempdir
from subprocess import Popen
from nodejs import npm, node
from .log import critical, err, info, execute

tmp_dir = gettempdir()
server_dir = os.path.join(tmp_dir, "node-chatgpt-api")
process: Popen | None = None


def _setup_api_server():
    if not shutil.which("git"):
        err("Couldn't find the executable for git on the PATH")
        critical(1, "Please make sure git is installed before continuing")

    if not os.path.isdir(server_dir):
        info("Cloning node-chatgpt-api into", server_dir)

        curr = os.getcwd()

        os.chdir(tmp_dir)
        execute("git clone https://github.com/waylaidwanderer/node-chatgpt-api")

        os.chdir(server_dir)
        npm.call(["install"])

        os.chdir(curr)


def start_api_server(settings_path: str):
    """
        Starts the node-chatgpt-api server in a separate thread
        :param settings_path: the absolute path to the settings.js, find an example here: https://github.com/waylaidwanderer/node-chatgpt-api/blob/main/settings.example.js
    """
    _setup_api_server()

    os.chdir(server_dir)
    print(">", "node bin/server.js --settings=" + settings_path)

    global process
    process = node.Popen(["bin/server.js", "--settings=" + settings_path])


def stop_api_server():
    """
        Stops the node-chatgpt-api server.
        This is important because unless this is executed, the server keeps running.
        On Windows, this will instantly terminate the process, whilst on Linux it will properly shut down.
    """

    global process
    process.kill()
