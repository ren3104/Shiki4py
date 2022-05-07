import logging
import textwrap


class RequestFormatter(logging.Formatter):
    def _formatHeaders(self, d):
        return '\n'.join(f'{k}: {v}' for k, v in d.items())

    def formatMessage(self, record):
        result = super().formatMessage(record)
        if record.message == 'Request error':
            result += textwrap.dedent('''
                ---------------- request ----------------
                {req.method} {req.url}
                {reqhdrs}

                {req.body}
                ---------------- response ----------------
                {res.status_code} {res.reason} {res.url}
                {reshdrs}

                {res.text}
            ''').format(req=record.req,
                        res=record.res,
                        reqhdrs=self._formatHeaders(record.req.headers),
                        reshdrs=self._formatHeaders(record.res.headers))
        return result


class LogManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)  
        self.logger.setLevel(logging.ERROR)

        file_handler = logging.FileHandler(filename='shiki4py.log', mode='w')
        formatter = RequestFormatter('{asctime} {levelname} {name} {message}', style='{')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def requestError(self, response):
        extra = {'req': response.request, 'res': response}
        self.logger.error('Request error', extra=extra)
