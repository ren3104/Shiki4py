from typing import MutableMapping
from requests import Response
import logging
import textwrap
import sys
import os.path


class LogManager:
    def __init__(self,
                 debug: bool = False,
                 console: bool = False) -> None:
        self.logger = logging.getLogger(__name__)

        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.ERROR)

        formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s',
                                      '%Y-%m-%d %H:%M:%S')
        file_path = os.path.splitext(os.path.split(sys.argv[0])[1])[0]
        file_handler = logging.FileHandler(filename=f"shiki4py-{file_path}.log",
                                           mode='w')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def _formatHeaders(self, d: MutableMapping) -> str:
        return '\n'.join(f'{k}: {v}' for k, v in d.items())

    def requestError(self, response: Response) -> None:
        self.logger.error(textwrap.dedent('''
            ---------------- request ----------------
            {req.method} {req.url}
            {reqhdrs}

            {req.body}
            ---------------- response ----------------
            {res.status_code} {res.reason} {res.url}
            {reshdrs}

            {res.text}
        ''').format(req=response.request,
                    res=response,
                    reqhdrs=self._formatHeaders(response.request.headers),
                    reshdrs=self._formatHeaders(response.headers)))
