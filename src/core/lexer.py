"""Implementation of the lexical analyzer for 8086 assembly code."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from collections.abc import Generator


class Token(BaseModel):
    """Represents a lexical token with its value, type, and line number."""
    
    value: str
    type: str
    line: int


# Define the dictionaries for fast lookup
INSTRUCTIONS = {
    "AAA", "AAD", "HLT", "INTO", "SCASW", "STC", 
    "DEC", "IDIV", "IMUL", "POP", "ADC", "CMP", 
    "LES", "LDS", "JAE", "JC", "JGE", "JNB", "JNG", "JNO"
}

REGISTERS = {
    # 16-bit registers
    "AX", "BX", "CX", "DX", "SI", "DI", "SP", "BP",
    # 8-bit registers 
    "AL", "AH", "BL", "BH", "CL", "CH", "DL", "DH",
    # Segment registers
    "CS", "DS", "SS", "ES"
}

PSEUDO_INSTRUCTIONS = {
    ".CODE SEGMENT", ".DATA SEGMENT", ".STACK SEGMENT", 
    ".CODE ENDS", ".DATA ENDS", ".STACK ENDS",
    "DUP", "DB", "DW", "DD", "EQU", "ORG"
}

TYPES = {
    "BYTE PTR", "WORD PTR"
}


class Lexer:
    """Lexical analyzer for 8086 assembly code."""
    
    def __init__(self, source_code: str) -> None:
        """Initialize the lexer with the source code.
        
        Args:
            source_code: The complete source code as a single string
        """
        self.source_code = source_code
        self.tokens: list[Token] = []
    
    def _clean_code(self) -> str:
        """Remove comments from the source code.
        
        Returns:
            Source code with comments removed
        """
        lines = self.source_code.split('\n')
        cleaned_lines = []
        for i, line in enumerate(lines):
            # Find comment start
            comment_pos = line.find(';')
            if comment_pos != -1:
                # Remove everything from the comment onwards
                cleaned_line = line[:comment_pos].strip()
            else:
                cleaned_line = line.strip()
            
            if cleaned_line:  # Only add non-empty lines
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def _is_hex_constant(self, value: str) -> bool:
        """Check if a value is a hexadecimal constant.
        
        Args:
            value: String to check
            
        Returns:
            True if it's a hex constant, False otherwise
        """
        # Check for 0x prefix
        if value.upper().startswith('0X'):
            hex_part = value[2:]
            return bool(re.fullmatch(r'[0-9A-F]+', hex_part))
        
        # Check for trailing 'h' or 'H'
        if value.upper().endswith('H') and len(value) > 1:
            hex_part = value[:-1]
            return bool(re.fullmatch(r'[0-9A-F]+', hex_part))
        
        return False
    
    def _is_binary_constant(self, value: str) -> bool:
        """Check if a value is a binary constant.
        
        Args:
            value: String to check
            
        Returns:
            True if it's a binary constant, False otherwise
        """
        if value.upper().endswith('B') and len(value) > 1:
            bin_part = value[:-1]
            return bool(re.fullmatch(r'[01]+', bin_part))
        
        return False
    
    def _is_decimal_constant(self, value: str) -> bool:
        """Check if a value is a decimal constant.
        
        Args:
            value: String to check
            
        Returns:
            True if it's a decimal constant, False otherwise
        """
        return bool(re.fullmatch(r'[0-9]+', value))
    
    def _is_string_constant(self, value: str) -> bool:
        """Check if a value is a string constant.
        
        Args:
            value: String to check
            
        Returns:
            True if it's a string constant, False otherwise
        """
        # Check if it starts and ends with quotes (single or double)
        if len(value) >= 2:
            if (value.startswith("'") and value.endswith("'")) or \
               (value.startswith('"') and value.endswith('"')):
                return True
        return False
    
    def _classify(self, token_value: str, line_num: int) -> str:
        """Classify a token based on its value.
        
        Args:
            token_value: The value of the token to classify
            line_num: The line number where the token was found
            
        Returns:
            The type of the token
        """
        upper_value = token_value.upper()
        
        # Check for instructions
        if upper_value in INSTRUCTIONS:
            return "INSTRUCCIÓN"
        
        # Check for registers
        if upper_value in REGISTERS:
            return "REGISTRO"
        
        # Check for type specifiers
        if upper_value in TYPES:
            return "TIPO_DATO"
        
        # Check for constants
        if self._is_hex_constant(upper_value):
            return "CONSTANTE_HEX"
        if self._is_binary_constant(upper_value):
            return "CONSTANTE_BIN"
        if self._is_decimal_constant(token_value):
            return "CONSTANTE_DEC"
        if self._is_string_constant(token_value):
            return "CONSTANTE_STR"
        
        # Check for pseudoinstructions
        if token_value in PSEUDO_INSTRUCTIONS:
            return "PSEUDOINSTRUCCIÓN"
        
        # Default to symbol for everything else
        return "SÍMBOLO"
    
    def _tokenize(self) -> Generator[Token, None, None]:
        """Tokenize the cleaned source code.
        
        Yields:
            Token: A token from the source code
        """
        cleaned_code = self._clean_code()
        lines = cleaned_code.split('\n')
        
        for line_num, original_line in enumerate(lines, start=1):
            if not original_line.strip():
                continue
                
            # First, handle pseudoinstructions as single tokens by replacing them with markers
            line = original_line
            markers = {}
            
            for pseudo in PSEUDO_INSTRUCTIONS:
                if pseudo in line:
                    # Create a unique marker for this pseudoinstruction
                    marker = f"___PSEUDO_{len(markers)}___"
                    line = line.replace(pseudo, marker)
                    markers[marker] = pseudo
            
            # Process the line character by character
            i = 0
            current_token = ""
            
            while i < len(line):
                char = line[i]
                
                # Check if we're at a pseudoinstruction marker
                marker_found = False
                for marker, pseudo_value in markers.items():
                    if line[i:].startswith(marker):
                        if current_token.strip():
                            yield from self._process_simple_token(current_token.strip(), line_num)
                            current_token = ""
                        # Yield the pseudoinstruction token
                        yield Token(value=pseudo_value, type="PSEUDOINSTRUCCIÓN", line=line_num)
                        i += len(marker)  # Skip the marker
                        marker_found = True
                        break
                
                if marker_found:
                    continue
                
                # Handle quoted strings
                if char in ['"', "'"]:
                    if current_token.strip():
                        yield from self._process_simple_token(current_token.strip(), line_num)
                        current_token = ""
                    
                    # Extract the full quoted string
                    quote_char = char
                    quote_start = i
                    i += 1  # Skip opening quote
                    
                    while i < len(line) and line[i] != quote_char:
                        current_token += line[i]
                        i += 1
                    
                    if i < len(line) and line[i] == quote_char:
                        # Complete quoted string found
                        quoted_value = quote_char + current_token + quote_char
                        yield Token(value=quoted_value, type="CONSTANTE_STR", line=line_num)
                        current_token = ""
                        i += 1  # Skip closing quote
                    else:
                        # Unmatched quote - treat as error or regular token
                        current_token = quote_char + current_token
                        i += 1
                
                # Handle whitespace as separator
                elif char.isspace():
                    if current_token.strip():
                        yield from self._process_simple_token(current_token.strip(), line_num)
                        current_token = ""
                    i += 1
                
                # Handle separators
                elif char in [',', ':']:
                    if current_token.strip():
                        yield from self._process_simple_token(current_token.strip(), line_num)
                        current_token = ""
                    yield Token(value=char, type="SEPARADOR", line=line_num)
                    i += 1
                
                # Handle bracket operators
                elif char in ['[', ']']:
                    if current_token.strip():
                        yield from self._process_simple_token(current_token.strip(), line_num)
                        current_token = ""
                    yield Token(value=char, type="SEPARADOR", line=line_num)
                    i += 1
                
                # Add character to current token
                else:
                    current_token += char
                    i += 1
            
            # Yield any remaining token
            if current_token.strip():
                yield from self._process_simple_token(current_token.strip(), line_num)
    
    def _process_simple_token(self, token: str, line_num: int) -> Generator[Token, None, None]:
        """Process a simple token that doesn't contain special constructs.
        
        Args:
            token: The token string to process
            line_num: Line number for the token
            
        Yields:
            Token: Processed tokens from the simple token
        """
        # Check if it's a bracket expression like [xxx]
        if token.startswith('[') and token.endswith(']'):
            yield Token(value=token, type="OPERADOR_COMPUESTO", line=line_num)
        else:
            # Classify and yield the token
            token_type = self._classify(token, line_num)
            yield Token(value=token, type=token_type, line=line_num)
    
    def analyze(self) -> list[Token]:
        """Run the lexical analysis on the source code.
        
        Returns:
            A list of tokens extracted from the source code
        """
        self.tokens = list(self._tokenize())
        return self.tokens