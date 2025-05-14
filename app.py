import random

time1, time2 = 0, 0
q1, q2, q3, q4 = 1, 1, 1, 1
j1, j2, j3, j4 = 2, 2, 2, 2
k1, k2, k3, k4 = 3, 3, 3, 3
a1, a2, a3 = 4, 4, 4
d1, d2, d3, d4 = 5, 5, 5, 5
t1, t2, t3, t4 = 6, 6, 6, 6
cortazap, joker, ouros, espadilha, copão, zap = 0, 7, 8, 9, 10, 11

nomes_cartas = {0: "Porcão",1: "Q",2: "J",3: "K", 4: "A",5: "2",6: "3",7: "Coringa",8: "Ouros",9: "Espadilha",10: "Copão",11: "Zap"}

cartas = [cortazap, q1, q2, q3, q4, j1, j2, j3, j4, k1, k2, k3, k4, a1, a2, a3, d1, d2, d3, d4, joker, ouros, espadilha, copão, zap]
random.shuffle(cartas)
familias = [q1, q2, q3, q4, j1, j2, j3, j4, k1, k2, k3, k4]
jogadores= [p1, p2, p3, p4] = [], [], [], []

def distribuir(p1, p2, p3, p4):
    global cartas
    for i in range(3):
        p1.append(cartas.pop(random.choice(cartas)))
        p2.append(cartas.pop(random.choice(cartas)))
        p3.append(cartas.pop(random.choice(cartas)))
        p4.append(cartas.pop(random.choice(cartas)))
   
def ver_fam():
    global jogadores, cartas, familias
    for i in jogadores:
        if i[0] in familias and i[1] in familias and i[2] in familias:
            i.clear()
            for k in range(3):
                i.append(cartas.pop(random.choice(range(len(cartas))))) 
def printar_p(p):
    k = jogadores.index(p)
    print(f"p{k+1} tem: ", end="")
    for i in p:
        if i != -1:
            print(nomes_cartas[i], end=" ")
    print()
def printar():
    k = 1
    for j in jogadores:
        print(f"p{k} tem: ", end="")
        print(" ".join([nomes_cartas[i] for i in j]))
        k += 1
    print()
def rodada(P, Q, p1, p2, p3, p4):
    global cartas
    cartas = [cortazap, q1, q2, q3, q4, j1, j2, j3, j4, k1, k2, k3, k4, a1, a2, a3, d1, d2, d3, d4, joker, ouros, espadilha, copão, zap]
    random.shuffle(cartas)
    p1.clear()
    p2.clear()
    p3.clear()
    p4.clear()
    ti1, ti2 = 0, 0
    distribuir(p1, p2, p3, p4)
    printar()
    for i in range(3):
        ver_fam()
    printar()
    bolo = [] #1a rodada
    for p in jogadores:
        printar_p(p)
        x = int(input(f"Escolha uma carta:\n1- {nomes_cartas[p[0]]}\n2- {nomes_cartas[p[1]]}\n3- {nomes_cartas[p[2]]} \n"))
        if x == 1:
            bolo.append(p.pop(0))
        elif x == 2:
            bolo.append(p.pop(1))
        elif x == 3:
            bolo.append(p.pop(2))
        print("\nNa mesa: "," ".join([nomes_cartas[b] for b in bolo]),"\n")
    if cortazap in bolo and zap in bolo:
        m = bolo.index(cortazap)
    else:
        m = bolo.index(max(bolo))
    if m == 0 or m == 2:
            ti1 += 1
    elif m == 1 or m == 3:
            ti2 += 1
    bolo = [] #2a rodada
    for p in jogadores:
        printar_p(p)
        x = int(input(f"Escolha uma carta:\n1- {nomes_cartas[p[0]]}\n2- {nomes_cartas[p[1]]}\nJogar escuro\n3- {nomes_cartas[p[0]]}\n4- {nomes_cartas[p[1]]}\n"))
        if x == 1:
            bolo.append(p.pop(0))
        elif x == 2:
            bolo.append(p.pop(1))
        elif x == 3:
            p.pop(0)
            p.append(-1)
        elif x == 4:
            p.pop(1)
            p.append(-1)
        print("\nNa mesa: "," ".join([nomes_cartas[b] for b in bolo]),"\n")
    if cortazap in bolo and zap in bolo:
        m = bolo.index(cortazap)
    else:
        m = bolo.index(max(bolo))
    if m == 0 or m == 2:
        ti1 += 1
    elif m == 1 or m == 3:
        ti2 += 1
    if ti1 !=2 and ti2 != 2: #3a rodada
        bolo = []
        for p in jogadores:
            printar_p(p)
            x = int(input(f"Escolha uma carta:\n1- {nomes_cartas[p[0]]}\nJogar escuro\n2- {nomes_cartas[p[0]]}\n"))
            if x == 1:
                bolo.append(p.pop(0))
            elif x == 2:
                p.pop(0)
                p.append(-1)
            print("\nNa mesa: "," ".join([nomes_cartas[b] for b in bolo]),"\n")
        if cortazap in bolo and zap in bolo:
            m = bolo.index(cortazap)
        else:
            m = bolo.index(max(bolo))
        if m == 0 or m == 2:
            ti1 += 1
        elif m == 1 or m == 3:
            ti2 += 1
    if ti1 == 2:
        print(f"Ponto pro time 1")
        return 'time1'
    elif ti2 == 2:
        print(f"Ponto pro time 2")
        return 'time2'
    return P
while time1 < 1 and time2 < 1:
    print('Placar: time1 =', time1, 'time2 =', time2, '\n')
    ven = rodada(time1, time2, p1, p2, p3, p4)
    if ven == 'time1':
        time1 += 1
        continue
    elif ven == 'time2':
        time2 += 1
        continue
print('Placar: time1 =', time1, 'time2 =', time2,'\n')
if time1 == 1:
    print("Time 1 ganhou")
elif time2 == 1:
    print("Time 2 ganhou")