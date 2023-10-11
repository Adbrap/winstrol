import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import json
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import math



print('')
Write.Print('Backtester Live 1.0', Colors.green, interval=0.000)
print('')
print('-------------------------')
print('')

Write.Print('Voir les figures ? (o/n)', Colors.white, interval=0.000)
print('')
a = 0
while a != 1:
    Write.Print('>> ', Colors.white, interval=0.000)
    voir = input()
    print('')
    if voir == 'o' or voir == 'n' or voir == 'O' or voir == 'N':
        a = 1
    else:
        print('')
        Write.Print('Choix Non Reconnu!', Colors.red, interval=0.000)
        print('')

Write.Print('TakeProfit Cloture ou volatilitée ? (c/v)', Colors.white, interval=0.000)
print('')
a = 0
while a != 1:
    Write.Print('>> ', Colors.white, interval=0.000)
    clo1 = input()
    if clo1 == 'c' or clo1 == 'v' or clo1 == 'C' or clo1 == 'V':
        a = 1
    else:
        print('')
        Write.Print('Choix Non Reconnu!', Colors.red, interval=0.000)
        print('')
print('')
print('')
Write.Print('Pourcentage TakeProfit :', Colors.white, interval=0.000)
print('')
Write.Print('>> ', Colors.white, interval=0.000)
pourc = input()
pourc = int(pourc)
print('')

Write.Print('StopLoss Cloture ou volatilitée ? (c/v)', Colors.white, interval=0.000)
print('')
a = 0
while a != 1:
    Write.Print('>> ', Colors.white, interval=0.000)
    clo2 = input()
    if clo2 == 'c' or clo2 == 'v' or clo2 == 'C' or clo2 == 'V':
        a = 1
    else:
        print('')
        Write.Print('Choix Non Reconnu!', Colors.red, interval=0.000)
        print('')
verif = False
if clo2 == 'c' or clo2 == 'C':
    print('')
    print('')
    Write.Print('StopLoss Regler Sur Epaule 2 ? (o/n)', Colors.white, interval=0.000)
    print('')
    a = 0
    while a != 1:
        Write.Print('>> ', Colors.white, interval=0.000)
        stop_epaule = input()
        print('')
        if stop_epaule == 'o' or stop_epaule == 'n' or stop_epaule == 'O' or stop_epaule == 'N':
            a = 1
        else:
            print('')
            Write.Print('Choix Non Reconnu!', Colors.red, interval=0.000)
            print('')

        if stop_epaule == 'o' or stop_epaule == 'O':
            condition1 = True
            verif = True

        if stop_epaule == 'n' or stop_epaule == 'N':
            print('')                                                            
            print('')
            Write.Print('Pourcentage StopLoss :', Colors.white, interval=0.000)
            print('')
            Write.Print('>> ', Colors.white, interval=0.000)
            pourc2 = input()
            pourc2 = int(pourc2)
            print('')
            condition1 = False


if clo2 == 'v' or clo2 == 'V':
    if verif == False:
        print('')
        print('')
        Write.Print('Pourcentage StopLoss :', Colors.white, interval=0.000)
        print('')
        Write.Print('>> ', Colors.white, interval=0.000)
        pourc2 = input()
        pourc2 = int(pourc2)
        print('')
        condition1 = False



if clo1 == 'c' or clo1 == 'C':
    clo11 = 'c'
if clo1 == 'v' or clo1 == 'V':
    clo11 = 'h'


if clo2 == 'c' or clo2 == 'C':
    clo22 = 'c'
if clo2 == 'v' or clo2 == 'V':
    clo22 = 'l'

nombre_point = 0
nombre_magique = 0
mise  = 1000
minargent = 5
laquelle = []
plusbas = []
plusbas1 = 0
changement = []

def get_angle(point1, point2):
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]

    # Pour une ligne verticale, on retourne 90 directement
    if x_diff == 0:
        return 90

    angle = math.atan2(y_diff, x_diff)
    angle = math.degrees(angle)
    return angle


def plot_points(point1, point2):
    angle = get_angle(point1, point2)

    # Si l'angle est 90 (ligne verticale), la pente est "infinie"
    if angle == 90:
        slope_percent = "90"
        return slope_percent
    else:
        slope_percent = math.tan(math.radians(angle)) * 100
        return slope_percent
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('les courbes ne se coupent pas')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

pourcent_gain = 0
if voir == 'o' or voir == 'O':
    activ = True
else:
    activ = False
nombre_regarder = 0
nombre_gagnant = 0
nombre_perdant = 0
debug = []
condition = 0
placebas = 0
pourcentbastete = []
toutemoyennetete = []

for t in range(1,8255):
    #try:
        nombre_regarder = nombre_regarder +1
        Write.Print(f'Figure Numero {t}', Colors.pink, interval=0.000)
        print('')
        dossier = "baki/"
        nom_fichier = f"{t}.json"
        chemin_fichier = dossier + nom_fichier
        with open(chemin_fichier, 'r') as fichiers:
            data = json.load(fichiers)
        df = pd.DataFrame(data)
        df = df.reset_index(drop=True)
        #df = pd.DataFrame(data['results'])
        #with open(chemin_fichier, 'w') as fichier:
        #json.dump(data, fichier)
        local_max = argrelextrema(df['c'].values, np.greater, order=1, mode='clip')[0]
        local_min = argrelextrema(df['c'].values, np.less, order=1, mode='clip')[0]
        highs = df.iloc[local_max, :]
        lows = df.iloc[local_min, :]
        A = float(highs['c'].iloc[0])
        B = float(lows['c'].iloc[0])
        C = float(highs['c'].iloc[1])
        D = float(lows['c'].iloc[1])
        E = float(highs['c'].iloc[2])
        F = float(lows['c'].iloc[2])
        G = float(highs['c'].iloc[3])
        vert = []
        rouge = []
        bleu = []
        vert.append(local_max[0]) #A
        vert.append(local_max[1]) #C
        vert.append(local_max[2]) #E
        vert.append(local_max[3]) #G
        rouge.append(local_max[0])
        rouge.append(local_min[0])
        rouge.append(local_max[1])
        rouge.append(local_min[1])
        rouge.append(local_max[2])
        rouge.append(local_min[2])
        rouge.append(local_max[3])
        i = 0
        for i in range(local_min[2], len(df)):
            bleu.append(i)
        mirande2 = df.iloc[vert, :]
        mirande = df.iloc[rouge, :]
        mirande3 = df.iloc[bleu, :]
        if C > E:
            differ = (C - E)
            pas = (local_max[2] - local_max[1])
            suite = differ / pas
        if C < E:
            differ = (E - C)
            pas = (local_max[2] - local_max[1])
            suite = differ / pas
        if E > C:
            mirande2['c'].values[0] = mirande2['c'].values[1] - ((suite * (local_max[1] - local_max[0])))
            mirande2['c'].values[3] = mirande2['c'].values[2] + ((suite * (local_max[3] - local_max[2])))
        if E < C:
            mirande2['c'].values[0] = mirande2['c'].values[1] + ((suite * (local_max[1] - local_max[0])))
            mirande2['c'].values[3] = mirande2['c'].values[2] - ((suite * (local_max[3] - local_max[2])))
        if E == C:
            mirande2['c'].values[0] = df['c'].values[local_max[1]]
            mirande2['c'].values[3] = df['c'].values[local_max[1]]
        vert1 = {'c': vert}
        vert2 = pd.DataFrame(data=vert1)
        rouge1 = {'c': rouge}
        rouge2 = pd.DataFrame(data=rouge1)
        AI = [local_max[0], mirande2['c'].iloc[0]]
        BI = [local_max[1], mirande2['c'].iloc[1]]
        CI = [local_max[0], A]
        DI = [local_min[0], B]
        AJ = [local_max[2], mirande2['c'].iloc[2]]
        BJ = [local_max[3], mirande2['c'].iloc[3]]
        CJ = [local_max[3], G]
        DJ = [local_min[2], F]
        J = line_intersection((AJ, BJ), (CJ, DJ))
        I = line_intersection((AI, BI), (CI, DI))
        point_I = (I[0],I[1])
        point_J = (J[0],J[1])
        slope_percent = plot_points(point_I, point_J)
        moyenne_tete = ((C - D) + (E - D)) / 2
        pourcent_tete = ((((C - D) + (E - D)) / 2) * 100)/ D
        toutemoyennetete.append(pourcent_tete)
        #ticker = data['ticker']
        trouver = False
        try:
            for i in range(local_min[2], local_max[3] + 5):
                if df['c'].iloc[i] >= J[1] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                    # if df['c'].iloc[i] > df['c'].iloc[local_min[ff]] and df['c'].iloc[i] <= J[1] + (moyenne_tete) / 4 and trouver == False:
                    placejaune = i
                    trouver = True
                    plusbas1 = df['h'].iloc[placejaune]
            if condition1 == True:
                condition = F
            if condition1 == False:
                condition = J[1] - ((moyenne_tete)*pourc2 / 100)
            trouver2 = False
            trouver3 = False
            trouver4 = False
            changement1 = False
            if (((((( df['c'].iloc[placejaune] + ((moyenne_tete)*pourc / 100)) - df['c'].iloc[placejaune])) * 100) / df['c'].iloc[placejaune]) * mise )/100 >= minargent:
                for i in range(placejaune, len(df)):
                    if df[f'{clo22}'].iloc[i] < condition and trouver3 == False and trouver2 == False:
                        placerouge = i
                        pourcent_gain = pourcent_gain + ((((df[f'{clo22}'].iloc[i] - df['c'].iloc[placejaune]))*100) /df['c'].iloc[placejaune])
                        #print(((((df['c'].iloc[i] - df['c'].iloc[placejaune]))*100) /df['c'].iloc[placejaune]))
                        prix = ((((df[f'{clo22}'].iloc[i] - df['c'].iloc[placejaune]))*100) /df['c'].iloc[placejaune])
                        debug.append(round(prix,2))
                        nombre_perdant = nombre_perdant +1
                        nombre_point = nombre_point + (placerouge - placejaune)
                        trouver3 = True
                    if df[f'{clo11}'].iloc[i] >= J[1] + ((moyenne_tete)*pourc / 100) and trouver2 == False and trouver3 == False:
                        placevert = i
                        #pourcent_gain = pourcent_gain + ((((df[f'{clo11}'].iloc[i] - df['c'].iloc[placejaune] ))*100) /df['c'].iloc[placejaune])
                        pourcent_gain = pourcent_gain + ((((( J[1]+ ((moyenne_tete)*pourc / 100)) - df['c'].iloc[placejaune])) * 100) / df['c'].iloc[placejaune])
                        #print(((((df['c'].iloc[i] - df['c'].iloc[placejaune] ))*100) /df['c'].iloc[placejaune]))
                        #prix = ((((df[f'{clo11}'].iloc[i] - df['c'].iloc[placejaune] ))*100) /df['c'].iloc[placejaune])
                        prix = ((((( J[1] + ((moyenne_tete)*pourc / 100)) - df['c'].iloc[placejaune])) * 100) / df['c'].iloc[placejaune])
                        print()
                        debug.append(round(prix, 2))
                        nombre_gagnant = nombre_gagnant +1
                        nombre_point = nombre_point + (placevert - placejaune)
                        trouver2 = True
                if (A-B) >= (C-D) and  slope_percent <= 5:
                    nombre_magique = nombre_magique + 1
                    laquelle.append(len(debug))
                if (((((( df['c'].iloc[placejaune] + ((moyenne_tete)*pourc / 100)) - df['c'].iloc[placejaune])) * 100) / df['c'].iloc[placejaune]) * mise )/100 >= minargent:
                    if trouver2 == True:
                        for m in range(placejaune, placevert+1) :
                            if df['h'].iloc[m] < plusbas1:
                                plusbas1 = df['h'].iloc[m]
                                placebas = m
                                changement1 = True
                        if changement1 == True:
                            changement.append(t)
                        if changement1 == False:
                            placebas = placejaune
                        plusbas.append(plusbas1)
                        trouver4 = True
                        pourcentbastete.append(round(((df['h'].iloc[placebas] - df['c'].iloc[placejaune])*100)/moyenne_tete,2))
            # ----- creation des locals(min/max) -----#
            fig1 = plt.figure(figsize=(10, 7))
            plt.plot([], [], " ")
            fig1.patch.set_facecolor('#17DE17')
            fig1.patch.set_alpha(0.3)
            plt.title(f'IETE : {t} {slope_percent}', fontweight="bold", color='black')
            df['c'].plot(color=['blue'], label='Clotures')
            mirande2['c'].plot(color=['green'], linestyle='--', label='Ligne de coup')
            mirande['c'].plot(color=['red'], alpha = 0.3, linestyle='-', label='Forme IETE')
            mirande3['h'].plot(color=['green'], alpha = 0.3, linestyle='-', label='Plus Haut')
            mirande3['l'].plot(color=['red'], alpha = 0.3, linestyle='-', label='Plus Bas')
            plt.axhline(y=J[1] + moyenne_tete, linestyle='--', alpha=0.3, color='red', label='100% objectif')
            plt.axhline(y=J[1] + (((moyenne_tete) / 2) + ((moyenne_tete) / 4)), linestyle='--', alpha=0.3, color='black', label='75% objectif')
            plt.axhline(y=J[1] + ((moyenne_tete)*50) / 100, linestyle='--', alpha=0.3, color='orange', label='50% objectif')
            plt.axhline(y=J[1] + (moyenne_tete) / 4, linestyle='--', alpha=0.3, color='black', label='25% objectif')
            plt.axhline(y=df['c'].iloc[placejaune] + ((moyenne_tete)*pourc) / 100, linestyle=':', color='pink', label=f'{pourc}% objectif')
            plt.axhline(y=df['c'].iloc[placejaune] - ((moyenne_tete) * pourc2 / 100), linestyle='--', color='red', alpha=0.3, label=f'-{pourc2}% objectif')
            #plt.scatter(x=highs.index, y=highs['c'], alpha=0.5)
            #plt.scatter(x=lows.index, y=lows['c'], alpha=0.5)
            plt.scatter(local_max[0], A, color='blue')
            plt.scatter(local_min[0], B, color='blue')
            plt.scatter(local_max[1], C, color='blue')
            plt.scatter(local_min[1], D, color='blue')
            plt.scatter(local_max[2], E, color='blue')
            plt.scatter(local_min[2], F, color='blue')
            plt.scatter(local_max[3], G, color='blue')
            plt.scatter(I[0], I[1], color='green')
            plt.scatter(J[0], J[1], color='green')
            plt.scatter(placejaune, df['c'].values[placejaune], color='orange', label='BUY')
            if trouver2 == True:
                plt.scatter(placevert, df['c'].iloc[placejaune] + ((moyenne_tete)*pourc / 100), color='green', label='SELL')
            if trouver3 == True:
                plt.scatter(placerouge, df['c'].values[placerouge], color='red', label='SELL')
            if trouver4 == True:
                plt.scatter(placebas, plusbas1, color='purple', label='PLUS BAS')
            plt.text(local_max[0], A, "A", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[0], B, "B", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[1], C, "C", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[1], D, f"D {round(D, 5)}  +{round(pourcent_tete, 3)}%", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[2], E, "E", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_min[2], F, f"F  {round(F, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(local_max[3], G, f"G  {round(G, 5)}", ha='left', style='normal', size=10.5, color='red', wrap=True)
            plt.text(I[0], I[1], "I", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
            plt.text(J[0], J[1], "J", ha='left', style='normal', size=10.5, color='#00FF36', wrap=True)
            # plt.scatter(x=local_max.values, y=df['c'].iloc[local_max], color=['red'], label='haut')
            # plt.scatter(x=highs.index, y=highs["c"])
            # plt.scatter(x=low.index, y=low["c"])
            plt.legend()
            if activ == True:
                plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.1)
                plt.show()
    #exc    ept:
    #        print('')
    #        Write.Print(f'Probleme Titre', Colors.red, interval=0.000)
    #        print('')
        except:
            print('elle beug')
pg_gain = max(debug)
pg_perte = min(debug)
if pg_gain <= 0:
    pg_gain = 'NULL'
if pg_perte >= 0:
    pg_perte = 'NULL'
print('')
print('')
Write.Print(f'Le Gain Cumulé est  : {round(pourcent_gain, 2)}', Colors.purple, interval=0.000)
print('')
Write.Print(f'{round(nombre_regarder, 2)} : Figure(s) Testée(s)', Colors.purple, interval=0.000)
print('')
Write.Print(f'{debug}', Colors.white, interval=0.000)
print('')
print('-------------------')
print('')
Write.Print(f'Gain en Euro pour des mises de : {mise}', Colors.purple, interval=0.000)
print('')
debug2 = []
for nombre in debug:
    resultat = (nombre * mise)/100
    debug2.append(round(resultat,2))
Write.Print(f'{debug2}', Colors.white, interval=0.000)
print('')
print('-------------------')
print('')
Write.Print(f'Plus bas avant Gagner ', Colors.purple, interval=0.000)
print('')
Write.Print(f'{plusbas}', Colors.white, interval=0.000)
print('')
Write.Print(f'Changement : {changement}', Colors.white, interval=0.000)
print('')
Write.Print(f'En pourcentage de la tete :', Colors.purple, interval=0.000)
print('')
Write.Print(f'{pourcentbastete}', Colors.white, interval=0.000)
print('')
Write.Print(f'MIN --> {min(pourcentbastete)}  {pourcentbastete.index(min(pourcentbastete))+1}', Colors.orange, interval=0.000)
pourcentbastete.remove(min(pourcentbastete))
print('')
Write.Print(f'MIN2 --> {min(pourcentbastete)}', Colors.orange, interval=0.000)
print('')
print('-------------------')
print('')
Write.Print(f'{round(nombre_gagnant, 2)} Figure(s) Gagnante(s)', Colors.green, interval=0.000)
print('')
Write.Print(f'{round(nombre_perdant, 2)} Figure(s) Perdante(s)', Colors.red, interval=0.000)
print('')
print('')
pourc_gagn = (nombre_gagnant*100)/len(debug)
pourc_gagn = round(pourc_gagn,2)
Write.Print(f'{pourc_gagn} Pourcentage gagnant', Colors.white, interval=0.000)
print('')
Write.Print(f'Le Plus gros Gain : {pg_gain}', Colors.white, interval=0.000)
print('')
Write.Print(f'La Plus grosse Perte : {pg_perte}', Colors.white, interval=0.000)
print('')
argent_final = (mise*pourcent_gain)/100
argent_final = round(argent_final,3)
if argent_final > 0:
    ajout = '+'
if argent_final < 0:
    ajout = ''
Write.Print(f'Solde : {ajout}{argent_final}€', Colors.white, interval=0.000)
print('')
somme = sum(debug)
moyenne = somme / len(debug)
print(somme)
print(len(debug))
Write.Print(f'Gain Moyen : {round(moyenne,3)}', Colors.white, interval=0.000)
print('')
Write.Print(f'Nombre de Figure(s) Fini(s) : {len(debug)}', Colors.white, interval=0.000)
print('')
Write.Print(f'Nombre de Figure(s) en Cour(s) : {round(nombre_regarder - (len(debug)),2)}', Colors.white, interval=0.000)
print('')
Write.Print(f'Nombre de Point(s) Moyen(s) : {round(nombre_point / len(debug),2)}', Colors.white, interval=0.000)
print('')
Write.Print(f'Nombre Magique(s) : {nombre_magique}', Colors.white, interval=0.000)
print('')
Write.Print(f'{laquelle}', Colors.white, interval=0.000)
print('')
Write.Print(f'pourcent tete {toutemoyennetete}', Colors.white, interval=0.000)
print('')
Write.Print(f'pourcent tete {sum(toutemoyennetete)}', Colors.white, interval=0.000)
print('')
Write.Print(f'pourcent tete {len(toutemoyennetete)}', Colors.white, interval=0.000)
print('')