import PySimpleGUIWeb as sg

layout = [[sg.Text("Hello World")]]
window = sg.window("try", layout)

while True:
    event, values = window.read()
if event == "EXIT" or event == sg.WIN_CLOSED::
	break

window.close()
