from datetime import datetime

class Comanda:
    def __init__(self, id, client, produse, data=None):
        self.id = id
        self.client = client
        self.produse = produse
        self.data = data if data else datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "client": self.client.to_dict(),
            "produse": [(produs.to_dict(), cantitate) for produs, cantitate in self.produse],
            "data": self.data.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def total(self):
        return sum(prod.pret * cant for prod, cant in self.produse)
    
    def __str__(self):
        lista = "\n  ".join([f"{prod.nume} x{cant}" for prod, cant in self.produse])
        return f"Comanda #{self.id} de la {self.client.nume}:\n  {lista}\n  Total: {self.total()} lei"
    
    def __eq__(self, other):
        if isinstance(other, Comanda):
            return self.id == other.id
        return False
