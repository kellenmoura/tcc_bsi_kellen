"""The action definition for the UML3 toolbox."""


from gaphor.diagram.diagramtoolbox import ToolboxDefinition, general_tools
from gaphor.UML3.classesonto.classesontotoolbox import ontogeneral, sortal, nonsortal, aspects, relations
from gaphor.UML3.profile.profileontotoolbox import relation

uml3_toolbox_actions: ToolboxDefinition = (
    ontogeneral,
    sortal,
    nonsortal,
    aspects,
    #relation,
    relations
)
