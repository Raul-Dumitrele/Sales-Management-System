class Client:
    def __init__(self, id, nume):
        self.id = id
        self.nume = nume
        self.istoric_comenzi = []
        
    def to_dict(self):
        return {
            "id": self.id,
            "nume": self.nume
        }

    def __str__(self):
        return f"{self.nume} (ID: {self.id})"
    
    def adauga_comanda(self, comanda):
        self.istoric_comenzi.append(comanda)
        
    def total_cheltuieli(self):
        return sum(comanda.total() for comanda in self.istoric_comenzi)
    
    def are_comenzi(self):
        return len(self.istoric_comenzi) > 0
    
    def __eq__(self, other):
        if isinstance(other, Client):
            return self.id == other.id
        return False
