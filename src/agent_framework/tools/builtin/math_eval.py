"""Math evaluation tool - safe arithmetic operations."""

from typing import Any
import operator
from ...base.tool import BaseTool


class MathEvalTool(BaseTool):
    """
    Safe math evaluation tool.
    
    Supports basic arithmetic operations: +, -, *, /
    Does NOT use eval() for security.
    """
    
    # Safe operators mapping
    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }
    
    @property
    def name(self) -> str:
        return "math_eval"
    
    @property
    def description(self) -> str:
        return "Evaluates a simple math expression with two operands. Supports +, -, *, /"
    
    @property
    def params_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First operand"
                },
                "operator": {
                    "type": "string",
                    "description": "Operation to perform",
                    "enum": ["+", "-", "*", "/"]
                },
                "b": {
                    "type": "number",
                    "description": "Second operand"
                }
            },
            "required": ["a", "operator", "b"]
        }
    
    def __call__(self, a: float, operator: str, b: float, **kwargs) -> float:
        """
        Evaluate a simple arithmetic expression.
        
        Args:
            a: First operand
            operator: One of +, -, *, /
            b: Second operand
            
        Returns:
            Result of the operation
            
        Raises:
            ValueError: If operator is not supported
            ZeroDivisionError: If dividing by zero
        """
        if operator not in self.OPERATORS:
            raise ValueError(f"Unsupported operator: {operator}")
        
        op_func = self.OPERATORS[operator]
        return op_func(a, b)
