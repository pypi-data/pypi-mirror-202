# hu_nev


## Leírás

Magyar listák gyűjteménye - Collection of Hungarian lists.

Az alábbi listákat találod :
1. vezetéknevek   =  magyarorszag.vezeteknev
2. női keresztnevek  = nev.keresztnev_n
3. férfi keresztnevek = nev.keresztnev_f
4. utcanevek = nev.utca
5. telelpülésnevek= nev.telepules
6. vármegyék nevei = nev.megye
7. folyók nevei = nev.folyo
8. a hét napjai = nev.nap
9. az év hónapjai = nev.honap

## Description
1. last names =  nev.vezeteknev
2. female first names = nev.keresztnev_n
3. male first names  = nev.keresztnev_f
4. street names = nev.utca
5. city names = nev.telepules
6. names of counties = nev.megye
7. names of rivers = nev.folyo
8. he days of the week = nev.nap
9. the months of the year = nev.honap
## Használat:

 Főként véletlengenerátorok kiegészítőjeként ajánlom
 
I recommend it mainly as a supplement to random number generators. 
       
             random.choice
telepulesek = random.choices(hu_nev.telepules, k=25)


## Szerző

* Név: Nagy BÉLa
* E-mail:nagy.bela.budapest@gmail.com

## Licenc

Oktatási célra készült, szabadon használható