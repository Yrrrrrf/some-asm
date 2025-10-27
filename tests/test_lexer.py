"""Tests for the 8086 assembly lexer."""

import sys
from pathlib import Path

# Add the src directory to the path so we can import from core
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.lexer import Lexer, Token


def _analyze_tokens(source_code: str) -> list[Token]:
    """Helper function to analyze source code and return tokens."""
    lexer = Lexer(source_code)
    return lexer.analyze()


def _assert_token(tokens: list[Token], index: int, value: str, token_type: str) -> None:
    """Helper function to assert token properties."""
    assert tokens[index].value == value
    assert tokens[index].type == token_type


def test_basic_tokenization() -> None:
    """Test basic tokenization functionality."""
    source_code = """
    .DATA SEGMENT
        msg DB 'Hello', 10
    .DATA ENDS
    """
    
    tokens = _analyze_tokens(source_code)
    
    # Verify we have the expected tokens
    assert len(tokens) == 7  # .DATA SEGMENT, msg, DB, 'Hello', ',', 10, .DATA ENDS
    
    # Check specific tokens
    _assert_token(tokens, 0, ".DATA SEGMENT", "PSEUDOINSTRUCCIÓN")
    _assert_token(tokens, 1, "msg", "SÍMBOLO")
    _assert_token(tokens, 2, "DB", "PSEUDOINSTRUCCIÓN")
    _assert_token(tokens, 3, "'Hello'", "CONSTANTE_STR")
    _assert_token(tokens, 4, ",", "SEPARADOR")
    _assert_token(tokens, 5, "10", "CONSTANTE_DEC")
    _assert_token(tokens, 6, ".DATA ENDS", "PSEUDOINSTRUCCIÓN")


def test_register_recognition() -> None:
    """Test that registers are correctly identified."""
    source_code = "MOV AX, BX"
    
    tokens = _analyze_tokens(source_code)
    
    assert len(tokens) == 4  # MOV, AX, ,, BX
    
    # MOV is not in our specific instructions list, so it should be SÍMBOLO
    _assert_token(tokens, 0, "MOV", "SÍMBOLO")
    _assert_token(tokens, 1, "AX", "REGISTRO")
    _assert_token(tokens, 2, ",", "SEPARADOR")
    _assert_token(tokens, 3, "BX", "REGISTRO")


def test_hexadecimal_constants() -> None:
    """Test hexadecimal constant recognition."""
    # Test 'h' suffix
    source_code = "MOV AX, 0ABCDh"
    tokens = _analyze_tokens(source_code)
    _assert_token(tokens, 3, "0ABCDh", "CONSTANTE_HEX")
    
    # Test 0x prefix
    source_code = "MOV AX, 0xABCD"
    tokens = _analyze_tokens(source_code)
    _assert_token(tokens, 3, "0xABCD", "CONSTANTE_HEX")


def test_binary_constants() -> None:
    """Test binary constant recognition."""
    source_code = "MOV AX, 1010b"
    
    tokens = _analyze_tokens(source_code)
    _assert_token(tokens, 3, "1010b", "CONSTANTE_BIN")


def test_comment_removal() -> None:
    """Test that comments are properly removed."""
    source_code = """MOV AX, BX ; This is a comment
    ; This is a full line comment
    MOV CX, DX"""
    
    tokens = _analyze_tokens(source_code)
    
    # Should only have 8 tokens: MOV, AX, ,, BX, MOV, CX, ,, DX
    assert len(tokens) == 8
    _assert_token(tokens, 0, "MOV", "SÍMBOLO")
    _assert_token(tokens, 1, "AX", "REGISTRO")
    _assert_token(tokens, 2, ",", "SEPARADOR")
    _assert_token(tokens, 3, "BX", "REGISTRO")
    _assert_token(tokens, 4, "MOV", "SÍMBOLO")
    _assert_token(tokens, 5, "CX", "REGISTRO")
    _assert_token(tokens, 6, ",", "SEPARADOR")
    _assert_token(tokens, 7, "DX", "REGISTRO")


def test_instruction_recognition() -> None:
    """Test that specified instructions are recognized."""
    source_code = "HLT ADC"
    
    tokens = _analyze_tokens(source_code)
    
    _assert_token(tokens, 0, "HLT", "INSTRUCCIÓN")
    _assert_token(tokens, 1, "ADC", "INSTRUCCIÓN")


def test_string_constants() -> None:
    """Test string constant recognition."""
    source_code = 'DB "Hello", \'World\''
    
    tokens = _analyze_tokens(source_code)
    
    assert len(tokens) == 4  # DB, "Hello", ,, 'World'
    _assert_token(tokens, 0, "DB", "PSEUDOINSTRUCCIÓN")
    _assert_token(tokens, 1, '"Hello"', "CONSTANTE_STR")
    _assert_token(tokens, 2, ",", "SEPARADOR")
    _assert_token(tokens, 3, "'World'", "CONSTANTE_STR")


def test_bracket_expressions() -> None:
    """Test bracket expression recognition."""
    source_code = "MOV AX, [BX]"
    
    tokens = _analyze_tokens(source_code)
    
    assert len(tokens) == 6  # MOV, AX, ,, [, BX, ]
    _assert_token(tokens, 0, "MOV", "SÍMBOLO")
    _assert_token(tokens, 1, "AX", "REGISTRO")
    _assert_token(tokens, 2, ",", "SEPARADOR")
    _assert_token(tokens, 3, "[", "SEPARADOR")
    _assert_token(tokens, 4, "BX", "REGISTRO")
    _assert_token(tokens, 5, "]", "SEPARADOR")


if __name__ == "__main__":
    test_basic_tokenization()
    test_register_recognition()
    test_hexadecimal_constants()
    test_binary_constants()
    test_comment_removal()
    test_instruction_recognition()
    test_string_constants()
    test_bracket_expressions()
    print("All tests passed!")