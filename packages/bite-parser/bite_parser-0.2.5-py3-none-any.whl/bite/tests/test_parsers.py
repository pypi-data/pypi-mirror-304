import pytest

from bite.io import BytesBuffer, ParserBuffer
from bite.parsers import (
    And,
    CaselessLiteral,
    CharacterSet,
    Combine,
    Counted,
    FixedByteCount,
    Forward,
    Literal,
    MatchFirst,
    Not,
    OneOrMore,
    Opt,
    ParsedAnd,
    ParsedCharacterSet,
    ParsedCombine,
    ParsedFixedByteCount,
    ParsedLeaf,
    ParsedLiteral,
    ParsedMatchFirst,
    ParsedNil,
    ParsedNode,
    ParsedOneOrMore,
    ParsedOpt,
    ParsedRepeat,
    ParsedZeroOrMore,
    Parser,
    Repeat,
    UnmetExpectationError,
    ZeroOrMore,
)
from bite.transformers import ParsedTransform, Suppress


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar,expected",
    [
        # Literals
        (
            b"LITERAL foo",
            Literal(b"LITERAL", name="literal"),
            ParsedLiteral("literal", b"LITERAL", 4, 11),
        ),
        (
            b"LiTeRaL foo",
            CaselessLiteral(b"lItErAl", name="literal"),
            ParsedLiteral("literal", b"lItErAl", 4, 11),
        ),
        # CharacterSet
        (
            b"123",
            CharacterSet(b"0123456789", name="charset"),
            ParsedCharacterSet("charset", b"1", 4, 5),
        ),
        (
            b"ABC",
            CharacterSet(b"0123456789", invert=True, name="inverted charset"),
            ParsedCharacterSet("inverted charset", b"A", 4, 5),
        ),
        # FixedByteCount
        (
            b"0123456789",
            FixedByteCount(4, name="fixed length"),
            ParsedFixedByteCount("fixed length", b"0123", 4, 8),
        ),
        # MatchFirst
        (
            b"A foo",
            MatchFirst([Literal(b"A"), Literal(b"B")]),
            ParsedMatchFirst(None, ParsedLiteral("b'A'", b"A", 4, 5), 0),
        ),
        (
            b"B foo",
            MatchFirst([Literal(b"A"), Literal(b"B")]),
            ParsedMatchFirst(None, ParsedLiteral("b'B'", b"B", 4, 5), 1),
        ),
        (
            b"A foo",
            MatchFirst(
                [Literal(b"A", name="first"), Literal(b"A", name="second")],
                name="precedence test",
            ),
            ParsedMatchFirst("precedence test", ParsedLiteral("first", b"A", 4, 5), 0),
        ),
        # And
        (
            b"AB foo",
            And([Literal(b"A"), Literal(b"B")], name="and"),
            ParsedAnd(
                "and",
                (ParsedLiteral("b'A'", b"A", 4, 5), ParsedLiteral("b'B'", b"B", 5, 6)),
                loc=4,
            ),
        ),
        # Repeated
        (
            b"AA foo",
            Repeat(
                Literal(b"A", name="A"), min_repeats=2, max_repeats=3, name="repeated"
            ),
            ParsedRepeat(
                "repeated",
                (ParsedLiteral("A", b"A", 4, 5), ParsedLiteral("A", b"A", 5, 6)),
                loc=4,
            ),
        ),
        (
            b"AAA foo",
            Repeat(
                Literal(b"A", name="A"), min_repeats=2, max_repeats=3, name="repeated"
            ),
            ParsedRepeat(
                "repeated",
                (
                    ParsedLiteral("A", b"A", 4, 5),
                    ParsedLiteral("A", b"A", 5, 6),
                    ParsedLiteral("A", b"A", 6, 7),
                ),
                loc=4,
            ),
        ),
        (
            b"AAAAA foo",
            Repeat(
                Literal(b"A", name="A"), min_repeats=2, max_repeats=3, name="repeated"
            ),
            ParsedRepeat(
                "repeated",
                (
                    ParsedLiteral("A", b"A", 4, 5),
                    ParsedLiteral("A", b"A", 5, 6),
                    ParsedLiteral("A", b"A", 6, 7),
                ),
                loc=4,
            ),
        ),
        (
            b"AAA foo",
            Repeat(
                Literal(b"A", name="A"),
                min_repeats=2,
                max_repeats=None,
                name="repeated",
            ),
            ParsedRepeat(
                "repeated",
                (
                    ParsedLiteral("A", b"A", 4, 5),
                    ParsedLiteral("A", b"A", 5, 6),
                    ParsedLiteral("A", b"A", 6, 7),
                ),
                loc=4,
            ),
        ),
        # Opt
        (
            b"foo",
            Opt(Literal(b"A", name="A"), name="opt"),
            ParsedOpt("opt", (), 4),  # type: ignore
        ),
        (
            b"A foo",
            Opt(Literal(b"A", name="A"), name="opt"),
            ParsedOpt("opt", (ParsedLiteral("A", b"A", 4, 5),), 4),
        ),
        # ZeroOrMore
        (
            b"foo",
            ZeroOrMore(Literal(b"A", name="A"), name="zero or more"),
            ParsedZeroOrMore(
                "zero or more",
                (),
                loc=4,
            ),
        ),
        (
            b"A foo",
            ZeroOrMore(Literal(b"A", name="A"), name="zero or more"),
            ParsedZeroOrMore(
                "zero or more",
                (ParsedLiteral("A", b"A", 4, 5),),
                loc=4,
            ),
        ),
        (
            b"AA foo",
            ZeroOrMore(Literal(b"A", name="A"), name="zero or more"),
            ParsedZeroOrMore(
                "zero or more",
                (
                    ParsedLiteral("A", b"A", 4, 5),
                    ParsedLiteral("A", b"A", 5, 6),
                ),
                loc=4,
            ),
        ),
        # OneOrMore
        (
            b"A foo",
            OneOrMore(Literal(b"A", name="A"), name="one or more"),
            ParsedOneOrMore(
                "one or more",
                (ParsedLiteral("A", b"A", 4, 5),),
                loc=4,
            ),
        ),
        (
            b"AA foo",
            OneOrMore(Literal(b"A", name="A"), name="one or more"),
            ParsedOneOrMore(
                "one or more",
                (
                    ParsedLiteral("A", b"A", 4, 5),
                    ParsedLiteral("A", b"A", 5, 6),
                ),
                loc=4,
            ),
        ),
        # Combine
        (
            b"AB",
            Combine(OneOrMore(CharacterSet(b"ABC")), name="combine"),
            ParsedCombine("combine", b"AB", 4, 6),
        ),
        # Not
        (b"A foo", Not(Literal(b"B"), name="not"), ParsedNil("not", 4)),
        # Operators
        (
            b"AB",
            Literal(b"A", name="A") + Literal(b"B", name="B"),
            ParsedAnd(
                "(A) + (B)",
                (ParsedLiteral("A", b"A", 4, 5), ParsedLiteral("B", b"B", 5, 6)),
                loc=4,
            ),
        ),
        (
            b"ABC",
            Literal(b"A", name="A") + Literal(b"B", name="B") + Literal(b"C", name="C"),
            ParsedAnd(
                "(A) + (B) + (C)",
                (
                    ParsedLiteral("A", b"A", 4, 5),
                    ParsedLiteral("B", b"B", 5, 6),
                    ParsedLiteral("C", b"C", 6, 7),
                ),
                loc=4,
            ),
        ),
        (
            b"B",
            Literal(b"A", name="A") | Literal(b"B", name="B"),
            ParsedMatchFirst(
                "(A) | (B)", ParsedLiteral("B", b"B", 4, 5), choice_index=1
            ),
        ),
        (
            b"B",
            Literal(b"A", name="A") | Literal(b"B", name="B") | Literal(b"C", name="C"),
            ParsedMatchFirst(
                "(A) | (B) | (C)", ParsedLiteral("B", b"B", 4, 5), choice_index=1
            ),
        ),
        (
            b"AA",
            Literal(b"A", name="A")[0, 2],
            ParsedRepeat(
                "(A)[0, 2]",
                (ParsedLiteral("A", b"A", 4, 5), ParsedLiteral("A", b"A", 5, 6)),
                loc=4,
            ),
        ),
        (
            b"AA",
            Literal(b"A", name="A")[0, ...],
            ParsedRepeat(
                "(A)[0, ...]",
                (ParsedLiteral("A", b"A", 4, 5), ParsedLiteral("A", b"A", 5, 6)),
                loc=4,
            ),
        ),
        (
            b"AA",
            Literal(b"A", name="A")[0, None],
            ParsedRepeat(
                "(A)[0, ...]",
                (ParsedLiteral("A", b"A", 4, 5), ParsedLiteral("A", b"A", 5, 6)),
                loc=4,
            ),
        ),
        (
            b"AA",
            Literal(b"A", name="A")[2, ...],
            ParsedRepeat(
                "(A)[2, ...]",
                (ParsedLiteral("A", b"A", 4, 5), ParsedLiteral("A", b"A", 5, 6)),
                loc=4,
            ),
        ),
        (
            b"AA",
            Literal(b"A", name="A")[0, 1],
            ParsedRepeat("(A)[0, 1]", (ParsedLiteral("A", b"A", 4, 5),), loc=4),
        ),
        (
            b"AA",
            Literal(b"A", name="A")[1],
            ParsedRepeat("(A)[1, 1]", (ParsedLiteral("A", b"A", 4, 5),), loc=4),
        ),
        (b"A", ~Literal(b"B"), ParsedNil("Not(b'B')", 4)),
    ],
)
async def test_successful_parsing(input_buf, grammar, expected):
    buffer = BytesBuffer(b"foo " + input_buf)
    assert await grammar.parse(buffer, 4) == expected


@pytest.mark.asyncio
async def test_successful_counted_parsing():
    buffer = BytesBuffer(b"foo [4]0123456789")
    grammar = Counted(
        And(
            [
                Suppress(Literal(b"[")),
                CharacterSet(b"0123456789"),
                Suppress(Literal(b"]")),
            ],
            name="and",
        ),
        lambda count: FixedByteCount(count, name="fixed byte count"),
    )
    parsed = await grammar.parse(buffer, 4)

    assert parsed.parse_tree.count_expr.name == "and"
    assert parsed.parse_tree.count_expr.values == (b"4",)
    assert parsed.parse_tree.counted_expr == ParsedFixedByteCount(
        "fixed byte count", b"0123", 7, 11
    )
    assert parsed.values == (b"0123",)


@pytest.mark.asyncio
@pytest.mark.parametrize("input_buf, at_loc", [(b"[4x012345689]", 2), (b"[4]01", 3)])
async def test_unsuccessful_counted_parsing(input_buf, at_loc):
    buffer = BytesBuffer(input_buf)
    grammar = Counted(
        And(
            [
                Suppress(Literal(b"[")),
                CharacterSet(b"0123456789"),
                Suppress(Literal(b"]")),
            ]
        ),
        lambda count: FixedByteCount(count, name="fixed byte count"),
    )

    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.at_loc == at_loc


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_buf,grammar",
    [
        (b"foo", Literal(b"LITERAL")),
        (b"C", MatchFirst([Literal(b"A"), Literal(b"B")])),
        (b"A", CharacterSet(b"0123456789")),
        (b"0", CharacterSet(b"0123456789", invert=True)),
        (b"0123", FixedByteCount(6)),
        (b"A", Not(Literal(b"A"))),
    ],
)
async def test_parsing_failure(input_buf, grammar):
    buffer = BytesBuffer(input_buf)
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar
    assert excinfo.value.at_loc == 0


@pytest.mark.asyncio
async def test_parsing_failure_and():
    buffer = BytesBuffer(b"AB")

    grammar = And([Literal(b"C"), Literal(b"B")])
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar.parsers[0]
    assert excinfo.value.at_loc == 0

    grammar = And([Literal(b"A"), Literal(b"C")])
    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(buffer)
    assert excinfo.value.expected == grammar.parsers[1]
    assert excinfo.value.at_loc == 1


@pytest.mark.asyncio
async def test_parsing_failure_repeat():
    grammar = Repeat(Literal(b"A"), min_repeats=2, max_repeats=3)

    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(BytesBuffer(b"A"))
    assert excinfo.value.expected == grammar.parser
    assert excinfo.value.at_loc == 1

    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(BytesBuffer(b"Abbb"))
    assert excinfo.value.expected == grammar.parser
    assert excinfo.value.at_loc == 1


@pytest.mark.asyncio
async def test_parsing_failure_one_or_more():
    grammar = OneOrMore(Literal(b"A"))

    with pytest.raises(UnmetExpectationError) as excinfo:
        await grammar.parse(BytesBuffer(b"B"))
    assert excinfo.value.expected == grammar.parser
    assert excinfo.value.at_loc == 0


@pytest.mark.parametrize(
    "parse_tree,expected_values",
    [
        (ParsedLeaf("leaf", b"foo", 0, 3), (b"foo",)),
        (
            ParsedMatchFirst("match-first", ParsedLeaf("leaf", b"foo", 0, 3), 0),
            (b"foo",),
        ),
        (
            ParsedAnd(
                "and",
                (
                    ParsedTransform(
                        "suppress", ParsedLeaf("x", b"x", 0, 1), lambda _: []
                    ),
                    ParsedLeaf("leaf", b"foo", 1, 4),
                ),
                loc=0,
            ),
            (b"foo",),
        ),
    ],
)
def test_parsed_vaule(parse_tree, expected_values):
    assert parse_tree.values == expected_values


def test_parsed_match_first_loc_range():
    parsed_one_of = ParsedMatchFirst(None, ParsedLiteral(None, b"val", 4, 7), 0)
    assert parsed_one_of.start_loc == 4
    assert parsed_one_of.end_loc == 7


def test_parsed_and_loc_range():
    parsed_and = ParsedAnd(
        None,
        (ParsedLiteral(None, b"val", 4, 7), ParsedLiteral(None, b"val", 7, 10)),
        loc=4,
    )
    assert parsed_and.start_loc == 4
    assert parsed_and.end_loc == 10

    parsed_and = ParsedAnd(None, (), loc=4)
    assert parsed_and.start_loc == 4
    assert parsed_and.end_loc == 4


def test_parsed_repeat_loc_range():
    parsed_and = ParsedRepeat(
        None,
        (ParsedLiteral(None, b"val", 4, 7), ParsedLiteral(None, b"val", 7, 10)),
        loc=4,
    )
    assert parsed_and.start_loc == 4
    assert parsed_and.end_loc == 10

    parsed_and = ParsedRepeat(None, (), loc=4)
    assert parsed_and.start_loc == 4
    assert parsed_and.end_loc == 4


def test_parsed_opt():
    parsed_opt = ParsedOpt(None, (ParsedLiteral(None, b"0123", 4, 8),), 4)
    assert parsed_opt.values == (b"0123",)
    assert parsed_opt.start_loc == 4
    assert parsed_opt.end_loc == 8

    parsed_opt = ParsedOpt(None, (), 4)
    assert not parsed_opt.values
    assert parsed_opt.start_loc == 4
    assert parsed_opt.end_loc == 4


@pytest.mark.asyncio
async def test_forward():
    buffer = BytesBuffer(b" ((())) foo")
    forward = Forward()
    forward.assign(Literal(b"(") + Opt(forward) + Literal(b")"))
    parse_tree = await forward.parse(buffer, 1)

    assert parse_tree == ParsedAnd(
        "(b'(') + ((forward)[0, 1]) + (b')')",
        (
            ParsedLiteral("b'('", b"(", 1, 2),
            ParsedOpt(
                None,
                (
                    ParsedAnd(
                        "(b'(') + ((forward)[0, 1]) + (b')')",
                        (
                            ParsedLiteral("b'('", b"(", 2, 3),
                            ParsedOpt(
                                None,
                                (
                                    ParsedAnd(
                                        "(b'(') + ((forward)[0, 1]) + (b')')",
                                        (
                                            ParsedLiteral("b'('", b"(", 3, 4),
                                            ParsedOpt(None, (), 4),
                                            ParsedLiteral("b')'", b")", 4, 5),
                                        ),
                                        3,
                                    ),
                                ),
                                3,
                            ),
                            ParsedLiteral("b')'", b")", 5, 6),
                        ),
                        2,
                    ),
                ),
                2,
            ),
            ParsedLiteral("b')'", b")", 6, 7),
        ),
        1,
    )


@pytest.mark.asyncio
async def test_forward_failure():
    buffer = BytesBuffer(b" ((()) foo")
    forward = Forward()
    forward.assign(Literal(b"(") + Opt(forward) + Literal(b")"))

    with pytest.raises(UnmetExpectationError):
        await forward.parse(buffer, 1)


def test_unmet_expectation_error_string_representation():
    class ParserStub(Parser[None, None]):
        def __init__(self):
            super().__init__("ParserStubName")

        async def parse(
            self, buf: ParserBuffer, loc: int = 0
        ) -> ParsedNode[None, None]:
            raise NotImplementedError

    buf = BytesBuffer(b"01234567890abcdef")
    err = UnmetExpectationError(ParserStub(), 12, buf)

    assert (
        str(err)
        == """expected ParserStubName at position 12

Input: b'01234567890abcdef'
                     ^ location of error
"""
    )
