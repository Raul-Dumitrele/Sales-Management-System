import tkinter as tk
from tkinter import messagebox
from produs import Produs
from client import Client
from comanda import Comanda
from vanzari import Vanzari
from autentificare import Autentificare


def interfata_logare():
    auth = Autentificare()

    while True:
        print("\n=== Autentificare utilizator ===")
        print("1. Autentificare")
        print("2. Înregistrare")
        print("0. Ieșire")
        optiune = input("Alege o opțiune: ")

        if optiune == '1':
            username = input("Utilizator: ")
            parola = input("Parolă: ")
            rol = auth.autentifica_utilizator(username, parola)
            if rol:
                print(f"\n✅ Autentificat ca {username} (rol: {rol})\n")
                return username, rol  # îl ducem în meniul principal
            else:
                print("❌ Autentificare eșuată. Verifică datele.")

        elif optiune == '2':
            username = input("Alege un nume de utilizator: ")
            parola = input("Alege o parolă: ")
            rol = input("Rol (admin/vanzator): ").lower()
            if rol in ['admin', 'vanzator']:
                auth.inregistreaza_utilizator(username, parola, rol)
            else:
                print("⚠️ Rol invalid. Folosește doar 'admin' sau 'vanzator'.")

        elif optiune == '0':
            print("La revedere!")
            exit()

        else:
            print("⚠️ Opțiune invalidă.")

def main():
    vanzari = Vanzari()
    
    while True:
        print("\n--- Meniu ---")
        print("1. Adaugă produs")
        print("2. Adaugă client")
        print("3. Adaugă comandă")
        print("4. Afișează produse")
        print("5. Afișează clienți")
        print("6. Afișează comenzi")
        print("7. Șterge produs")
        print("8. Șterge client")
        print("9. Șterge comandă")
        print("10. Caută produs după nume")
        print("11. Caută produs după categorie")
        print("12. Caută comenzi după client")
        print("13. Filtrează comenzi după dată")
        print("14. Raport produse cu stoc scăzut")
        print("15. Top clienți")
        print("16. Top produse")
        print("17. Salvează datele")
        print("18. Încarcă datele")
        print("0. Ieșire")
        
        alegere = input("Alege o opțiune: ")
        
        if alegere == "1":
            # Adăugarea unui produs
            while True:
                id_produs_str = input("ID produs: ")
                try:
                    id_produs = int(id_produs_str)
                except ValueError:
                    print("❌ ID invalid. Vă rugăm să introduceți un număr.")
                    continue

                if any(produs.id == id_produs for produs in vanzari.produse):
                    new_id_produs = max(produs.id for produs in vanzari.produse) + 1
                    print(f"❌ ID-ul {id_produs} este deja folosit. S-a ales automat ID-ul {new_id_produs}.")
                    id_produs = new_id_produs
                
                nume = input("Nume produs: ")
                pret = float(input("Preț: "))
                stoc = int(input("Stoc: "))
                categorie= input("Categorie produs: ")
                vanzari.adauga_produs(Produs(id_produs, nume, pret, stoc,categorie))
                print("✅ Produs adăugat.")
                break

        elif alegere == "2":
            # Adăugarea unui client
            while True:
                id_client_str = input("ID client: ")
                try:
                    id_client = int(id_client_str)
                except ValueError:
                    print("❌ ID invalid. Vă rugăm să introduceți un număr.")
                    continue

                if any(client.id == id_client for client in vanzari.clienti):
                    new_id_client = max(client.id for client in vanzari.clienti) + 1
                    print(f"❌ ID-ul {id_client} este deja folosit. S-a ales automat ID-ul {new_id_client}.")
                    id_client = new_id_client
                
                nume = input("Nume client: ")
                vanzari.adauga_client(Client(id_client, nume))
                print("✅ Client adăugat.")
                break

        elif alegere == "3":
            # Adăugarea unei comenzi
            id_comanda_str = input("ID comandă: ")
            try:
                id_comanda = int(id_comanda_str)
            except ValueError:
                print("❌ ID invalid. Vă rugăm să introduceți un număr.")
                continue

            if any(comanda.id == id_comanda for comanda in vanzari.comenzi):
                new_id = max(comanda.id for comanda in vanzari.comenzi) + 1
                print(f"❌ ID-ul {id_comanda} este deja folosit. S-a ales automat ID-ul {new_id}.")
                id_comanda = new_id

            id_client = input("ID client: ")
            try:
                client = next((c for c in vanzari.clienti if str(c.id) == id_client), None)
                if not client:
                    print("❌ Client inexistent.")
                    continue
                print(f"✅ Clientul {client.nume} a fost găsit.")
            except ValueError:
                print("❌ ID client invalid. Vă rugăm să introduceți un ID valid.")
                continue

            produse = []
            while True:
                id_produs = input("ID produs (sau enter pentru a termina): ")
                if not id_produs:
                    break
                produs = next((p for p in vanzari.produse if str(p.id) == id_produs), None)
                if not produs:
                    print("❌ Produs inexistent.")
                    continue
                try:
                    cantitate = int(input("Cantitate: "))
                except ValueError:
                    print("❌ Cantitate invalidă.")
                    continue
                produse.append((produs, cantitate))

            try:
                vanzari.plaseaza_comanda(id_comanda, produse)
                print("✅ Comandă adăugată.")
            except ValueError as e:
                print(f"❌ Eroare: {e}")

        elif alegere == "4":
            # Afișare produse
            vanzari.afiseaza_produse()

        elif alegere == "5":
            # Afișare clienți
            vanzari.afiseaza_clienti()

        elif alegere == "6":
            # Afișare comenzi
            vanzari.afiseaza_comenzi()

        elif alegere == "7":
            # Șterge produs
            id_produs = input("ID produs de șters: ")
            if not any(produs.id == int(id_produs) for produs in vanzari.produse):
                print("❌ Produsul nu există.")
                continue
            vanzari.sterge_produs(id_produs)

        elif alegere == "8":
            # Șterge client
            id_client = input("ID client de șters: ")
            if not any(client.id == int(id_client) for client in vanzari.clienti):
                print("❌ Clientul nu există.")
                continue
            vanzari.sterge_client(id_client)

        elif alegere == "9":
            # Șterge comandă
            id_comanda = input("Introduceti ID-ul comenzii de sters: ")
            try:
                id_comanda = int(id_comanda)
                vanzari.sterge_comanda(id_comanda)
            except ValueError:
                print("❌ID invalid. Vă rugăm să introduceți un număr.")
        
        elif alegere == "10":
            # Căutare produs după nume
            nume_produs = input("Introduceți numele produsului de căutat: ")
            produse_gasite = vanzari.cauta_produs_dupa_nume(nume_produs)
            for produs in produse_gasite:
                print(produs)
            
        elif alegere == "11":
            # Căutare produs după categorie
            categorie_produs = input("Introduceți categoria produsului de căutat: ")
            produse_gasite = vanzari.cauta_produs_dupa_categorie(categorie_produs)
            for produs in produse_gasite:
                print(produs)
            
        elif alegere == "12":
            # Căutare comenzi după client
            nume_client = input("Introduceți numele clientului: ")
            comenzi_gasite = vanzari.cauta_comenzi_dupa_client(nume_client)
            for comanda in comenzi_gasite:
                print(comanda)

        elif alegere == "13":
            # Filtrare comenzi după dată
            data_start = input("Introduceți data de început (YYYY-MM-DD): ")
            data_end = input("Introduceți data de sfârșit (YYYY-MM-DD): ")
            data_start = datetime.strptime(data_start, "%Y-%m-%d")
            data_end = datetime.strptime(data_end, "%Y-%m-%d")
            comenzi_filtrate = vanzari.filtreaza_comenzi_dupa_data(data_start, data_end)
            for comanda in comenzi_filtrate:
                print(comanda)

        elif alegere == "14":
            # Raport produse cu stoc scăzut
            prag = int(input("Introduceți pragul pentru stocuri scăzute: "))
            vanzari.raporteaza_stocuri_scazute(prag)

        elif alegere == "15":
            # Top clienți
            top_clienti = vanzari.top_clienti()
            for client in top_clienti:
                print(client)

        elif alegere == "16":
            # Top produse
            top_produse = vanzari.top_produse()
            for produs, cantitate in top_produse:
                print(f"{produs}: {cantitate} vândute")

        elif alegere == "17":
            # Salvare date
            fisier = input("Introduceți numele fișierului pentru salvare: ")
            vanzari.salveaza_date(fisier)
            print("✅ Datele au fost salvate.")

        elif alegere == "18":
            # Încărcare date
            fisier = input("Introduceți numele fișierului pentru încărcare: ")
            vanzari.incarca_date(fisier)
            print("✅ Datele au fost încărcate.")

        elif alegere == "0":
            # Ieșire
            print("👋 La revedere!")
            break

        else:
            print("⚠️ Opțiune invalidă.")


if __name__ == "__main__":
    utilizator, rol = interfata_logare()
    
    # Aici putem adăuga verificări pe rolul utilizatorului pentru acces la funcții
    if rol == "admin":
        print("\nAcces pentru administratori.")
        # Poți adăuga funcționalități suplimentare pentru admini
    elif rol == "vanzator":
        print("\nAcces pentru vânzători.")
        # Poți adăuga funcționalități suplimentare pentru vânzători
    main()