import typing

from .._value_editor import ValueEditor

# TODO: Use PEP 747 if accepted
type TypeExpr[T] = typing.Any


class EditorBuilder:
    """Construct widgets to edit values of given types.

    Editors must be registered with the builder using the method :meth:`register_editor`
    before the method :meth:`build_editor` is called.
    """

    def __init__(self) -> None:
        self._type_editors: dict[TypeExpr, type[ValueEditor]] = {}

    def register_editor[
        T
    ](self, type_: TypeExpr[T], editor_type: type[ValueEditor[T]]) -> None:
        """Specify an editor to use when encountering a given type.

        When the method :meth:`build_editor` is called with this type, this editor
        will be used.

        Warning:
            If an editor is already registered for this type, it will be overwritten.
        """

        self._type_editors[type_] = editor_type

    def build_editor(self, type_: TypeExpr) -> type[ValueEditor]:
        """Construct a gui class to edit value of a given type.

        This method dispatches the type passed as argument to the editor registered
        for this type.

        If the type is not registered, and the type is an attrs class, an editor will
        be built for it by aggregating editors for its attributes.

        Raises:
            TypeNotRegisteredError: If no editor is registered to handle the given type,
                and it is not possible to infer an editor from the type.
        """

        try:
            return self._type_editors[type_]
        except KeyError:
            import attrs

            from ._attrs import build_editor_for_attrs_class

            if attrs.has(type_):
                return build_editor_for_attrs_class(type_, self)
            raise TypeNotRegisteredError(
                f"No editor is registered to handle {type_}"
            ) from None


class EditorBuildingError(Exception):
    pass


class TypeNotRegisteredError(EditorBuildingError):
    pass
