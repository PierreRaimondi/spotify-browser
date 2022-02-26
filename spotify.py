# Projet base de données : Spotify
# Zoé BONNEFON, Marco JORGE, Pierre RAIMONDI

import sqlite3
import webbrowser
conn = sqlite3.connect('spotify.db')
c = conn.cursor()

def menu():
    print((" Bienvenue ! ").center(70,('=')))
    print("\nBienvenue sur l'outil de recherche dans la base de données de Spotify.\nQue souhaitez-vous faire ?\n")
    print("1/ Faire une recherche concernant une musique\n")
    print("2/ Faire une recherche concernant un artiste\n")
    print("A tout moment, vous pouvez entrer \"quitter\" pour quitter le programme\n")
    response = input("Entrez le numéro de votre demande (ex: 1) : ")
    if response == '1':
        musique()
    elif response == '2':
        artiste()
    elif response == 'quitter':
        quitter()
    else:
        erreur("Vous devez entrer un des numéros proposés.")
        quitter()
    return None

def quitter():
    print((" A bientôt ! ").center(70,('=')))
    conn.close()
    return None

def erreur(errMsg):
    print((" Erreur ").center(70,('=')))
    print("\n"+str(errMsg)+"\n")
    return None

def musique():
    print((" Recherche de musique ").center(70,('=')))
    print("\nComment souhaitez-vous recherche votre musique ?\n")
    print("1/ Rechercher avec le nom\n")
    print("2/ Rechercher avec l'artiste\n")
    response = input("Entrez le numéro de votre demande (ex: 1) : ")
    if response == '1':
        searchSong('songName')
    elif response == '2':
        searchSong('artistName')
    elif response == 'quitter':
        quitter()
    else:
        erreur("Vous devez entrer un des numéros proposés.")
        musique()
    return None

def artiste():
    print((" Recherche d'artiste ").center(70,('=')))
    print("\nQuel est le nom de l'artiste que vous recherchez ?\n")
    response = input("Entrez le nom d'un artiste : (ex : Imagine Dragons) : ")
    c.execute("""SELECT id, name FROM artists WHERE name LIKE ? ORDER BY popularity DESC LIMIT 10""",('%'+str(response)+'%',))
    queryResult = c.fetchall()
    print((" Résultats de la recherche ").center(70,('=')))
    print("")
    if not(queryResult):
        print("Aucun résultat a été trouvé pour \""+str(response)+"\"")
        menu()
    else:
        print("Sélectionnez l'artiste souhaité\n")
        resultsId = []
        nb = 0
        for i in queryResult:
                nb += 1
                resultsId.append(str(i[0]))
                print(str(nb)+"/ "+str(i[1])+'\n')
        nb += 1
        print(str(nb)+'/ Annuler')
        response = input("Entrez le numéro de l'artiste souhaitée (ex: 1) : ")
        if response.isdigit() and int(response) < 1:
            erreur("Vous devez entrer un des numéros proposés.")
            artiste()
        elif response.isdigit() and int(response) <= len(resultsId):
            artistInfos(resultsId[int(response)-1])
        elif response.isdigit() and int(response) == nb:
            menu()
        elif response == 'quitter':
            quitter()
        else:
            erreur("Vous devez entrer un des numéros proposés.")
            artiste()

def searchSong(method):
    if method == 'songName':
        print("\nQuel est le nom de la musique recherché ?\n")
        response = input("Entrez le nom d'une musique : (ex : Fever) : ")
        c.execute("""SELECT id, name, artists FROM tracks WHERE name LIKE ? ORDER BY popularity DESC LIMIT 10""",('%'+str(response)+'%',))
        queryResult = c.fetchall()
        print((" Résultats de la recherche ").center(70,('=')))
        print("")
        if not(queryResult):
            print("Aucun résultat a été trouvé pour \""+str(response)+"\"")
            menu()
        else:
            print("Sélectionnez la musique souhaitée\n")
            resultsId = []
            nb = 0
            for i in queryResult:
                nb += 1
                resultsId.append(str(i[0]))
                artists = eval(i[2])
                print(str(nb)+"/ "+str(i[1])+" | "+' / '.join(artists)+'\n')
            nb += 1
            print(str(nb)+'/ Annuler')
            response = input("Entrez le numéro de la musique souhaitée (ex: 1) : ")
            if response.isdigit() and int(response) < 1:
                erreur("Vous devez entrer un des numéros proposés.")
                searchSong('songName')
            elif response.isdigit() and int(response) <= len(resultsId):
                songInfos(resultsId[int(response)-1])
            elif response.isdigit() and int(response) == nb:
                menu()
            elif response == 'quitter':
                quitter()
            else:
                erreur("Vous devez entrer un des numéros proposés.")
                searchSong('songName')
    elif method == 'artistName':
        print("\nQuel est le nom de l'artiste ?\n")
        response = input("Entrez le nom de l'artiste : (ex : Imagine Dragons) : ")
        c.execute("""SELECT id, name FROM artists WHERE name LIKE ? ORDER BY popularity DESC LIMIT 10""",('%'+str(response)+'%',))
        queryResult = c.fetchall()
        print((" Résultats de la recherche ").center(70,('=')))
        print("")
        if not(queryResult):
            print("Aucun résultat a été trouvé pour \""+str(response)+"\"")
            menu()
        else:
            print("Sélectionnez l'artiste souhaité\n")
            resultsId = []
            nb = 0
            for i in queryResult:
                    nb += 1
                    resultsId.append(str(i[0]))
                    print(str(nb)+"/ "+str(i[1])+'\n')
            nb += 1
            print(str(nb)+'/ Annuler')
            response = input("Entrez le numéro de l'artiste souhaitée (ex: 1) : ")
            if response.isdigit() and int(response) < 1:
                erreur("Vous devez entrer un des numéros proposés.")
                searchSong('artistName')
            elif response.isdigit() and int(response) <= len(resultsId):
                artistSongs(resultsId[int(response)-1])
            elif response.isdigit() and int(response) == nb:
                menu()
            elif response == 'quitter':
                quitter()
            else:
                erreur("Vous devez entrer un des numéros proposés.")
                searchSong('artistName')
    else:
        erreur('Une erreur est survenue.')
        menu()
    return None


def songInfos(songId):
    c.execute("""SELECT * FROM tracks WHERE id = ?""",(str(songId),))
    queryResult = c.fetchone()
    print((" "+str(queryResult[1])+" ").center(70,('=')))
    print("")
    print("Nom : "+str(queryResult[1]))
    artistsId = eval(queryResult[6])
    artists = eval(queryResult[5])
    print("Artiste(s) : "+', '.join(artists))
    lengthInSeconds = round(int(queryResult[3])/1000)
    lengthInMinutes = 0
    while lengthInSeconds - 60 > 0:
        lengthInMinutes += 1
        lengthInSeconds -= 60
    print("Durée : "+str(lengthInMinutes)+"min"+str(lengthInSeconds)+"s")
    print("Date de sortie : " +str(queryResult[7]))
    print("")
    print("Tempo (BPM) : " +str(round(queryResult[18])))
    print("Popularité (entre 0 et 100) : " +str(queryResult[2]))
    print("Dansabilité (entre 0 et 1) : " +str(queryResult[8]))
    print("Énergie (entre 0 et 1) : " +str(queryResult[9]))
    print("Intensité (-60 = très calme; 0 = très fort) : " +str(queryResult[11]))
    print("Présence de paroles (0 = aucune; 1 = talk show) : " +str(queryResult[13]))
    print("Acoustique (0 = pas acoustique; 1 = très acoustique) : " +str(queryResult[14]))
    print("Instrumentalité (entre 0 et 1) : " +str(queryResult[15]))
    print("Présence d'un public (0 = enregistrement de studio; 1 = concert) : " +str(queryResult[16]))
    print("Positivité (0 = triste; 1 = de bonne humeur) : " +str(queryResult[16]))
    print("")
    print("1/ Écouter sur Spotify\n")
    print("2/ Plus d'informations sur "+str(artists[0])+"\n")
    print("3/ Chercher des musiques similaires\n")
    print("4/ Retourner au menu principal\n")
    response = input("Entrez le numéro de votre demande (ex: 1) : ")
    if response == '1':
        webbrowser.open('https://open.spotify.com/track/'+str(queryResult[0]))
        songInfos(str(queryResult[0]))
    elif response == '2':
        artistInfos(str(artistsId[0]))
    elif response == '3':
        similarSong(str(songId))
    elif response == '4':
        menu()
    elif response == 'quitter':
        quitter()
    else:
        erreur("Vous devez entrer un des numéros proposés.")
        songInfos(songId)
    return None


def artistInfos(artistId):
    c.execute("""SELECT * FROM artists WHERE id = ?""",(str(artistId),))
    queryResult = c.fetchone()
    if not(queryResult):
        print("Aucun résultat a été trouvé")
        menu()
    else:
        print((" "+str(queryResult[3])+" ").center(70,('=')))
        print("")
        print("Nom : "+str(queryResult[3]))
        genres = eval(queryResult[2])
        print("Genres : "+', '.join(genres))
        print("Followers sur Spotify : "+str(round(queryResult[1])))
        print("Popularité (entre 0 et 100): "+str(queryResult[4]))
        print("")
        print("1/ Chercher les musiques de "+str(queryResult[3])+"\n")
        print("2/ Retourner au menu principal\n")
        response = input("Entrez le numéro de votre demande (ex: 1) : ")
        if response == '1':
            artistSongs(str(queryResult[0]))
        elif response == '2':
            menu()
        elif response == 'quitter':
            quitter()
        else:
            erreur("Vous devez entrer un des numéros proposés.")
            artistInfos(artistId)
    return None

def artistSongs(artistId):
    c.execute("""SELECT id, name, artists FROM tracks WHERE id_artists LIKE ?""",('%'+str(artistId)+'%',))
    queryResult = c.fetchall()
    print((" Résultats de la recherche ").center(70,('=')))
    print("")
    if not(queryResult):
        print("Aucun résultat a été trouvé")
        menu()
    else:
        print("Sélectionnez la musique souhaitée\n")
        resultsId = []
        nb = 0
        for i in queryResult:
            nb += 1
            resultsId.append(str(i[0]))
            artists = eval(i[2])
            print(str(nb)+"/ "+str(i[1])+" | "+' / '.join(artists)+'\n')
        nb += 1
        print(str(nb)+'/ Annuler')
        response = input("Entrez le numéro de la musique souhaitée (ex: 1) : ")
        if response.isdigit() and int(response) < 1:
            erreur("Vous devez entrer un des numéros proposés.")
            artistSongs(artistId)
        elif response.isdigit() and int(response) <= len(resultsId):
            songInfos(resultsId[int(response)-1])
        elif response.isdigit() and int(response) == nb:
            menu()
        elif response == 'quitter':
            quitter()
        else:
            erreur("Vous devez entrer un des numéros proposés.")
            artistSongs(artistId)
    return None

def similarSong(songId):
    c.execute("""SELECT * FROM tracks WHERE id = ?""",(str(songId),))
    queryResult = c.fetchone()
    if not(queryResult):
        erreur("Une erreur est survenue")
        menu()
    else:
        print((" Similaire à "+str(queryResult[1])+" ").center(70,('=')))
        print("")
        print("Sélectionnez une musique à afficher\n")
        nb = 0
        songsResultId = []
        c.execute("""SELECT id, name, artists FROM tracks WHERE danceability = ? AND popularity > 60 ORDER BY random() LIMIT 1""",(str(queryResult[8]),))
        sameDanceability = c.fetchone()
        c.execute("""SELECT id, name, artists FROM tracks WHERE energy = ? AND popularity > 60 ORDER BY random() LIMIT 1""",(str(queryResult[9]),))
        sameEnergy = c.fetchone()
        c.execute("""SELECT id, name, artists FROM tracks WHERE liveness = ? AND popularity > 60 ORDER BY random() LIMIT 1""",(str(queryResult[16]),))
        sameLiveness = c.fetchone()
        if sameDanceability:
            nb += 1
            songsResultId.append(str(sameDanceability[0]))
            sameDanceabilityArtists = eval(sameDanceability[2])
            print(str(nb)+"/ Même dansabilité : "+str(sameDanceability[1])+" | "+' / '.join(sameDanceabilityArtists)+"\n")
        if sameEnergy:
            nb += 1
            songsResultId.append(str(sameEnergy[0]))
            sameEnergyArtists = eval(sameEnergy[2])
            print(str(nb)+"/ Même énergie : "+str(sameEnergy[1])+" | "+' / '.join(sameEnergyArtists)+"\n")
        if sameLiveness:
            nb += 1
            songsResultId.append(str(sameLiveness[0]))
            sameLivenessArtists = eval(sameLiveness[2])
            print(str(nb)+"/ Même positivité : "+str(sameLiveness[1])+" | "+' / '.join(sameLivenessArtists)+"\n")
        nb += 1
        print(str(nb)+"/ Retourner au menu principal")
        response = input("Entrez le numéro de la musique souhaitée (ex: 1) : ")
        if response.isdigit() and int(response) < 1:
            erreur("Vous devez entrer un des numéros proposés.")
            similarSong(songId)
        elif response.isdigit() and int(response) <= len(songsResultId):
            songInfos(songsResultId[int(response)-1])
        elif response == str(nb):
            menu()
        elif response == 'quitter':
            quitter()
        else:
            erreur("Vous devez entrer un des numéros proposés.")
            similarSong(songId)
    return None


menu()


# POUR TESTER LES DIFFERENTES FONCTIONS

# quitter()
# erreur("Message d'erreur personnalisé")
# musique()
# artiste()
# searchSong("songName")
# searchSong('artistName')
# songInfos('0boS4e6uXwp3zAvz1mLxZS')
# artistInfos("44TGR1CzjKBxSHsSEy7bi9")
# artistSongs("44TGR1CzjKBxSHsSEy7bi9")
# similarSong("0boS4e6uXwp3zAvz1mLxZS")