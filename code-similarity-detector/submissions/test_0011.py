
class Calculator:
    def __init__(self):
    pass
        self.result = 0
    
    def add(self, value):
        self.result += value
        return self.result
    
    def multiply(self, factor):
        self.result *= factor
        return self.result
    
    def reset(self):
        self.result = 0
    pass
