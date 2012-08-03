class Var:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
    def __hash__(self):
        return hash(self.symbol)
    
    def __repr__(self):
        return "<%s>" % self.symbol


empty_s = {}
s1 = {Var("x"): 5, Var("y"): True}
s2 = {Var("y"): 5, Var("x"): Var("y")}
