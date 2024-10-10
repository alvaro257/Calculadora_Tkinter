from tkinter import *
import re

# Paleta de cores

cor1 = "#3b3b3b"
cor2 = "#feffff"
cor3 = "#38576b"
cor4 = "#ECEFF1"
cor5 = "#FFAB40"
cor6 = "#0388fc"

# Criando uma janela

janela = Tk()
janela.title("Calculadora")
janela.geometry("319x543")
janela.config(bg=cor4)
janela.resizable(False,False)

# Dividindo a janela em frames

# frame que contem a tela que exibe a expressao
frame_tela = Frame(janela, width=319, height=65, bg=cor3)
frame_tela.grid(row=0, column=0)

# frame que contem os botoes
frame_bts = Frame(janela, width=319, height=478)
frame_bts.grid(row=1, column=0)

# Variaveis globais

expressao = ''
tela_resultado = StringVar()
recuperacao_memoria = False
memoria = 0

# Textos

# texto que exibe a expressao no frame_tela
texto = Label(frame_tela, textvariable=tela_resultado, width=16, height=2, padx=1, relief=FLAT, anchor="e", justify=RIGHT, font=('Ivy 25'), bg=cor3, fg=cor2)
texto.place(x=0, y=0)

# texto que indica que existe valor "!= 0" na memoria
texto_M = Label(frame_tela, text='M', bg=cor3, fg=cor5, font=('Ivy 17 bold'))
texto_M.place(x=0, y=0)
texto_M.place_forget()

# Funcoes

# funcao que monta a expressao
def operacao(botao):
    global expressao
    global recuperacao_memoria
    global tela_resultado
    
    # Substitui (ao inves de concatenar) a expressao pelo numero digitado após recuperar_memoria()
    if recuperacao_memoria:
        expressao = str(botao)
        recuperacao_memoria = False
    else:
        expressao = str(expressao) + str(botao)
        
    tela_resultado.set(expressao)

# funcao que calcula a expressao
def calcular():
    global expressao
    
    try:
        # resolve multiplicacao implicita de parenteses
        nova_expressao = []
        
        for i in range(len(expressao)):
            if expressao[i] == '(' and i > 0:
                if( expressao[i-1].isdigit() or expressao[i-1] == ')' ):
                    nova_expressao.append('*')
            nova_expressao.append(expressao[i])
        
        expressao = ''.join(nova_expressao)
        
        # calcula a expressao ja formatada
        resultado = eval(expressao)
        tela_resultado.set(str(resultado))
        expressao = str(resultado)
    except:
        tela_resultado.set("Erro")
        expressao = ''

# funcao que limpa a expressao  
def limpar():
    global expressao
    expressao = ""
    tela_resultado.set(expressao)

# funcao usada para apagar erros cometidos ao montar a expressao
def deletar():
    global expressao
    expressao = expressao[:-1]
    tela_resultado.set(expressao)

# funcao usada para calcular porcentagem
def porcentagem():
    global expressao
    global tela_resultado
    
    try:
        expressao+='%'
        simbolo = re.search(r'[^.\d]', expressao).group()
        expressao = expressao[:-1]
        
        if(simbolo=='%'):
            expressao = float(expressao) / 100
            tela_resultado.set(str(expressao))
        elif(simbolo=='('):
            parentese = expressao.find('(')
            numero = expressao[parentese+1:]
            expressao = '(' + str(float(numero) / 100)
            tela_resultado.set(expressao)
        else:
            posicao_simbolo = expressao.find(simbolo)
            anterior = expressao[:posicao_simbolo]
            sucessor = expressao[posicao_simbolo+1:]
            
            if(simbolo == '+' or simbolo == '-'):
                expressao = anterior + simbolo + anterior + '*' + sucessor + '/100'
            else:
                expressao = anterior + simbolo + '(' + sucessor + '/100' + ')'
            
            expressao = eval(expressao)
            tela_resultado.set(str(expressao))
            expressao = str(expressao)
    except:
        tela_resultado.set("Erro")
        expressao = ''

# funcao para raizes2

def raiz():
    global expressao
    if expressao:
        valor = float(expressao)
        if valor >= 0:
            res = valor **0.5
            expressao = str(res)
            tela_resultado.set(expressao)
        else:
            tela_resultado.set("Erro")
            expressao = ''
    else:
        tela_resultado.set("0")
        expressao = ''
        
# Sistema de memoria

# funcao que adiciona a memoria
def memoria_ad():
    global expressao
    global memoria
    global tela_resultado
    
    if(expressao == ''):
        expressao+='0'
    
    texto_M.place(x=0,y=0)
    memoria+= float(expressao)
    expressao = ''
    tela_resultado.set(expressao)
    print(memoria)
    
# funcao que subtrai a memoria
def memoria_sub():
    global expressao
    global memoria
    global tela_resultado
    
    if(expressao == ''):
        expressao+='0'
    
    texto_M.place(x=0,y=0)
    memoria-= float(expressao)
    expressao = ''
    tela_resultado.set(expressao)
    print(memoria)

# funcao que recupera a memoria e a exibe na tela
def recuperar_memoria():
    global memoria
    global expressao
    global tela_resultado
    global recuperacao_memoria
    
    expressao = str(memoria)
    tela_resultado.set(expressao)
    recuperacao_memoria = True

# funcao que reseta a memoria para 0
def limpar_memoria():
    global memoria
    global expressao
    global tela_resultado
    
    memoria = 0
    expressao = ''
    tela_resultado.set(expressao)
    texto_M.place_forget()

# Botoes

b1 = Button(frame_bts, text="MC",command= limpar_memoria, width=7, height=2, bg= cor6, fg= cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b1.place(x=0,y=0)

b2 = Button(frame_bts, text="MR", command= recuperar_memoria, width=7, height=2, bg=cor6, fg= cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b2.place(x=80,y=0)

b3 = Button(frame_bts, command= memoria_sub, text="M-", width=7, height=2, bg=cor6, fg= cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b3.place(x=160,y=0)

b4 = Button(frame_bts, command= memoria_ad, text="M+", width=7, height=2, bg=cor6, fg= cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b4.place(x=240,y=0)


b5 = Button(frame_bts, text="C", command=limpar, width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b5.place(x=0,y=52)

b6 = Button(frame_bts, command=lambda: operacao('('), text="(", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b6.place(x=80,y=52)

b7 = Button(frame_bts, command=lambda: operacao(')'), text=")", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b7.place(x=160,y=52)

b8 = Button(frame_bts, text="Del", command= deletar, width=7, height=3, bg=cor5, fg=cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b8.place(x=240,y=52)

b9 = Button(frame_bts, text="%", command= porcentagem, width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b9.place(x=0,y=123)

b10 = Button(frame_bts, command=lambda: operacao('**'), text="^", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b10.place(x=80,y=123)

b11 = Button(frame_bts, command= raiz, text="√", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b11.place(x=160,y=123)

b12 = Button(frame_bts, command=lambda: operacao('/'), text="/", width=7, height=3, bg=cor5, fg=cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b12.place(x=240,y=123)


b13 = Button(frame_bts, command=lambda: operacao('9'), text="9", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b13.place(x=0,y=194)

b14 = Button(frame_bts, command=lambda: operacao('8'), text="8", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b14.place(x=80,y=194)

b15 = Button(frame_bts, command=lambda: operacao('7'), text="7", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b15.place(x=160,y=194)

b16 = Button(frame_bts, command=lambda: operacao('*'), text="x", width=7, height=3, bg=cor5, fg=cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b16.place(x=240,y=194)

b17 = Button(frame_bts, command=lambda: operacao('6'), text="6", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b17.place(x=0,y=265)

b18 = Button(frame_bts, command=lambda: operacao('5'), text="5", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b18.place(x=80,y=265)

b19 = Button(frame_bts, command=lambda: operacao('4'), text="4", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b19.place(x=160,y=265)

b20 = Button(frame_bts, command=lambda: operacao('-'), text="-", width=7, height=3, bg=cor5, fg=cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b20.place(x=240,y=265)

b21 = Button(frame_bts, command=lambda: operacao('3'), text="3", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b21.place(x=0,y=336)

b22 = Button(frame_bts, command=lambda: operacao('2'), text="2", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b22.place(x=80,y=336)

b23 = Button(frame_bts, command=lambda: operacao('1'), text="1", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b23.place(x=160,y=336)

b24 = Button(frame_bts, command=lambda: operacao('+'), text="+", width=7, height=3, bg=cor5, fg=cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b24.place(x=240,y=336)

b25 = Button(frame_bts, command=lambda: operacao('0'), text="0", width=15, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b25.place(x=0,y=407)

b26 = Button(frame_bts, command=lambda: operacao('.'), text=".", width=7, height=3, bg=cor4, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b26.place(x=160,y=407)

b27 = Button(frame_bts, command= calcular, text="=", width=7, height=3, bg=cor5, fg=cor2, font=('Ivy 13 bold'), relief=RAISED, overrelief=RIDGE)
b27.place(x=240,y=407)


janela.mainloop()