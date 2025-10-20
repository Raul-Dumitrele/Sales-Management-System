import json
from produs import Produs
from client import Client
from comanda import Comanda

class Vanzari:
    def __init__(self):
        self.produse = []
        self.clienti = []
        self.comenzi = []
        
    def adauga_produs(self, produs):
        self.produse.append(produs)

    def adauga_client(self, client):
        self.clienti.append(client)
    
    def plaseaza_comanda(self, id_client, produse):
        client = next((client for client in self.clienti if client.id == id_client), None)
        if not client:
            print("❌ Clientul nu a fost găsit!")
            return
        
        print(f"Client găsit: {client.nume}")
        
        for produs, cantitate in produse:
            if produs.stoc < cantitate:
                print(f"❌ Stoc insuficient pentru produsul {produs.nume}.")
                return
            produs.stoc -= cantitate
            
        comanda = Comanda(len(self.comenzi) + 1, client, produse)
        self.comenzi.append(comanda)
        print(f"✅ Comanda pentru clientul {client.nume} a fost plasată.")
        print(comanda)
        
        print(f"Produse rămase în stoc:")
        self.afiseaza_produse()
        
    def afiseaza_produse(self):
        print("\nProduse disponibile:")
        for p in self.produse:
            print(p)

    def afiseaza_clienti(self):
        print("\nClienți:")
        for c in self.clienti:
            print(c)

    def afiseaza_comenzi(self):
        print("\nComenzi:")
        for com in self.comenzi:
            print(com)

    def sterge_produs(self, id):
        id = int(id)  # 👈 Conversie
        produs_de_sters = next((p for p in self.produse if p.id == id), None)
        if produs_de_sters:
            self.produse.remove(produs_de_sters)
            print("🗑️ Produs șters.")
        else:
            print("❌ Produsul nu a fost găsit.")

    def sterge_client(self, id_client):
        id_client = int(id_client)  # 👈 Conversie
        client_de_sters = next((c for c in self.clienti if c.id == id_client), None)
        if client_de_sters:
            self.clienti.remove(client_de_sters)
            print("🗑️ Client șters.")
        else:
            print("❌ Clientul nu a fost găsit.")

    def sterge_comanda(self, id_comanda):
        comanda_de_sters = next((comanda for comanda in self.comenzi if comanda.id == id_comanda), None)
        if comanda_de_sters:
            self.comenzi.remove(comanda_de_sters)
            print(f"✅ Comanda cu ID-ul {id_comanda} a fost ștearsă.")
        else:
            print(f"❌ Comanda cu ID-ul {id_comanda} nu a fost găsită.")

    def cauta_produs_dupa_nume(self, nume):
        return [p for p in self.produse if nume.lower() in p.nume.lower()]

    def cauta_produs_dupa_categorie(self, categorie):
        return [p for p in self.produse if categorie.lower() in p.categorie.lower()]
    
    def cauta_comenzi_dupa_client(self, nume_client):
        return [c for c in self.comenzi if c.client.nume.lower() == nume_client.lower()]

    def filtreaza_comenzi_dupa_data(self, data_start, data_end):
        return [com for com in self.comenzi if data_start <= com.data <= data_end]

    def raporteaza_stocuri_scazute(self, prag=5):
        print(f"\n📉 Produse cu stoc sub {prag}:")
        for produs in self.produse:
            if produs.stoc < prag:
                print(produs)

    def top_clienti(self):
        return sorted(self.clienti, key=lambda c: sum(cmd.total() for cmd in c.istoric_comenzi), reverse=True)

    def top_produse(self):
        vanzari = {}
        for comanda in self.comenzi:
            for p, q in comanda.produse:
                vanzari[p.nume] = vanzari.get(p.nume, 0) + q
        return sorted(vanzari.items(), key=lambda x: x[1], reverse=True)

    def salveaza_date(self, fisier):
        data = {
            "produse": [produs.to_dict() for produs in self.produse],
            "clienti": [client.to_dict() for client in self.clienti],
            "comenzi": [comanda.to_dict() for comanda in self.comenzi]
        }
        with open(fisier, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("✅ Datele au fost salvate cu succes.")

    def incarca_date(self, fisier):
        try:
            with open(fisier, "r") as f:
                data = json.load(f)
            
            self.produse = [Produs(**p) for p in data["produse"]]
            self.clienti = [Client(**c) for c in data["clienti"]]
            self.comenzi = []
            for comanda_data in data["comenzi"]:
                client = next((c for c in self.clienti if c.id == comanda_data["client"]["id"]), None)
                if client:
                    produse = []
                    for p_data in comanda_data["produse"]:
                        produs = next((p for p in self.produse if p.id == p_data[0]["id"]), None)
                        if produs:
                            produse.append((produs, p_data[1]))
                    self.comenzi.append(Comanda(comanda_data["id"], client, produse))
        except json.JSONDecodeError as e:
            print(f"Eroare la decodarea fișierului JSON: {e}")
        except FileNotFoundError:
            print("Fișierul nu a fost găsit!")
        except Exception as e:
            print(f"A apărut o eroare: {e}")
