from tkinter import * 
from tkinter import Tk, ttk

#importando pillow
from PIL import Image, ImageTk

#importanto barra de progresso do tkinter
from tkinter.ttk import Progressbar


#importanto matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#importando calendario
from tkcalendar import Calendar, DateEntry
from datetime import date
import datetime
#import mensage box
from tkinter import messagebox

#importando funcoes da view
from view import bar_valores, pie_valores, inserir_categoria,porcentagem_valor, ver_categoria, inserir_receita, inserir_gastos, tabela, deletar_gastos, deletar_receitas

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
# cores 
co0 = "#2e2d2b" # preta
co1 = "#feffff" # branca
co2 = "#4fa882" # verde
co3 = "#38576b" #valor
co4 = "#403d3d" #letra
co5 = "#e06636"
co6 = "#038cfc"
co7 = "#3fbfb9"
co8 = "#263238"
co9 = "#e9edf5"

colors = ['#5588bb', '#66bbbb', '#99bb55','#ee9944','#bb5555']

# criando janela 
janela = Tk()
janela.title('Controle Financeiro')
janela.geometry('900x650')
janela.configure(background=co0)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use("clam")

janela.wm_iconbitmap('Imagens/crescimento.ico')
# Configurando a localização para português do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
#criando frames para divisão da tela
frameCima= Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0,column=0)

frameMeio= Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1,column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo= Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2,column=0, pady=0, padx=10, sticky=NSEW)

# Trabalhando no frame cima  

#  Acessando a imagem*
app_img = Image.open('Imagens/log.png')
app_img = app_img.resize((45,45))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text= "Controle Financeiro", width=900, compound=LEFT,padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg= co1, fg= co4,)
app_logo.place(x=0,y=0)

#defindo tree como global 
global tree 
 
#função inserir categoria
def inserir_categoria_b():
    nome = e_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro','Preencha todos os campos')
            return
        
    #passando para a funcao inserir_gasto presente na view
    inserir_categoria(lista_inserir)

    # messagebox.showinfo('Sucesso','Os dados foram inserirdos com sucesso')

    e_categoria.delete(0,'end')

    #pegando os valores de categoria
    categorias_funcao = ver_categoria()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])
    
    #atualizando a lista de categorias
    combo_categoria_despesa['values'] = (categoria)

# função limpar valor para formatar
def limpar_valor(valor_str):
    # Remove espaços em branco extras
    valor_str = valor_str.strip()

    # Remove pontos de milhar (caso haja) para facilitar a conversão
    valor_str = valor_str.replace('.', '')

    # Substitui vírgulas por pontos para garantir um formato de número válido
    valor_str = valor_str.replace(',', '.')

    return valor_str
# função inserir receitas
def inserir_receitas_b():
    nome = 'Receita'
    data = e_cal_receitas.get()
    quantia_str = e_valor_receitas.get()

    # Limpar o valor para remover caracteres indesejados e formatar corretamente
    quantia_limpa = limpar_valor(quantia_str)

    # Verificar se o valor pode ser convertido para float
    try:
        quantia = float(quantia_limpa)
    except ValueError:
        messagebox.showerror('Erro', 'Valor da quantia não é válido')
        return

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if not i:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Chamando a função inserir Receitas presente na view
    inserir_receita(lista_inserir)

    # messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    e_cal_receitas.delete(0, 'end')
    e_valor_receitas.delete(0, 'end')

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()

#função inserir despesas

def inserir_despesas_b():
    nome = combo_categoria_despesa.get()
    data = e_cal_despesas.get()
    quantia_str = e_valor_despesas.get()

    # Limpar o valor para remover caracteres indesejados e formatar corretamente
    quantia_limpa = limpar_valor(quantia_str)

    # Verificar se o valor pode ser convertido para float
    try:
        quantia = float(quantia_limpa)
    except ValueError:
        messagebox.showerror('Erro', 'Valor da quantia não é válido')
        return

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if not i:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Chamando a função inserir_gastos presente na view
    inserir_gastos(lista_inserir)

    # messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

    combo_categoria_despesa.set('')  # Limpar seleção da categoria
    e_cal_despesas.delete(0, 'end')
    e_valor_despesas.delete(0, 'end')

    # Atualizando dados
    mostrar_renda()
    porcentagem()
    grafico_bar()
    resumo()
    grafico_pie()


#função deletar
def deletar_dados():
    try:
        treev_dados= tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor= treev_lista[0]
        nome= treev_lista[1]

        if nome =='Receita':
            deletar_receitas([valor])
            # messagebox.showinfo('Sucesso','Os dados foram deletados com sucesso')

            # atualizando dados 
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            # messagebox.showinfo('Sucesso','Os dados foram deletados com sucesso')

            # atualizando dados 
            mostrar_renda()
            porcentagem()
            grafico_bar()
            resumo()
            grafico_pie()
        
    except IndexError:
        messagebox.showerror('Erro','Seleciona um dos dados da tabela')
        


#porcentagem ----------------------------------------------
def porcentagem():
    # Calcula a porcentagem de despesas em relação à receita total
    valor = porcentagem_valor()
    
    l_nome = Label(frameMeio, text="Porcentagem Da Receita Gasta", height=1, anchor=NW, font=('Verdana 12'),bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure("black.Horizontal.TProgressbar", background='#daed6b')
    style.configure("TProgressbar", thickness=25)

    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = valor  # Atualiza o valor da barra de progresso

    l_porcentagem = Label(frameMeio, text="{:,.2f}%".format(valor), anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_porcentagem.place(x=200, y=35)

# funcao para grafico bars ---------------------------------------------

def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    #faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)
    #ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(lista_categorias, lista_valores,  color=colors, width=0.9)
    #create a list to collect the plt.patches data

    c = 0
    #set individual bar lables using above list
    for i in ax.patches:
        #get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias,fontsize=16)

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

#funcao de resumo total 
def resumo ():
    valor = bar_valores()

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMeio, text="Total Renda Mensal      ".upper(),anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMeio, text="R$ {:,.2F}".format(valor[0]),anchor=NW, font=('arial 17'), bg=co1, fg=co2)
    l_sumario.place(x=309, y=75)
          
    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=132)
    l_sumario = Label(frameMeio, text="Total Despesas Mensais   ".upper(),anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=115)
    l_sumario = Label(frameMeio, text="R$ {:,.2F}".format(valor[1]),anchor=NW, font=('arial 17'), bg=co1, fg=co5)
    l_sumario.place(x=309, y=150)

    l_linha = Label(frameMeio, text="", width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=207)
    l_sumario = Label(frameMeio, text="Total Saldo Do Caixa      ".upper(),anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=190)
    l_sumario = Label(frameMeio, text="R$ {:,.2F}".format(valor[2]),anchor=NW, font=('arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=220)
    
#frame do grafico da função python 
frame_gra_pie = Frame(frameMeio, width=580, height=250, bg=co0)
frame_gra_pie.place(x=415, y=5)

#função grafico python
def grafico_pie():
    #faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    #only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)

    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)

porcentagem()
grafico_bar()
resumo()
grafico_pie()


# Criando frames dentro do frame baixo
frame_renda= Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0,column=0)

frame_operacoes= Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0,column=1, padx=5)

frame_configuracao= Frame(frameBaixo, width=220, height=250, bg=co1)
frame_configuracao.grid(row=0,column=2, padx=5)


#tabela renda mensal --------------------------------
app_tabela = Label(frameMeio,text= "Tabela Receitas e Despesas",anchor=NW, font=('Verdana 12'), bg= co1, fg= co4,)
app_tabela.place(x=5,y=309)

#função para mostrar tabela

def mostrar_renda():
    #creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Quantia']

    lista_itens = tabela()
    
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    #vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    #horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        #adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)


#configurações despesas------------------------------------
l_info= Label(frame_operacoes, text= 'Insira novas despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=10)

#categoria-----------------------------
l_categoria= Label(frame_operacoes, text= 'Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10,y=40)

#pegando categorias
categoria_funcao= ver_categoria()
categoria= []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesa= ttk.Combobox(frame_operacoes, width=10, font=('Ivy 10'))
combo_categoria_despesa['values']=(categoria)
combo_categoria_despesa.place(x=110,y=41)

#despesas-----------------------------
l_cal_despesas= Label(frame_operacoes, text= 'Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10,y=70)
e_cal_despesas = DateEntry(frame_operacoes, width=12,locale='pt_BR', background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_despesas.place(x=110,y=71)

#VALOR-----------------------------
l_valor_despesas= Label(frame_operacoes, text= 'Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10,y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110,y=101)


# Botão inserir
img_add_despesas = Image.open('Imagens/adicionar.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes,command=inserir_despesas_b, image= img_add_despesas, text= "Adicionar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7'), bg= co1, fg= co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110,y=131)


# Botão excluir
l_excluir= Label(frame_operacoes, text= 'Excluir ação', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_excluir.place(x=10,y=190)

img_deletar = Image.open('Imagens/excluir_red.png')
img_deletar = img_deletar.resize((17,17))
img_deletar = ImageTk.PhotoImage(img_deletar)
botao_deletar = Button(frame_operacoes,command=deletar_dados ,image= img_deletar, text= "Deletar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7 bold'), bg= co1, fg= co0, overrelief=RIDGE)
botao_deletar.place(x=110,y=190)

#configurações de receitas--------------
l_info= Label(frame_configuracao, text= 'Insira novas receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=10)

#Receitas / calendario -----------------------------
l_cal_receitas= Label(frame_configuracao, text= 'Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=10,y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12,locale='pt_BR', background='darkblue', foreground='white', borderwidth=2, year=2024)
e_cal_receitas.place(x=110,y=41)


#VALOR-----------------------------
l_valor_receitas= Label(frame_configuracao, text= 'Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=10,y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=110,y=71)

# Botão inserir------- valor
img_add_receitas = Image.open('Imagens/adicionar.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_despesas = Button(frame_configuracao,command=inserir_receitas_b ,image= img_add_receitas, text= "Adicionar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7'), bg= co1, fg= co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110,y=111)


#operação nova categoria ---------------------------------------

l_info= Label(frame_configuracao, text= 'Categoria', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_info.place(x=10,y=160)
e_categoria = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_categoria.place(x=110,y=160)

# Botão inserir ---------categoria
img_add_categoria = Image.open('Imagens/adicionar.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_despesas = Button(frame_configuracao,command=inserir_categoria_b, image= img_add_categoria, text= "Adicionar".upper(), width=80, compound=LEFT,anchor=NW, font=('Ivy 7'), bg= co1, fg= co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110,y=190)

#Função para alterar a aparência tentar corrigir/ sugestão Tiago
# Função para mudar o tema

# def change_apm(choice):
#     global co1, co2, co4, co5, co9
    
#     if choice == "Light":
#         co1 = "#ffffff"
#         co2 = "#545454"
#         co4 = "#000000"
#         frameCima.config(bg=co2)
#         frameMeio.config(bg=co2)
#         frameBaixo.config(bg=co2)
#         janela.config(bg=co2)  # Alterar a cor de fundo da janela principal
#             # Atualizar as labels com as novas cores
#         grafico_pie()
#         grafico_pie()
#         tabela()
#         resumo()
#         porcentagem()
#         mostrar_renda()
        
#     else:
#         co1 = "#333333"
#         co2 = "#ffffff"
#         co4 = "#ffffff"
#         frameCima.config(bg=co0)
#         frameMeio.config(bg=co0)
#         frameBaixo.config(bg=co0)
#         janela.config(bg=co0)  # Alterar a cor de fundo da janela principal
    
#         # Atualizar as labels com as novas cores
#         grafico_pie()
#         grafico_pie()
#         tabela()
#         resumo()
#         grafico_bar()
#         porcentagem()
#         mostrar_renda()
#         l_cal_despesas
# # Função de aparência
# def appearance():
#     lb_apm = Label(frameCima, text="Tema", bg=co1, fg=co4)
#     lb_apm.place(x=800, y=10)
#     opt_apm = ttk.Combobox(frameCima, values=["Light", "System"], state="readonly")
#     opt_apm.place(x=850, y=10)
#     opt_apm.bind("<<ComboboxSelected>>", lambda event: change_apm(opt_apm.get()))

# appearance()
mostrar_renda()
janela.mainloop()