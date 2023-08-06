"""
Functions for finding and calling CBC functions.
"""
from typing import Any

import importlib
import sys

from ixoncdkingress.cbc.context import CbcContext
from ixoncdkingress.types import FunctionLocation, FunctionArguments
from ixoncdkingress.webserver.config import Config

def call_cbc(
        config: Config, context: CbcContext,
        function_location: FunctionLocation,
        function_kwargs: FunctionArguments) -> Any:
    """
    Finds, loads and calls the function specified in the body. The content_type specifies the
    format of the body.
    """

    # Get the specified module
    sys.path.insert(0, config.cbc_path)
    module = importlib.import_module(function_location[0])
    del sys.path[0]

    # Get the specified function
    function = getattr(module, function_location[1])

    return function(context, **function_kwargs)
