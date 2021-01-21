from lexer_items.comment import Comment
from lexer_items.keyword_ import Keyword
from lexer_items.multi_line_comment import MultiLineComment
from lexer_items.number_ import Number
from lexer_items.numbers_hex_bin import NumberHexBin
from lexer_items.operator_ import Operator
from lexer_items.punctuation import Punctuation
from lexer_items.special_symbol import SpecialSymbol
from lexer_items.string_ import String
from lexer_items.whitespace import Whitespace

class Utils:
    MATCHERS = [
        Operator(),
        Number(),
        NumberHexBin(),
        SpecialSymbol(),
        Punctuation(),
        Keyword(),
        Whitespace(),
        String(),
        Comment(),
        MultiLineComment()
    ]



