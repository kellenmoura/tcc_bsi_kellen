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



relation = ToolSection (
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
    )