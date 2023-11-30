from enum import Enum

from gaphas.item import SE

from gaphor import UML
from gaphor import UML3
from gaphor.core import gettext
from gaphor.diagram.diagramtoolbox import ToolDef, ToolSection, namespace_config
from gaphor.diagram.diagramtools import new_item_factory
from gaphor.UML import diagramitems
from gaphor.UML3 import diagramitems as uml3_items
from gaphor.diagram import general

class AssociationType(Enum):
    COMPOSITE = "composite"
    SHARED = "shared"

def create_association(
    assoc_item: diagramitems.AssociationItem, association_type: AssociationType
) -> None:
    assoc = assoc_item.subject
    assoc.memberEnd.append(assoc_item.model.create(UML.Property))
    assoc.memberEnd.append(assoc_item.model.create(UML.Property))

    assoc_item.head_subject = assoc.memberEnd[0]
    assoc_item.tail_subject = assoc.memberEnd[1]

    UML.model.set_navigability(assoc, assoc_item.head_subject, True)
    assoc_item.head_subject.aggregation = association_type.value

def composite_teste_config(assoc_item: uml3_items.TesteItem) -> None:
    create_association(assoc_item, AssociationType.COMPOSITE)

def shared_formal_config(assoc_item: uml3_items.FormalItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def composite_characterization_config(assoc_item: uml3_items.CharacterizationItem) -> None:
    create_association(assoc_item, AssociationType.COMPOSITE)

def shared_componentof_config(assoc_item: uml3_items.ComponentofItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_containment_config(assoc_item: uml3_items.ContainmentItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_dependencyblack_config(assoc_item: uml3_items.DependencyblackItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_dependencywhite_config(assoc_item: uml3_items.DependencywhiteItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_derivation_config(assoc_item: uml3_items.DerivationItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_heritage_config(assoc_item: uml3_items.HeritageItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_material_config(assoc_item: uml3_items.MaterialItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_mediation_config(assoc_item: uml3_items.MediationItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_memberof_config(assoc_item: uml3_items.MemberofItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_memberofblack_config(assoc_item: uml3_items.MemberofblackItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_partwhole_config(assoc_item: uml3_items.PartwholeItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_partwholeblack_config(assoc_item: uml3_items.PartwholeblackItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_structuration_config(assoc_item: uml3_items.StructurationItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_subcollectionof_config(assoc_item: uml3_items.SubcollectionofItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)

def shared_subquantityof_config(assoc_item: uml3_items.SubquantityofItem) -> None:
    create_association(assoc_item, AssociationType.SHARED)


ontogeneral = ToolSection (
        gettext("General"),
        (
            ToolDef(
                "toolbox-pointer",
                gettext("Pointer"),
                "gaphor-pointer-symbolic",
                "Escape",
                item_factory=None,
            ),
            ToolDef(
                "toolbox-package",
                gettext("Package"),
                "gaphor-package-symbolic",
                "p",
                new_item_factory(
                    diagramitems.PackageItem, UML.Package, config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-comment",
                gettext("Comment"),
                "gaphor-comment-symbolic",
                "k",
                new_item_factory(general.CommentItem, UML.Comment),
                handle_index=SE,
            ),

        ),
    )
sortal = ToolSection (
        gettext("Sortals"),
        (
            ToolDef(
                "toolbox-kind",
                gettext("Kind"),
                "gaphor-sortal-kind-symbolic",
                "l",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeKind,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-subkind",
                gettext("Subkind"),
                "gaphor-sortal-subkind-symbolic",
                "a",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeSubkind,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-phase",
                gettext("Phase"),
                "gaphor-sortal-phase-symbolic",
                "p",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypePhase,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-role",
                gettext("Role"),
                "gaphor-sortal-role-symbolic",
                "<Shift>R",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeRole,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-collective",
                gettext("Collective"),
                "gaphor-sortal-collective-symbolic",
                "c",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeCollective,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-quantity",
                gettext("Quantity"),
                "gaphor-sortal-quantity-symbolic",
                "q",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeQuantity,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-relator",
                gettext("Relator"),
                "gaphor-sortal-relator-symbolic",
                "t",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeRelator,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
        ),
    )
nonsortal = ToolSection (
    gettext("NonSortals"),
        (
            ToolDef(
                "toolbox-category",
                gettext("Category"),
                "gaphor-nonsortal-category-symbolic",
                "<Shift>C",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeCategory,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-phasemixin",
                gettext("Phasemixin"),
                "gaphor-nonsortal-phasemixin-symbolic",
                "o",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypePhasemixin,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-mixin",
                gettext("Mixin"),
                "gaphor-nonsortal-mixin-symbolic",
                "ç",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeMixin,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-rolemixin",
                gettext("Rolemixin"),
                "gaphor-nonsortal-rolemixin-symbolic",
                "x",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeRolemixin,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
        ),
    )
aspects = ToolSection (
        gettext("Aspects"),
        (
            ToolDef(
                "toolbox-mode",
                gettext("Mode"),
                "gaphor-aspects-mode-symbolic",
                "r",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeMode,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
            ToolDef(
                "toolbox-quality",
                gettext("Quality"),
                "gaphor-aspects-quality-symbolic",
                "<Shift>I",
                new_item_factory(
                    uml3_items.ClassItem,
                    UML3.StereotypeQuality,
                    config_func=namespace_config,
                ),
                handle_index=SE,
            ),
        ),
    )

relations = ToolSection (
        gettext("Relationship"),
        (
            ToolDef(
                "toolbox-formalt-association",
                gettext("Formalt Association"),
                "gaphor-associations-formal-symbolic",
                "<Shift>K",
                new_item_factory(
                    uml3_items.FormalItem,
                    UML3.Formal,
                    config_func=shared_formal_config,
                ),
            ),
            ToolDef(
                "toolbox-characterization-association",
                gettext("Characterization"),
                "gaphor-associations-characterization-symbolic",
                "u",
                new_item_factory(
                    uml3_items.CharacterizationItem,
                    UML3.Characterization,
                    config_func=composite_characterization_config,
                ),
            ),
            ToolDef(
                "toolbox-componentof-association",
                gettext("Componentof"),
                "gaphor-agregations-componentof-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.ComponentofItem,
                    UML3.Componentof,
                    config_func=shared_componentof_config,
                ),
            ),

            ToolDef(
                "toolbox-containment-association",
                gettext("Containment"),
                "gaphor-agregations-containment-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.ContainmentItem,
                    UML3.Containment,
                    config_func=shared_containment_config,
                ),
            ),
            ToolDef(
                "toolbox-dependencyblack-association",
                gettext("Dependencyblack"),
                "gaphor-dependency-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.DependencyblackItem,
                    UML3.Dependencyblack,
                    config_func=shared_dependencyblack_config,
                ),
            ),
            ToolDef(
                "toolbox-dependencywhite-association",
                gettext("Dependencywhite"),
                "gaphor-dependency-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.DependencywhiteItem,
                    UML3.Dependencywhite,
                    config_func=shared_dependencywhite_config,
                ),
            ),
            ToolDef(
                "toolbox-derivation-association",
                gettext("Derivation"),
                "gaphor-associations-derivation-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.DerivationItem,
                    UML3.Derivation,
                    config_func=shared_derivation_config,
                ),
            ),
            ToolDef(
                "toolbox-heritage-association",
                gettext("Heritage"),
                "gaphor-generalization-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.HeritageItem,
                    UML3.Heritage,
                    config_func=shared_heritage_config,
                ),
            ),
            ToolDef(
                "toolbox-material-association",
                gettext("Material"),
                "gaphor-associations-material-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.MaterialItem,
                    UML3.Material,
                    config_func=shared_material_config,
                ),
            ),
            ToolDef(
                "toolbox-mediation-association",
                gettext("Mediation"),
                "gaphor-associations-mediation-symbolic",
                "<Shift>Z",
                new_item_factory(
                    uml3_items.MediationItem,
                    UML3.Mediation,
                    config_func=shared_mediation_config,
                ),
            ),
            ToolDef(
                "toolbox-memberof-association",
                gettext("Memberof"),
                "gaphor-agregations-memberof-symbolic",
                "<Shift>M",
                new_item_factory(
                    uml3_items.MemberofItem,
                    UML3.Memberof,
                    config_func=shared_memberof_config,
                ),
            ),
            ToolDef(
                "toolbox-memberofblack-association",
                gettext("Memberofblack"),
                "gaphor-agregations-memberofblack-symbolic",
                "<Shift>W",
                new_item_factory(
                    uml3_items.MemberofblackItem,
                    UML3.Memberofblack,
                    config_func=shared_memberofblack_config,
                ),
            ),
            ToolDef(
                "toolbox-partwhole-association",
                gettext("Partwhole"),
                "gaphor-agregations-partwhole-symbolic",
                "<Shift>P",
                new_item_factory(
                    uml3_items.PartwholeItem,
                    UML3.Partwhole,
                    config_func=shared_partwhole_config,
                ),
            ),
            ToolDef(
                "toolbox-Partwholeblack-association",
                gettext("Partwholeblack"),
                "gaphor-agregations-partwholeblack-symbolic",
                "<Shift>Ç",
                new_item_factory(
                    uml3_items.PartwholeblackItem,
                    UML3.Partwholeblack,
                    config_func=shared_partwholeblack_config,
                ),
            ),
            ToolDef(
                "toolbox-structuration-association",
                gettext("Structuration"),
                "gaphor-associations-structuration-symbolic",
                "s",
                new_item_factory(
                    uml3_items.StructurationItem,
                    UML3.Structuration,
                    config_func=shared_structuration_config,
                ),
            ),
            ToolDef(
                "toolbox-subcollectionof-association",
                gettext("Subcollectionof"),
                "gaphor-agregations-subcollectionof-symbolic",
                "<Shift>S",
                new_item_factory(
                    uml3_items.SubcollectionofItem,
                    UML3.Subcollectionof,
                    config_func=shared_subcollectionof_config,
                ),
            ),
            ToolDef(
                "toolbox-subquantityof-association",
                gettext("Subquantityof"),
                "gaphor-agregations-subquantityof-symbolic",
                "<Shift>Q",
                new_item_factory(
                    uml3_items.SubquantityofItem,
                    UML3.Subquantityof,
                    config_func=shared_subquantityof_config,
                ),
            ),            
        ),
    )
'''
        gettext("Relationship"),
        (
            ToolDef(
                "toolbox-associations-formal",
                gettext("Formal"),
                "gaphor-associations-formal-symbolic",
                "<Shift>F",
                new_item_factory(uml3_items.FormalItem),
            ),
            ToolDef(
                "toolbox-associations-material",
                gettext("Material"),
                "gaphor-associations-material-symbolic",
                "<Shift>B",
                new_item_factory(uml3_items.MaterialItem),
            ),
            ToolDef(
                "toolbox-associations-mediation",
                gettext("Mediation"),
                "gaphor-associations-mediation-symbolic",
                "<Shift>A",
                new_item_factory(uml3_items.MediationItem),
            ),
            ToolDef(
                "toolbox-associations-characterization",
                gettext("Characterization"),
                "gaphor-associations-characterization-symbolic",
                "<Shift>E",
                new_item_factory(uml3_items.CharacterizationItem),
            ),
            ToolDef(
                "toolbox-associations-derivation",
                gettext("Derivation"),
                "gaphor-associations-derivation-symbolic",
                "d",
                new_item_factory(uml3_items.DerivationItem),
            ),
            ToolDef(
                "toolbox-associations-structuration",
                gettext("Structuration"),
                "gaphor-associations-structuration-symbolic",
                "s",
                new_item_factory(uml3_items.StructurationItem),
            ),
            ToolDef(
                "toolbox-agregations-partwhole",
                gettext("Partwhole"),
                "gaphor-agregations-partwhole-symbolic",
                "<Shift>P",
                new_item_factory(uml3_items.PartwholeItem),
            ),
            ToolDef(
                "toolbox-agregations-partwholeblack",
                gettext("Partwhole Black"),
                "gaphor-agregations-partwholeblack-symbolic",
                "<Shift>Ç",
                new_item_factory(uml3_items.PartwholeblackItem),
            ),
            ToolDef(
                "toolbox-agregations-componentof",
                gettext("Componentof"),
                "gaphor-agregations-componentof-symbolic",
                "m",
                new_item_factory(uml3_items.ComponentofItem),
            ),
            ToolDef(
                "toolbox-agregations-containment",
                gettext("Containment"),
                "gaphor-agregations-containment-symbolic",
                "n",
                new_item_factory(uml3_items.ContainmentItem),
            ),
            ToolDef(
                "toolbox-agregations-memberof",
                gettext("Memberof"),
                "gaphor-agregations-memberof-symbolic",
                "<Shift>M",
                new_item_factory(uml3_items.MemberofItem),
            ),
            ToolDef(
                "toolbox-agregations-memberofblack",
                gettext("Memberof Black"),
                "gaphor-agregations-memberofblack-symbolic",
                "<Shift>W",
                new_item_factory(uml3_items.MemberofblackItem),
            ),
            ToolDef(
                "toolbox-agregations-subcollectionof",
                gettext("Subcollectionof"),
                "gaphor-agregations-subcollectionof-symbolic",
                "<Shift>S",
                new_item_factory(uml3_items.SubcollectionofItem),
            ),
            ToolDef(
                "toolbox-agregations-subquantityof",
                gettext("Subquantityof"),
                "gaphor-agregations-subquantityof-symbolic",
                "<Shift>Q",
                new_item_factory(uml3_items.SubquantityofItem),
            ),
            ToolDef(
                "toolbox-dependency",
                gettext("Dependency"),
                "gaphor-dependency-symbolic",
                "<Shift>D",
new_item_factory(uml3_items.DependencywhiteItem),
            ),
            ToolDef(
                "toolbox-heritage",
                gettext("Heritage"),
                "gaphor-generalization-symbolic",
                "<Shift>G",
                new_item_factory(uml3_items.HeritageItem),
            ),
        ),
    )'''