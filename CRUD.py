'''
Dependencias
    pip3 install pynput
'''
import os
import sys
import time
from pynput.keyboard import Listener
from pynput import keyboard
import ctypes
import random

menu = {
    "0":   ["CADASTRO DE CLIENTES ","CADASTRO DE MOTOCICLETAS ","EFETUAR VENDAS ","LISTAGEM DE VENDAS ","CONSULTAR VENDAS "],
    "0.0": ["CADASTRAR CLIENTE ","LISTAR CLIENTES ","EDITAR CLIENTE ", "DELETAR CLIENTE "],
    "0.1": ["CADASTRAR MOTOCICLETA ","LISTAR MOTOCICLETA ","EDITAR MOTOCICLETA ", "DELETAR MOTOCICLETA "]
}

titulo   = ["MENU"]
tecla    = ""
caminho  = [0]
local    = ""
escolha  = 0
vCliente = ""
vMotocicleta = ""

idAutoIncremento = {
    "cliente": 0,
    "moto": 0,
    "venda": 0
}

banco = "banco.txt"
try:
    arquivo = open(banco, "r")
except IOError:
    arquivo = open(banco, 'w+')
    arquivo.write("[BANCO DE DADOS DO PROGRAMA PYMOTOS]\n")
    arquivo.write("[I]|0|0|0\n")
finally:
    linhas = arquivo.readlines() 
    
    for linha in linhas:
        dados = linha.strip().split("|")
        if dados[0] == "[I]":
            idAutoIncremento["cliente"] = int(dados[1])
            idAutoIncremento["moto"]    = int(dados[2])
            idAutoIncremento["venda"]   = int(dados[3])
            break
    arquivo.close()

STD_OUTPUT_HANDLE = -11
stdout_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = ctypes.windll.kernel32.SetConsoleTextAttribute

def cores(color: int) -> None:
    SetConsoleTextAttribute(stdout_handle, color)

def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios    #for linux/unix
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

def on_release(key):
    global tecla
    try:
        tecla = key.char
    except AttributeError:
        tecla = key

def limpar():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def navegar(menu, escolha):
    limpar()
    for s in titulo:
        print(f"{s} >", end=" ")
    print("\n\n") 
    for posicao,item in enumerate(menu):
        tamanho = len(menu[posicao])
        tamanho = max(30,tamanho)       
        if escolha == posicao:
            cores(0xF0)
            print(f"{menu[posicao] : >{tamanho}}")
            print(f" "*tamanho)
            cores(0xF8)
            print(" "+"\u2026"*(tamanho-2)+" ")
        else:
            cores(0x0F)
            print(f"{menu[posicao]: >{tamanho}}")
            cores(0x08)
            print(" "+"\u2026"*(tamanho-2)+" ")
    cores(0x0F)  

def mascaraReal(valor):
    a = '{:,.2f}'.format(float(valor))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')

def AtualizarID(): #[I]|Cliente|Moto|Venda
    global idAutoIncremento
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    contador = 0
    for linha in linhas:
        dados = linha.strip().split("|")
        if dados[0] == "[I]":
            break
        contador += 1
    arquivo = open(banco, "w+")
    linhas[contador] = "[I]|" + "|".join(map(str, idAutoIncremento.values())) + "\n"
    arquivo.writelines(linhas)
    arquivo.close()

#CRUD CLIENTES
def cadastrarCliente(): #[C]|id|nome|numero|cpf
    print(f"\n{titulo[-1]}")
    dicionario = {}
    dicionario["nome"]    = input("  Digite o nome do cliente:")
    dicionario["numero"]  = input("Digite o numero do cliente:")
    dicionario["cpf"]     = input("   Digite o cpf do cliente:")
    print(f"\n\n{dicionario}")
    salvar  = input("Deseja salvar esses dados? S/N: ")
    if (salvar == "s" or salvar == "S"):
        arquivo = open(banco, "a+")
        linha = "\n[C]|{}|".format(idAutoIncremento["cliente"]) + "|".join(map(str, dicionario.values()))
        arquivo.write(linha)
        arquivo.close()
        idAutoIncremento["cliente"] += 1
        AtualizarID()

def listarCliente(): #[C]|id|nome|numero|cpf
    print(f"\n{titulo[-1]}\n")
    print(f"{'ID' : <6}{'NOME' : ^32}{'NUMERO' : ^17}{'CPF' : >16}")
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    for linha in linhas:
        dados = linha.strip().split("|")
        if dados[0] == "[C]" and 5 == len(dados):
            print(f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}")
    arquivo.close()
    input(f"\n{'Tecle [ENTER] para continuar.': >80}")

def editarCliente(id): #[C]|id|nome|numero|cpf
    clientes = []
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    contador = 0
    for numero,linha in enumerate(linhas):
        dados = linha.strip().split("|")
        if dados[0] == "[C]" and 5 == len(dados):
            if id > -1:
                if id == contador:
                    print(dados)
                    temp = input("    Digite o novo nome do cliente:")
                    if temp:
                        dados[2] = temp
                    temp = input("  Digite o novo numero do cliente:")
                    if temp:
                        dados[3] = temp
                    temp = input("     Digite o novo cpf do cliente:")
                    if temp:
                        dados[4] = temp
                    confirmacao = input(f"Confirma a Edição S/N ?: ")
                    if confirmacao == "s" or confirmacao == "S":
                        linhas[numero] = "|".join(dados) + "\n"
                        arquivo = open(banco, "w+")
                        arquivo.writelines(linhas)
                        arquivo.close()
                    else:
                        dados = linha.strip().split("|")                        
                contador += 1
            cliente = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
            clientes.append(cliente)                
    global escolha
    escolha = 0              
    menu["0.0.2"] = clientes
    arquivo.close()

def deletarCliente(id): #[C]|id|nome|numero|cpf
    clientes = []
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    contador = 0
    deletar = -1
    for numero,linha in enumerate(linhas):
        dados = linha.strip().split("|")
        if dados[0] == "[C]" and 5 == len(dados):
            if id > -1:
                if id == contador:
                    confirmacao = input(f"Deseja realmente deletar [{dados[1]}] {dados[2]} S/N ?: ")
                    if confirmacao == "s" or confirmacao == "S":
                        deletar = numero
                    else:
                        cliente = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                        clientes.append(cliente)
                else:
                    cliente = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                    clientes.append(cliente)
                contador += 1
            else:
                cliente = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                clientes.append(cliente)
    global escolha
    escolha = 0              
    menu["0.0.3"] = clientes
    if deletar > -1:
        arquivo = open(banco, "w+")
        del linhas[deletar]
        arquivo.writelines(linhas)
    arquivo.close()

#CRUD MOTOCICLETA
def cadastrarMotocicleta(): #[M]|id|modelo|placa|preço
    print(f"\n{titulo[-1]}")
    dicionario = {}
    dicionario["modelo"]    = input("  Digite o modelo da motocicleta:")
    dicionario["placa"]     = input("   Digite a placa da motocicleta:")
    dicionario["preco"]     = input("   Digite o preço da motocicleta:")
    print(f"\n\n{dicionario}")
    salvar  = input("Deseja salvar esses dados? S/N: ")
    if (salvar == "s" or salvar == "S"):
        arquivo = open(banco, "a+")
        linha = "\n[M]|{}|".format(idAutoIncremento["moto"]) + "|".join(map(str, dicionario.values()))
        arquivo.write(linha)
        arquivo.close()
        idAutoIncremento["moto"] += 1
        AtualizarID()

def listarMotocicleta(): #[M]|id|modelo|placa|preço
    print(f"\n{titulo[-1]}\n")
    print(f"{'ID' : <6}{'MODELO' : ^32}{'PLACA' : ^17}{'PREÇO' : >16}")
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    for linha in linhas:
        dados = linha.strip().split("|")
        if dados[0] == "[M]" and 5 == len(dados):
            print(f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{'R$ '+dados[4]: >16}")
    arquivo.close()
    input(f"\n{'Tecle [ENTER] para continuar.': >80}")

def editarMotocicleta(id): #[M]|id|modelo|placa|preço
    motocicletas = []
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    contador = 0
    for numero,linha in enumerate(linhas):
        dados = linha.strip().split("|")
        if dados[0] == "[M]" and 5 == len(dados):
            if id > -1:
                if id == contador:
                    print(dados)
                    temp = input("    Digite o novo modelo da motocicleta:")
                    if temp:
                        dados[2] = temp
                    temp = input("  Digite a nova placa da motocicleta:")
                    if temp:
                        dados[3] = temp
                    temp = input("     Digite o novo preço da motocicleta:")
                    if temp:
                        dados[4] = temp
                    confirmacao = input(f"Confirma a Edição S/N ?: ")
                    if confirmacao == "s" or confirmacao == "S":
                        linhas[numero] = "|".join(dados) + "\n"
                        arquivo = open(banco, "w+")
                        arquivo.writelines(linhas)
                        arquivo.close()
                    else:
                        dados = linha.strip().split("|")                        
                contador += 1
            motocicleta = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
            motocicletas.append(motocicleta)                
    global escolha
    escolha = 0              
    menu["0.1.2"] = motocicletas
    arquivo.close()

def deletarMotocicleta(id): #[M]|id|modelo|placa|preço
    motocicletas = []
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    contador = 0
    deletar = -1
    for numero,linha in enumerate(linhas):
        dados = linha.strip().split("|")
        if dados[0] == "[M]" and 5 == len(dados):
            if id > -1:
                if id == contador:
                    confirmacao = input(f"Deseja realmente deletar [{dados[1]}] {dados[2]} S/N ?: ")
                    if confirmacao == "s" or confirmacao == "S":
                        deletar = numero
                    else:
                        motocicleta = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                        motocicletas.append(motocicleta)
                else:
                    motocicleta = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                    motocicletas.append(motocicleta)
                contador += 1
            else:
                motocicleta = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                motocicletas.append(motocicleta)
    global escolha
    escolha = 0              
    menu["0.1.3"] = motocicletas
    if deletar > -1:
        arquivo = open(banco, "w+")
        del linhas[deletar]
        arquivo.writelines(linhas)
    arquivo.close()

#VENDAS
def efetuarVenda(id): #[V]|id|modelo|placa|preço|nome|numero|cpf|datahora
    motocicletas = []
    clientes     = []
    contador = 0
    global vMotocicleta
    global vCliente
    global escolha

    arquivo = open(banco, "r")
    linhas = arquivo.readlines()

    if not vMotocicleta:
        for numero,linha in enumerate(linhas):
            dados = linha.strip().split("|")    
            if dados[0] == "[M]" and 5 == len(dados):
                if id > -1:
                    if id == contador:
                        vMotocicleta = f"{dados[2]}|{dados[3]}|{dados[4]}"
                contador += 1        
                motocicleta = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                motocicletas.append(motocicleta)
        escolha = 0              
        menu["0.2"] = motocicletas
        arquivo.close()

    if vMotocicleta and not vCliente:
        for numero,linha in enumerate(linhas):
            dados = linha.strip().split("|")
            if dados[0] == "[C]" and 5 == len(dados):
                if id > -1:
                    if id == contador:
                        vCliente = f"{dados[2]}|{dados[3]}|{dados[4]}"
                contador += 1        
                cliente = f"{dados[1]: <6}{dados[2]: ^32}{dados[3]: ^17}{dados[4]: >16}"
                clientes.append(cliente)
        escolha = 0    
        menu["0.2"] = clientes
        arquivo.close()

    if vMotocicleta and vCliente: #[V]|id|modelo|placa|preço|nome|numero|cpf|datahora
        nomeCliente = vCliente.strip().split("|")
        nomeCliente = nomeCliente[0]
        placaMoto = vMotocicleta.strip().split("|")
        placaMoto = placaMoto[1]
        deletarMoto = -1
        confirmacao = input(f"Corfirma a venda da motocicleta\n\t {vMotocicleta}\n\t para {nomeCliente}    ? S/N:")
        if confirmacao == "s" or confirmacao == "S":
            arquivo = open(banco, "a+")
            linha = "\n[V]|{}|{}|{}".format(idAutoIncremento["venda"],vMotocicleta,vCliente) 
            arquivo.write(linha)
            arquivo.close()
            idAutoIncremento["venda"] += 1
            AtualizarID()
            arquivo = open(banco, "r")
            linhas = arquivo.readlines()
            for numero,linha in enumerate(linhas):
                dados = linha.strip().split("|")
                if dados[0] == "[M]" and dados[3] == placaMoto and 5 == len(dados):
                    deletarMoto = numero
            if deletarMoto > -1:
                arquivo = open(banco, "w+")
                del linhas[deletarMoto]
                arquivo.writelines(linhas)
            arquivo.close()
        #reset
        global caminho
        global local
        global titulo
        caminho  = [0]
        escolha = 0
        local = "0"
        titulo   = ["MENU"]
        print("**** Venda Concluida. ****")
        vMotocicleta = ""
        vCliente = ""
        flush_input()
        time.sleep(1)
                    
def listarVendas(): #[V]|id|modelo|placa|preço|nome|numero|cpf
    total = 0
    print(f"\n{titulo[-1]}\n")
    print(f"{'ID' : <6}{'MODELO' : ^17}{'PLACA' : ^9}{'NOME' : ^20}{'PREÇO' : >16}")
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    for linha in linhas:
        dados = linha.strip().split("|")
        if dados[0] == "[V]" and 8 == len(dados):
            print(f"{dados[1]: <6}{dados[2]: ^17}{dados[3]: ^9}{dados[5]: ^20}{'R$ '+dados[4]: >16}")
            dados[4] = dados[4].replace(".","")
            dados[4] = dados[4].replace(",",".")
            total += float(dados[4])
    arquivo.close()
    total = mascaraReal(total)
    print(f"\nTotal de vendas: R$ {total}")
    input(f"\n{'Tecle [ENTER] para continuar.': >80}")

def ConsultarVendas(): #[V]|id|modelo|placa|preço|nome|numero|cpf
    total = 0
    encontrados = 0
    print(f"\n{titulo[-1]}\n")
    buscar = input("Digite uma palavra até mesmo parcial para a consulta:")
    print(f"{'ID' : <6}{'MODELO' : ^17}{'PLACA' : ^9}{'NOME' : ^20}{'PREÇO' : >16}")
    arquivo = open(banco, "r")
    linhas = arquivo.readlines()
    for linha in linhas:
        dados = linha.strip().split("|")
        if dados[0] == "[V]" and 8 == len(dados):
            for dado in dados:
                if buscar in dado:
                    print(f"{dados[1]: <6}{dados[2]: ^17}{dados[3]: ^9}{dados[5]: ^20}{'R$ '+dados[4]: >16}")
                    dados[4] = dados[4].replace(".","")
                    dados[4] = dados[4].replace(",",".")
                    total += float(dados[4])
    arquivo.close()
    total = mascaraReal(total)
    print(f"\nTotal de vendas (nesta consulta): R$ {total}")
    input(f"\n{'Tecle [ENTER] para continuar.': >80}")
#INICIO    

local = ".".join(map(str, caminho))
navegar(menu[local], escolha)

threadTeclado = Listener(on_release=on_release)
threadTeclado.start()

while True:
    while tecla == "":
        time.sleep(0.1)
    if tecla == "q" or tecla == "esc" or tecla == keyboard.Key.esc:
        if (len(caminho) == 1):
          break
        escolha = caminho[-1]
        del caminho[-1]
        del titulo[-1]
        local = ".".join(map(str, caminho))
    if tecla == keyboard.Key.up:
        escolha -= 1
    elif tecla == keyboard.Key.down:
        escolha += 1
    if escolha < 0:
        escolha = len(menu[local])-1
    elif escolha == len(menu[local]):
        escolha = 0
    
    if tecla == keyboard.Key.enter:
        flush_input()
        titulo.append(menu[local][escolha])
        caminho.append(escolha)
        local = ".".join(map(str, caminho))
        escolha = 0

        #CRUD clientes
        if local == "0.0.0":
            cadastrarCliente()
        if local == "0.0.1":
            listarCliente()
        if local == "0.0.2":
            editarCliente(-1)
        if local[:-1] == "0.0.2.":
            editarCliente(int(local[-1]))            
        if local == "0.0.3":
            deletarCliente(-1)
        if local[:-1] == "0.0.3.":
            deletarCliente(int(local[-1]))

        #CRUD motocicletas
        if local == "0.1.0":
            cadastrarMotocicleta()
        if local == "0.1.1":
            listarMotocicleta()
        if local == "0.1.2":
            editarMotocicleta(-1)
        if local[:-1] == "0.1.2.":
            editarMotocicleta(int(local[-1]))            
        if local == "0.1.3":
            deletarMotocicleta(-1)
        if local[:-1] == "0.1.3.":
            deletarMotocicleta(int(local[-1]))

        #Vendas
        if local == "0.2":
            efetuarVenda(-1)
        if local[:-1] == "0.2.":
            efetuarVenda(int(local[-1]))
        if local == "0.3":
            listarVendas()
        if local == "0.4":
            ConsultarVendas()

        if local not in menu:
            #print(f"menu escolhido {local}")
            del caminho[-1]
            del titulo[-1]
            local = ".".join(map(str, caminho))
            time.sleep(1)
       
    
    navegar(menu[local], escolha)
    tecla = ""
    time.sleep(0.1)

threadTeclado.stop()
flush_input()