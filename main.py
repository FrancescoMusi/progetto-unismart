from datetime import date
from functions import *

fileMatricole = './AnagraficaMatricole.csv'
fileEsami = './Esami.csv'
fileMaterie = './Materie.csv'


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
    rowsMaterie = readFile(fileMaterie)


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
        matricola = getMatricola(rowsMatricole)
        printExams(matricola, rowsEsami, rowsMaterie)
        stop()

    #inserimento nuovo studente
    elif choice == 4:
        InserisciMatricola(rowsMatricole, fileMatricole)
          
    #pagamento esami
    elif choice == 5:
        PagaEsami(rowsMatricole, rowsEsami, rowsMaterie, fileEsami)

    #aggiungere esito esame
    elif choice == 6:
        clear()
        
        matricola = getMatricola(rowsMatricole)
        printExams(matricola, rowsEsami, rowsMaterie)

        #ciclo inserimento esame
        correctExam = False
        while not correctExam:
            id_esame = 0
            esito = 0 #un esito possibile non è mai negativo

            #controlla che l'id esame non sia vuoto
            while id_esame == 0:
                id_esame = checkInt(input("Numero esame: "))
                clear()

            #controlla che il voto non sia vuoto
            while esito == 0: 
                esito = checkInt(input("Esito: "))
                clear()
            correctExam = True
            print()

        for row in rowsEsami[1:]:
            if int(row[0]) == int(matricola[0]) and int(row[1]) == id_esame:
                row[4] = esito
                row[5] = date.today()
        
        writeFile(fileEsami, rowsEsami)
        # row = [matricola[0], esame, esito, date.today()]6
        print("Esame inserito correttamente!")
        stop()

    else: 
        choice = checkInt(input("Inserisci un opzione accettabile!\n"))
        err = True

