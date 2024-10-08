# =====[Projeto Ora Bolas!]=====

# Feito por: Gabriela M. Ciocci | Gabriel Balbine | João Paulo
# Ciclo: 2° Semestre. 
# Curso: Ciência da Computação
# Universidade: Centro Universitário FEI



# DADOS:
# Modelo do robô: Small-Size.
# Algorítmo escolhido para realização do trabalho: robô caçador.



Objetivo: fazer com que o robô intercepte com a bola.

Problemática: quanto o robô deve se movimentar em X e em Y para que sua movimentação não ultrapasse 2.8 metros por segundo.

Solução: inicialmente recebemos do usuário as coordenadas X e Y do robô. Com essas coordenadas, precisamos criar uma reta entre a posição da bola e a do robô. Como estamos trabalhando em um plano 2D, nossa reta tem como parâmetros uma distância em X e uma distância em Y. Ligando esses pontos, obtemos um triângulo pitagórico. Em nossas aulas de física, aprendemos que para descobrir a distância de um vetor em X e em Y é feito sua decomposição vetorial para determinar as distâncias nas respectivas direções através das fórmulas (Ax = A * cos Θ) e (Ay  = A * sen Θ).

Nosso robô inicia parado, ou seja, com velocidade e aceleração iguais a 0. E sabemos que nosso robô tem como especificações a velocidade máxima de 2.8m/s e aceleração máxima de 2.8m/s². A professora nos forneceu os pontos de movimentação da bola com um intervalo de 0.02s, então por isso, precisamos fazer todos os cálculos a cada 0.02s. Primeiramente, precisamos descobrir qual é a aceleração máxima para esse intervalo de tempo, multiplicando 2.8 por 0.02. Também precisamos criar o triângulo pitagórico a cada 0.02s, para poder obter os diferentes valores em X e em Y e calcular o ângulo que o vetor de aceleração deve ter para o robô estar sempre em direção à bola.

Enquanto o módulo da aceleração não chega em 2.8m/s², o valor obtido através das fórmulas é somado com o anterior e a velocidade do robô está crescendo proporcionalmente com a aceleração. Quando o módulo da aceleração chega à 2.8m/s², então a aceleração do robô se torna contantemente 0, pois não é mais necessário acelerar. Porém, quando fazemos isso, perdemos nossa referência do ângulo. Para reverter essa situação, pegamos o valor máximo da velocidade que é 2.8m/s e multiplicamos pelo cosseno (X) e seno (Y) do ângulo, pois dessa forma, nosso robô não perde velocidade e ajusta constantemente sua trajetória em direção à bola.

O valor da posição do robô é obtido somando o valor da velocidade do instante com seu último ponto. Quando a distância euclidiana do robô e da bola é igual ao valor do raio de interceptação, então o robô realiza o seu chute ao gol. Para esse projeto, não foi necessário animar o chute pois nosso objetivo era apenas interceptar o robô e a bola. 

Obs: todos os valores são obtidos simultaneamente e estão em constante mudança.
Obs: todos os cálculos são feitos para cada intervalo de tempo. Ou seja, todas as contas são refeitas a cada intervalo de tempo de 0.02s.
Obs: o código está documentado, explicado onde está cada função, as variáveis e explicando as funções de adaptação da aceleração e do ponto de interseptação.

Como exemplo, utilizamos o ponto inicial do robô (4,6).



# ORDEM DOS GRÁFICOS:

1) Gráfico das trajetórias da bola e do robô em um plano XY, até o ponto de interceptação;
2) Gráfico das coordenadas X da posição da bola em função do tempo t até o instante de interceptação;
3) Gráfico das coordenadas Y da posição da bola em função do tempo t até o instante de interceptação;
4) Gráfico das coordenadas X da posição do robô em função do tempo t até o instante de interceptação;
5) Gráfico das coordenadas Y da posição do robô em função do tempo t até o instante de interceptação;
6) Gráfico dos componentes VX da velocidade da bola em função do tempo t até o instante de interceptação;
7) Gráfico dos componentes VY da velocidade da bola em função do tempo t até o instante de interceptação;
8) Gráfico dos componentes VX da velocidade do robô em função do tempo t até o instante de interceptação;
9) Gráfico dos componentes VY da velocidade do robô em função do tempo t até o instante de interceptação;
10) Gráfico dos componentes AX da aceleração da bola em função do tempo t até o instante de interceptação;
11) Gráfico dos componentes AY da aceleração da bola em função do tempo t até o instante de interceptação;
12) Gráfico dos componentes AX da aceleração do robô em função do tempo t até o instante de interceptação;
13) Gráfico dos componentes AY da aceleração do robô em função do tempo t até o instante de interceptação;
14) Gráfico da distância relativa D entre o robô e a bola como função do tempo t até o instante de interceptação.
