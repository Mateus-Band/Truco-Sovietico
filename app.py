from flask import Flask, jsonify, request, render_template
import random
import os
from threading import Lock

app = Flask(__name__)
app_lock = Lock()

# --- Definições do jogo ---
nomes_cartas = {
    0: "Porcão", 1: "Q", 2: "J", 3: "K", 4: "A", 5: "2", 6: "3",
    7: "Coringa", 8: "Ouros", 9: "Espadilha", 10: "Copão", 11: "Zap"
}

# Variáveis globais protegidas por lock
game_state = {
    'cartas_disponiveis': [],
    'jogadores': [[] for _ in range(4)],
    'mesa': [],
    'vez': 0,
    'ti1': 0,
    'ti2': 0,
    'rodada_atual': 1,
    'jogo_iniciado': False
}

# --- Funções do jogo ---
def resetar_cartas():
    game_state['cartas_disponiveis'] = [
        0, 1, 1, 1, 1, 2, 2, 2, 2,
        3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5,
        7, 8, 9, 10, 11
    ]
    random.shuffle(game_state['cartas_disponiveis'])

def distribuir():
    for p in game_state['jogadores']:
        p.clear()
    for _ in range(3):
        for p in game_state['jogadores']:
            if game_state['cartas_disponiveis']:
                p.append(game_state['cartas_disponiveis'].pop())

def reiniciar_rodada():
    with app_lock:
        resetar_cartas()
        distribuir()
        game_state['mesa'] = []
        game_state['vez'] = 0
        game_state['ti1'] = 0
        game_state['ti2'] = 0
        game_state['rodada_atual'] = 1
        game_state['jogo_iniciado'] = True

def determinar_ganhador():
    valores = [c for _, c in game_state['mesa']]
    if 0 in valores and 11 in valores:  # Porcão e Zap
        return [i for i, c in game_state['mesa'] if c == 0][0]
    maior = max(valores)
    return [i for i, c in game_state['mesa'] if c == maior][0]

def jogar(indice):
    with app_lock:
        if not game_state['jogo_iniciado']:
            return "Jogo não iniciado. Clique em Iniciar Jogo."
        
        if game_state['vez'] > 3:
            return "Aguardando nova rodada."
        
        if indice < 0 or indice >= len(game_state['jogadores'][game_state['vez']]):
            return "Índice de carta inválido."
        
        carta = game_state['jogadores'][game_state['vez']].pop(indice)
        game_state['mesa'].append((game_state['vez'], carta))
        game_state['vez'] += 1

        if game_state['vez'] == 4:
            ganhador = determinar_ganhador()
            if ganhador in [0, 2]:
                game_state['ti1'] += 1
            else:
                game_state['ti2'] += 1
            
            game_state['rodada_atual'] += 1
            game_state['vez'] = 0
            game_state['mesa'] = []
            
            # Redistribui cartas se o jogo não terminou
            if game_state['ti1'] < 2 and game_state['ti2'] < 2:
                resetar_cartas()
                distribuir()

        if game_state['ti1'] == 2:
            resultado = "Time 1 venceu a rodada!"
            reiniciar_rodada()
            return resultado
        elif game_state['ti2'] == 2:
            resultado = "Time 2 venceu a rodada!"
            reiniciar_rodada()
            return resultado
        
        return "Carta jogada com sucesso!"

# --- Rotas da API ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cartas')
def get_cartas():
    if not game_state['jogo_iniciado']:
        return jsonify(cartas=["Jogo não iniciado"], status="aguardando")
    
    if game_state['vez'] > 3:
        return jsonify(cartas=["Aguardando próxima rodada"], status="espera")
    
    cartas = game_state['jogadores'][game_state['vez']]
    nomes = [nomes_cartas[c] for c in cartas]
    return jsonify(cartas=nomes, status="ativo", vez=game_state['vez']+1)

@app.route('/jogar/<int:indice>', methods=['POST'])
def jogar_carta(indice):
    resultado = jogar(indice)
    return jsonify(resultado=resultado)

@app.route('/iniciar', methods=['POST'])
def iniciar():
    reiniciar_rodada()
    return jsonify(mensagem="Jogo iniciado!", status="sucesso")

@app.route('/placar')
def placar():
    return jsonify(
        time1=game_state['ti1'],
        time2=game_state['ti2'],
        rodada=game_state['rodada_atual'],
        jogo_iniciado=game_state['jogo_iniciado']
    )

@app.route('/status')
def status():
    return jsonify(game_state)

# --- Inicialização ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
