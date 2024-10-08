# Projeto Ora Bolas!
#
# Feito por: Gabriela M. Ciocci, Gabriel Balbine, João Paulo
# Disciplina: CF2111
# Coordenador(a): Simone Camargo Trippe
# Ciclo: 2° Semestre. 
# Curso: Ciência da Computação
# Universidade: Centro Universitário FEI

# Para começar o nosso projeto, primeiro precisamos importar todas as bibliotecas que iremos utilizar.

# Utilizamos a biblioteca matplotlib para criar os gráficos do programa.
# Utilizamos a biblioteca tkinter para conseguir criar a interface gráfica do programa.
# Utilizamos a biblioteca math para poder executar contas matemáticas mais complexas.
# Utilizamos a biblioteca random para poder criar a opção de criar um ponto randômico, que será explicado futuramente.
# Utilizamos a biblioteca time para conseguir criar a animação no intervalo de tempo definido pela professora.

import matplotlib.pyplot as plt
from tkinter import *
import math
import random
import time

# Variáveis globais necessárias para criação do projeto.
# Delta: variável responsável por definir a aceleração máxima que o robô pode ter no intervalo de tempo de 20ms,
# que foi definido pela professora através dos dados da bola fornecidos.
# Count: variável criada para caminhar pelas listas de dados e será explicada futuramente.
# Collision: variável responsável por dizer ao código se houve colisão entre a bola e o robô ou não. Esta colisão é definida
# pelo raio de interceptação, que será explicado futuramente.
# Dist_Euclidean: lista responsável por armazenar a distância do robô e da bola a cada intervalo de tempo de 20ms.
# Scale: variável responsável por definir a relação entre as dimensões reais e do espaço representado no programa.

delta = 2.8 * 0.02
count = 0
collision = False
dist_euclidean = []
scale = 1.5
interception_radius = 0
error_percentual = 0.005

# Abrimos o arquivo onde estão os pontos da bola, chamado de "pontos.txt"
# OBS: não esqueça de verificar se o arquivo "pontos.txt" está na mesma pasta do programa!

archive = open("pontos.txt", "r")
archive_read = archive.read()
archive.close()

# Formatação do arquivo para facilitar no processo de adição às listas.

archive_read = archive_read.replace("\n", " ")
archive_read = archive_read.split(" ")

# Aqui estão todos os atores necessários para conclusão deste trabalho. Cada ator foi separado através de dicionários
# para organização, e assim adicionar seus devidos atributos de forma visível e prática.

robot = {
    "d": 18,
    "a": [[0, 0]],
    "v": [[0, 0]],
    "s": [],
}

ball = {
    "d": 4.3,
    "time": [],
    "x": [],
    "y": [],
    "v": [],
    "a": [],
}

# Momento da adição dos dados da bola em suas devidas listas
# Primeira lista: tempo (20ms, de 0 à 20s)
# Segunda lista: pontos X - abiscissas
# Terceira lista: pontos Y - ordenadas

for i in range(0, len(archive_read), 3):
    ball["time"].append(float(archive_read[i]))

for i in range(1, len(archive_read), 3):
    ball["x"].append(float(archive_read[i]))

for i in range(2, len(archive_read), 3):
    ball["y"].append(float(archive_read[i]))

# DADOS:
# Modelo do robô: Small-Size.
# Algorítmo escolhido para realização do trabalho: robô caçador.

# Objetivo: fazer com que o robô intercepte com a bola.

# Problemática: quanto o robô deve se movimentar em X e em Y para que sua movimentação não ultrapasse 2.8 metros por segundo.

# Solução: inicialmente recebemos do usuário as coordenadas X e Y do robô. Com essas coordenadas, precisamos criar uma reta 
# entre a posição da bola e a do robô. Como estamos trabalhando em um plano 2D, nossa reta tem como parâmetros uma distância 
# em X e uma distância em Y. Ligando esses pontos, obtemos um triângulo pitagórico. Em nossas aulas de física, aprendemos 
# que para descobrir a distância de um vetor em X e em Y é feito sua decomposição vetorial para determinar as distâncias nas 
# respectivas direções através das fórmulas (Ax = A * cos Θ) e (Ay  = A * sen Θ).

# Nosso robô inicia parado, ou seja, com velocidade e aceleração iguais a 0. E sabemos que nosso robô tem como especificações
# a velocidade máxima de 2.8m/s e aceleração máxima de 2.8m/s². A professora nos forneceu os pontos de movimentação da bola
# com um intervalo de 0.02s, então por isso, precisamos fazer todos os cálculos a cada 0.02s. Primeiramente, precisamos descobrir 
# qual é a aceleração máxima para esse intervalo de tempo, multiplicando 2.8 por 0.02 e obtendo nosso delta da aceleração
# que foi apresentado anteriormente. Também precisamos criar o triângulo pitagórico a cada 0.02s, para poder obter os diferentes
# valores em X e em Y e calcular o ângulo que o vetor de aceleração deve ter para o robô estar sempre em direção à bola.

# Enquanto o módulo da aceleração não chega em 2.8m/s², o valor obtido através das fórmulas é somado com o anterior e a velocidade
# do robô está crescendo proporcionalmente com a aceleração. Quando o módulo da aceleração chega à 2.8m/s², então a aceleração do
# robô se torna contantemente 0, pois não é mais necessário acelerar. Porém, quando fazemos isso, perdemos nossa referência do
# ângulo. Para reverter essa situação, pegamos o valor máximo da velocidade que é 2.8m/s e multiplicamos pelo cosseno (X) e 
# seno (Y) do ângulo, pois dessa forma, nosso robô não perde velocidade e ajusta constantemente sua trajetória em direção à bola.

# O valor da posição do robô é obtido somando o valor da velocidade do instante com seu último ponto. Quando a
# distância euclidiana do robô e da bola é igual ao valor do raio de interceptação, então o robô realiza o seu chute ao gol.
# Para esse projeto, não foi necessário animar o chute pois nosso objetivo era apenas interceptar o robô e a bola.

# Obs: todos os valores são obtidos simultaneamente e estão em constante mudança: aceleração, velocidade e posição.
# Obs: todos os cálculos são feitos para cada intervalo de tempo. Ou seja, todas as funções são chamadas para cada ponto.

# Aqui estão todas as funções necessárias para a conclusão do projeto. 

# getAngle(): cria o triângulo pitagórico e pega o ângulo.

def getAngle():
    global count
    Q = 0
    dist_x = ball["x"][int(count/0.02)] - robot["s"][-1][0]
    dist_y = ball["y"][int(count/0.02)] - robot["s"][-1][1]

    if dist_x == 0:
        if dist_y > 0:
            ang = math.pi / 2
            return ang
        else:
            ang = 3 * (math.pi / 2)
            return ang
    if dist_y == 0:
        if dist_x > 0:
            ang = 0
            return ang
        else:
            ang = math.pi
            return ang
    elif dist_x > 0 and dist_y > 0:
        Q = 1
    elif dist_x < 0 and dist_y > 0:
        Q = 2
    elif dist_x < 0 and dist_y < 0:
        Q = 3
    elif dist_x > 0 and dist_y < 0:
        Q = 4

    if(dist_x != 0):
        tg = 0
        if(Q == 2 or Q == 4):
            tg = abs(dist_x) / abs(dist_y)
        else:
            tg = abs(dist_y) / abs(dist_x)

        tg = math.atan(tg)
        ang = tg + (Q - 1) * (math.pi / 2)
        return ang


# adaptedAcceleration(vector): IMPORTANTE! 
# É muito difícil ocorrer um caso onde o módulo da aceleração será igual a 2.8m/s, por isso, fizemos essa função que adapta
# a aceleração caso o módulo da próxima aceleração (ponto futuro) seja maior que 2.8 e o atual seja menor.
# Ele pega o módulo do vetor da aceleração futura e compara com o valor desejado (que é 2.8m/s²) mais um erro percentual que  
# foi estabelecido por nós, se caso o valor da diferença do módulo entre o ponto futuro e o ponto atual estiver maior que o
# erro percentual, ele pega esse valor e divide pela metade. Se for menor, ele pega esse valor e multiplica por sua metade.
# Enquanto o valor da diferença do módulo não estiver dentro do erro percentual, ele ficará adaptando.

def adaptedAcceleration(vector):
    actual = 0
    desired = 2.8
    while True:
        next_vector = [[robot["v"][-1][0] + vector[0], robot["v"][-1][1] + vector[1]]]
        actual = verifyVector(next_vector)
        if((actual - desired) < 0.00005 and (actual - desired) > -0.00005):
            return vector
        if((actual - desired) > 0.00005):
            vector[0] /= 2
            vector[1] /= 2
        elif((actual - desired) < -0.00005):
            vector[0] *= 1.5
            vector[1] *= 1.5


# getAccelerationRobot(): pega a aceleração do robô.

def getAccelerationRobot():
    global delta
    ang = getAngle()
    delta_a = [delta * math.cos(ang), delta * math.sin(ang)]

    if(len(robot["a"]) > 0 and verifyVector(robot["v"]) < 2.8):
        next_acceleration = [delta_a[0] + robot["a"][-1][0], delta_a[1] + robot["a"][-1][1]]
        if(verifyVector([[robot["v"][-1][0] + next_acceleration[0], robot["v"][-1][1] + next_acceleration[1]]]) >= 2.8):
            next_acceleration = adaptedAcceleration(next_acceleration)
        robot["a"].append(next_acceleration)
    else:
        robot["a"].append([0, 0])

# getSpeedRobot(): pega a velocidade do robô.

def getSpeedRobot():
    ang = getAngle()

    if(robot["a"][-1] != [0, 0]):
        robot["v"].append([robot["v"][-1][0] + robot["a"][-1][0], robot["v"][-1][1] + robot["a"][-1][1]])
    else: 
        robot["v"].append([2.8 * math.cos(ang), 2.8 * math.sin(ang)])


# verifyVector(vector): verifica o módulo do vetor.

def verifyVector(vector):
    return math.sqrt((vector[-1][0] ** 2) + (vector[-1][1] ** 2))


# getPositionRobot(): pega a posição do robô

def getPositionRobot():
    robot["s"].append([robot["s"][-1][0] + robot["v"][-1][0] * 0.02, robot["s"][-1][1] + robot["v"][-1][1] * 0.02])


# getDistanceEuclidean(): pega o valor da distância euclidiana

def getDistanceEuclidean():
    dist_x = ball["x"][int(count/0.02)] - robot["s"][-1][0]
    dist_y = ball["y"][int(count/0.02)] - robot["s"][-1][1]
    return (math.sqrt((dist_x ** 2) + (dist_y ** 2)))


# getInterceptionPoint(): IMPORTANTE!
# Nesse caso, também precisamos criar uma adaptação do ponto de interceptação, pois a chance de as distâncias serem exatamente
# iguais ao ponto de interceptação é muito difícil de ocorrer. O processo é basicamente o mesmo que o da aceleração adaptativa,
# porém, também é necessário pegar o tempo exato em que o robô e a bola interceptam, e assim substituir o valor do tempo no
# valor que seria se não tivesse ocorrido a interceptação. Esse valor sempre será menor que 0.02s.
# Ele é necessário para nosso aprofundamento e para criar os gráficos da aceleração, pois se não existisse esse valor do tempo
# exato, o código entenderia que a velocidade e a aceleração da bola teriam mudado de forma extremamente significativa.

def getInterceptionPoint():
    global interception_radius
    time_value = 0.02
    time_pos = len(robot["s"]) - 1
    factor = 1
    error_percentual = interception_radius * 0.005

    delta_x_robot = 0
    delta_y_robot = 0
    delta_x_ball = 0
    delta_y_ball = 0

    while True:
        delta_x_robot = (robot["s"][time_pos][0] - robot["s"][time_pos - 1][0]) * factor + robot["s"][time_pos - 1][0]
        delta_y_robot = (robot["s"][time_pos][1] - robot["s"][time_pos - 1][1]) * factor + robot["s"][time_pos - 1][1]
        delta_x_ball = (ball["x"][time_pos] - ball["x"][time_pos - 1]) * factor + ball["x"][time_pos - 1]
        delta_y_ball = (ball["y"][time_pos] - ball["y"][time_pos - 1]) * factor + ball["y"][time_pos - 1]
        time_value = 0.02 * factor

        delta_x = delta_x_ball - delta_x_robot
        delta_y = delta_y_ball - delta_y_robot
        dist_interpolation = math.sqrt(delta_x ** 2 + delta_y ** 2)

        if(dist_interpolation > interception_radius + error_percentual):
            factor *= 1.5
        elif(dist_interpolation < interception_radius - error_percentual):
            factor /= 2
        else:
            ball["x"][time_pos] = delta_x_ball
            ball["y"][time_pos] = delta_y_ball
            ball["time"][time_pos] = ball["time"][time_pos - 1] + time_value

            robot["s"][time_pos][0] = delta_x_robot
            robot["s"][time_pos][1] = delta_y_robot
            return


# getInterceptionRadius(): verifica se houve interceptação comparando o valor da distância euclidiana com o valor do raio de
# interceptação.

def getInterceptionRadius():
    global collision
    global dist_euclidean
    global interception_radius

    robot_radius = robot["d"] / 2
    ball_radius = ball["d"] / 2
    inner_radius = ball["d"] * 0.2

    dist = getDistanceEuclidean()
    interception_radius = (robot_radius + ball_radius - inner_radius) / 100

    if(dist > interception_radius):
        dist_euclidean.append(dist)

    elif(dist <= interception_radius):
        dist_euclidean.append(dist)
        getInterceptionPoint()
        collision = True


# updateRobot(): função responsável por fazer os cálculos da velocidade, aceleração e posição do robô para cada intervalo de
# 0.02s, também compara se houve colisão entre os objetos ou não.

def updateRobot():
    global count

    getDistanceEuclidean()
    getInterceptionRadius()

    if(collision == False):
        getAccelerationRobot()
        getSpeedRobot()
        getPositionRobot()
        count += 0.02


# getRobotCoords(): estabelece o ponto inicial do robô.

def getRobotCoords():
    print("Você gostaria de escolher a posição inicial ou criar uma posição aleatória?")
    print("1) Escolher posição;")
    print("2) Criar posição inicial aletaória.")
    option = int(input())

    if(option == 1):
        print()
        x_robot = float(input("Digite a posição X do robô: "))
        y_robot = float(input("Digite a posição Y do robô: "))
        robot["s"].append([x_robot, y_robot])

    elif(option == 2):
        print()
        x_robot = random.randrange(0, 91, 1) / 10
        y_robot = random.randrange(0, 61, 1) / 10
        robot["s"].append([x_robot, y_robot])

    else:
        print("Opção inválida.\n")
        getRobotCoords()


# createVectorDeepening(): nosso aprofundamento. Cria os vetores na animação pegando a velocidade e aceleração instantânea
# do robô e da bola. Lembrando que a velocidade e a aceleração instantânea são obtidos subtraindo o valor atual menos o anterior.

def createVectorDeepening():
    time_interception = []

    for i in range(len(robot["s"])):
        time_interception.append(ball["time"][i])

    for i in range(len(time_interception)):
        time_divider = 0.02
        
        if ball["time"][i + 1] % 0.02 != 0:
            time_divider = ball["time"][i + 1] - ball["time"][i]

        ball["v"].append([(ball["x"][i + 1] - ball["x"][i]) / time_divider, (ball["y"][i + 1] - ball["y"][i]) / time_divider])
        ball["a"].append([(ball["v"][i][0] - ball["v"][i - 1][0]) / time_divider, (ball["v"][i][1] - ball["v"][i - 1][1]) / time_divider])


# createGraphics(): cria os gráficos.

def createGraphics():
    robot_x2 = []
    robot_y2 = []
    robot_vx = []
    robot_vy = []
    robot_ax = []
    robot_ay = []

    ball_x2 = []
    ball_y2 = []
    ball_vx = []
    ball_vy = []
    ball_ax = []
    ball_ay = []

    time_interception = []

    for i in range(len(robot["s"])):
        ball_x2.append(ball["x"][i])
        ball_y2.append(ball["y"][i])
        robot_x2.append(robot["s"][i][0])
        robot_y2.append(robot["s"][i][1])
        time_interception.append(ball["time"][i])

    for i in range(len(time_interception)):
        time_divider = 0.02
        robot_vx.append(robot["v"][i][0])
        robot_vy.append(robot["v"][i][1])
        robot_ax.append(robot["a"][i][0])
        robot_ay.append(robot["a"][i][1])

        if ball["time"][i + 1] % 0.02 != 0:
            time_divider = ball["time"][i + 1] - ball["time"][i]

        ball_vx.append((ball["x"][i + 1] - ball["x"][i]) / time_divider)
        ball_vy.append((ball["y"][i + 1] - ball["y"][i]) / time_divider)
        ball_ax.append((ball_vx[i] - ball_vx[i - 1]) / time_divider)
        ball_ay.append((ball_vy[i] - ball_vy[i - 1]) / time_divider)

    print("===================================================")
    print("                    GRÁFICOS")
    print("===================================================\n")
    print("Qual gráfico você gostaria de observar?")
    print("1) Gráfico das trajetórias da bola e do robô em um plano XY, até o ponto de interceptação;")
    print("2) Gráfico das coordenadas X da posição da bola em função do tempo t até o instante de interceptação;")
    print("3) Gráfico das coordenadas Y da posição da bola em função do tempo t até o instante de interceptação;")
    print("4) Gráfico das coordenadas X da posição do robô em função do tempo t até o instante de interceptação;")
    print("5) Gráfico das coordenadas Y da posição do robô em função do tempo t até o instante de interceptação;")
    print("6) Gráfico dos componentes VX da velocidade da bola em função do tempo t até o instante de interceptação;")
    print("7) Gráfico dos componentes VY da velocidade da bola em função do tempo t até o instante de interceptação;")
    print("8) Gráfico dos componentes VX da velocidade do robô em função do tempo t até o instante de interceptação;")
    print("9) Gráfico dos componentes VY da velocidade do robô em função do tempo t até o instante de interceptação;")
    print("10) Gráfico dos componentes AX da aceleração da bola em função do tempo t até o instante de interceptação;")
    print("11) Gráfico dos componentes AY da aceleração da bola em função do tempo t até o instante de interceptação;")
    print("12) Gráfico dos componentes AX da aceleração do robô em função do tempo t até o instante de interceptação;")
    print("13) Gráfico dos componentes AY da aceleração do robô em função do tempo t até o instante de interceptação;")
    print("14) Gráfico da distância relativa D entre o robô e a bola como função do tempo t até o instante de interceptação;")
    print("15) Rever a animação;")
    print("16) Sair.")

    while True:
        option = int(input())

        if(option == 1):
            plt.plot(robot_x2, robot_y2)
            plt.plot(ball_x2, ball_y2)
            plt.plot(ball["x"], ball["y"], 'r--')
            plt.plot(robot_x2[-1], robot_y2[-1], 'ro')
            plt.plot(ball_x2[-1], ball_y2[-1], 'ro')

            # Título e nome dos eixos
            plt.title("Gráfico da trajetória da bola e do robô.")
            plt.xlabel("X")
            plt.ylabel("Y")

            # Mostra o gráfico
            plt.show()

        elif(option == 2):
            plt.plot(time_interception, ball_x2)

            # Título e nome dos eixos
            plt.title("Gráfico das coordenadas X da bola em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("X")

            # Mostra o gráfico
            plt.show()

        elif(option == 3):
            plt.plot(time_interception, ball_y2)

            # Título e nome dos eixos
            plt.title("Gráfico das coordenadas Y da bola em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("Y")

            # Mostra o gráfico
            plt.show()

        elif(option == 4):
            plt.plot(time_interception, robot_x2)

            # Título e nome dos eixos
            plt.title("Gráfico das coordenadas X do robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("X")

            # Mostra o gráfico
            plt.show()

        elif(option == 5):
            plt.plot(time_interception, robot_y2)

            # Título e nome dos eixos
            plt.title("Gráfico das coordenadas Y do robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("Y")

            # Mostra o gráfico
            plt.show()

        elif(option == 6):
            plt.plot(time_interception, ball_vx)

            # Título e nome dos eixos
            plt.title("Gráfico de velocidade em X da bola em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("VX")

            # Mostra o gráfico
            plt.show()

        elif(option == 7):
            plt.plot(time_interception, ball_vy)

            # Título e nome dos eixos
            plt.title("Gráfico de velocidade em Y da bola em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("VY")

            # Mostra o gráfico
            plt.show()

        elif(option == 8):
            plt.plot(time_interception, robot_vx)

            # Título e nome dos eixos
            plt.title("Gráfico de velocidade em X do robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("VX")

            # Mostra o gráfico
            plt.show()

        elif(option == 9):
            plt.plot(time_interception, robot_vy)

            # Título e nome dos eixos
            plt.title("Gráfico de velocidade em Y do robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("VY")

            # Mostra o gráfico
            plt.show()

        elif(option == 10):
            plt.plot(time_interception, ball_ax)

            # Título e nome dos eixos
            plt.title("Gráfico da aceleração em X da bola em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("AX")

            # Mostra o gráfico
            plt.show()

        elif(option == 11):
            plt.plot(time_interception, ball_ay)

            # Título e nome dos eixos
            plt.title("Gráfico da aceleração em Y da bola em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("AY")

            # Mostra o gráfico
            plt.show()

        elif(option == 12):
            plt.plot(time_interception, robot_ax)

            # Título e nome dos eixos
            plt.title("Gráfico da aceleração em X do robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("AX")

            # Mostra o gráfico
            plt.show()

        elif(option == 13):
            plt.plot(time_interception, robot_ay)

            # Título e nome dos eixos
            plt.title("Gráfico da aceleração em Y do robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("AY")

            # Mostra o gráfico
            plt.show()

        elif(option == 14):
            plt.plot(time_interception, dist_euclidean)

            # Título e nome dos eixos
            plt.title("Distância relativa D entre a bola e o robô em função do tempo.")
            plt.xlabel("Tempo (t)")
            plt.ylabel("Distância")

            # Mostra o gráfico
            plt.show()

        elif(option == 15):
            createInterface()

        elif(option == 16):
            break

        else:
            print("Opção inválida.")


# createInterface(): cria a janela de animação.

def createInterface():
    global scale
    w = int(900 * scale)
    h = int(600 * scale)

    root = Tk()
    root.title("Ora Bolas")
    root.geometry("{}x{}+0+0".format(w, h))
    root.maxsize(w, h)
    root.minsize(w, h)
    root.attributes('-topmost',True)

    C = Canvas(root, height=h, width=w)

    cont_interface = 0
    pixel_scale = int(100 * scale)
    vector_scale = float(1 / 5)

    while(cont_interface != len(robot["s"])):
        C.delete("all")
        C.config(bg="#306324")
        C.pack()

        x0_robot_pixel = (robot["s"][cont_interface][0] * pixel_scale) - ((robot["d"] / 2) * scale)
        y0_robot_pixel = (robot["s"][cont_interface][1] * pixel_scale) - ((robot["d"] / 2) * scale)
        x_robot_pixel = (robot["s"][cont_interface][0] * pixel_scale) + ((robot["d"] / 2) * scale)
        y_robot_pixel = (robot["s"][cont_interface][1] * pixel_scale) + ((robot["d"] / 2) * scale)
        center_robot_pixel = [(robot["s"][cont_interface][0] * pixel_scale), (robot["s"][cont_interface][1] * pixel_scale)]
        v_robot_pixel = [((robot["s"][cont_interface][0] + (robot["v"][cont_interface][0] * vector_scale)) * pixel_scale), ((robot["s"][cont_interface][1] + (robot["v"][cont_interface][1] * vector_scale)) * pixel_scale)]
        a_robot_pixel = [((robot["s"][cont_interface][0] + (robot["a"][cont_interface][0]* vector_scale)) * pixel_scale), ((robot["s"][cont_interface][1] + (robot["a"][cont_interface][1] * vector_scale)) * pixel_scale)]
        v_mod_robot = math.sqrt((robot["v"][cont_interface][0] ** 2) + (robot["v"][cont_interface][1] ** 2))
        a_mod_robot = math.sqrt((robot["a"][cont_interface][0] ** 2) + (robot["a"][cont_interface][1] ** 2))

        x0_ball_pixel = (ball["x"][cont_interface] * pixel_scale) - ((ball["d"] / 2) * scale)
        y0_ball_pixel = (ball["y"][cont_interface] * pixel_scale) - ((ball["d"] / 2) * scale)
        x_ball_pixel = (ball["x"][cont_interface] * pixel_scale) + ((ball["d"] / 2) * scale)
        y_ball_pixel = (ball["y"][cont_interface] * pixel_scale) + ((ball["d"] / 2) * scale)
        center_ball_pixel = [(ball["x"][cont_interface] * pixel_scale), (ball["y"][cont_interface] * pixel_scale)]
        v_ball_pixel = [((ball["x"][cont_interface] + (ball["v"][cont_interface][0] * vector_scale)) * pixel_scale), ((ball["y"][cont_interface] + (ball["v"][cont_interface][1] * vector_scale)) * pixel_scale)]
        a_ball_pixel = [((ball["x"][cont_interface] + (ball["a"][cont_interface][0] * vector_scale)) * pixel_scale), ((ball["y"][cont_interface] + (ball["a"][cont_interface][1] * vector_scale)) * pixel_scale)]
        v_mod_ball = math.sqrt((ball["v"][cont_interface][0] ** 2) + (ball["v"][cont_interface][1] ** 2))
        a_mod_ball = math.sqrt((ball["a"][cont_interface][0] ** 2) + (ball["a"][cont_interface][1] ** 2))

        for i in range(0, cont_interface, 2):
            draw_robot_path = line = C.create_line((robot["s"][i][0] * pixel_scale), (h - (robot["s"][i][1] * pixel_scale)), (robot["s"][i + 1][0] * pixel_scale), (h - (robot["s"][i + 1][1] * pixel_scale)), fill="#333333", width=4)
            draw_ball_path = line = C.create_line((ball["x"][i] * pixel_scale), (h - (ball["y"][i] * pixel_scale)), (ball["x"][i + 1] * pixel_scale), (h - (ball["y"][i + 1] * pixel_scale)), fill="#bbbbbb", width=4)

        draw_robot_vel = C.create_line(center_robot_pixel[0], (h - center_robot_pixel[1]), v_robot_pixel[0], (h - v_robot_pixel[1]), arrow=LAST, width=3, fill="#95abc1")
        draw_ball_vel = C.create_line(center_ball_pixel[0], (h - center_ball_pixel[1]), v_ball_pixel[0], (h - v_ball_pixel[1]), arrow=LAST, width=3, fill="#fcdbe2")
        draw_robot_acc = C.create_line(center_robot_pixel[0], (h - center_robot_pixel[1]), a_robot_pixel[0], (h - a_robot_pixel[1]), arrow=LAST, width=3, fill="#e4d1e6")
        draw_ball_acc = C.create_line(center_ball_pixel[0], (h - center_ball_pixel[1]), a_ball_pixel[0], (h - a_ball_pixel[1]), arrow=LAST, width=3, fill="#f7b1bd")

        text_robot_vel = C.create_text(v_robot_pixel[0] + 25, (h - v_robot_pixel[1] + 25), text="|V| = {:.3g}".format(v_mod_robot), font=("Helvetica", "15", "bold"))
        text_ball_vel = C.create_text(v_ball_pixel[0] + 25, (h - v_ball_pixel[1] + 25), text="|V| = {:.3g}".format(v_mod_ball), font=("Helvetica", "15", "bold"))
        text_robot_acc = C.create_text(a_robot_pixel[0] + 25, (h - a_robot_pixel[1] + 25), text="|A| = {:.3g}".format(a_mod_robot), font=("Helvetica", "15", "bold"))
        text_ball_acc = C.create_text(a_ball_pixel[0] + 25, (h - a_ball_pixel[1] + 25), text="|A| = {:.3g}".format(a_mod_ball), font=("Helvetica", "15", "bold"))

        draw_robot = C.create_oval(x0_robot_pixel, (h - y0_robot_pixel), x_robot_pixel, (h - y_robot_pixel), fill="#000000")
        draw_ball = C.create_oval(x0_ball_pixel, (h - y0_ball_pixel), x_ball_pixel, (h - y_ball_pixel), fill="#ffffff")
            
        cont_interface += 1
        time.sleep(0.02)
        C.update()

    root.mainloop()


# main() = tick()

def tick():
    global collision

    print("===================================================")
    print("               Projeto Ora Bolas!")
    print("Por: Gabriela Ciocci, João Paulo, Gabriel Balbine")
    print("            Aperte enter para começar.")
    print("===================================================")
    input()

    getRobotCoords()

    while(collision == False):
        updateRobot()
    else:
        createVectorDeepening()
        createInterface()
        createGraphics()


tick()
