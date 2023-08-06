from typing import Any
from typing import Dict

import openapi3.object_base
import tqdm

__func_alias__ = {"type_": "type"}


def plugins(hub, ctx, api: openapi3.OpenAPI) -> Dict[str, Any]:
    ret = {}
    paths: openapi3.object_base.Map = api.paths
    for name, path in tqdm.tqdm(paths.items(), desc="Parsing paths"):
        if not isinstance(path, openapi3.paths.Path):
            # Let's not fail but continue to other paths instead
            hub.log.warning(
                f"The {name} is not an instance of Path. It will not be parsed."
            )
            continue

        # Get the request type that works for this request
        for request_type in path.raw_element.keys():
            func: openapi3.paths.Operation = getattr(path, request_type)
            if not func:
                continue
            subs = [hub.tool.format.case.snake(sub) for sub in func.tags]
            if not subs:
                plugin = "init"
            else:
                plugin = subs.pop()

            # service name is already added in pop-create
            refs = subs + [plugin]
            ref = ".".join(refs)
            if ref not in ret:
                # This is the first time we have looked at this plugin
                ret[ref] = {
                    "functions": {},
                    "doc": "",
                    "imports": [
                        "from typing import Any",
                        "from typing import Dict",
                        "import dict_tools.differ as differ",
                    ],
                }

            # See if this function will be reserved CRUD operations, if so change the name
            reserved_func_name = (
                hub.pop_create.openapi3.parse.resolve_reserved_function_name(
                    name, plugin, request_type, func
                )
            )

            # Anything that doesn't resolved in reserved function name, would go into tools/{resource_name}/*
            func_name = (
                hub.pop_create.openapi3.parse.resolve_function_name(name, plugin, func)
                if not reserved_func_name
                else reserved_func_name
            )

            # print(f"{func_name}: {name}: {plugin}")

            func_data = hub.pop_create.openapi3.parse.function(func, api)
            func_data["hardcoded"] = {
                "method": request_type,
                "path": name.split(" ")[0],
                "service_name": ctx.service_name,
                "resource_name": plugin,
            }
            ret[ref]["functions"][func_name] = func_data

    return ret


def function(
    hub,
    func: openapi3.paths.Operation,
    api: openapi3.OpenAPI,
) -> Dict[str, Any]:

    params = {}
    for p in func.parameters:
        # TODO: openapi3.general.Reference is unsupported at the moment
        if isinstance(p, openapi3.paths.Parameter):
            params[p.name] = hub.pop_create.openapi3.parse.parameter(p)

    deprecated_text = "\nDEPRECATED" if func.deprecated else ""

    return {
        "doc": f"{func.summary}\n    {func.description}    {deprecated_text}".strip(),
        "params": params,
    }


def parameter(hub, parameter: openapi3.paths.Parameter):
    if parameter.in_ == "query":
        target_type = "mapping"
    elif parameter.in_ == "path":
        target_type = "mapping"
    elif parameter.in_ == "header":
        target_type = "mapping"
    elif parameter.in_ == "cookie":
        target_type = "mapping"
    else:
        raise ValueError(f"Unknown parameter type: {parameter.in_}")

    return {
        "required": parameter.required,
        "target_type": target_type,
        "target": parameter.in_,
        "param_type": hub.pop_create.openapi3.parse.type(
            parameter.schema.type
            if isinstance(parameter.schema, openapi3.schemas.Schema)
            else None
        ),
        "doc": parameter.description or parameter.name,
    }


def type_(hub, param_type: str) -> str:
    if "integer" == param_type:
        return "int"
    elif "boolean" == param_type:
        return "bool"
    elif "number" == param_type:
        return "float"
    elif "string" == param_type:
        return "str"
    elif "array" == param_type:
        return "list"
    else:
        return ""


def resolve_reserved_function_name(
    hub, name: str, plugin: str, request_type: str, func: openapi3.paths.Operation
):
    # Do not make deprecated API paths into CRUDs and throw them into tools/*
    if not func.deprecated:
        # e.g. plugin: pets, path: /pets
        if name.endswith(plugin):
            # list/post
            if request_type == "get":
                return "list"
            elif request_type == "post":
                return "create"
        # e.g.: plugin: pets, path: /pets/{id}
        elif name.rsplit("/", 1)[0].endswith(plugin):
            # get/list/put
            if request_type == "get":
                return "get"
            elif request_type == "put" or request_type == "patch":
                return "update"
            elif request_type == "delete":
                return "delete"

    return None


def resolve_function_name(hub, name: str, plugin: str, func: openapi3.paths.Operation):
    # This is the preferred way to get a function name
    # However, some APIs can just put reserved/known operationId which is not helpful here in parsing and codegen
    # Also, we always handle reserved/known operation names in different way
    func_name = (
        func.operationId
        if func.operationId
        not in ["get", "list", "create", "patch", "update", "put", "delete"]
        else None
    )

    # Fallback function name based on the pets example
    if not func_name and " " in name:
        func_name = "_".join(name.split(" ")[1:]).lower()

    if not func_name:
        # Truncate it to 10 characters and add plugin name in the end
        func_name = f"{func.summary[:10]}_{plugin}"

    if not func_name and func.extensions:
        func_name = func.extensions[sorted(func.extensions.keys())[0]]

    # Maybe we need more fallbacks, you tell me
    if not func_name:
        # Maybe a fallback based on the path and method?
        raise AttributeError(f"Not sure how to find func name for {name}, help me out")

    return hub.tool.format.case.snake(func_name)
