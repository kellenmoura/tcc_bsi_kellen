import logging

from gaphor import UML
from gaphor import UML3
from gaphor.core.modeling.properties import attribute
from gaphor.core.styling import (
    FontStyle,
    FontWeight,
    TextAlign,
    TextDecoration,
    VerticalAlign,
)
from gaphor.diagram.presentation import (
    Classified,
    ElementPresentation,
    from_package_str,
)
from gaphor.diagram.shapes import (
    Box,
    Text,
    draw_border,
    draw_top_separator,
)
from gaphor.diagram.shapes import Box, Text, draw_border, draw_top_separator
from gaphor.diagram.support import represents
from gaphor.UML.classes.stereotype import stereotype_compartments
from gaphor.UML.modelfactory import stereotypes_str
from gaphor.UML.umlfmt import format_property

log = logging.getLogger(__name__)


@represents(UML.Class)
@represents(UML.Stereotype)
@represents(UML3.StereotypeKind)
@represents(UML3.StereotypeSubkind)
@represents(UML3.StereotypePhase)
@represents(UML3.StereotypeRole)
@represents(UML3.StereotypeCollective)
@represents(UML3.StereotypeQuantity)
@represents(UML3.StereotypeRelator)
@represents(UML3.StereotypeCategory)
@represents(UML3.StereotypeRolemixin)
@represents(UML3.StereotypePhasemixin)
@represents(UML3.StereotypeMixin)
@represents(UML3.StereotypeMode)
@represents(UML3.StereotypeQuality)
class ClassItem(ElementPresentation[UML.Class], Classified):
    """This item visualizes a Class instance.

    A ClassItem contains two compartments: one for attributes and one for
    operations.
    """

    def __init__(self, diagram, id=None):
        super().__init__(diagram, id=id)

        self.watch("show_stereotypes", self.update_shapes).watch(
            "show_attributes", self.update_shapes
        ).watch("show_operations", self.update_shapes).watch(
            "subject[NamedElement].name"
        ).watch(
            "subject[NamedElement].namespace.name"
        ).watch(
            "subject[Classifier].isAbstract", self.update_shapes
        )
        attribute_watches(self, "Class")
        operation_watches(self, "Class")
        stereotype_watches(self)

    show_stereotypes: attribute[int] = attribute("show_stereotypes", int)

    show_attributes: attribute[int] = attribute("show_attributes", int, default=True)

    show_operations: attribute[int] = attribute("show_operations", int, default=True)

    def additional_stereotypes(self):
        #aqui foram adicionados estereótipos da ontouml
        if isinstance(self.subject, UML3.StereotypeKind):
            return ["kind"]
        elif isinstance(self.subject, UML3.StereotypeSubkind):
            return ["subkind"]
        elif isinstance(self.subject, UML3.StereotypePhase):
            return ["phase"]
        elif isinstance(self.subject, UML3.StereotypeRole):
            return ["role"]
        elif isinstance(self.subject, UML3.StereotypeCollective):
            return ["collective"]
        elif isinstance(self.subject, UML3.StereotypeQuantity):
            return ["quantity"]
        elif isinstance(self.subject, UML3.StereotypeRelator):
            return ["relator"]
        elif isinstance(self.subject, UML3.StereotypeCategory):
            return ["category"]
        elif isinstance(self.subject, UML3.StereotypeRolemixin):
            return ["rolemixin"]
        elif isinstance(self.subject, UML3.StereotypeMixin):
            return ["mixin"]
        elif isinstance(self.subject, UML3.StereotypeMode):
            return ["mode"]
        elif isinstance(self.subject, UML3.StereotypePhasemixin):
            return ["phasemixin"]
        elif isinstance(self.subject, UML3.StereotypeQuality):
            return ["quality"]
        #elif isinstance(self.subject, UML3.Material):
        #    return ["material"]
        else:
            return ()

    def update_shapes(self, event=None):
        self.shape = Box(
            Box(
                Text(
                    text=lambda: stereotypes_str(self.subject, self.additional_stereotypes()),
                ),
                Text(
                    text=lambda: self.subject.name or "",
                    style={
                        "font-weight": FontWeight.BOLD,
                        "font-style": FontStyle.ITALIC
                        if self.subject and self.subject.isAbstract
                        else FontStyle.NORMAL,
                    },
                ),
                Text(
                    text=lambda: from_package_str(self),
                    style={"font-size": "x-small"},
                ),
                style={"padding": (12, 4, 12, 4)},
            ),
            *(
                self.show_attributes
                and self.subject
                and [attributes_compartment(self.subject)]
                or []
            ),
            *(
                self.show_operations
                and self.subject
                and [operations_compartment(self.subject)]
                or []
            ),
            *(self.show_stereotypes and stereotype_compartments(self.subject) or []),
            style={
                "vertical-align": VerticalAlign.TOP,
            },
            draw=draw_border,
        )


def attribute_watches(presentation, cast):
    presentation.watch(
        f"subject[{cast}].ownedAttribute", presentation.update_shapes
    ).watch(
        f"subject[{cast}].ownedAttribute.association", presentation.update_shapes
    ).watch(
        f"subject[{cast}].ownedAttribute.name"
    ).watch(
        f"subject[{cast}].ownedAttribute.isStatic", presentation.update_shapes
    ).watch(
        f"subject[{cast}].ownedAttribute.isDerived"
    ).watch(
        f"subject[{cast}].ownedAttribute.visibility"
    ).watch(
        f"subject[{cast}].ownedAttribute.lowerValue"
    ).watch(
        f"subject[{cast}].ownedAttribute.upperValue"
    ).watch(
        f"subject[{cast}].ownedAttribute.defaultValue"
    ).watch(
        f"subject[{cast}].ownedAttribute.type"
    ).watch(
        f"subject[{cast}].ownedAttribute.typeValue"
    )


def operation_watches(presentation, cast):
    presentation.watch(
        f"subject[{cast}].ownedOperation", presentation.update_shapes
    ).watch(f"subject[{cast}].ownedOperation.name").watch(
        f"subject[{cast}].ownedOperation.isAbstract", presentation.update_shapes
    ).watch(
        f"subject[{cast}].ownedOperation.isStatic", presentation.update_shapes
    ).watch(
        f"subject[{cast}].ownedOperation.visibility"
    ).watch(
        f"subject[{cast}].ownedOperation.ownedParameter.lowerValue"
    ).watch(
        f"subject[{cast}].ownedOperation.ownedParameter.upperValue"
    ).watch(
        f"subject[{cast}].ownedOperation.ownedParameter.typeValue"
    ).watch(
        f"subject[{cast}].ownedOperation.ownedParameter.defaultValue"
    )
    

def stereotype_watches(presentation):
    presentation.watch("subject.appliedStereotype", presentation.update_shapes).watch(
        "subject.appliedStereotype.classifier.name"
    ).watch("subject.appliedStereotype.slot", presentation.update_shapes).watch(
        "subject.appliedStereotype.slot.definingFeature.name"
    ).watch(
        "subject.appliedStereotype.slot.value", presentation.update_shapes
    )


def attributes_compartment(subject):
    # We need to fix the attribute value, since the for loop changes it.
    def lazy_format(attribute):
        return lambda: format(attribute)

    return Box(
        *(
            Text(
                text=lazy_format(attribute),
                style={
                    "text-align": TextAlign.LEFT,
                    "text-decoration": TextDecoration.UNDERLINE
                    if attribute.isStatic
                    else TextDecoration.NONE,
                },
            )
            for attribute in subject.ownedAttribute
            if not attribute.association
        ),
        style={"padding": (4, 4, 4, 4)},
        draw=draw_top_separator,
    )

def operations_compartment(subject):
    def lazy_format(operation):
        return lambda: format(
            operation, visibility=True, type=True, multiplicity=True, default=True
        )

    return Box(
        *(
            Text(
                text=lazy_format(operation),
                style={
                    "text-align": TextAlign.LEFT,
                    "font-style": FontStyle.ITALIC
                    if operation.isAbstract
                    else FontStyle.NORMAL,
                    "text-decoration": TextDecoration.UNDERLINE
                    if operation.isStatic
                    else TextDecoration.NONE,
                },
            )
            for operation in subject.ownedOperation
        ),
        style={"padding": (4, 4, 4, 4)},
        draw=draw_top_separator,
    )
