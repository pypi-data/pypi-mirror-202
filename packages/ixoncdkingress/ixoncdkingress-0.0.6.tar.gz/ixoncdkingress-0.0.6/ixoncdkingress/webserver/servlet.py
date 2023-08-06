"""CBC servlet module."""
from http.cookies import SimpleCookie
from typing import Tuple, Optional, Dict, Any, Iterable, TYPE_CHECKING

import json
from urllib.parse import parse_qs

from ixoncdkingress.cbc.caller import call_cbc
from ixoncdkingress.cbc.context import CbcContext
from ixoncdkingress.webserver.form import generate_form, parse_form_input
from ixoncdkingress.webserver.utils import read_qs_as_dict, parse_json_input

from ixoncdkingress.types import ResponseCode, ContentType, FunctionLocation, FunctionArguments, \
    RequestMethod

from ixoncdkingress.webserver.config import Config

if TYPE_CHECKING:
    # pylint: disable=E0401,E0611
    from _typeshed.wsgi import WSGIEnvironment, StartResponse

class Request:
    """
    Represents an HTTP request, containing headers and optionally a body
    """
    body: Optional[Dict[str, Any]]
    config: Config
    content_type: Optional[ContentType]
    cookies: Optional[SimpleCookie[str]]
    request_body: bytes
    request_method: RequestMethod

    def __init__(self, config: Config, environ: 'WSGIEnvironment') -> None:
        self.config = config
        self.request_method = RequestMethod(environ['REQUEST_METHOD'])
        self.body = None

        if cookies_env := environ.get('HTTP_COOKIE'):
            self.cookies = SimpleCookie(cookies_env)
        else:
            self.cookies = None

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            self.request_body = environ['wsgi.input'].read(request_body_size)
        except ValueError:
            self.request_body = b''

        try:
            self.content_type = ContentType(environ['CONTENT_TYPE'])
        except (KeyError, ValueError):
            self.content_type = None

    def parse_body(self) -> None:
        """
        Parses the request body according to the `content_type`.

        Must only be called once.
        """
        assert self.body is None

        if ContentType.FORM == self.content_type:
            self.body = parse_qs(self.request_body.decode('utf-8'))
        elif ContentType.JSON == self.content_type:
            self.body = json.loads(self.request_body)
        else:
            raise NotImplementedError()

class Response:
    """
    Represents an HTTP response, containing headers and a body
    """
    body: Optional[bytes]
    content_type: Optional[ContentType]
    cookie: dict[str, str]
    headers: list[tuple[str, str]]
    start_response: 'StartResponse'
    status_code: ResponseCode

    def __init__(self, start_response: 'StartResponse') -> None:
        self.body = None
        self.content_type = None
        self.cookie = {}
        self.headers = []
        self.start_response = start_response
        self.status_code = ResponseCode.OK

    def __call__(self, *args: Any, **kwargs: Any) -> Iterable[bytes]:
        headers = [*self.headers, *[('Set-Cookie', f'{k}={v}') for (k,v) in self.cookie.items()]]

        if self.content_type:
            headers.insert(0, ('Content-Type', f'{self.content_type.value}; charset=utf-8'))

        self.start_response(self.status_code.status_line(), headers)

        if self.body:
            return [self.body]

        return []

    def set_body(self, body: bytes) -> None:
        """
        Sets the body of the response
        """
        self.body = body

class Servlet:
    """Servlet handling CBC calls."""
    config: Config

    def __init__(self, config: Config) -> None:
        self.config = config

    def do_options(self, request: Request, response: Response) -> None:
        """
        Handle an OPTIONS request
        """
        del request

        response.status_code = ResponseCode.NO_CONTENT
        response.content_type = ContentType.HTML
        response.headers = [
            # Only useful for testing with swagger
            # when not running behind a production nginx
            ('Access-Control-Allow-Credentials', 'false'),
            ('Access-Control-Allow-Headers', '*'),
            ('Access-Control-Allow-Methods', '*'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Expose-Headers', '*'),
            ('Access-Control-Max-Age', '30'),  # cache time of the above
        ]

    def do_get(self, request: Request, response: Response) -> None:
        """
        Handle a GET request
        """
        response.status_code = ResponseCode.OK
        response.headers = [('Content-Type', ContentType.HTML.value)]

        pre_fill = {}

        if request.cookies:
            pre_fill = {k: v.value for k, v in request.cookies.items()}

        response.set_body(bytes(generate_form(pre_fill), 'utf-8'))

    def do_post(self, request: Request, response: Response) -> None:
        """
        Handle a POST request
        """
        available_content_types = [ContentType.JSON]
        if not self.config.production_mode:
            # Only JSON requests are allowed in production mode
            available_content_types.append(ContentType.FORM)

        if request.content_type not in available_content_types:
            raise NotImplementedError()

        out_put = call_cbc(
            self.config,
            *(self._parse_body(request.request_body, request.content_type)))

        if ContentType.FORM == request.content_type:
            pre_fill = read_qs_as_dict(request.request_body)
            response.set_body(
                bytes(generate_form(pre_fill, json.dumps(out_put, indent=4)), 'utf-8')
            )
            response.content_type = ContentType.HTML
            response.cookie = {k: f'{v}; Max-Age=28800' for k, v in pre_fill.items()}
        else: # ContentType.JSON by exclusion
            response.set_body(bytes(json.dumps(out_put), 'utf-8'))
            response.content_type = request.content_type
            response.headers.append(('Access-Control-Allow-Origin', '*'))

    def _parse_body(
        self,
        in_put: bytes,
        content_type: ContentType
    ) -> Tuple[CbcContext, FunctionLocation, FunctionArguments]:
        """
        Parses the request body to a key-value dictionary.
        """
        body = in_put.decode('utf-8')

        if content_type == ContentType.FORM:
            return parse_form_input(self.config, body)

        if content_type == ContentType.JSON:
            return parse_json_input(self.config, body)

        raise NotImplementedError()
