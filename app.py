from flask import Flask, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# --- Definições do jogo ---
nomes_cartas = {
    0: "Porcão", 1: "Q", 2: "J", 3: "K", 4: "A", 5: "2", 6: "3",
    7: "Coringa", 8: "Ouros", 9: "Espadilha", 10: "Copão", 11: "Zap"
}

# Códigos de cartas
cortazap, joker, ouros, espadilha, copão, zap = 0, 7, 8, 9, 10, 11
familias = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 4, 4]

# Jogo atual
cartas_disponiveis = []
jogadores = [[] for _ in range(4)]
mesa = []
vez = 0
ti1, ti2 = 0, 0
rodada_atual = 1

# --- Funções do jogo ---
def resetar_cartas():
    global cartas_disponiveis
    cartas_disponiveis = [
        0, 1, 1, 1, 1, 2, 2, 2, 2,
        3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5,
        7, 8, 9, 10, 11
    ]
    random.shuffle(cartas_disponiveis)

def distribuir():
    global jogadores
    for p in jogadores:
        p.clear()
        for _ in range(3):
            p.append(cartas_disponiveis.pop())

def reiniciar_rodada():
    global mesa, vez, ti1, ti2, rodada_atual
    resetar_cartas()
    distribuir()
    mesa = []
    vez = 0
    ti1 = 0
    ti2 = 0
    rodada_atual = 1

def jogar(indice):
    global vez, mesa, jogadores, ti1, ti2, rodada_atual
    if vez > 3:
        return "Aguardando nova rodada."
    
    carta = jogadores[vez].pop(indice)
    mesa.append((vez, carta))
    vez += 1

    if vez == 4:
        ganhador = determinar_ganhador()
        if ganhador in [0, 2]:
            ti1 += 1
        else:
            ti2 += 1
        rodada_atual += 1
        vez = 0
        mesa.clear()

    if ti1 == 2:
        reiniciar_rodada()
        return "Time 1 venceu a rodada!"
    elif ti2 == 2:
        reiniciar_rodada()
        return "Time 2 venceu a rodada!"
    return "Carta jogada."

def determinar_ganhador():
    valores = [c for _, c in mesa]
    if cortazap in valores and zap in valores:
        return [i for i, c in mesa if c == cortazap][0]
    maior = max(valores)
    return [i for i, c in mesa if c == maior][0]

# --- Rotas da API ---

@app.route('/cartas')
def get_cartas():
    if vez > 3:
        return jsonify(cartas=["Aguardando próxima rodada"])
    cartas = jogadores[vez]
    nomes = [nomes_cartas[c] for c in cartas]
    return jsonify(cartas=nomes)

@app.route('/jogar/<int:indice>', methods=['POST'])
def jogar_carta(indice):
    if vez > 3 or indice < 0 or indice > 2:
        return jsonify(resultado="Jogada inválida.")
    resultado = jogar(indice)
    return jsonify(resultado=resultado)

@app.route('/iniciar')
def iniciar():
    reiniciar_rodada()
    return jsonify(mensagem="Rodada iniciada.")

@app.route('/placar')
def placar():
    return jsonify(time1=ti1, time2=ti2, rodada=rodada_atual)

# --- Inicializa servidor ---
if __name__ == '__main__':
    reiniciar_rodada()
    app.run(debug=True)
