import strawberry
from strawberry.lazy_type import (
    LazyType as InitialLazyType,
    StrawberryLazyReference as InitialStrawberryLazyReference
)
from strawberry.utils.str_converters import to_camel_case
from dataclasses import dataclass
from typing import ForwardRef, Annotated, Type, cast
import inspect


@dataclass(frozen=True)
class LazyType(InitialLazyType):
    back_populates: str | None = None

    def resolve_type(self) -> Type:
        src_kls = super().resolve_type()
        class_name = self.create_name(kls=src_kls)
        src_kls._rel_classes = getattr(src_kls, '_rel_classes', {})
        if class_name in src_kls._rel_classes:
            return src_kls._rel_classes[class_name]
        kls = strawberry.type(
            type(
                class_name,
                (src_kls,), dict(src_kls.__dict__)
            ),
            is_input=src_kls._type_definition.is_input,
            is_interface=src_kls._type_definition.is_interface,
            description=src_kls._type_definition.description,
            directives=src_kls._type_definition.directives,
            extend=src_kls._type_definition.extend
        )
        kls.__dataclass_fields__.pop(self.back_populates)
        for field_idx in range(len(kls._type_definition._fields)):
            if kls._type_definition._fields[field_idx].name == self.back_populates:
                kls._type_definition._fields.pop(field_idx)
                break
        src_kls._rel_classes[class_name] = kls
        return kls

    def create_name(self, kls):
        return f"{kls._type_definition.name}{to_camel_case(self.back_populates.capitalize())}Rel"


class StrawberryLazyReference(InitialStrawberryLazyReference):
    def __init__(self, module, back_populates: str):
        self.back_populates = back_populates
        self.module = module
        self.package = None

        if module.startswith("."):
            frame = inspect.stack()[2][0]
            # TODO: raise a nice error if frame is None
            assert frame is not None
            self.package = cast(str, frame.f_globals["__package__"])

    def resolve_forward_ref(self, forward_ref: ForwardRef) -> LazyType:
        return LazyType(
            forward_ref.__forward_arg__,
            self.module,
            self.package,
            self.back_populates
        )


def Relationship(
        name: str,
        module_path: str,
        back_populates: str,
) -> StrawberryLazyReference:
    return Annotated[
        name,
        StrawberryLazyReference(module_path, back_populates=back_populates)
    ]