class Converter():
    def __init__(self):
        
        self.length_factors = {
            "m" : 1,
            "km" : 0.001,
            "cm" : 100,
            "mm" : 1000
        }

        self.weight_factors = {
            'g' : 1,
            'kg' : 0.001,
            'mg' : 1000,
            'pounds' : 0.00220462,
            'ounces' : 0.035274
        }

    def convert_length(self, value : float, unit_from : str, unit_to: str) -> float: 

        if unit_from not in self.length_factors or unit_to not in self.length_factors:
            return "UnsupportedUnit"
        
        else:
            meters = value / self.length_factors[unit_from]
            
            return meters * self.lenght_factors[unit_to]
        
    def convert_weight(self, value : float, unit_from : str, unit_to : str) -> float:

        if unit_from not in self.weight_factors or unit_to not in self.weight_factors:
            return "UnsupportedUnit"
        
        else:
            
            grams = value / self.weight_factors[unit_from]
            
            return grams * self.weight_factors[unit_to]
        
    def convert_temperature(self, value: float, unit_from: str, unit_to: str) -> float:
        if unit_from == unit_to:
            return value
        
        if unit_from == 'C':
            if unit_to == 'F':
                return (value * 9/5) + 32
            elif unit_to == 'K':
                return value + 273.15
        elif unit_from == 'F':
            if unit_to == 'C':
                return (value - 32) * 5/9
            elif unit_to == 'K':
                return (value - 32) * 5/9 + 273.15
        elif unit_from == 'K':
            if unit_to == 'C':
                return value - 273.15
            elif unit_to == 'F':
                return (value - 273.15) * 9/5 + 32
        
        else:
            return "UnsupportedUnit"