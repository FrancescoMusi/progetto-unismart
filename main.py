import csv
import os
from datetime import date
from functions import *

fileMatricole = './AnagraficaMatricole.csv'
fileEsami = './Esami.csv'


err = False

#main cicle
while True:

    if not err:
        choice = options()
    else: 
        err = False
    

    #dentro al while perchè se aggiungo dati devo leggerli
    rowsMatricole = readFile(fileMatricole)
    rowsEsami = readFile(fileEsami)


    #fine del programma
    if choice == 0:
        clear()
        break
    

    #visualizza lista matricole
    elif choice == 1:
        stampaMatricole(rowsMatricole)

    #ricerca studente per numero matricola
    elif choice == 2:
        stampaMatricola(rowsMatricole)

    #ricerca esami per numero di matricola
    elif choice == 3:
        clear()
        name = getName(rowsMatricole)
        printExams(name, rowsEsami)
        stop()

    #inserimento nuovo studente
    elif choice == 4:
        InserisciMatricola(rowsMatricole, fileMatricole)
          
    #pagamento esami
    elif choice == 5:
        PagaEsami(rowsMatricole, rowsEsami, fileEsami)

    #aggiungere esito esame
    elif choice == 6:
        clear()
        
        name = getName(rowsMatricole)
        printExams(name, rowsEsami)

        #ciclo inserimento esame
        correctExam = False
        while not correctExam:
            esame = ""
            esito = -1 #un esito possibile non è mai negativo

            #controlla che il nome esame non sia vuoto
            while esame == "":
                esame = checkInt(input("Numero esame: "))
                clear()

            #controlla che il voto non sia vuoto
            while esito < 0: 
                esito = checkInt(input("Esito: "))
                clear()

    
            print()

        row = [name[2], esame, esito, date.today()]

        appendFile(fileEsiti, [row])
        print("Esame inserito correttamente!")
        stop()




    else: 
        choice = checkInt(input("Inserisci un opzione accettabile!\n"))
        err = True

