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
    name = getMatricola(rowsMatricole)
    print("\n- cognome: {}\n- nome: {}".format(name[1], name[2]))
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



def PagaEsami(rowsMatricole, rowsEsami, rowsMaterie, fileEsami):
    clear()

    correctName = False
    while not correctName:
        matricola = getMatricola(rowsMatricole)
        examsToDoToPay = getExams(matricola[0], rowsEsami, "to do to pay")
        correctName = checkData("{} {} è la matricola di cui vuoi pagare gli esami?".format(matricola[1], matricola[2]))

    
    printExams(matricola, rowsEsami, rowsMaterie, "to pay")

    if examsToDoToPay == []:
        stop()
    
    else: 
        print("\nQuali esami vuoi pagare? scrivi una lista separata da virgole (es: \"1, 3\")")

        #ciclo che fa inserire una lista scritta correttamente
        while True:
            toPay = input()

            #rimuove spazi e rende la stringa una lista
            toPay = removeSpaces(toPay)

            try:
                toPay = toPay.split(",")
                totalPrice = 0
            
                #ciclo che fa inserire una lista con numeri corretti.
                for number in toPay:
                    for exam in examsToDoToPay:
                        if int(exam[0]) == int(number): #[0] è l'indice dell'esame
                            totalPrice += int(exam[2]) #[2] è il prezzo dell'esame in questione
                    
                            
                    #riscrive le righe del file esami
                    for row in rowsEsami[1:]:
                        if int(row[0]) == int(matricola[0]) and int(row[1]) == int(exam[1]): #se numero matricola e nome esame corrispondono
                            row[3] = "True"

                
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

#funzione che trova il nome della materia
def getNameMateria(id, rowsMaterie):
    for row in rowsMaterie[1:]:
        if int(row[0]) == id:
            return row[1]


def getMatricola(rowsMatricole):
    id_matricola = checkInt(input("Inserisci numero matricola: "))
    lista = [] #[matricola, cognome, nome]
    
    #trova nome e cognome
    userFound = False
    while not userFound:
        for row in rowsMatricole[1:]:
            if int(row[0]) == id_matricola:
                lista.append(id_matricola)
                lista.append(row[1])
                lista.append(row[2])
                userFound = True
        
        if not userFound: 
            id_matricola = checkInt(input("Utente non trovato, inserisci un numero diverso!\n"))

    
    return lista 



def getExams(id_matricola, rowsEsami, mode):
    examsDone = []
    examsToDoNotPayed = []
    examsToDoPayed = []
    #[[indice1, esame1, costo1, pagato1, voto1, data1], [indice2, esame2, costo2, pagato2, voto2, data2],...]
    #trova lista esami, se non ci sono lista = []

    #non fatti e non pagati
    index = 1 
    for row in rowsEsami[1:]:
        if int(row[0]) == id_matricola:
            if row[4] == " " and row[5] == " " and row[3].lower() == "false":
                examsToDoNotPayed.append([index, row[1], row[2], row[3]])
                index += 1

    #non fatti e pagati
    index = 1 
    for row in rowsEsami[1:]:
        if int(row[0]) == id_matricola:
            if row[4] == " " and row[5] == " " and row[3].lower() != "false":
                examsToDoPayed.append([index, row[1], row[2], row[3]])
                index += 1
    
    #fatti 
    index = 1 
    for row in rowsEsami[1:]:
        if int(row[0]) == id_matricola:
            if row[5] != " ":
                examsDone.append([index, row[1], row[2], row[3], row[4], row[5]])
                index += 1

    
    if mode == "done":
        return examsDone
    elif mode == "to do to pay":
        return examsToDoNotPayed
    else:
        return examsToDoPayed



#funzione che restituisce la lista di esiti per una matricola
def getResults(m, rowsEsiti):
    lista = [] #[indice, esame, esito, data]
    
    index = 0
    for row in rowsEsiti[1:]:
        if int(row[0]) == m:
            lista.append([index, row[1], row[2], row[3]])
            index += 1

    return lista




def printExams(matricola, rowsEsami, rowsMaterie,  option=""): #argomento facoltativo
    
    examsDone = getExams(matricola[0], rowsEsami, "done")
    examsToDoToPay = getExams(matricola[0], rowsEsami, "to do to pay")
    examsToDoPayed = getExams(matricola[0], rowsEsami, "to do payed")
    
    clear()
    print("{} {}\n".format(matricola[1], matricola[2]))


    #stampa solo quelli da pagare
    if option == "to pay":
        print("Esami da pagare:")
        if examsToDoToPay == []:
            print("Non risultano esami da pagare!\n")
        else:
            for exam in examsToDoToPay: 
                if exam[3].lower() == "false": #casella contenente pagato True / False
                    print("{}. {} (costo: {}, NON pagato)".format(exam[0], getNameMateria(int(exam[1]), rowsMaterie), exam[2]))
                    toPay = True


    #stampa solo quelli da pagare
    if option == "payed":
        print("Esami pagati:")
        if examsToDoPayed == []:
            print("Non risultano esami pagati!\n")
        else:
            for exam in examsToDoPayed: 
                if exam[3].lower() != "false": #casella contenente pagato True / False
                    print("{}. {} (costo: {}, pagato)".format(exam[0], getNameMateria(int(exam[1]), rowsMaterie), exam[2]))
                    toPay = True


    #stampa tutti gli esami
    else:
        print("Esami da sostenere pagati:")
        if examsToDoPayed == []:
            print("Non risultano esami da sostenere pagati!")
        else:
            for exam in examsToDoPayed: 
                print("{}. {} (costo: {}, pagato)".format(exam[0], getNameMateria(int(exam[1]), rowsMaterie), exam[2]))


        print("\nEsami da sostenere non pagati:")
        if examsToDoToPay == []:
            print("Non risultano esami da sostenere non pagati!")
        else:
            for exam in examsToDoToPay: 
                print("{}. {} (costo: {}, NON pagato)".format(exam[0], getNameMateria(int(exam[1]), rowsMaterie), exam[2]))
               


        print("\nEsami sostenuti:")
        if examsDone == []:
            print("Non risultano esami sostenuti!\n")
        else:
            for exam in examsDone:
                print("{}. {} (esito: {}, data: {})".format(exam[0], getNameMateria(int(exam[1]), rowsMaterie), exam[4], exam[5]))




def correctSintax(string):
    string = string.strip()
    string = string.lower()
    string = string.capitalize()
    return string
