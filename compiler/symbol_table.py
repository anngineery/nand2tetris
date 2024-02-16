"""
When compiling error-free Jack code, any identifier not found in the symbol table
maybe assumed to be a subroutine name or a class name.
"""
from enum import Enum


class Category (str, Enum):
    STATIC ="static"
    FIELD = "field"
    ARGUMENT = "argument"
    VARIALBE = "var"


class SymbolTable:
    """
    Associates the identifier names in the HL program with properties needed for
    compilation. (ex: data type, category and index within the category)
    It has 2 scopes: class (only field and static) and subroutine (only argument and variable).
    """
    def __init__(self): 
        self.class_table = {}
        self.subroutine_table = {}
        self.index_table = {
            Category.STATIC: 0,
            Category.FIELD: 0,
            Category.ARGUMENT: 0,
            Category.VARIALBE: 0,
        }

    def start_subroutine(self): 
        self.subroutine_table = {}  # reset
        self.index_table[Category.ARGUMENT] = 0
        self.index_table[Category.VARIALBE] = 0

    def define(self, name: str, data_type: str, category: Category): 
        if category in [Category.STATIC, Category.FIELD]:
            self.class_table[name] = (data_type, category, self.index_table[category])
        else:
            self.subroutine_table[name] = (data_type, category, self.index_table[category])

        self.index_table[category] += 1        

    def count_variables(self, category: Category) -> int:
        return self.index_table[category]

    def which_data_type(self, name: str) -> str:
        try:
            return self.subroutine_table[name][0]
        
        except KeyError:
            try:
                return self.class_table[name][0]

            except KeyError:
                return None

    def which_category(self, name: str) -> Category:
        try:
            return self.subroutine_table[name][1]
        
        except KeyError:
            try:
                return self.class_table[name][1]

            except KeyError:
                return None
    
    def which_index(self, name: str) -> int:
        try:
            return self.subroutine_table[name][2]
        
        except KeyError:
            try:
                return self.class_table[name][2]

            except KeyError:
                return None
            
    def print(self):
        # only for debugging
        print(f"class table:\n{self.class_table}")
        print(f"subroutine table:\n{self.subroutine_table}")