from gaphas.geometry import Rectangle, distance_point_point_fast

from gaphor.core import transactional
from gaphor.core.format import format, parse
from gaphor.diagram.inlineeditors import InlineEditor, popup_entry, show_popover
#from gaphor.UML.classes.association import AssociationItem
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


@InlineEditor.register(TesteItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True

@InlineEditor.register(CharacterizationItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(FormalItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = "Formal"

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(ComponentofItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(ContainmentItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(DependencyblackItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(DependencywhiteItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(DerivationItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(HeritageItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(MaterialItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(MediationItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(MemberofItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(MemberofblackItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(PartwholeItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(PartwholeblackItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(StructurationItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(SubcollectionofItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



@InlineEditor.register(SubquantityofItem)
def association_item_inline_editor(item, view, pos=None) -> bool:
    """Text edit support for Named items."""

    @transactional
    def update_text(text):
        item.subject.name = text
        return True

    @transactional
    def update_end_text(text):
        assert end_item
        parse(end_item.subject, text)
        return True

    subject = item.subject
    if not subject:
        return False

    end_item = None
    if pos and distance_point_point_fast(item.handles()[0].pos, pos) < 50:
        end_item = item.head_end
    elif pos and distance_point_point_fast(item.handles()[-1].pos, pos) < 50:
        end_item = item.tail_end

    if end_item:
        text = (
            format(
                end_item.subject,
                visibility=True,
                is_derived=True,
                type=False,
                multiplicity=True,
                default=True,
            )
            or ""
        )

        def escape():
            assert end_item
            parse(end_item.subject, text)

        entry = popup_entry(text, update_end_text)
        bb = end_item.name_bounds
        x, y = view.get_matrix_i2v(item).transform_point(bb.x, bb.y)
        box = Rectangle(x, y, 10, 10)
    else:
        text = item.subject.name or ""

        def escape():
            item.subject.name = text

        entry = popup_entry(text, update_text)

        box = item.middle_shape_size
        i2v = view.get_matrix_i2v(item)
        x, y = i2v.transform_point(box.x, box.y)
        w, h = i2v.transform_distance(box.width, box.height)
        box = Rectangle(x, y, w, h)

    show_popover(entry, view, box, escape)
    return True



