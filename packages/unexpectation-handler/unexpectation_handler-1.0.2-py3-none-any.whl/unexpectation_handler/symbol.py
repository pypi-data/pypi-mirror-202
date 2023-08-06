from enum import Enum
_symbolScopeType = Enum('SymbolScopeType', ('GLOBAL'))

class GlobalSymbol:
    type = _symbolScopeType.GLOBAL.value

    def __init__(self, pythonFilePath, globalSymbols):
        self.__m_filePath = pythonFilePath
        self.__m_globalSymbols = globalSymbols

    @property
    def path(self):
        return self.__m_filePath

    @property
    def name(self):
        return self.__m_filePath.split("\\")[-1].split(".")[0]

    @property
    def symbols(self):
        symbols = []
        for symbol in self.__m_globalSymbols:
            symbols.append(symbol)
        return symbols