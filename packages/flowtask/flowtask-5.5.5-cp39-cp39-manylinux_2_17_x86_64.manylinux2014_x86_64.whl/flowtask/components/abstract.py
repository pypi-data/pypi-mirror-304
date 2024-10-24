import os
from typing import Optional, Any, Union, ParamSpec
from abc import ABC, abstractmethod
from collections.abc import Callable
import glob
from pathlib import Path, PurePath
import orjson
from navconfig import config
from ..conf import FILE_STORAGES
from ..exceptions import (
    ComponentError,
    FileNotFound
)
from ..utils import SafeDict, fnExecutor
from ..utils.constants import (
    get_constant,
    get_func_value,
    is_constant,
    is_function
)
from ..interfaces import (
    FuncSupport,
    LogSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
    SkipErrors
)


valid_types = {
    "<class 'str'>": str,
    "<class 'int'>": int,
    "<class 'float'>": float,
    "<class 'list'>": list,
    "<class 'tuple'>": tuple,
    "<class 'dict'>": dict
}


P = ParamSpec("P")


class FlowComponent(
    LogSupport,
    FuncSupport,
    ResultSupport,
    StatSupport,
    LocaleSupport,
    ABC,
):
    """Abstract

    Overview:

            Helper for building components that consume REST APIs

        .. table:: Properties
       :widths: auto
    +--------------+----------+-----------+--------------------------------------+
    | Name         | Required | Summary                                          |
    +--------------+----------+-----------+--------------------------------------+
    |  method      |   Yes    | Component for Data Integrator                    |
    +--------------+----------+-----------+--------------------------------------+
    |  attributes  |   Yes    | Attribute: barcode                               |
    +--------------+----------+-----------+--------------------------------------+


    Return the list of arbitrary days

    """
    def __init__(
        self,
        job: Optional[Union[Callable, list]] = None,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        # Task Related Component Name
        self.TaskName: Optional[str] = kwargs.pop('step_name', None)
        # Future Logic: trigger logic:
        self.runIf: list = []
        self.triggers: list = []
        self._attrs: dict = {}  # attributes
        self._variables = {}  # variables
        self._mask = {}  # masks for function replacing
        self._params = {}  # other parameters
        self._args: dict = {}
        self._filestore: Any = FILE_STORAGES.get('default')
        self._started: bool = False  # Avoid multiple start methods.
        # Object Name:
        self.__name__: str = self.__class__.__name__
        # Super classes and interfaces
        super().__init__(*args, **kwargs)
        # program
        self._program = kwargs.pop('program', 'navigator')
        # getting the argument parser:
        self._argparser = kwargs.pop('argparser', None)
        # getting the Task Pile (components pile)
        self._TaskPile = kwargs.pop(
            "TaskPile",
            {}
        )
        if self._TaskPile:
            setattr(self, "TaskPile", self._TaskPile)
        # Config Environment
        self._environment = kwargs.pop('ENV', config)
        # for changing vars (in components with "vars" feature):
        self._vars = kwargs.get('vars', {})   # other vars
        # attributes (root-level of component arguments):
        self._attributes: dict = kwargs.pop("attributes", {})
        if self._attributes:
            self.add_metric("ATTRIBUTES", self._attributes)
        self._args: dict = kwargs.pop("_args", {})
        # conditions:
        if "conditions" in kwargs:
            self.conditions: dict = kwargs.pop("conditions", {})
        # params:
        self._params = kwargs.pop("params", {})
        # parameters
        self._parameters = kwargs.pop(
            "parameters", []
        )
        # arguments list
        self._arguments = kwargs.pop(
            "arguments", []
        )
        # processing variables
        try:
            variables = kwargs.pop("variables", {})
            if isinstance(variables, str):
                try:
                    variables = orjson.loads(variables)
                except ValueError:
                    try:
                        variables = dict(x.split(":") for x in variables.split(","))
                    except (TypeError, ValueError, IndexError):
                        variables = {}
            for arg, val in variables.items():
                self._variables[arg] = val
        except KeyError:
            pass
        # previous Job has variables, need to update from existing
        self._multi: bool = False
        if job:
            self._component = job
            if isinstance(job, list):
                self._multi = True
                variables = {}
                for j in job:
                    variables = {**variables, **j.variables}
                try:
                    self._variables = {**self._variables, **variables}
                except Exception as err:
                    print(err)
            else:
                try:
                    self._variables = {**self._variables, **job.variables}
                except Exception as err:
                    print(err)
        # mask processing:
        masks = kwargs.pop('_masks', {})
        # filling Masks:
        if "masks" in kwargs:
            self._mask = kwargs["masks"]
            del kwargs["masks"]
            object.__setattr__(self, "masks", self._mask)
        for mask, replace in masks.items():
            self._mask[mask] = replace  # override component's masks
        try:
            for mask, replace in self._mask.items():
                # first: making replacement of masks based on vars:
                try:
                    if mask in self._variables:
                        value = self._variables[mask]
                    else:
                        value = replace.format(**self._variables)
                except Exception:
                    value = replace
                value = fnExecutor(value)
                # value = fnExecutor(value, env=self._environment)
                self._logger.debug(
                    f"Set Mask: {self.TaskName}:{mask} to {value!s}"
                )
                self._mask[mask] = value
        except Exception as err:
            self._logger.debug(f"Mask Error: {err}")
        # existing parameters:
        try:
            self._params = {**kwargs, **self._params}
        except (TypeError, ValueError):
            pass
        for arg, val in self._params.items():
            try:
                if arg == "no-worker":
                    continue
                if arg == self.TaskName:
                    values = dict(x.split(":") for x in self._params[arg].split(","))
                    for key, value in values.items():
                        self._params[key] = value
                        object.__setattr__(self, key, value)
                elif arg not in ["program", "TaskPile", "TaskName"]:
                    if self.TaskName in self._attributes:
                        # extracting this properties from Attributes:
                        new_args = self._attributes.pop(self.TaskName, {})
                        self._attributes = {**self._attributes, **new_args}
                    self._attrs[arg] = val
                    if arg in self._attributes:
                        val = self._attributes[arg]
                    try:
                        setattr(self, arg, val)
                    except Exception as err:
                        self._logger.warning(f"Wrong Attribute: {arg}={val}")
                        self._logger.exception(err)
            except (AttributeError, KeyError) as err:
                self._logger.error(err)
        # attributes: component-based parameters (only for that component):
        for key, val in self._attributes.items():
            # TODO: check Attributes
            if key in self._attributes:
                # i need to override attibute
                current_val = self._attributes[key]
                if isinstance(current_val, dict):
                    val = {**current_val, **val}
                elif isinstance(current_val, list):
                    current_val.append(val)
                    val = current_val
                try:
                    object.__setattr__(self, key, val)
                    self._attrs[key] = val
                except (ValueError, AttributeError) as err:
                    self._logger.error(err)
        # processing the variables:
        if hasattr(self, "vars"):
            for key, val in self._vars.items():
                if key in self.vars:
                    self.vars[key] = val
        ### File Storage:
        self._fileStorage = FILE_STORAGES
        # SkipError:
        if self.skipError == "skip":
            self.skipError = SkipErrors.SKIP
        elif self.skipError == "log":
            self.skipError = SkipErrors.LOG
        else:
            self.skipError = SkipErrors.ENFORCE

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"<{type(self).__name__}>"

    def set_filestore(self, store):
        if not store:
            raise RuntimeError(
                "Unable to detect File Storage."
            )
        self._filestore = store

    def SetPile(self, pile):
        self._TaskPile = pile

    # Abstract Context Methods:
    async def __aenter__(self):
        if not self._started:
            await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.close()
        except Exception as exc:
            self._logger.warning(
                f"Error Closing Component: {exc!s}"
            )
        return self

    @abstractmethod
    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """

    @abstractmethod
    async def run(self):
        """
        run.

        Run operations declared inside Component.
        """

    @abstractmethod
    async def close(self):
        """
        close.

        Close (if needed) component requirements.
        """

    def ComponentName(self):
        return self.__name__

    def user_params(self):
        return self._params

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    def setVar(self, name, value):
        # self._logger.debug(f'Setting VAR ON: {name} = {value}')
        self._variables[name] = value

    def setTaskVar(self, name, value):
        name = f"{self.TaskName}_{name}"
        self._variables[name] = value

    def set_attributes(self, name: str = "pattern"):
        if hasattr(self, name):
            obj = getattr(self, name)
            for field, val in obj.items():
                if field in self._params:
                    # already calculated:
                    self._attrs[field] = self._params[field]
                    setattr(self, field, self._params[field])
                elif field in self._attributes:
                    self._attrs[field] = self._attributes[field]
                    setattr(self, field, self._attributes[field])
                elif field in self._parameters:
                    self._attrs[field] = self._parameters[field]
                    setattr(self, field, self._parameters[field])
                elif field in self._variables:
                    self._attrs[field] = self._variables[field]
                    setattr(self, field, self._variables[field])
                else:
                    value = self.getFunc(val)
                    self._attrs[field] = value
                    setattr(self, field, value)
            del self._attrs["pattern"]

    def get_obj(self, name, parent):
        try:
            if not parent:
                return getattr(self, name)
            else:
                return parent[name]
        except AttributeError:
            return False

    def get_pattern(self, obj):
        try:
            pattern = obj["pattern"]
            # del obj['pattern']
            return pattern, obj
        except Exception:
            return None, obj

    def process_pattern(self, name: str = "file", parent=None):
        if not (obj := self.get_obj(name, parent)):
            return False
        # pattern has the form {file, value}:
        if not isinstance(obj, dict):
            return obj

        # first, I need the pattern object:
        pattern, obj = self.get_pattern(obj)
        if pattern is None:
            return obj

        # processing the rest of variables:
        if self._vars and f"{name}.pattern" in self._vars:
            pattern = self._vars[f"{name}.pattern"]
        elif self._variables and "pattern" in self._variables:
            pattern = self._variables["pattern"]
        elif "value" in self._variables:
            pattern = pattern.format_map(SafeDict(value=self._variables["value"]))
        if self._vars and f"{name}.value" in self._vars:
            result = self._vars[f"{name}.value"]
            return pattern.format_map(SafeDict(value=result))
        elif "value" in obj:
            # simple replacement:
            result = self.getFunc(obj["value"])
            # print('RESULT IS ', result)
            return pattern.format_map(SafeDict(value=result))
        elif "values" in obj:
            variables = {}
            result = obj["values"]
            for key, val in result.items():
                variables[key] = self.getFunc(val)
            return pattern.format_map(SafeDict(**variables))
        else:
            # multi-value replacement
            variables = {}
            if self._variables:
                pattern = pattern.format_map(SafeDict(**self._variables))
            for key, val in obj.items():
                if key in self._variables:
                    variables[key] = self._variables[key]
                else:
                    variables[key] = self.getFunc(val)
            # Return the entire object with the formatted pattern
            return pattern.format_map(SafeDict(**variables))

    def process_mask(self, name):
        if hasattr(self, name):
            obj = getattr(self, name)
            for key, value in obj.items():
                if key in self._vars:
                    obj[key] = self._vars[key]
                elif self._vars and f"{name}.{key}" in self._vars:
                    obj[key] = self._vars[f"{name}.{key}"]
                elif key in self._variables:
                    obj[key] = self._variables[key]
                else:
                    # processing mask
                    for mask, replace in self._mask.items():
                        if mask in value:
                            obj[key] = value.replace(mask, str(replace))
            return obj
        else:
            return {}

    def var_replacement(self, obj: dict):
        """var_replacement.

        Replacing occurrences of Variables into an String.
        Args:
            obj (Any): Any kind of object.

        Returns:
            Any: Object with replaced variables.
        """
        if not isinstance(obj, dict):
            return obj
        for var, replace in obj.items():
            if var in self._mask:
                value = self._mask[var]
            else:
                if isinstance(replace, str):
                    value = replace.format_map(SafeDict(**self._variables))
                elif var in self._variables:
                    value = self._variables[var]
                else:
                    value = replace
            if isinstance(obj, PurePath):
                value = Path(value).resolve()
            obj[var] = value
        return obj

    def mask_replacement(self, obj: Any):
        """mask_replacement.

        Replacing occurrences of Masks into an String.
        Args:
            obj (Any): Any kind of object.

        Returns:
            Any: Object with replaced masks.
        """
        for mask, replace in self._mask.items():
            if mask in self._variables:
                value = self._variables[mask]
                # Using SafeDict instead direct replacement:
                value = str(obj).format_map(SafeDict(**self._variables))
            else:
                if str(obj) == mask and mask.startswith("#"):
                    # full replacement of the mask
                    obj = replace
                    return obj
                else:
                    try:
                        if str(obj) == mask and mask.startswith("{"):
                            value = str(obj).replace(mask, str(replace))
                        elif mask in str(obj) and mask.startswith("{"):
                            try:
                                value = str(obj).replace(mask, str(replace))
                            except (ValueError, TypeError) as exc:
                                # remove the "{" and "}" from the mask
                                mask = mask[1:-1]
                                value = str(obj).format_map(
                                    SafeDict({mask: replace})
                                )
                        else:
                            value = str(obj).format_map(
                                SafeDict({mask: replace})
                            )
                    except (ValueError, TypeError):
                        value = str(obj).replace(mask, str(replace))
            if isinstance(obj, PurePath):
                obj = Path(value).resolve()
            else:
                obj = value
        return obj

    def mask_replacement_recursively(self, obj: Any):
        """
        This function replaces all occurrences of "{key}" in the obj structure
        with the corresponding value from the replacements dictionary, recursively.

        Args:
            obj: an object to process.

        Returns:
            The modified obj structure with curly brace replacements.
        """

        if isinstance(obj, dict):
            # If it's a dictionary, iterate through each key-value pair
            for key, value in obj.copy().items():
                # Recursively replace in the key and value
                obj[key] = self.mask_replacement_recursively(value)

                # Check if the key itself has curly braces
                if isinstance(key, str):
                    # Use f-string for formatted key
                    new_key = self.mask_replacement(key)

                    if new_key != key:
                        obj.pop(key)  # Remove old key and add formatted one
                        obj[new_key] = value  # Add key-value pair with formatted key

        elif isinstance(obj, list):
            # If it's a list, iterate through each element and replace recursively
            for idx, value in enumerate(obj):
                obj[idx] = self.mask_replacement_recursively(value)

        elif isinstance(obj, str):
            # If it's a string, use f-string formatting to replace
            return self.mask_replacement(obj)

        return obj

    def set_variables(self, obj):
        return obj.format_map(SafeDict(**self._variables))

    def set_conditions(self, name: str = "conditions"):
        if hasattr(self, name):
            obj = getattr(self, name)
            for condition, val in obj.items():
                self._logger.notice(
                    f":: Condition : {condition} = {val}"
                )
                if hasattr(self, condition):
                    obj[condition] = getattr(self, condition)
                elif is_constant(val):
                    obj[condition] = get_constant(val)
                elif is_function(val):
                    obj[condition] = get_func_value(val)
                if condition in self._variables:
                    obj[condition] = self._variables[condition]
                elif condition in self._mask:
                    obj[condition] = self._mask[condition]
                elif condition in self.conditions:
                    obj[condition] = val
            if "pattern" in obj:
                pattern = obj["pattern"]
                del obj["pattern"]
                # getting conditions as patterns
                for field in pattern:
                    if field in obj:
                        # already settled
                        continue
                    if field in self._params:
                        obj[field] = self._params[field]
                    else:
                        result = None
                        val = pattern[field]
                        if is_constant(val):
                            result = get_constant(val)
                        else:
                            result = self.getFunc(val)
                        obj[field] = result

    def get_filename(self):
        """
        get_filename.
        Detect if File exists.
        """
        if not self.filename:  # pylint: disable=E0203
            if hasattr(self, "file") and self.file:
                file = self.get_filepattern()
                if filelist := glob.glob(os.path.join(self.directory, file)):
                    self.filename = filelist[0]
                    self._variables["__FILEPATH__"] = self.filename
                    self._variables["__FILENAME__"] = os.path.basename(self.filename)
                else:
                    raise FileNotFound(f"File is empty or doesn't exists: {file}")
            elif self.previous:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = filenames[0]
                        self._variables["__FILEPATH__"] = self.filename
                        self._variables["__FILENAME__"] = os.path.basename(
                            self.filename
                        )
                    except IndexError as e:
                        raise FileNotFound(
                            f"({__name__}): File is empty or doesn't exists"
                        ) from e
            else:
                raise FileNotFound(f"({__name__}): File is empty or doesn't exists")
        else:
            return self.filename

    def get_env_value(self, key, default: str = None, expected_type: object = None):
        """
        Retrieves a value from the environment variables or the configuration.

        :param key: The key for the environment variable.
        :param default: The default value to return if the key is not found.
        :return: The value of the environment variable or the default value.
        """
        if key is None:
            return default
        if val := os.getenv(str(key)):
            return val
        elif expected_type is not None:
            if expected_type in (int, float):
                return self._environment.getint(key, default)
            elif expected_type == bool:
                return self._environment.getboolean(key, default)
            else:
                return self._environment.get(key, default)
        elif val := self._environment.get(key, default):
            return val
        else:
            if hasattr(self, "masks"):
                if key in self._masks.keys():
                    return self._masks[key]
            return key

    def processing_credentials(self):
        if self.credentials:
            for key, expected_type in self._credentials.items():
                try:
                    value = self.credentials[key]
                    if type(value) == expected_type or isinstance(value, valid_types[str(expected_type)]):  # pylint: disable=E1136 # noqa
                        # can process the credentials, extracted from environment or variables:
                        default = getattr(self, key, value)
                        val = self.get_env_value(
                            value, default=default, expected_type=expected_type
                        )
                        self.credentials[key] = val
                    elif isinstance(value, str):
                        # Use os.getenv to get the value from environment variables
                        env_value = self.get_env_value(
                            value, default=default, expected_type=expected_type
                        )
                        self.credentials[key] = env_value
                    else:
                        self.credentials[key] = value
                except KeyError as exc:
                    print(f'Failed credential {key} with value {value}: {exc}')
                    continue
                except (TypeError, ValueError) as ex:
                    self._logger.error(f"{__name__}: Wrong or missing Credentials")
                    raise ComponentError(
                        f"{__name__}: Wrong or missing Credentials"
                    ) from ex
                except Exception as ex:
                    self._logger.exception(
                        f"Error Processing Credentials: {ex}"
                    )
                    raise ComponentError(
                        f"Error Processing Credentials: {ex}"
                    ) from ex
