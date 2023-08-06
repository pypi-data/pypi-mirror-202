import sys

from .symbol import (
    _symbolScopeType,
    GlobalSymbol
)

class Handler:
    def __init__(self, symbolObject, expression, handledMode=0, handledFunction=None, *handledFunctionParams):
        if symbolObject.type == _symbolScopeType.GLOBAL.value:  # Synchronize symbols of executed python global scope.
            sys.path.append(symbolObject.path)
            exec("import {}".format(symbolObject.name))
            # Adding the owning module prefix to the import symbols in the statement.
            for symbols_index in range(0, len(symbolObject.symbols)):
                symbol = symbolObject.symbols[symbols_index]
                symbolAppearIndexList = []
                newExpression = ""
                expression_index = 0
                while expression_index < len(expression) + 1:
                    symbolAppearIndex = expression.find(symbol, expression_index, len(expression))
                    if symbolAppearIndex != -1 and (symbolAppearIndex == 0 or (expression[symbolAppearIndex - 1] != "." and expression[symbolAppearIndex + len(symbol)] != "." and (expression[symbolAppearIndex - 1] == "," or expression[symbolAppearIndex - 1] == "("))):
                        symbolAppearIndexList.append(symbolAppearIndex)
                        # Splits expressions and inserts prefixed symbols.
                        if len(symbolAppearIndexList) == 1:
                            if symbolAppearIndexList[-1] == 0:
                                newExpression = symbolObject.name + "." + symbol
                            else:
                                newExpression = expression[0:symbolAppearIndexList[-1]] + symbolObject.name + "." + symbol
                        elif len(symbolAppearIndexList) > 1:
                            newExpression = newExpression + expression[symbolAppearIndexList[-2] + len(symbol):symbolAppearIndexList[-1]] + symbolObject.name + "." + symbol

                        expression_index += symbolAppearIndex + len(symbol)
                    else:
                        expression_index += 1
                # Complete the remaining unmerged non-symbolic slices at the end of the expression.
                if len(symbolAppearIndexList) != 0:
                    if len(expression) == symbolAppearIndexList[-1] + len(symbol):
                        expression = newExpression
                    else:
                        expression = newExpression + expression[symbolAppearIndexList[-1] + len(symbol):len(expression)]

        if handledMode == 0:
            # Judge the exception.
            try:
                    self.__m_value = eval(expression)
            except:
                    self.__m_status = False
            else:
                    self.__m_status = True
            # Function handle.
            if self.__m_status == False:
                if handledFunction != None:
                    handledFunction(*handledFunctionParams)
                self.__m_value = None

    @property
    def value(self):
        return self.__m_value

    @property
    def status(self):
        return self.__m_status