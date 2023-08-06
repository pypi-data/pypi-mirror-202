"""Hook infrastructure for Bitfount."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from functools import partial, wraps
import logging
from types import FunctionType, MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Tuple,
    Type,
    Union,
    cast,
    overload,
    runtime_checkable,
)

from bitfount.config import BITFOUNT_TASK_BATCH_SIZE
from bitfount.data.datasources.base_source import BaseSource, FileSystemIterableSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.types import DataSplit
from bitfount.exceptions import HookError
from bitfount.federated.exceptions import BitfountTaskStartError
from bitfount.federated.helper import TaskContext
from bitfount.federated.transport.modeller_transport import _ModellerMailbox
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.types import _StrAnyDict

if TYPE_CHECKING:
    from bitfount.federated.algorithms.base import _BaseAlgorithm
    from bitfount.federated.pod import Pod
    from bitfount.federated.protocols.base import _BaseProtocol


__all__: List[str] = [
    "BaseAlgorithmHook",
    "BasePodHook",
    "HookType",
    "get_hooks",
]

logger = logging.getLogger(__name__)

_HOOK_DECORATED_ATTRIBUTE = "_decorate"


class HookType(Enum):
    """Enum for hook types."""

    POD = "POD"
    ALGORITHM = "ALGORITHM"
    PROTOCOL = "PROTOCOL"


@runtime_checkable
class HookProtocol(Protocol):
    """Base Protocol for hooks used just for type annotation."""

    hook_name: str

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        ...

    @property
    def registered(self) -> bool:
        """Return whether the hook is registered."""
        ...

    def register(self) -> None:
        """Register the hook.

        Adds hook to the registry against the hook type.
        """
        ...


@runtime_checkable
class PodHookProtocol(HookProtocol, Protocol):
    """Protocol for Pod hooks."""

    def on_pod_init_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod initialisation."""
        ...

    def on_pod_init_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod initialisation."""
        ...

    def on_pod_init_error(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook if an uncaught exception is raised during pod initialisation."""
        ...

    def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod startup."""
        ...

    def on_pod_startup_error(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook if an uncaught exception is raised during pod startup."""
        ...

    def on_pod_startup_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod startup."""
        ...

    def on_task_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the start."""
        ...

    def on_task_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the end."""
        ...

    def on_pod_shutdown_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod shutdown."""
        ...

    def on_pod_shutdown_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of pod shutdown."""
        ...


@runtime_checkable
class AlgorithmHookProtocol(HookProtocol, Protocol):
    """Protocol for Algorithm hooks."""

    def on_init_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm initialisation."""
        ...

    def on_init_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm initialisation."""
        ...

    def on_run_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm run."""
        ...

    def on_run_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm run."""
        ...


@runtime_checkable
class ProtocolHookProtocol(HookProtocol, Protocol):
    """Protocol for Protocol hooks."""

    def on_init_start(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of protocol initialisation."""
        ...

    def on_init_end(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of protocol initialisation."""
        ...

    def on_run_start(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of protocol run."""
        ...

    def on_run_end(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of protocol run."""
        ...


HOOK_TYPE_TO_PROTOCOL_MAPPING: Dict[HookType, Type[HookProtocol]] = {
    HookType.POD: PodHookProtocol,
    HookType.ALGORITHM: AlgorithmHookProtocol,
    HookType.PROTOCOL: ProtocolHookProtocol,
}

# The mutable underlying dict that holds the registry information
_registry: Dict[HookType, List[HookProtocol]] = {}
# The read-only version of the registry that is allowed to be imported
registry: Mapping[HookType, List[HookProtocol]] = MappingProxyType(_registry)


@overload
def get_hooks(type: Literal[HookType.POD]) -> List[PodHookProtocol]:
    ...


@overload
def get_hooks(type: Literal[HookType.ALGORITHM]) -> List[AlgorithmHookProtocol]:
    ...


@overload
def get_hooks(type: Literal[HookType.PROTOCOL]) -> List[ProtocolHookProtocol]:
    ...


def get_hooks(
    type: HookType,
) -> Union[
    List[AlgorithmHookProtocol], List[PodHookProtocol], List[ProtocolHookProtocol]
]:
    """Get all registered hooks of a particular type.

    Args:
        type: The type of hook to get.

    Returns:
        A list of hooks of the provided type.

    Raises:
        ValueError: If the provided type is not a valid hook type.
    """
    hooks = registry.get(type, [])
    if type == HookType.POD:
        return cast(List[PodHookProtocol], hooks)
    elif type == HookType.ALGORITHM:
        return cast(List[AlgorithmHookProtocol], hooks)
    elif type == HookType.PROTOCOL:
        return cast(List[ProtocolHookProtocol], hooks)

    raise ValueError(f"Unknown hook type {type}")


def ignore_decorator(f: Callable) -> Callable:
    """Decorator to exclude methods from autodecoration."""
    setattr(f, _HOOK_DECORATED_ATTRIBUTE, False)
    return f


def _on_pod_error(hook_name: str, f: Callable) -> Callable:
    """Pod method decorator which catches exceptions in the method.

    If an exception is caught, all registered pod hooks with the provided `hook_name`
    are called.

    Args:
        hook_name: The name of the hook to call if an exception is caught.
        f: The method to decorate.
    """

    @wraps(f)
    def pod_method_wrapper(self: Pod, *args: Any, **kwargs: Any) -> Any:
        """Wraps provided function and calls the relevant hook if there is an exception.

        Re-raises the exception if there are no hooks registered.
        """
        try:
            return_val = f(self, *args, **kwargs)
        except Exception as e:
            logger.error(f"Exception in pod {f.__name__}")
            hooks = get_hooks(HookType.POD)
            # Re-raise the exception if there are no hooks registered
            if not hooks:
                raise e
            # Otherwise log the exception and call the hooks
            logger.exception(e)
            for hook in hooks:
                try:
                    getattr(hook, hook_name)(self)  # Passing pod instance to hook
                # If Pod hooks are registered but do not have the hook, log a warning
                except NotImplementedError:
                    logger.warning(
                        f"{hook.hook_name} has not implemented hook {hook_name}"
                    )
        else:
            return return_val

    return pod_method_wrapper


#: Decorator to be used on Pod.__init__ method.
on_pod_init_error: Callable[[Callable], Callable] = partial(
    _on_pod_error, "on_pod_init_error"
)

#: Decorator to be used on Pod.start method.
on_pod_startup_error: Callable[[Callable], Callable] = partial(
    _on_pod_error, "on_pod_startup_error"
)


class BaseDecoratorMetaClass(type):
    """Base Metaclass for auto-decorating specific methods of a class."""

    @classmethod
    @abstractmethod
    def do_decorate(cls, attr: str, value: Any) -> bool:
        """Checks if an object should be decorated."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def decorator(f: Callable) -> Callable:
        """Returns the decorator to use."""
        raise NotImplementedError

    def __new__(
        cls,
        name: str,
        bases: Tuple[type, ...],
        dct: Dict[str, Any],
    ) -> type:
        """Creates a new class with specific methods decorated.

        The methods to decorate are determined by the `do_decorate` method. The class
        must not be abstract.
        """
        # Only decorate if the class is not a subclass of ABC i.e. not abstract
        if ABC not in bases:
            for attr, value in dct.items():
                if cls.do_decorate(attr, value):
                    setattr(value, _HOOK_DECORATED_ATTRIBUTE, True)
                    dct[attr] = cls.decorator(value)
        return super().__new__(cls, name, bases, dct)

    def __setattr__(self, attr: str, value: Any) -> None:
        if self.do_decorate(attr, value):
            value = self.decorator(value)
        super().__setattr__(attr, value)


class HookDecoratorMetaClass(BaseDecoratorMetaClass, type):
    """Decorate all instance methods (unless excluded) with the same decorator."""

    @staticmethod
    def decorator(f: Callable) -> Callable:
        """Hook decorator which logs before and after the hook it decorates.

        The decorator also catches any exceptions in the hook so that a hook can never
        be the cause of an error.
        """

        @wraps(f)
        def wrapper(self: BaseHook, *args: Any, **kwargs: Any) -> Any:
            """Wraps provided function and prints before and after."""
            logger.debug(f"Calling hook {f.__name__} from {self.hook_name}")
            try:
                return_val = f(self, *args, **kwargs)
            # NotImplementedError is re-raised as this is unrelated to the behaviour
            # of the hook and is re-caught elsewhere if necessary
            except NotImplementedError as e:
                raise e
            except Exception as e:
                logger.error(f"Exception in hook {f.__name__} from {self.hook_name}")
                logger.exception(e)
            else:
                logger.debug(f"Called hook {f.__name__} from {self.hook_name}")
                return return_val

        return wrapper

    @classmethod
    def do_decorate(cls, attr: str, value: Any) -> bool:
        """Checks if an object should be decorated.

        Private methods beginning with an underscore are not decorated.
        """
        return (
            "__" not in attr
            and not attr.startswith("_")
            and isinstance(value, FunctionType)
            and getattr(value, _HOOK_DECORATED_ATTRIBUTE, True)
        )


class ProtocolDecoratorMetaClass(BaseDecoratorMetaClass, type):
    """Decorates the `__init__` and `run` protocol methods."""

    @staticmethod
    def decorator(f: Callable) -> Callable:
        """Hook decorator which logs before and after the hook it decorates."""
        method_name = f.__name__
        if method_name == "__init__":

            @wraps(f)
            def init_wrapper(
                self: _BaseProtocol,
                hook_kwargs: Optional[_StrAnyDict] = None,
                *args: Any,
                **kwargs: Any,
            ) -> None:
                """Wraps __init__ method of protocol.

                Calls relevant hooks before and after the protocol is initialised.

                Args:
                    self: The protocol instance.
                    hook_kwargs: Keyword arguments to pass to the hooks.
                    *args: Positional arguments to pass to the protocol.
                    **kwargs: Keyword arguments to pass to the protocol.
                """
                hook_kwargs = hook_kwargs or {}
                for hook in get_hooks(HookType.PROTOCOL):
                    hook.on_init_start(self, **hook_kwargs)
                logger.debug(f"Calling method {method_name} from protocol")
                f(self, *args, **kwargs)
                for hook in get_hooks(HookType.PROTOCOL):
                    hook.on_init_end(self, **hook_kwargs)

            return init_wrapper

        elif method_name == "run":

            @wraps(f)
            async def run_wrapper(
                self: _BaseProtocol,
                context: Optional[TaskContext] = None,
                batched_execution: bool = False,
                hook_kwargs: Optional[_StrAnyDict] = None,
                *args: Any,
                **kwargs: Any,
            ) -> Union[Any, List[Any]]:
                """Wraps run method of protocol.

                Calls hooks before and after the run method is called and also
                orchestrates batched execution if set to True.

                Args:
                    self: Protocol instance.
                    context: Context in which the protocol is being run. Only required
                        if batched_execution is True.
                    batched_execution: Whether to run the protocol in batched mode.
                    hook_kwargs: Keyword arguments to pass to the hooks.
                    *args: Positional arguments to pass to the run method.
                    **kwargs: Keyword arguments to pass to the run method.

                Returns:
                    Return value of the run method. Or a list of return values if
                    batched_execution is True.

                Raises:
                    BitfountTaskStartError: If batched_execution is True but the
                    datasource does not support batched execution.
                """
                return_values = []
                hook_kwargs = hook_kwargs or {}
                num_batches: int = 1
                datasource: Optional[BaseSource] = None
                mailbox: Union[_WorkerMailbox, _ModellerMailbox]

                try:
                    # This should never be raised as the protocol run method is called
                    # by our own worker and modeller classes which always pass the
                    # context
                    if batched_execution and not isinstance(context, TaskContext):
                        raise BitfountTaskStartError(
                            "Context must be provided for batched execution."
                        )
                    if batched_execution and context == TaskContext.WORKER:
                        try:
                            datasource = kwargs.pop("datasource")
                        except KeyError:
                            raise BitfountTaskStartError(
                                "Datasource must be provided as a keyword argument for "
                                "batched execution."
                            )

                        # Reassuring mypy that datasource is not None at this point
                        assert datasource is not None  # nosec[assert_used]

                        batch_size = BITFOUNT_TASK_BATCH_SIZE
                        data_splitter = datasource.data_splitter or PercentageSplitter()
                        if isinstance(datasource, FileSystemIterableSource):
                            original_selected_test_file_names = (
                                data_splitter.get_filenames(datasource, DataSplit.TEST)
                            )
                            original_selected_file_names_override = (
                                datasource.selected_file_names_override
                            )
                            datasource_len = len(original_selected_test_file_names)
                        elif datasource.iterable:
                            raise BitfountTaskStartError(
                                "Batched execution is not supported for non-filesystem "
                                "iterable sources."
                            )
                        else:
                            if datasource._test_idxs is None:
                                (
                                    datasource._train_idxs,
                                    datasource._validation_idxs,
                                    datasource._test_idxs,
                                ) = data_splitter.create_dataset_splits(datasource.data)
                            assert (  # nosec[assert_used]
                                datasource._test_idxs is not None
                            )
                            original_test_indices = datasource._test_idxs
                            datasource_len = len(original_test_indices)

                        # Calculate the number of batches in the test set
                        num_batches = datasource_len // batch_size
                        if datasource_len % batch_size != 0:
                            num_batches += 1
                        # Send the total number of batches to the modeller
                        mailbox = cast(_WorkerMailbox, self.mailbox)
                        await mailbox.send_num_batches_message(num_batches)
                    elif batched_execution and context == TaskContext.MODELLER:
                        # Get the total number of batches from the worker
                        mailbox = cast(_ModellerMailbox, self.mailbox)
                        num_batches = await mailbox.get_num_batches_message()

                    # Loop through the batches of data. If batched_execution is False,
                    # this loop will only run once.
                    final_batch: bool = not batched_execution
                    for batch_num in range(num_batches):
                        logger.info(
                            f"Running batch {batch_num + 1} of {num_batches}..."
                        )
                        if batched_execution and context == TaskContext.WORKER:
                            if batch_num == num_batches - 1:
                                final_batch = True
                            start_idx = batch_num * batch_size
                            end_idx = (
                                (batch_num + 1) * batch_size
                                if not final_batch
                                else None
                            )
                            # FileSystemIterableSource and other non-iterable sources
                            # are the only two types of source that are possible at this
                            # point as we will have raised an error already if the
                            # datasource is anything else.
                            assert datasource is not None  # nosec[assert_used]
                            if isinstance(datasource, FileSystemIterableSource):
                                datasource.selected_file_names_override = (
                                    original_selected_test_file_names[start_idx:end_idx]
                                )
                            else:
                                datasource._test_idxs = original_test_indices[
                                    start_idx:end_idx
                                ]

                            # We need to reset the datasource kwarg
                            kwargs["datasource"] = datasource

                        # Call on_run_start hooks
                        for hook in get_hooks(HookType.PROTOCOL):
                            hook.on_run_start(self, **hook_kwargs)

                        # Await on the run method of the protocol
                        return_val = await f(
                            self, *args, final_batch=final_batch, **kwargs
                        )
                        hook_kwargs["results"] = return_val
                        return_values.append(return_val)

                        # Call on_run_end hooks
                        for hook in get_hooks(HookType.PROTOCOL):
                            hook.on_run_end(self, **hook_kwargs)
                except BitfountTaskStartError as e:
                    # If the task did not start correctly, the datasource was not
                    # modified so it does not need to be reset.
                    raise e
                except Exception as e:
                    # Log the exception before re-raising it in case there is
                    # another exception encountered before then
                    logger.exception(e)
                    # Return datasource to original state
                    if (
                        batched_execution
                        and context == TaskContext.WORKER
                        and datasource is not None
                    ):
                        if isinstance(datasource, FileSystemIterableSource):
                            datasource.selected_file_names_override = (
                                original_selected_file_names_override
                            )
                        else:
                            datasource._test_idxs = original_test_indices
                    raise e
                else:
                    # Return datasource to original state
                    if (
                        batched_execution
                        and context == TaskContext.WORKER
                        and datasource is not None
                    ):
                        if isinstance(datasource, FileSystemIterableSource):
                            datasource.selected_file_names_override = (
                                original_selected_file_names_override
                            )
                        else:
                            datasource._test_idxs = original_test_indices

                if batched_execution:
                    return return_values

                # If batched_execution is False, return the return value of the run. We
                # don't need to return a list of return values as there is only one.
                return return_val

            return run_wrapper

        # This is not expected to ever happen, but if it does, raise an error
        raise ValueError(f"Method {method_name} cannot be decorated.")

    @classmethod
    def do_decorate(cls, attr: str, value: Any) -> bool:
        """Checks if an object should be decorated.

        Only the __init__ and run methods should be decorated.
        """
        return (
            attr in ("__init__", "run")
            and isinstance(value, FunctionType)
            and getattr(value, _HOOK_DECORATED_ATTRIBUTE, True)
        )


class BaseHook(metaclass=HookDecoratorMetaClass):
    """Base hook class."""

    def __init__(self) -> None:
        """Initialise the hook."""
        self.hook_name = type(self).__name__

    @property
    @abstractmethod
    def type(self) -> HookType:
        """Return the hook type."""
        raise NotImplementedError

    @property
    def registered(self) -> bool:
        """Return whether the hook is registered."""
        return self.hook_name in [h.hook_name for h in _registry.get(self.type, [])]

    @ignore_decorator
    def register(self) -> None:
        """Register the hook.

        Adds hook to the registry against the hook type.
        """
        if not isinstance(self, HOOK_TYPE_TO_PROTOCOL_MAPPING[self.type]):
            raise HookError("Hook does not implement the specified protocol")

        if self.registered:
            logger.info(f"{self.hook_name} hook already registered")
            return

        logger.debug(f"Adding {self.hook_name} to Hooks registry")
        existing_hooks = _registry.get(self.type, [])
        existing_hooks.append(self)
        _registry[self.type] = existing_hooks
        logger.info(f"Added {self.hook_name} to Hooks registry")


class BasePodHook(BaseHook):
    """Base pod hook class."""

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        return HookType.POD

    def on_pod_init_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod initialisation."""
        pass

    def on_pod_init_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod initialisation."""
        pass

    def on_pod_init_error(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook if an uncaught exception is raised during pod initialisation.

        Raises:
            NotImplementedError: If the hook is not implemented. This is to ensure that
                underlying exceptions are not swallowed if the hook is not implemented.
                This error is caught further up the chain and the underlying exception
                is raised instead.
        """
        raise NotImplementedError()

    def on_pod_startup_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod startup."""
        pass

    def on_pod_startup_error(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook if an uncaught exception is raised during pod startup.

        Raises:
            NotImplementedError: If the hook is not implemented. This is to ensure that
                underlying exceptions are not swallowed if the hook is not implemented.
                This error is caught further up the chain and the underlying exception
                is raised instead.
        """
        raise NotImplementedError()

    def on_pod_startup_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the end of pod startup."""
        pass

    def on_task_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the start."""
        pass

    def on_task_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook when a new task is received at the end."""
        pass

    def on_pod_shutdown_start(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of pod shutdown."""
        pass

    def on_pod_shutdown_end(self, pod: Pod, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of pod shutdown."""
        pass


class BaseAlgorithmHook(BaseHook):
    """Base algorithm hook class."""

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        return HookType.ALGORITHM

    def on_init_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm initialisation."""
        pass

    def on_init_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm initialisation."""
        pass

    def on_run_start(
        self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any
    ) -> None:
        """Run the hook at the very start of algorithm run."""
        pass

    def on_run_end(self, algorithm: _BaseAlgorithm, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of algorithm run."""
        pass


class BaseProtocolHook(BaseHook):
    """Base protocol hook class."""

    @property
    def type(self) -> HookType:
        """Return the hook type."""
        return HookType.PROTOCOL

    def on_init_start(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of protocol initialisation."""
        pass

    def on_init_end(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of protocol initialisation."""
        pass

    def on_run_start(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very start of protocol run."""
        pass

    def on_run_end(self, protocol: _BaseProtocol, *args: Any, **kwargs: Any) -> None:
        """Run the hook at the very end of protocol run."""
        pass
