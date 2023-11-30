"""Classes related (dependency, implementation) adapter connections."""

from gaphas import Handle

from gaphor import UML
from gaphor import UML3
from gaphor.diagram.connectors import (
    Connector,
    RelationshipConnect,
    UnaryRelationshipConnect,
)
from gaphor.diagram.presentation import Classified, Named
from gaphor.UML3.classesonto.teste import TesteItem
from gaphor.UML3.profile.formal import FormalItem
from gaphor.UML3.profile.characterization import CharacterizationItem
from gaphor.UML3.profile.componentof import ComponentofItem
from gaphor.UML3.profile.containment import ContainmentItem
from gaphor.UML3.profile.dependencyblack import DependencyblackItem
from gaphor.UML3.profile.dependencywhite import DependencywhiteItem
from gaphor.UML3.profile.derivation import DerivationItem
from gaphor.UML3.profile.heritage import HeritageItem
from gaphor.UML3.profile.material import MaterialItem
from gaphor.UML3.profile.mediation import MediationItem
from gaphor.UML3.profile.memberof import MemberofItem
from gaphor.UML3.profile.memberofblack import MemberofblackItem
from gaphor.UML3.profile.partwhole import PartwholeItem
from gaphor.UML3.profile.partwholeblack import PartwholeblackItem
from gaphor.UML3.profile.structuration import StructurationItem
from gaphor.UML3.profile.subcollectionof import SubcollectionofItem
from gaphor.UML3.profile.subquantityof import SubquantityofItem


@Connector.register(Classified, FormalItem)
class FormalConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: FormalItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, TesteItem)
class TesteConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: TesteItem

    def allow(self, handle, port):
        element = self.element
        # Element should be a Classifier
        subject = self.element.subject
        tipo = str(type(subject))
        line = self.line
        result = False
        global head

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            nome = (UML3.StereotypeKind)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            nome = (UML3.StereotypeSubkind)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            nome = (UML3.StereotypePhase)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            nome = (UML3.StereotypeRole)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            nome = (UML3.StereotypeCollective)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            nome = (UML3.StereotypeQuantity)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            nome = (UML3.StereotypeRelator)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            nome = (UML3.StereotypeCategory)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            nome = (UML3.StereotypePhasemixin)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            nome = (UML3.StereotypeMixin)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            nome = (UML3.StereotypeRolemixin)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            nome = (UML3.StereotypeMode)
            
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            nome = (UML3.StereotypeQuality)
            

        if handle is line.head:
            result = isinstance(subject, nome)
            if nome == UML3.StereotypeKind:
                head = "Kind"
            elif nome == UML3.StereotypeSubkind:
                head = "Subkind"
            elif nome == UML3.StereotypePhase:
                head = "Phase"
            elif nome == UML3.StereotypeRole:
                head = "Role"
            elif nome == UML3.StereotypeCollective:
                head = "Collective"
            elif nome == UML3.StereotypeQuantity:
                head = "Quantity"
            elif nome == UML3.StereotypeRelator:
                head = "Relator"
            elif nome == UML3.StereotypeCategory:
                head = "Category"
            elif nome == UML3.StereotypePhasemixin:
                head = "Phasemixin"
            elif nome == UML3.StereotypeMixin:
                head = "Mixin"
            elif nome == UML3.StereotypeRolemixin:
                head = "Rolemixin"
            elif nome == UML3.StereotypeMode:
                head = "Mode"
            elif nome == UML3.StereotypeQuality:
                head = "Quality"


        if handle is line.tail:
            if head == "Kind":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Subkind":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Phase":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Role":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Collective":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Quantity":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Relator":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Category":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Phasemixin":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Mixin":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Rolemixin":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Mode":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Quality":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]

            if nome in opc:
                result = isinstance(subject, nome)

        return result

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, CharacterizationItem)
class CharacterizationConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: CharacterizationItem

    def allow(self, handle, port):
        element = self.element
        # Element should be a Classifier
        subject = self.element.subject
        tipo = str(type(subject))
        line = self.line
        result = False
        global head

        #condições para saber qual é o stereotype
        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        if handle is line.head:
            result = isinstance(subject, nome)
            if nome == UML3.StereotypeKind:
                head = "Kind"
            elif nome == UML3.StereotypeSubkind:
                head = "Subkind"
            elif nome == UML3.StereotypePhase:
                head = "Phase"
            elif nome == UML3.StereotypeRole:
                head = "Role"
            elif nome == UML3.StereotypeCollective:
                head = "Collective"
            elif nome == UML3.StereotypeQuantity:
                head = "Quantity"
            elif nome == UML3.StereotypeRelator:
                head = "Relator"
            elif nome == UML3.StereotypeCategory:
                head = "Category"
            elif nome == UML3.StereotypePhasemixin:
                head = "Phasemixin"
            elif nome == UML3.StereotypeMixin:
                head = "Mixin"
            elif nome == UML3.StereotypeRolemixin:
                head = "Rolemixin"
            elif nome == UML3.StereotypeMode:
                head = "Mode"
            elif nome == UML3.StereotypeQuality:
                head = "Quality"


        if handle is line.tail:
            if head == "Kind":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Subkind":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Phase":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Role":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Collective":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Quantity":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Relator":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Category":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Phasemixin":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Mixin":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Rolemixin":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Mode":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            elif head == "Quality":
                opc = [UML3.StereotypeQuality, UML3.StereotypeMode]

            if nome in opc:
                result = isinstance(subject, nome)

        return result
        
        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None



@Connector.register(Classified, ComponentofItem)
class ComponentofConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: ComponentofItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)


    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, ContainmentItem)
class ContainmentConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: ContainmentItem

    def allow(self, handle, port):
        element = self.element
        # Element should be a Classifier
        subject = self.element.subject
        tipo = str(type(subject))
        line = self.line
        result = False
        global head

        #condições para saber qual é o stereotype
        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        if handle is line.head:
            result = isinstance(subject, nome)
            if nome == UML3.StereotypeKind:
                head = "Kind"
            elif nome == UML3.StereotypeSubkind:
                head = "Subkind"
            elif nome == UML3.StereotypePhase:
                head = "Phase"
            elif nome == UML3.StereotypeRole:
                head = "Role"
            elif nome == UML3.StereotypeCollective:
                head = "Collective"
            elif nome == UML3.StereotypeQuantity:
                head = "Quantity"
            elif nome == UML3.StereotypeRelator:
                head = "Relator"
            elif nome == UML3.StereotypeCategory:
                head = "Category"
            elif nome == UML3.StereotypePhasemixin:
                head = "Phasemixin"
            elif nome == UML3.StereotypeMixin:
                head = "Mixin"
            elif nome == UML3.StereotypeRolemixin:
                head = "Rolemixin"
            elif nome == UML3.StereotypeMode:
                head = "Mode"
            elif nome == UML3.StereotypeQuality:
                head = "Quality"


        if handle is line.tail:
            if head == "Kind":
                opc = [UML3.StereotypeQuantity]
            elif head == "Subkind":
                opc = [UML3.StereotypeQuantity]
            elif head == "Phase":
                opc = [UML3.StereotypeQuantity]
            elif head == "Role":
                opc = [UML3.StereotypeQuantity]
            elif head == "Collective":
                opc = [UML3.StereotypeQuantity]
            elif head == "Quantity":
                opc = [UML3.StereotypeQuantity]
            elif head == "Relator":
                opc = [UML3.StereotypeQuantity]
            elif head == "Category":
                opc = [UML3.StereotypeQuantity]
            elif head == "Phasemixin":
                opc = [UML3.StereotypeQuantity]
            elif head == "Mixin":
                opc = [UML3.StereotypeQuantity]
            elif head == "Rolemixin":
                opc = [UML3.StereotypeQuantity]
            elif head == "Mode":
                opc = [UML3.StereotypeQuantity]
            elif head == "Quality":
                opc = [UML3.StereotypeQuantity]

            if nome in opc:
                result = isinstance(subject, nome)

        return result

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, DependencyblackItem)
class DependencyblackConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: DependencyblackItem

    
    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)

        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)


    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, DependencywhiteItem)
class DependencywhiteConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: DependencywhiteItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)

        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)


    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, DerivationItem)
class DerivationConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: DerivationItem

    def allow(self, handle, port):
        element = self.element        

        # Element should be a Classifier
        if not isinstance(element.subject, UML3.StereotypeRelator):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        print("linesub", line.subject)
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)


    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, HeritageItem)
class HeritageConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: HeritageItem

    def allow(self, handle, port):
        element = self.element
        # Element should be a Classifier
        subject = self.element.subject
        tipo = str(type(subject))
        line = self.line
        result = False
        global head

       #condições para saber qual é o stereotype
        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
            #tuplatail = (UML3.StereotypeRelator)
            '''print("tipo antes", tipo)
            tipo = ""
            print("tipo depois", tipo)
            tipo = str(type(subject))
            print("tipo depois de depois", tipo)'''
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        if handle is line.head:
            result = isinstance(subject, nome)
            if nome == UML3.StereotypeKind:
                head = "Kind"
            elif nome == UML3.StereotypeSubkind:
                head = "Subkind"
            elif nome == UML3.StereotypePhase:
                head = "Phase"
            elif nome == UML3.StereotypeRole:
                head = "Role"
            elif nome == UML3.StereotypeCollective:
                head = "Collective"
            elif nome == UML3.StereotypeQuantity:
                head = "Quantity"
            elif nome == UML3.StereotypeRelator:
                head = "Relator"
            elif nome == UML3.StereotypeCategory:
                head = "Category"
            elif nome == UML3.StereotypePhasemixin:
                head = "Phasemixin"
            elif nome == UML3.StereotypeMixin:
                head = "Mixin"
            elif nome == UML3.StereotypeRolemixin:
                head = "Rolemixin"
            elif nome == UML3.StereotypeMode:
                head = "Mode"
            elif nome == UML3.StereotypeQuality:
                head = "Quality"


        if handle is line.tail:
            if head == "Kind":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole]
            elif head == "Subkind":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole]
            elif head == "Phase":
                opc = [UML3.StereotypePhase, UML3.StereotypeRole]
            elif head == "Role":
                opc = [UML3.StereotypeRole]
            elif head == "Collective":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole]
            elif head == "Quantity":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole]
            elif head == "Relator":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole]
            elif head == "Category":
                opc = [UML3.StereotypeKind, UML3.StereotypeCollective, UML3.StereotypeCategory, UML3.StereotypeSubkind, UML3.StereotypeQuantity, UML3.StereotypeRelator]
            elif head == "Phasemixin":
                opc = [UML3.StereotypePhase, UML3.StereotypePhasemixin]
            elif head == "Mixin":
                opc = [UML3.StereotypeSubkind, UML3.StereotypeKind, UML3.StereotypeCollective, UML3.StereotypeQuantity, UML3.StereotypeCategory, UML3.StereotypeMixin, UML3.StereotypeRole, UML3.StereotypePhase, UML3.StereotypeRolemixin, UML3.StereotypeRelator]
            elif head == "Rolemixin":
                opc = [UML3.StereotypeRolemixin, UML3.StereotypeRole]
            elif head == "Mode":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole, UML3.StereotypeMode]
            elif head == "Quality":
                opc = [UML3.StereotypeSubkind, UML3.StereotypePhase, UML3.StereotypeRole]

            if nome in opc:
                result = isinstance(subject, nome)

        return result

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, MaterialItem)
class MaterialConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: MaterialItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)

        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)


    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, MemberofblackItem)
class MemberofblackConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: MemberofblackItem

    def allow(self, handle, port):
        line = self.line
        subject = self.element.subject
        tipo = str(type(subject))
        result = False

        #condições para saber qual é o stereotype
        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            nome = (UML3.StereotypeRelator)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            nome = (UML3.StereotypeQuality)


        if handle is line.head:
            result = isinstance(subject, UML3.StereotypeCollective)


        if handle is line.tail:
            result = isinstance(subject, nome)


        return result

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, PartwholeItem)
class PartwholeConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: PartwholeItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, PartwholeblackItem)
class PartwholeblackConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: PartwholeblackItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None

@Connector.register(Classified, StructurationItem)
class StructurationConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: StructurationItem

    def allow(self, handle, port):
        element = self.element
        # Element should be a Classifier
        subject = self.element.subject
        tipo = str(type(subject))
        line = self.line
        result = False
        global head

        #condições para saber qual é o stereotype
        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
            tuplahead = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        if handle is line.head:
            result = isinstance(subject, UML3.StereotypeQuality)


        if handle is line.tail:
            opc = [UML3.StereotypeQuality, UML3.StereotypeMode]
            if nome in opc:
                result = isinstance(subject, nome)


        return result

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, SubcollectionofItem)
class SubcollectionofConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: SubcollectionofItem

    def allow(self, handle, port):
        element = self.element

        # Element should be a Classifier
        if not isinstance(element.subject, UML3.StereotypeCollective):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None


@Connector.register(Classified, SubquantityofItem)
class SubquantityofConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: SubquantityofItem

    def allow(self, handle, port):
        element = self.element

        # Element should be a Classifier
        if not isinstance(element.subject, UML3.StereotypeQuantity):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None

@Connector.register(Classified, MediationItem)
class MediationConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: MediationItem

    def allow(self, handle, port):
        element = self.element
        subject = self.element.subject
        tipo = str(type(subject))

        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)

        # Element should be a Classifier
        if not isinstance(element.subject, nome):
            return None

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None

@Connector.register(Classified, MemberofItem)
class MemberofConnect(UnaryRelationshipConnect):
    """Connect association to classifier."""

    line: MemberofItem

    def allow(self, handle, port):
        line = self.line
        subject = self.element.subject
        tipo = str(type(subject))
        result = False

        #condições para saber qual é o stereotype
        if tipo == "<class 'gaphor.UML3.uml3.StereotypeKind'>":
            #aux = "Kind"
            nome = (UML3.StereotypeKind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeSubkind'>":
            #aux = "Subkind"
            nome = (UML3.StereotypeSubkind)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhase'>":
            #aux = "Phase"
            nome = (UML3.StereotypePhase)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRole'>":
            #aux = "Role"
            nome = (UML3.StereotypeRole)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCollective'>":
            #aux = "Collective"
            nome = (UML3.StereotypeCollective)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuantity'>":
            #aux = "Quantity"
            nome = (UML3.StereotypeQuantity)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRelator'>":
            #aux = "Relator"
            nome = (UML3.StereotypeRelator)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeCategory'>":
            #aux = "Category"
            nome = (UML3.StereotypeCategory)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypePhasemixin'>":
            #aux = "Phasemixin"
            nome = (UML3.StereotypePhasemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMixin'>":
            #aux = "Mixin"
            nome = (UML3.StereotypeMixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeRolemixin'>":
            #aux = "Rolemixin"
            nome = (UML3.StereotypeRolemixin)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeMode'>":
            #aux = "Mode"
            nome = (UML3.StereotypeMode)
        elif tipo == "<class 'gaphor.UML3.uml3.StereotypeQuality'>":
            #aux = "Quality"
            nome = (UML3.StereotypeQuality)


        if handle is line.head:
            result = isinstance(subject, UML3.StereotypeCollective)


        if handle is line.tail:
            result = isinstance(subject, nome)


        return result

        if not self.line.subject:
            return True

        line = self.line
        subject = line.subject
        is_head = handle is line.head

        def is_connection_allowed(p):
            end = p.head_end if is_head else p.tail_end
            h = end.owner_handle
            if h is handle:
                return True
            connected = self.get_connected(h)
            return (not connected) or connected.subject is element.subject

        return all(is_connection_allowed(p) for p in subject.presentation)

    def connect_subject(self, handle):
        element = self.element
        line = self.line

        assert element.diagram

        c1 = self.get_connected(line.head)
        c2 = self.get_connected(line.tail)
        if c1 and c2:

            if not line.subject:
                relation = UML.model.create_association(c1.subject, c2.subject)
                relation.package = element.diagram.namespace
                line.head_subject = relation.memberEnd[0]
                line.tail_subject = relation.memberEnd[1]

                # Set subject last so that event handlers can trigger
                line.subject = relation

            line.head_subject.type = c1.subject  # type: ignore[assignment]
            line.tail_subject.type = c2.subject  # type: ignore[assignment]


    def reconnect(self, handle, port):
        line = self.line
        c = self.get_connected(handle)
        assert c
        if handle is line.head:
            end = line.tail_end
            oend = line.head_end
        elif handle is line.tail:
            end = line.head_end
            oend = line.tail_end
        else:
            raise ValueError("Incorrect handle passed to adapter")

        nav = oend.subject.navigability

        UML.model.set_navigability(line.subject, end.subject, None)  # clear old data

        oend.subject.type = c.subject
        UML.model.set_navigability(line.subject, oend.subject, nav)

    def disconnect_subject(self, handle: Handle) -> None:
        """Disconnect the type of each member end.

        On connect, we pair association member ends with the element
        they connect to. On disconnect, we remove this relation.
        """
        association = self.line.subject
        if association and len(association.presentation) <= 1:
            for e in list(association.memberEnd):
                UML.model.set_navigability(association, e, None)
            for e in list(association.memberEnd):
                e.type = None
