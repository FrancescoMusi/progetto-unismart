import csv
import os

#funzione che pulisce lo schermo
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


#funzione che rimuove spazi da una stringa data
def removeSpaces(string):
    return string.replace(" ", "")


#funzione che ferma il programma
def stop():
    input("\nPremi invio per continuare..")


#funzione che stampa tutte le matricole
def stampaMatricole(rowsMatricole):
    clear()
    print("\nLista matricole")
    for row in rowsMatricole[1:]:
        print("\n- matricola: {}\n- cognome: {}\n- nome: {}".format(row[0], row[1], row[2]))
    stop()


#funzione che stampa una matricola chiedendo in input l'id
def stampaMatricola(rowsMatricole):
    clear()  
    name = getName(rowsMatricole)
    print("\n- cognome: {}\n- nome: {}".format(name[0], name[1]))
    stop()


#funzione che aggiunge una matricola al file matricole.csv
def InserisciMatricola(rowsMatricole, fileMatricole):
    clear()
        
    correctName = False
    while not correctName:
        cognome = ""
        nome = ""

        #controlla che il cognome non sia vuoto
        while cognome == "":
            cognome = input("Cognome: ")
            clear()

        #controlla che il nome non sia vuoto
        while nome == "": 
            nome = input("Nome: ")
            clear()

        cognome = correctSintax(cognome)
        nome = correctSintax(nome)

        #conferna del nome con error handling
        correctName = checkData("{} {} è il nome corretto?".format(cognome, nome))
    
    #fine ciclo inserimento nome


    index = len(rowsMatricole) #prossimo numero matricola
    row = [index, cognome, nome]

    appendFile(fileMatricole, [row])

    print("Matricola inserita correttamente!")
    stop()



def PagaEsami(rowsMatricole, rowsEsami, fileEsami):
    clear()

    correctName = False
    while not correctName:
        name = getName(rowsMatricole)
        examsToDo = getExams(name[2], rowsEsami, "to do")
        correctName = checkData("{} {} è la matricola di cui vuoi pagare gli esami?".format(name[0], name[1]))

    
    x = printExams(name, rowsEsami, "to pay") #solo se non ci sono esami da stampare ritorna False

    if not x:
        stop()
    
    else: 
        print("\nQuali esmai vuoi pagare? scrivi una lista separata da virgole (es: \"1, 3\")")
        

        #ciclo che fa inserire una lista scritta correttamente
        while True:
            toPay = input()

            #rimuove spazi e rende la stringa una lista
            toPay = removeSpaces(toPay)

            try:
                toPay = toPay.split(",")
                totalPrice = 0

                print(toPay)
                print(examsToDo)
                stop()
            
                #ciclo che fa inserire una lista con numeri corretti.
                for n in toPay:
                    for exam in examsToDo:
                        if exam[0] == n-1: #[0] è l'indice dell'esame
                            totalPrice += int(exam[2]) #[2] è il prezzo dell'esame in questione
                    
                            
                        #riscrive le righe del file esami
                        #for row in rowsEsami[1:]:
                        #    if int(row[0]) == name[2] and row[1] == exam[1]: #se numero matricola e nome esame corrispondono
                        #        row[3] = "True"

                
                print("\nPREZZO TOTALE: {}eur".format(totalPrice))
                input("premi invio per pagare..")
                print("\nesami pagati correttamente!")

                break #finisce il ciclo
            
            except: #per qualsiasi errore nell'inserimento parte except
                print("inserisci la lista correttamente, con interi ed esami esistenti!")

    
        #riscrive il file
        writeFile(fileEsami, rowsEsami)
            

        stop()



#funzione che controlla se è un intero
def checkInt(n):
    while True:
        try:
            n = int(n)
            break
        except:
            n = input("Inserisci un intero!\n")
    
    return n



#funzione che riscrive il file
def writeFile(path, rows):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)



#funzione che aggiunge righe al file
def appendFile(path, rows):
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)




#funzione che stampa le opzioni selezionabili
def options():
    clear()
    print("Cosa vuoi fare?\n" +
        "0. esci\n" + 
        "1. visualizza matricole\n" + 
        "2. ricerca studente con numero matricola\n" + 
        "3. ricerca esami con numero matricola\n" +
        "4. inserisci nuovo studente\n" + 
        "5. paga esami\n" + 
        "6. aggiungi esito esame\n")

    choice = checkInt(input())
    return choice



#funzione che legge file, controlla ed elimina eventuali righe vuote
def readFile(path):
    rows = []
    
    #legge le righe
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    
    #controlla ed elimina righe vuote
    changed = False
    while ["", "", ""] in rows:
        rows.remove(["", "", ""])
        changed = True

    while [] in rows:
        rows.remove([])
        changed = True


    #se ha trovato righe vuote riscrive file
    if changed:
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)

    return rows



#funzione che controlla i dati
def checkData(message):
    clear()
    c = ""
    while c.lower() != "s" and c.lower() != "n":
        c = input(message + " (S/N): ")
        clear()
        if c.lower() == "s":
            return True
        else: 
            return False



def getName(rowsMatricole):
    m = checkInt(input("Inserisci numero matricola: "))
    lista = [] #[cognome, nome, matricola]
    
    #trova nome e cognome
    userFound = False
    while not userFound:
        for row in rowsMatricole[1:]:
            if int(row[0]) == m:
                lista.append(row[1])
                lista.append(row[2])
                lista.append(m)
                userFound = True
        
        if not userFound: 
            m = checkInt(input("Utente non trovato, inserisci un numero diverso!\n"))

    
    return lista 



def getExams(m, rowsEsami, mode):
    examsDone = []
    examsToDo = []
    #[[indice1, esame1, costo1, pagato1, voto1, data1], [indice2, esame2, costo2, pagato2, voto2, data2],...]
    #trova lista esami, se non ci sono lista = []
    index = 1 
    for row in rowsEsami[1:]:
        if int(row[0]) == m:
            if row[4] == "" and row[5] == "":
                examsToDo.append([index, row[1], row[2], row[3]])
                index += 1
            else:
                examsDone.append([index, row[1], row[2], row[3]])
                index += 1
    
    if mode == "done":
        return examsDone
    else:
        return examsToDo



#funzione che restituisce la lista di esiti per una matricola
def getResults(m, rowsEsiti):
    lista = [] #[indice, esame, esito, data]
    
    index = 0
    for row in rowsEsiti[1:]:
        if int(row[0]) == m:
            lista.append([index, row[1], row[2], row[3]])
            index += 1

    return lista




def printExams(name, rowsEsami, option=""): #argomento facoltativo
    
    examsDone = getExams(name[2], rowsEsami, "done")
    examsToDo = getExams(name[2], rowsEsami, "to do")
    
    clear()
    print("{} {}\n".format(name[0], name[1]))

    #stampa solo quelli da pagare
    if option == "to pay":
        print("Esami da pagare:")
        if examsToDo == []:
            print("Non risultano esami da sostenere!\n")
        else:
            toPay = False #se ci sono esami da pagare
            c = 1 #contatore perchè gli esami da pagare non sono in fila
            for exam in examsToDo: 
                if exam[3].lower() == "false": #casella contenente pagato True / False
                    print("{}. {} (costo: {}, NON pagato)".format(c, exam[1], exam[2]))
                    toPay = True
                    c += 1

            if not toPay:
                print("Non ci sono esmai da pagare!")
                return False #così posso usare la condizione "se non ci sono esami da stampare"
            else:
                return True


    #stampa tutti gli esami
    else:
        print("Esami da sostenre:")
        if examsToDo == []:
            print("Non risultano esami da sostenere!")
        else:
            for exam in examsToDo: 
                if exam[3] == "True": #casella contenente pagato True / False
                    print("- {} (costo: {}, pagato)".format(exam[1], exam[2]))
                else:
                    print("- {} (costo: {}, NON pagato)".format(exam[1], exam[2]))


        print("\nEsami sostenuti:")
        if examsDone == []:
            print("Non risultano esami sostenuti!\n")
        else:
            for exam in examsDone:
                print("- {}, esito: {}, data: {}".format(exam[1], exam[2], exam[3]))




def correctSintax(string):
    string = string.strip()
    string = string.lower()
    string = string.capitalize()
    return string
