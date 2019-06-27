# Copyright (c) 2016-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict


import inspect
import types
from typing import Callable, Iterable

from .inspect_parser import extract_annotation, extract_name, extract_view_name
from .model_generator import ModelGenerator


class RESTApiSourceGenerator(ModelGenerator):
    def __init__(self, whitelist: Iterable[str]) -> None:
        self.whitelist = whitelist

    def compute_models(self, visit_all_views: Callable[..., None]) -> Iterable[str]:
        entry_points = set()

        # pyre-fixme[2]: Parameter annotation cannot contain `Any`.
        def entry_point_visitor(view_func: Callable) -> None:
            view_name = extract_view_name(view_func)
            if view_name in self.WHITELISTED_VIEWS:
                return
            params = []
            if isinstance(view_func, types.FunctionType):
                view_params = inspect.signature(view_func).parameters
                for parameter_name in view_params:
                    parameter = view_params[parameter_name]
                    annotation = extract_annotation(parameter)
                    if annotation is None or annotation not in self.whitelist:
                        params.append(
                            f"{extract_name(parameter)}: TaintSource[UserControlled]"
                        )
                    else:
                        params.append(extract_name(parameter))
            elif isinstance(view_func, types.MethodType):
                # pyre-fixme
                view_params = inspect.signature(view_func.__func__).parameters
                for parameter_name in view_params:
                    parameter = view_params[parameter_name]

                    if extract_annotation(parameter) not in self.whitelist:
                        params.append(
                            f"{extract_name(parameter)}: TaintSource[UserControlled]"
                        )
                    else:
                        params.append(extract_name(parameter))
            else:
                return

            params = ", ".join(params) if len(params) > 0 else ""
            exit_node = "def {func_name}({params}): ...".format(
                func_name=view_name, params=params
            )
            entry_points.add(exit_node)

        visit_all_views(entry_point_visitor)
        return sorted(entry_points)