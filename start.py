
import io
import os
import PySimpleGUI as sg


def main():
    layout = [
        [sg.Text("Launcher BombCrypto")],
        [sg.Text("vBeta.001")],
        [sg.Button('Iniciar', size= (20,2))],
        [sg.Output(size=(80, 10))]
    ]
    return sg.Window("Lancher vBeta",layout=layout,finalize=True)
    

window = main()

while True:
    #Extrair os dados da tela
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Iniciar':
        print("apertei")
        window.close()

    #     # python index.py
        