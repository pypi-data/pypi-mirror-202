"""Contains primitive item type bases and item-related developer tools."""
import inspect
import types
import functools
from dearpygui import dearpygui, _dearpygui
from .px_typing import (
    # typing
    overload,
    Any,
    Callable,
    Generic,
    Literal,
    TypeVar,
    Sequence,
    Self,
    # px_typing
    T, P,
    ItemId,
    Array,
    DPGTypeId,
    DPGCommand,
    DPGCallback,
    DPGItemConfig,
    DPGItemInfo,
    DPGItemState,
)
from . import px_utils
from .px_utils import (
    get_config,
    get_info,
    get_state,
    get_value,
    set_config,
    set_value,
    generate_uuid,
)


__all__ = [
    # bases/mixins
    "AppItemType",
    "PositionedItem",
    "SizedItem",
    "ValueAbleItem",
    "ValueArrayItem",
    "CallableItem",
    "HandlerItem",
    "ContainerItem",
    "WindowItem",
    "RootItem",
    "RegistryItem",

    # functions
    "register_itemtype",
    "itp_from_callable",
]


# This kind of complicates user threading, but there's not much
# that can be done about it.
dearpygui.create_context()


########################################
########## MEMBER DESCRIPTORS ##########
########################################

_GT = TypeVar("_GT")
_ST = TypeVar("_ST")

class DPGProperty:
    __slots__ = ("_key")

    def __init__(self, key: str = None):
        self._key = key

    def __set_name__(self, cls, name: str):
        self._key = self._key or name


class Config(Generic[_GT, _ST], DPGProperty):
    __slots__ = ()

    def __get__(self, inst: 'AppItemType', cls) -> _GT:
        if inst is not None:
            return inst.configuration()[self._key]
        return self

    def __set__(self, inst: 'AppItemType', value: _ST) -> None:
        eval(f"inst.configure({self._key}=value)")  # no dict/unpacking


class Info(Generic[_GT], DPGProperty):
    __slots__ = ()

    def __get__(self, inst: 'AppItemType', cls) -> _GT:
        if inst is not None:
            return inst.information()[self._key]
        return self


class State(Generic[_GT], DPGProperty):
    __slots__ = ()

    def __get__(self, inst: 'AppItemType', cls) -> _GT:
        if inst is not None:
            return inst.state().get(self._key, None)
        return self


###########################################
######### APPITEM METACLASS STUFF #########
###########################################

_SELF_PARAM: inspect.Parameter = px_utils.create_parameter("self")
_KWDS_PARAM: inspect.Parameter = px_utils.create_parameter("kwargs", kind=inspect.Parameter.VAR_KEYWORD)

def _upd_pxmthd_metadata(mthd: T, parameters: dict[str, inspect.Parameter]) -> T:
    base_method   = getattr(AppItemType, mthd.__name__)
    base_mthd_sig = inspect.signature(base_method)
    _params = {_SELF_PARAM.name: _SELF_PARAM} | parameters

    mthd.__signature__ = base_mthd_sig.replace(parameters=_params.values())
    mthd.__doc__       = base_method.__doc__
    return mthd


def _new_px_configuration(parameters: dict[str, inspect.Parameter]):
    """`.configuration` method factory for `AppItemType` subclasses. The returned method
    filters settings not supported by the item."""
    def configuration(self) -> DPGItemConfig:
        return {k:v for k,v in get_config(self).items() if k in config_kwds}

    config_kwds   = frozenset(parameters)
    configuration = _upd_pxmthd_metadata(configuration, {})
    del parameters
    return configuration


def _new_px_configure(parameters: dict[str, inspect.Parameter]):
    """`.configure` method factory for `AppItemType` subclasses. The returned method
    tries to throw an appropriate error for the user when something goes wrong."""
    def configure(self, **kwargs) -> None:
        try:
            set_config(self, **kwargs)
        except SystemError:
            if _dearpygui.does_item_exist(self):
                raise TypeError(
                    f"`{type(self).__qualname__}(tag={self.real!r}).configure(...)` received an unexpected keyword argument."
                ) from None
            for kwd in kwargs:
                if kwd in config_kwds:
                    raise TypeError(f"cannot set read-only attribute {kwd!r}.")
            raise

    parameters  = px_utils.writable_cfg_from_params(parameters | {_KWDS_PARAM.name: _KWDS_PARAM})
    config_kwds = frozenset(parameters)
    configure   = _upd_pxmthd_metadata(configure, parameters)
    del parameters
    return configure



_NULL_REGISTER_FLAG: str                            = "__null_registration__"
_ITEMTYPE_REGISTRY : dict[str, type['AppItemType']] = {}  # {__qualname__: itemtype}

ITEMTYPE_REGISTRY = types.MappingProxyType(_ITEMTYPE_REGISTRY)

def register_itemtype(itp: T) -> T:
    """Register an itemtype with the global registry. Can be used as a decorator.

    The registry contains `AppItemType.__qualname__: AppItemType` pairs, and is
    primarily used to instantiate the correct itemtype interface when wrapping an
    existing Dear PyGui item. Base itemtypes are automatically registered when they
    are created, but not user subclasses.

    A user may use this to register a subclass with altered or extended functionality
    to that of an already-registered "built-in" itemtype. That aside, there is nothing
    for a user to immediately gain by registering classes. However, users are free
    to redefine and/or extend objects that use the registry to create desired features.
    """

    if hasattr(itp, _NULL_REGISTER_FLAG):
        delattr(itp, _NULL_REGISTER_FLAG)
    else:
        _ITEMTYPE_REGISTRY[itp.__qualname__] = itp
    return itp


def null_registration(itp: T) -> T:
    """Instruct `AppItemMeta` to avoid registering the new item type. Can be used
    as a decorator.

    This is a developer/debugging tool. There's no reason for a user to need this.
    """
    setattr(itp, _NULL_REGISTER_FLAG, True)
    return itp




def _metadata_conflict_check(command, identity, *bases: Sequence[type['AppItemType']]) -> bool:
    """Return True if using *bases* to create a new itemtype would cause
    a functional conflict.
    """
    try:
        bases = [b for b in bases if issubclass(b, AppItemType)]
    except NameError:  # AppItemBase
        return False
    # The command/identity must be identical (or the default) between all bases
    # and the new type's namespace.
    commands = {b.command for b in bases}
    commands.add(command)
    commands.discard(_DEFAULT_COMMAND)
    identities = {b.identity for b in bases}
    identities.add(identity)
    identities.discard(_DEFAULT_IDENTITY)
    return any(len(s) > 1 for s in (commands, identities))


def _null_command(*args, tag: ItemId | None = None, **kwargs) -> ItemId:
    return tag


_DEFAULT_COMMAND : DPGCommand      = _null_command
_DEFAULT_IDENTITY: tuple[int, str] = _dearpygui.mvAll, "mvAppItemType::mvAppItemType",



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
################################## Item API Base(s) ##################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class AppItemMeta(type):
    identity: DPGTypeId
    command : DPGCommand

    def __new__(
        mcls,
        name     : str,
        bases    : tuple[type[object], ...],
        namespace: dict[str],
        *,
        command  : DPGCommand = None,
        identity : DPGTypeId  = None,
        **kwargs
    ):
        command   = namespace.get("command", command)
        identity  = namespace.get("identity", identity)

        # Ensure that a itp from bases won't have an identity crisis.
        if _metadata_conflict_check(command or _DEFAULT_COMMAND, identity or _DEFAULT_IDENTITY, *bases):
            raise TypeError(f"could not resolve bases for {name!r}.")

        # integrity check special kwds
        if command and command is not _DEFAULT_COMMAND:
            if px_utils.is_ctxmgr_fn(command):
                command = command.__wrapped__
            if not px_utils.is_item_cmd(command):
                raise TypeError("`callable` is not callable.")
        if identity and identity is not _DEFAULT_IDENTITY:
            try:
                int_id, str_id = identity
                if not (isinstance(int_id, int) and isinstance(str_id, str)):
                    raise TypeError
            except TypeError:
                raise TypeError("`identity` must a 2-tuple containing an interger and string.") from None

        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        # new itemtype base
        if all((command, identity)):
            cls.identity = identity
            cls.command  = staticmethod(command) if not isinstance(
                           command, staticmethod) else command

            # early return for `AppItemType` & other prototypes
            if command is  _DEFAULT_COMMAND or identity is _DEFAULT_COMMAND:
                return cls

            cmd_signature = inspect.signature(command)
            px_parameters = px_utils.upd_param_annotations(cmd_signature.parameters)

            # can't set `__init__.__signature__` since `__init__` is inherited
            cls.__signature__ = cmd_signature.replace(
                parameters=px_parameters.values(),
                return_annotation=Self,
            )
            if getattr(cls, "configuration", None) is AppItemType.configuration:
                cls.configuration = _new_px_configuration(px_parameters)
            if getattr(cls, "configure", None) is AppItemType.configure:
                cls.configure = _new_px_configure(px_parameters)

            # these parameters *should* be writable configuration
            config_kwds = px_utils.writable_cfg_from_params(px_parameters)
            for kwd in config_kwds:
                # This is meant to add functionality to would-be base itemtypes, so do
                # not overwrite existing members of high-level classes.
                if hasattr(cls, kwd):
                    continue
                config_prop = Config()
                setattr(cls, kwd, config_prop)
                config_prop.__set_name__(cls, kwd)

            if not cls.__qualname__.startswith("_"):
                register_itemtype(cls)
        return cls

    def __repr__(cls) -> str:
        return f"<class {cls.__qualname__!r}>"

    def __str__(cls) -> str:
        return cls.identity[1]

    def __int__(cls) -> int:
        return cls.identity[0]


class _AppItemBase(int, Generic[P], metaclass=AppItemMeta):
    # The "base" is split into two base classes for organizational purposes. AppItemBase
    # contains only class-bound members and dunder methods. AppItemType is the actual base
    # class containing the bulk API. The only direct subclass of AppItemBase should be
    # AppItemType. Other than that, this class doesn't exist.

    @overload
    def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> Self: ...
    def __new__(cls, *args: P.args, tag: ItemId = 0, **kwargs: P.kwargs) -> Self:
        # `__new__` is responsible for generating an item uuid for the DPG item
        # created in `__init__`. A new uuid is not generated `tag` is included
        # and is an integer. If `tag` is a string ('alias'), then `__new__` tries
        # to work with it (XXX prepare for trouble).
        if not tag:  # faster op when does not include `tag`
            return super().__new__(cls, generate_uuid())

        if isinstance(tag, int):
            int_id = tag
        elif isinstance(tag, str):  # user has chosen violence
            # a string alias is being used; fetch the existing id or create a new one
            if _dearpygui.does_alias_exist(tag):
                int_id = _dearpygui.get_alias_id(tag)
            else:
                int_id = generate_uuid()
                _dearpygui.set_item_alias(int_id, tag)
            # pray that everything works
        else:
            raise TypeError(f"expected int, str identifier (got {int_id})")
        return super().__new__(cls, int_id)

    @overload
    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None: ...
    def __init__(self, *args: P.args, tag: ItemId = 0, **kwargs: P.kwargs) -> None:
        # `__init__` creates the DPG item using the item uuid generated in
        # `__new__`. If `tag` was passed to `__new__`, then the item may
        # already exist. In that case, `self.command(...)` throws an error.
        # It is suppressed and the instance is allowed to interface with the
        # existing item.
        super().__init__()
        try:
            self.command(*args, tag=self, **kwargs)
        except SystemError:
            if not _dearpygui.does_item_exist(self):
                raise px_utils.err_create_item(self.real, self.command, *args, **kwargs) from None

    def __repr__(self):
        return (
            f"{type(self).__qualname__}("
            f"tag={self.real!r}, "
            f"label={get_config(self)['label']!r}, "
            f"parent={get_info(self)['parent']!r}"
            f")"
        )

    def __getitem__(self, index: Literal[0, 1, 2, 3] | slice) -> list[ItemId] | list[list[ItemId]]:
        """Syntax sugar for fetching an item's children contained in slot *index*.

        Equivelent to `self.children(index)` when *index* is an `int`. If *index* is a
        `slice` object, returns a sliced list of `self.children().values()`.
        """
        slots = get_info(self)["children"]
        try:
            return slots[index]
        except KeyError:
            raise IndexError(f"expected a valid target slot as 0, 1, 2, or 3 (got {index!r}).") from None
        except TypeError:  # unhashable
            if isinstance(index, slice):
                return [*slots.values()][index.start, index.stop, index.step]
            raise

    def __getattr__(self, name: str) -> Any:  # fallback config getter
        try:
            return self.configuration()[name]
        except KeyError:
            raise AttributeError(
                f"{type(self).__qualname__!r} object has no attribute {name!r}."
            ) from None

    def __enter__(self) -> Self:
        """If this item is a container, temporarily place it atop the
        container stack.

        `TypeError` is raised if the item is not a container item.
        """
        try:
            _dearpygui.push_container_stack(self)
        except:
            raise TypeError("not a container item.")
        return self

    def __exit__(self, exc_val: Any = None, exc_tp: Any = None, traceback: Any = None) -> Any:
        if _dearpygui.top_container_stack() == self:
            _dearpygui.pop_container_stack()

    command : DPGCommand = _DEFAULT_COMMAND
    identity: DPGTypeId  = _DEFAULT_IDENTITY

    @px_utils.classproperty
    def is_container(cls) -> bool:
        """Return True if items of this type can contain other non-root
        items."""
        # A more accurate check would be to call `is_item_container`,
        # but the item would need to exist first.
        return issubclass(cls, ContainerItem)

    @px_utils.classproperty
    def is_root_item(cls) -> bool:
        """Return True if items of this type are containers, but they themselves
        cannot be parented."""
        return issubclass(cls, RootItem)

    @px_utils.classproperty
    def is_value_able(cls) -> bool:
        """Return True if items of this type have a writable value."""
        return issubclass(cls, ValueAbleItem)

    @px_utils.classproperty
    def is_plot_item(cls) -> bool:
        """Return True if items of this type are included in Dear PyGui's plotting API."""
        identity = cls.identity[1]
        return any(s in identity for s in ("Plot", "mvAnnotation"))

    @px_utils.classproperty
    def is_node_item(cls) -> bool:
        """Return True if items of this type are included in Dear PyGui's node API."""
        return "Node" in cls.identity[1]

    @px_utils.classproperty
    def is_table_item(cls) -> bool:
        """Return True if items of this type are included in Dear PyGui's table API."""
        return "mvTable" in cls.identity[1]

    @px_utils.classproperty
    def is_draw_item(cls) -> bool:
        """Return True if items of this type are included in Dear PyGui's drawing API."""
        return "mvDraw" in cls.identity[1]

    @px_utils.classproperty
    def target_slot(cls) -> int:  # XXX `target` would conflict with some items
        """Return the index of the slot that items of this type are stored in when parented.

        For more information regarding the slot system;
        <https://dearpygui.readthedocs.io/en/latest/documentation/container-slots.html#slots>
        """
        str_id = cls.identity[1].split("mvAppItemType::")
        if str_id in ("mvFileExtension", "mvFontRangeHint", "mvNodeLink",
        "mvAnnotation", "mvDragLine", "mvDragPoint", "mvLegend", "mvTableColumn"):
            return 0
        elif cls.is_draw_item:
            return 2
        elif str_id == "mvDragPayload":
            return 3
        return 1  # dearpygui.get_item_info(...) includes this even for root items

    @classmethod
    def wrap_item(cls, item: ItemId, *, null_init: bool = True) -> 'AppItemType':
        """Return an AppItemType interface for an existing item based on its' internal
        type.

        Args:
            * item: The unique identifier of the item to interface with.

            The following arguments are optional and keyword-only:

            * null_init: If True, the interface's `__init__` method will not be called
            during its creation. Default is True.

        If *null_init* is True, the returned interface will be created by calling the
        appropriate interface's `__new__` method and NOT through the traditional
        `type(class).__call__` invocation. See the `null_init` class method for more
        information.
        """
        # XXX good monkeypatch point (see `alias` property, `register_itemtype` fn)
        itp = _ITEMTYPE_REGISTRY.get(get_info(item)["type"].split("::")[1], AppItemType)
        call_obj = itp.null_init if null_init else itp
        return call_obj(tag=item)

    @classmethod
    def null_init(cls, *args: P.args, **kwargs: P.kwargs) -> Self:
        """Return a new instance of this class. The instance is not initialized.

        The new instance returned by this method is created by directly calling the
        class' `__new__` method (using *args* and *kwargs*) without ever calling
        `__init__`, and NOT through the traditional `type(class).__call__` invocation.

        It is not necessary to hook through this method to create an interface for an
        existing item, since the default `__init__` implementation will handle the
        resulting exception. This IS the more performant option though -- especially
        when creating interfaces for several existing items.
        """
        return cls.__new__(cls, *args, **kwargs)



class AppItemType(_AppItemBase, Generic[P]):
    """Generic object-oriented interface for existing Dear PyGui items.

    >>> import dearpygui.dearpygui as dpg
    >>>
    >>> wndw_id = dpg.add_window()
    >>> wndw = AppItemType(tag=wndw_id)
    >>> isinstance(wndw, AppItemType)
    True
    >>> wndw == wndw_id
    True
    >>> dpg.configure_item(wndw, width=500)
    None
    """

    @property
    def tag(self) -> int:
        """[get] Return the item's unique integer identifier."""
        return self.real

    @property
    def alias(self) -> str | None:
        """[get] Return the item's unique string identifier."""
        return dearpygui.get_item_alias(self)
    @alias.setter
    def alias(self, value: str | None) -> None:
        """[set] Set a unique string identifier for the item."""
        return dearpygui.set_item_alias(value)

    def delete(self, children_only: bool = False, slot: Literal[-1, 0, 1, 2, 3] = -1) -> None:
        """Destroy this item and/or this item's children. Comparable to Dear PyGui's
        `delete_item` function.

        Args:
            * children_only: If True, only this item's children are destroyed, and
            only those in *slot*. Default is False.

            * slot: If *children_only* is True, items in this slot are destroyed.
            Default is -1 (all slots).

        `SystemError` is raised in all cases where this call to Dear PyGui fails.
        """
        _dearpygui.delete_item(self, children_only=children_only, slot=slot)

    def destroy(self) -> None:
        """Destroy this item and the item's children.

        Functionally equivelent to calling `.delete(children_only=False)` while
        ignoring all errors.
        """
        try:
            self.delete(children_only=False)
        except:
            pass

    label             : Config[str | None , str] = Config()
    user_data         : Config[Any, Any]         = Config()
    use_internal_label: Config[bool, bool]       = Config()

    @overload
    def configure(self, *, label: str = ..., user_data: Any = ..., use_internal_label: bool = ..., **kwargs) -> None: ...
    def configure(self, **kwargs) -> None:
        """Update the item's writable settings. Comparable to Dear PyGui's
        `configure_item` function.

        Args:
            * label: Display name for the item.

            * user_data: Any object. Uses are user-implemented.

            * use_internal_label: If True, '##self.tag' is appended to *label*. This
            change is hidden where *label* would be displayed in the user interface.

            Other keyword-only arguments vary between items.

        The available configuration options for an item are not always obvious. Many
        keyword arguments used by the item type's constructor/initializer are writable.
        Common keyword arguments such as `parent` and `tag`, cannot be updated this
        way. Note that arguments prefixed with "default" are tied to the item's stored
        value, and can be updated using the `.set_value` method or `.value` property.

        `TypeError` is raised if this item exists and its configuration could not be
        updated or if the configuration option is not writable. `SystemError` is
        raised in all other cases where this call to Dear PyGui fails.
        """
        try:
            set_config(self, **kwargs)
        except SystemError:
            if _dearpygui.does_item_exist(self):
                raise TypeError(
                    f"`{type(self).__qualname__}(tag={self.real!r}).configure(...)` received an unexpected keyword argument."
                ) from None
            for kwd in kwargs:
                if kwd in self.command.__annotations__:
                    raise TypeError(f"cannot set read-only attribute {kwd!r}.")
            raise

    def configuration(self) -> DPGItemConfig:
        """Return the item's various settings. Comparable to Dear PyGui's
        `get_item_configuration` function.

        If the interface is generic (i.e. direct instance of `AppItemType`), calling
        this method is equivelent to calling `get_item_configuration(self)`. Otherwise,
        the returned dictionary is filtered to only include settings that are applicable
        to the item.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.
        """
        # NOTE: This is only for instances where `type(self) == AppItemType`. Derived
        # itemtypes have a different `configuration` method (assigned via metaclass).
        return get_config(self)

    parent: Info[ItemId] = Info()

    def information(self) -> DPGItemInfo:
        """Return item details that are read-only or are updated infrequently. Comparable
        to Dear PyGui's `get_item_info` function.

        The returned dictionary includes the 'handlers' key as of Dear PyGui v1.9.0.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.
        """
        return get_info(self)

    is_ok                    : State[bool       ]            = State(key="ok")
    is_hovered               : State[bool | None]            = State(key="hovered")
    is_active                : State[bool | None]            = State(key="active")
    is_focused               : State[bool | None]            = State(key="focused")
    is_clicked               : State[bool | None]            = State(key="clicked")
    is_left_clicked          : State[bool | None]            = State(key="left_clicked")
    is_right_clicked         : State[bool | None]            = State(key="right_clicked")
    is_middle_clicked        : State[bool | None]            = State(key="middle_clicked")
    is_visible               : State[bool | None]            = State(key="visible")
    is_edited                : State[bool | None]            = State(key="edited")
    is_activated             : State[bool | None]            = State(key="activated")
    is_deactivated           : State[bool | None]            = State(key="deactivated")
    is_deactivated_after_edit: State[bool | None]            = State(key="deactivated_after_edit")
    is_resized               : State[bool | None]            = State(key="resized")
    rect_min                 : State[Array[int, int] | None] = State()
    rect_max                 : State[Array[int, int] | None] = State()
    rect_size                : State[Array[int, int] | None] = State()
    content_region_avail     : State[Array[int, int] | None] = State()

    def state(self) -> DPGItemState:
        """Return the item's status. Comparable to Dear PyGui's `get_item_state`
        function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.


        Unlike Dear PyGui's `get_item_state` function, this method will include
        every state possible, even those that are not supported for the item. Unsupported
        states have a value of `None` in the returned dictionary.
        """
        return get_state(self)

    @overload
    def children(self) -> dict[Literal[0, 1, 2, 3], list[ItemId]]: ...
    @overload
    def children(self, slot: Literal[0, 1, 2, 3]) -> list[ItemId]: ...
    def children(self, slot: Literal[-1, 0, 1, 2, 3] = -1) -> dict[Literal[0, 1, 2, 3], list[ItemId]] | list[ItemId]:
        """Return one or all slots containing the item's children. Comparable to
        Dear PyGui's `get_item_children` function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.

        Args:
            * slot: The slot to return. Default is -1 (all slots).


        """
        # if the item isn't a container everything will be empty
        return dearpygui.get_item_children(self, slot)

    def move(self, parent: ItemId = 0, before: ItemId = 0) -> None:
        """Move this non-root item to another container item and/or before another
        item. Comparable to Dear PyGui's `move_item` function.

        `TypeError` is raised if this item is a root item. `SystemError` is raised
        in all other cases where this call to Dear PyGui fails.

        Args:
            * parent: The unique identifier of the container item that will serve as
            this item's parent. A value of 0 specifies the item's current parent.
            Default is 0.

            * before: The unique identifier of an item parented by *parent*. This item
            will be inserted before it in the same slot. A value of 0 will add the item
            to *parent* normally, without inserting before any other items. Default is
            0.
        """
        _dearpygui.move_item(self, parent=parent, before=before)

    def move_up(self) -> None:
        """In the slot that contains this item, swap the positions of this non-root
        item and the item that preceeds it. Comparable to Dear PyGui's `move_item_up`
        function.

        `TypeError` is raised if this item is a root item. `SystemError` is raised
        in all other cases where this call to Dear PyGui fails.
        """
        _dearpygui.move_item_up(self)

    def move_down(self) -> None:
        """In the slot that contains this item, swap the positions of this non-root
        item and the item that follows it. Comparable to Dear PyGui's `move_item_down`
        function.

        `TypeError` is raised if this item is a root item. `SystemError` is raised
        in all other cases where this call to Dear PyGui fails.
        """
        _dearpygui.move_item_down(self)

    def unstage(self) -> None:
        """Move this non-root item from the stage container item parenting it to the
        item atop the container stack. Comparable to Dear PyGui's `unstage` function.

        `TypeError` is raised if this item is a root item. `SystemError` is raised if
        this item is not parented by a stage container, and in all other cases where
        this call fails.
        """
        _dearpygui.unstage(self)

    def reorder(self, slot: Literal[0, 1, 2, 3], new_order: Sequence[ItemId]) -> None:
        """Rearrange the item's children within a chosen slot. Comparable to Dear
        PyGui's `reorder_items` function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.

        Args:
            * slot: Index of the target slot.

            * new_order: The new order of the item's children. The sequence
            must contain the identifiers of **all** items in the target slot.
        """
        _dearpygui.reorder_items(self, slot, new_order)

    def focus(self) -> None:
        """Bring this item to the foreground and set it as 'active' (if able).
        Comparable to Dear PyGui's `focus_item` function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.
        """
        _dearpygui.focus_item(self)

    @property
    def value(self) -> Any:
        """Return the item's stored value."""
        return self.get_value()
    @value.setter
    def value(self, value: Any) -> None:
        self.set_value(value)

    def get_value(self) -> Any:
        """Return the item's value. Comparable to Dear PyGui's `get_value`
        function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.


        This method will return `None` if the item's value has not or cannot be
        set.
        """
        return get_value(self)

    def set_value(self, value: Any) -> None:
        """Update the item's stored value. Comparable to Dear PyGui's `set_value`
        function.

        `SystemError` is raised if the value's type is not appropriate for the
        item, and in all other cases where this call to Dear PyGui fails.

        Args:
            * value: The new value to apply to the item. The type of *value*
            varies between items. Does not raise an error if the item cannot
            hold a value.


        Does nothing if the item cannot store a value.
        """
        set_value(self, value)

    @property
    def theme(self) -> ItemId | None:
        """[get] Return the theme set onto the item."""
        return self.get_theme()
    @theme.setter
    def theme(self, value: ItemId | None) -> None:
        """[set] Set the reflected theme item."""
        return self.set_theme(value)

    def get_theme(self) -> ItemId | None:
        """Return the theme set onto the item. Comparable to Dear PyGui's
        `get_item_theme' function..

        `SystemError` is raised in all cases where this call to Dear PyGui fails.
        """
        return self.information()["theme"]

    def set_theme(self, theme: ItemId | None = 0) -> None:
        """Set a theme for the item to use. Comparable to Dear PyGui's `bind_item_theme'
        function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.

        Args:
            * theme: A theme item's unique identifier. If this value is 0 or `None`,
            the item is unbound from the set theme (if any). Default is 0.


        Themes propagate downward, affecting item children. Items reflect elements
        of their explicity set theme over those propagated from a parenting item
        or application-level theme.
        """
        _dearpygui.bind_item_theme(self, theme)

    @property
    def handlers(self) -> ItemId | None:
        """[get] Return the handler registry used by the item."""
        return self.get_handlers()
    @handlers.setter
    def handlers(self, value: ItemId | None) -> None:
        """[set] Set an item handler registry for the item to use."""
        return self.set_handlers(value)

    def get_handlers(self) -> ItemId | None:
        """Return the item handler registry used by the item.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.


        As of Dear PyGui v1.9.0, this method is now comparable to
        `get_item_info(...)["handlers"].
        """
        return self.information().get("handlers", None)

    def set_handlers(self, handler_registry: ItemId | None = 0) -> None:
        """Bind this item to a item handler registry item. Comparable to Dear PyGui's
        `bind_item_handler_registry' function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.

        Args:
            * handler_registry: A item handler registry item's unique identifier. If
            this value is 0 or `None`, the item is unbound from the set registry.
            Default is 0.
        """
        _dearpygui.bind_item_handler_registry(self, handler_registry)

    @property
    def font(self) -> ItemId | None:
        return self.get_font()
    @font.setter
    def font(self, value: ItemId) -> None:
        self.set_font(value)

    def get_font(self) -> ItemId | None:
        """Return the item's bound font item. Comparable to Dear PyGui's `get_item_font`
        function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.
        """
        return self.information()["font"]

    def set_font(self, font: ItemId = 0) -> None:
        """Bind this item to a font item. Comparable to Dear PyGui's `bind_item_font`
        function.

        `SystemError` is raised in all cases where this call to Dear PyGui fails.

        Args:
            * font: A font item's unique identifier. Default is 0 (unbind this
            item from the currently bound font item if applicable).
        """
        _dearpygui.bind_item_font(self, font)

    @property
    def root_parent(self) -> ItemId:
        """[get] Return the identifier of the top-most container item in this item's
        parential tree."""
        return self.get_root_parent()

    def get_root_parent(self) -> ItemId:
        """Return the identifier of the top-most container item in this item's
        parential tree."""
        return px_utils.get_root_parent(self)




class AppItemLike:
    """Minimal item API for non-item interfaces."""
    __slots__ = ()

    command : DPGCommand = _null_command
    identity: DPGTypeId  = 0, ""

    def __repr__(self):
        config = ', '.join(f"{k}={str(v)!r}" for k, v in self.configuration().items())
        return f"{type(self).__qualname__}({config})"

    def __getattr__(self, name: str):
        try:
            return self.configuration()[name]
        except KeyError:
             raise AttributeError(
                f"{type(self).__qualname__!r} object has no attribute {name!r}."
            ) from None

    # Config, information, or state-related property getters should pull from
    # the relating method's returned dictionary to make extending easier. Config
    # setters should pass through to the `.configure` method. If the result needs
    # to be transformed,`.configure` should be doing it and not the setter.

    def configure(self, **kwargs) -> None:
        ...

    def configuration(self) -> dict[str, Any]:
        return {}

    def information(self) -> dict[str, Any]:
        return {}

    def state(self) -> dict[str, bool | None]:
        return {}




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
############################ Primitive Item Types (Mixins) ############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class PositionedItem(AppItemType):
    """A rendered Dear PyGui item that can have a set position."""
    @property
    def pos(self) -> Array[int, int]:
        return self.state()["pos"]
    @pos.setter
    def pos(self, value: Array[int, int]) -> None:
        self.configure(pos=value)


class SizedItem(PositionedItem):
    """A rendered Dear PyGui item with a bounding box. Can be resized."""

    # Every item with `pos` has sizing support. However, they are not
    # always configured through the `width` and `height` keywords. This
    # covers the common case.

    width : Config[int, int] = Config()
    height: Config[int, int] = Config()

    # Some items like `mvWindowAppItem` only support `rect_size`. The min/max
    # for these can be easily calculated.

    @property
    def rect_min(self) -> Array[int, int]:
        state = self.state()
        try:
            return state["rect_min"]
        except KeyError:
            return state["pos"]

    @property
    def rect_max(self) -> Array[int, int]:
        state = self.state()
        try:
            return state["rect_max"]
        except KeyError:
            config = self.configuration()
            x, y = state["pos"]
            return x + config["width"], y + config["height"]




class ValueAbleItem(AppItemType):
    """A Dear PyGui item that can store a value."""


class ValueArrayItem(ValueAbleItem, Generic[T]):
    """A Dear PyGui item that stores an array of values."""

    def __str__(self):
        return self.get_value()

    def __add__(self, other: Any) -> Self:
        self.set_value(self.get_value().__add__(other))
        return self

    def __iadd__(self, other: Any) -> Self:
        self.set_value(self.get_value().__iadd__(other))
        return self

    def __mul__(self, other: Any) -> Self:
        self.set_value(self.get_value().__mul__(other))
        return self

    def __imul__(self, other: Any) -> Self:
        self.set_value(self.get_value().__imul__(other))
        return self

    def __setitem__(self, index: int, value: T) -> None:
        item_value = self.get_value()
        item_value.__setitem__(index, value)
        self.set_value(item_value)

    @px_utils.forward_method("get_value", call=True)
    def __getitem__(self, index: int) -> T: ...
    @px_utils.forward_method("get_value", call=True)
    def __delitem__(self, index: int): ...
    @px_utils.forward_method("get_value", call=True)
    def __contains__(self, value: T): ...
    @px_utils.forward_method("get_value", call=True)
    def __reversed__(self): ...
    @px_utils.forward_method("get_value", call=True)
    def __str__(self): ...
    @px_utils.forward_method("get_value", call=True)
    def __len__(self): ...
    @px_utils.forward_method("get_value", call=True)
    def __iter__(self): ...
    @px_utils.forward_method("get_value", call=True)
    def __bool__(self): ...
    @px_utils.forward_method("get_value", call=True)
    def __lt__(self, other: Any): ...
    @px_utils.forward_method("get_value", call=True)
    def __le__(self, other: Any): ...
    @px_utils.forward_method("get_value", call=True)
    def __gt__(self, other: Any): ...
    @px_utils.forward_method("get_value", call=True)
    def __ge__(self, other: Any): ...
    @px_utils.forward_method("get_value", call=True)
    def __eq__(self, other: Any): ...
    @px_utils.forward_method("get_value", call=True)
    def count(self, value: Any) -> int: ...
    @px_utils.forward_method("get_value", call=True)
    def index(self, value: T, start: int = 0, stop: int = None) -> int: ...

    def append(self, value: T) -> None:
        """Add *value* to the end of this item's values."""
        item_value = self.get_value()
        item_value.append(value)
        self.set_value(item_value)

    def extend(self, iterable: Sequence[T]) -> None:
        """Append values in *iterable* to this item's values."""
        item_value = self.get_value()
        item_value.extend(iterable)
        self.set_value(item_value)

    def pop(self, index: int = -1) -> T:
        """Remove and return the last value at *index*."""
        item_value = self.get_value()
        value = item_value.pop(index)
        self.set_value(item_value)
        return value

    def insert(self, index: int, value: T):
        """Insert *value* before *index*."""
        item_value = self.get_value()
        item_value.insert(index, value)
        self.set_value(item_value)

    def remove(self, value: T):
        """Remove the first occurance of *value*."""
        item_value = self.get_value()
        item_value.remove(value)
        self.set_value(item_value)

    def sort(self, *, key: Callable[[T], Any] = None, reverse: bool = False) -> None:
        """Sort values in-place."""
        item_value = self.get_value()
        item_value.sort(key=key, reverse=reverse)
        self.set_value(item_value)

    def reverse(self) -> None:
        """Reverse item values in-place."""
        self.set_value(self.get_value()[::-1])

    def get_value(self) -> list[T]:
        return get_value(self)




class CallableItem(AppItemType):
    """A Dear PyGui item that supports an optional callback, which can be invoked
    by calling the item. The item can also be passed as a callback-related
    argument for other items."""

    show: Config[bool, bool] = Config()

    @property
    def callback(self) -> DPGCallback[P] | None:
        """[get] Return the item's assigned callback."""
        return self.configuration()["callback"]
    @callback.setter
    def callback(self, value: DPGCallback[P] | None) -> DPGCallback[P] | None:
        """[set] Set the item's callback. Can be used as a decorator."""
        self.configure(callback=value)
        return value

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        self.callback(*args, *kwargs)

    __code__ = __call__.__code__


class HandlerItem(CallableItem):
    """A Dear PyGui item that fires a callback on certain events."""




class ContainerItem(AppItemType):
    """A Dear PyGui item that can contain other items."""

    def __enter__(self) -> Self:
        self.push_stack()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.pop_stack()

    def push_stack(self) -> None:
        _dearpygui.push_container_stack(self)

    def pop_stack(self) -> bool:
        if _dearpygui.top_container_stack() == self:
            _dearpygui.pop_container_stack()
            return True
        return False


class WindowItem(ContainerItem):  # AFAIK "mvWindowAppItem" and "mvChildWindow" only
    """A Dear PyGui container item that supports scrolling on both axis."""

    x_scroll_max: float = property(
        lambda self:_dearpygui.get_x_scroll_max(self),
        doc="Return the end horizontal scroll position."
    )
    x_scroll_pos: float = property(
        lambda self:_dearpygui.get_x_scroll(self),
        lambda self, value: _dearpygui.set_x_scroll(self, value),
        doc="Get/set the horizontal scroll position of the item."
    )
    y_scroll_max: float = property(
        lambda self:_dearpygui.get_y_scroll_max(self),
        doc="Return the end vertical scroll position."
    )
    y_scroll_pos: float = property(
        lambda self:_dearpygui.get_y_scroll(self),
        lambda self, value: _dearpygui.set_y_scroll(self, value),
        doc="Get/set the vertical scroll position of the item."
    )

    @property
    def is_active_window(self) -> bool:
        """[get] Return True if this window or any of its' children are focused."""
        return self.tag == _dearpygui.get_active_window()



class RootItem(ContainerItem):
    """A top-level Dear PyGui container item. It cannot be parented."""

    def move(self, *args, **kwargs) -> TypeError:
        raise TypeError(f"{type(self).__qualname__} item cannot be moved.")

    move_up   = move
    move_down = move
    unstage   = move


class RegistryItem(RootItem):
    """A top-level Dear PyGui container item. It cannot be parented, and
    it (and its child items) are not typically rendered."""




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
############################## Non-Primitive Item Mixins ##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# XXX These are unique mixins that can make the resulting class or instances
# a bit weird and/or do unusual things. Not used in `itp_from_callable`

class PatchedItem(AppItemType):  # "do not import" indicator for genfile.py script
    ...




def _px_dndr_wrapper(mthd: Callable[P, ItemId]) -> Callable[P, AppItemType | ItemId]:
    @functools.wraps(mthd)
    def bound_method(self, *args: P.args, **kwargs: P.kwargs) -> AppItemType | ItemId:
        item = mthd(self, *args, **kwargs)
        return self.wrap_item(item)
    return bound_method


def _callback_getter(self: CallableItem) -> DPGCallback[P]:
    return self.configuration()["callback"]


def _callback_setter(self: CallableItem, value: DPGCallback[P] | None) -> None:
    if value is None:
        self.configure(callback=None)
        return

    arg_count = value.__code__.co_argcount
    if getattr(value, "__self__"):
        arg_count -= 1
    if not arg_count:
        self.configure(callback=value)
        return value

    @functools.wraps(value)
    def callback(sender: ItemId = None, app_data: Any = None, user_data: Any = None) -> None:
        if sender:
            sender = self.wrap_item(sender, null_init=True)
        value(*(sender, app_data, user_data)[:arg_count])
    return callback


class pxConfig(Config):
    __slots__ = ()

    PX_FLAG = True

    def __get__(self, inst, cls):
        result = super().__get__(inst, cls)
        if result is None:
            return self
        return inst.wrap_item(result)


class PixlatedItem(PatchedItem, Generic[P]):
    """AppItemType mixin that extends higher-level information-related methods and
    properties to return `AppItemType` instances where an item identifier would be
    returned.
    """
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        # wrap individually accessed children
        if cls.__getitem__ is AppItemType.__getitem__:
            setattr(cls, "__getitem__", _px_dndr_wrapper(cls.__getitem__))
        # wrap callback `sender` args for CallableItem
        if getattr(cls, "callback", None) is CallableItem.callback:
            cb_property = property(_callback_getter, _callback_setter)
            setattr(cls, "callback", cb_property)
        # wrap items individually returned from Config descriptor
        for param in inspect.signature(cls.configure).parameters.values():
            if param.annotation != ItemId:
                continue
            cfg_property = getattr(cls, param.name, None)
            if isinstance(cfg_property, Config) and not hasattr(cfg_property, "PX_FLAG"):
                pxcfg_property = pxConfig(cfg_property._key)
                setattr(cls, param.name, pxcfg_property)
                pxcfg_property.__set_name__(cls, cfg_property._key)

    @property
    def parent(self) -> ContainerItem | SizedItem | None:
        p_item = self.information()["parent"]
        return self.wrap_item(p_item) if p_item else None

    def get_font(self) -> ContainerItem | None:
        font = super().get_font()
        return self.wrap_item(font) if font else None

    def get_handlers(self) -> RegistryItem | None:
        hreg = super().get_handlers()
        return self.wrap_item(hreg) if hreg else None

    def get_theme(self) -> RegistryItem | None:
        theme = super().get_theme()
        return self.wrap_item(theme) if theme else None

    def get_root_parent(self) -> RootItem:
        root = super().get_root_parent()
        return self.wrap_item(root) if root else None





def _init_wrapper(mthd: Callable[P, T], *_args: P.args, **_kwargs: P.kwargs) -> Callable[[], T]:
    @functools.wraps(mthd)
    def init(*args: P.args, **kwargs: P.kwargs) -> T:
        mthd(*(args or _args), **(_kwargs | kwargs))
        mthd.__self__.__init__ = mthd
    return init


class _NullInitItemMeta(AppItemMeta):
    def __call__(cls, *args, **kwargs):
        return cls.__new__(cls, *args, **kwargs)


class NullInitItem(PatchedItem, Generic[P], metaclass=_NullInitItemMeta):
    """`AppItemType` mixin that disables auto initialization for new instances. The
    `.__init__` method must be called manually or through other means as defined by
    the user.

    When calling the `.__init__` method, it will automatically receive any arguments
    it would have received under normal circumstances. If keyword arguments are sent
    to the `.__init__` method, they will be merged into the keyword arguments used
    when the instance was created. If positional arguments are included, only those
    positional arguments will be used and NOT the positional arguments originally
    passed on instantiation (to `.__new__`).

    NOTE: Attempting to call instance methods before calling the `.__init__` method
    may result in an error because the Dear PyGui item may not exist yet. Class-bound
    descriptors will function as normal.
    """
    def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> Self:
        self = super().__new__(*args, **kwargs)
        self.__init__ = _init_wrapper(self.__init__, *args, **kwargs)
        return self




def _get_non_template_type(obj: type) -> type:
    for t in obj.mro():
        if not issubclass(t, PatchedItem):
            return t


class _TemplateItemMeta(Generic[P], AppItemMeta):
    def __new__(mcls, name: str, bases: tuple, namespace: dict[str], *args: P.args, **kwargs: P.kwargs):
        kwargs["__slots__"] = ()
        cls = super().__new__(mcls, name, bases, namespace,)
        cls.__init__    = None
        cls.__setattr__ = None
        cls.__type      = _get_non_template_type(cls)
        cls.__args      = args
        cls.__kwargs    = kwargs
        return cls

    def __call__(cls, *args: P.args, **kwargs: P.kwargs) -> Self:
        return cls._type(*(args or cls._args), **(cls._kwargs | kwargs))

    def template_type(cls, *args: P.args, **kwargs: P.kwargs):
        return cls.__type.template_type(*args, **kwargs)


class TemplateItem(PatchedItem, Generic[P], metaclass=_TemplateItemMeta):
    """An `AppItemType` mixin that turns the class into a superclass
    factory with pre-bound arguments of the user's choosing.
    """
    def __new__(cls, *args: P.args, **kwargs: P.kwargs) -> type[Self]:
        return cls




class _AutoParentItemMeta(AppItemMeta):
    def __new__(mcls, name, bases, namespace, auto_parent: DPGCommand = None, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        if auto_parent:=namespace.get("auto_parent", auto_parent):
            if cls.is_root_item:
                raise TypeError("cannot mix `AutoParentItem` with a root item type.")
            cls.auto_parent = staticmethod(auto_parent)
        return cls


class AutoParentItem(PatchedItem, Generic[P], metaclass=_AutoParentItemMeta):
    """An AppItemType mixin that creates a parent item for itself if one
    is not available and the container stack is empty.

    This does not check for a *compatible* parent. It will only trigger as
    a last resort -- the container stack must be empty and `parent` cannot
    be included as an argument.
    """

    auto_parent: DPGCommand = staticmethod(lambda self: 0)

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        if not kwargs.get("parent", None) and not _dearpygui.top_container_stack():
            kwargs["parent"] = self.auto_parent(label=kwargs.get("label", ""))
        super().__init__(*args, **kwargs)




###########################################
########### ITEMTYPE GENERATION ###########
###########################################

_ITEM_TO_CONST = {
    # inferred_item_name   : dpg_constant_name         -> logical_output           (the_problem)
    "2d_histogram_series"  : "mv2dHistogramSeries",  # -> "mv3DHistogramSeries"    ("d" needs to be lowercase)
    "3d_slider"            : "mvSlider3D",           # -> "mv3DSlider"             (uniquely named)
    "hline_series"         : "mvHLineSeries",        # -> "mvHlineSeries"          ("l" needs to be uppercase)
    "vline_series"         : "mvVLineSeries",        # -> "mvVlineSeries"          ("l" needs to be uppercase)
    "plot_annotation"      : "mvAnnotation",         # -> "mvPlotAnnotation"       (remove "Plot")
    "subplots"             : "mvSubPlots",           # -> "mvSubplots"             ("p" needs to be uppercase)
    "text_point"           : "mvLabelSeries",        # -> "mvTextPoint"            (completely different name)
    "draw_rectangle"       : "mvDrawRect",           # -> "mvDrawRectangle"        (drop "angle")
    "draw_image_quad"      : "mvDrawQuad",           # -> "mvDrawImageQuad"        (drop "image")
    "draw_bezier_quadratic": "mvDrawBezierQuad"      # -> "mvDrawBezierQuadratic"  (drop "ratic")
}

def itp_from_callable(command: DPGCommand[P, ItemId]) -> type[AppItemType[P]]:
    """Create and return a new AppItemType from a Dear PyGui item-creating
    function.

    Args:
        * command: A function object that return or yield an item identifier.
        All functions that create items in the `dearpygui.dearpygui` namespace
        are supported (except `popup`).

    Details from both the function and `dearpygui.dearpygui` module are used
    to help create the class. For example, its name will mirror the item's
    internal Dear PyGui type name:
    >>> # import dearpygui.dearpygui as dearpygui
    ...
    >>> Window = type_from_callable(dearpygui.window)  # or `dearpygui.add_window`
    >>> repr(Window)
    <class 'mvWindowAppItem'>

    Type information is exposed via the `.identity` class property -- as a
    2-tuple containing the type's internal enumeration value, and string
    representation as returned by `dearpygui.get_item_info(...)['type']`.
    >>> Window.identity
    (33, 'mvAppItemType::mvWindowAppItem')
    >>> Window.identity[0] == dearpygui.mvWindowAppItem
    True
    >>> dpg_wndw = dearpygui.add_window()
    >>> Window.identity[1] == dearpygui.get_item_info(dpg_wndw)['type']
    True

    Depending on the information inferred from the function and module, mixin
    classes may be included in the new class' bases. The logic is smart enough
    to, for example, include `RootItem` as a mixin for items that cannot be
    parented. This may change the result of other class properties such as
    `.is_root_item`.
    >>> Window.is_root_item  # issubclass(Window, RootItem)
    True
    >>> Window.is_container  # issubclass(Window, ContainerItem)
    True
    >>> ChildWindow = type_from_callable(dearpygui.child_window)
    >>> ChildWindow.is_root_item, ChildWindow.is_container
    (False, True)
    >>> Button = type_from_callable(dearpygui.add_button)
    >>> Button.is_root_item, Button.is_container
    (False, False)

    Mixins may extend (or limit) the available interface for the new class.
    Since `Window` is a derived `RootItem`, methods that would manage the item's
    parent will now raise a `TypeError` instead of the ambiguous `SystemError`
    thrown by Dear PyGui.

    The logic that includes mixin base classes is kept minimal, and can't
    account for every possibility. Typing information on the returned class is
    generalized and will be lost when subclassing (ex.
    `class Window(type_from_callable(dearpygui.window)): ...`). For better typing
    introspection and a more "accurate" class, it is best to statically define
    the class in its entirety using the mixin classes exposed in this module
    (ex. `class Window(RootItem, AppItemType): ...`).
    """

    try:
        cmd_name = command.__qualname__
    except:
        raise TypeError("`command` argument is not valid.")
    if not px_utils.is_item_cmd(command):
        raise TypeError(f"Invalid `command` argument {cmd_name!r}.")
    if cmd_name == "popup":
        raise ValueError("Invalid `command` argument `popup` (use `window`, `add_window`).")

    is_container = False
    if px_utils.is_ctxmgr_fn(command):  # is "container command" -- get the basic function
        _name1 = f"add_{cmd_name}"
        _name2 = f"draw_{cmd_name}"
        try:
            command = getattr(dearpygui, _name1, None) or getattr(dearpygui, _name2)
        except AttributeError:
            raise ValueError(
                f"Unable to get basic item command of context manager function {cmd_name!r}."
            ) from None
        is_container = True
    else:  # is basic function -- add container support if container command exists
        _name = cmd_name
        # chaining `.removeprefix(...)` could remove more than intended
        if cmd_name.startswith("draw_"):
            _name = cmd_name.removeprefix("draw_")
        elif cmd_name.startswith("add_"):
            _name = cmd_name.removeprefix("add_")
        try:
            getattr(dearpygui, _name)
        except AttributeError:
            pass
        else:
            is_container = True

    # ******************* #
    # * BUILD ITP CNAME * #
    # ******************* #

    item_name = cmd_name.removeprefix("add_")
    # DPG constants are cases as "mvColorMap" -- correct casing issue
    if item_name.startswith("colormap"):
        item_name = item_name.replace("colormap", "color_map", 1)
    # A SyntaxError could potentially be thrown IF the class were to be statically created
    # i.e. `add_3d_slider` -> "3dSlider", `add_2d_histogram` -> "2dHistogram", etc. So the
    # 'mv' (Marvel) prefix is added.
    basename = f'mv{item_name.title().replace("_", "")}'
    if basename == "mvWindow":  # sole exception to the typical function naming convention
        basename = "mvWindowAppItem"
    try:
        # item.identity[0] == dearpygui.mvConstant
        # item.identity[1] == dearpygui.get_item_info(item)["type"]
        getattr(dearpygui, basename)
    except AttributeError:
        # refer to the "this shit is weird" map
        if item_name in _ITEM_TO_CONST:
            basename = _ITEM_TO_CONST[item_name]
        # item handler?
        elif all(s in item_name for s in ("item_", "_handler")):
            basename = basename.replace("Item", "", 1)
        # x4 input item?
        elif item_name[-1] == "x":
            basename = f"{basename[:-1]}Multi"
        # panik
        else:
            raise
    identity = getattr(dearpygui, basename), f"mvAppItemType::{basename}"

    cmd_sig    = inspect.signature(command).replace(return_annotation=None)
    cmd_params = cmd_sig.parameters
    item_bases = [AppItemType,]

    # ******************* #
    # * BUILD ITP BASES * #
    # ******************* #

    # can the item support a callback?
    if "callback" in cmd_params:
        # is the non-container item a handler?
        if cmd_name.endswith("_handler") and not is_container:
            item_bases.append(HandlerItem)
        else:
            item_bases.append(CallableItem)
    # can the item store a value?
    if any(s in cmd_name for s in ("_series", "theme_color", "theme_style")):
        item_bases.append(ValueArrayItem)
    elif ("default_value" in cmd_params or any(s in cmd_name for s in ("tab_bar",))):
        item_bases.append(ValueAbleItem)
    # can the item be sized?
    if "pos" in cmd_params:
        if all(p in cmd_params for p in ("width", "height", "pos")):
            item_bases.append(SizedItem)
        else:
            item_bases.append(PositionedItem)
    # can the item parent other items?
    if is_container:
        # is the item a registry?
        if any(cmd_name.endswith(s) for s in ("_registry", "theme")):
            item_bases.append(RegistryItem)
        # can the non-registry item be parented?
        elif "parent" not in cmd_params:
            item_bases.append(RootItem)
            if basename == "mvWindowAppItem":
                item_bases.append(WindowItem)
        elif basename == "mvChildWindow":
            item_bases.append(WindowItem)
        else:
            item_bases.append(ContainerItem)

    cls: Any = type(  # type: ignore
        basename,
        tuple(item_bases[::-1]),
        # TODO: doc formatting
        {"__doc__": command.__doc__},
        command=command,
        identity=identity,
    )
    return cls
