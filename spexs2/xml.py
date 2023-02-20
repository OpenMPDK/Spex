from typing import Optional, cast, List, Union
from lxml.etree import _Element, _ElementTree
from lxml import etree

Element = Union[_Element, _ElementTree]


def fmt(elem: Element) -> str:
    """render XML element into a formatted string."""
    return etree.tostring(elem, pretty_print=True, encoding="unicode")


def pp(elem: Element) -> None:
    """pretty-print XML element."""
    print(fmt(elem))


def spit(path: str, elem: Element) -> None:
    """spit XML element out into a file."""
    with open(path, "w") as fh:
        fh.write(fmt(elem))


class Xpath:
    @classmethod
    def elems(cls, e: Element, query: str) -> List[Element]:
        res = e.xpath(query)
        assert isinstance(res, list)
        if len(res) > 0 and not isinstance(res[0], Element):
            if query.startswith("@") or "/@" in query:
                raise RuntimeError(
                    "don't query attribute values with this function, use `Xpath.attrs`"
                )
            else:
                raise RuntimeError(
                    f"query '{query}' did not return a list of Element, first element is {type(res[0])}"
                )
        return cast(List[Element], res)

    @classmethod
    def elem_first(cls, e: Element, query: str) -> Optional[Element]:
        res = cls.elems(e, query)
        return res[0] if len(res) > 0 else None

    @classmethod
    def elem_first_req(cls, e: Element, query: str) -> Optional[Element]:
        res = cls.elems(e, query)
        if len(res) == 0:
            raise RuntimeError("failed to find required element")
        return res[0]

    @classmethod
    def attrs(cls, e: Element, query: str) -> List[str]:
        res = e.xpath(query)
        assert isinstance(res, list)
        if len(res) > 0 and not isinstance(res[0], str):
            raise RuntimeError(
                f"query should return a list of str elements for attr-queries, got {type(res[0])}, use `Xpath.elems` instead?"
            )
        return cast(List[str], res)

    @classmethod
    def attr_first(cls, e: Element, query: str) -> Optional[str]:
        res = cls.attrs(e, query)
        return res[0] if len(res) > 0 else None

    @classmethod
    def attr_first_req(
        cls,
        e: Element,
        query: str,
    ) -> str:
        res = cls.attrs(e, query)
        if len(res) == 0:
            raise RuntimeError("failed to find required attribute")
        return res[0]


__all__ = ["fmt", "pp", "spit", "etree", "Element", "Xpath"]
