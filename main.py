import PySimpleGUI as sg
import matplotlib.pyplot as plt
from Cypher import *
from Analyzer import *


def is_number(n):
    try:
        int(n)
        return True
    except:
        return False


def create_options(_crypto, layout):
    if hasattr(_crypto, 'options'):
        for i, option in enumerate(_crypto.options):
            layout.insert(i + 1, [sg.Text(option[0]),
                                  sg.InputText(key=option[0],
                                               enable_events=True)])


def create_encrypt_decrypt_window(class_name):
    menu_def = [['File', ['Open', 'Save', 'Exit']]]

    # ------ GUI Defintion ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10), key='-INPUT-')],
        [sg.Button('Encrypt'), sg.Button('Decrypt')],
        [sg.Multiline(size=(60, 10), key='-OUTPUT-')]
    ]

    _crypto = class_name()

    create_options(_crypto, layout)

    window = sg.Window(str(class_name), layout,
                       default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       element_justification='c', finalize=True)

    window._crypto = _crypto

    return window


def create_analyzer_window(class_name):
    menu_def = [['File', ['Open', 'Save', 'Exit']]]

    # ------ GUI Defintion ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10), key='-INPUT-')],
        [sg.Button('Analyze')]
    ]

    _crypto = class_name()

    create_options(_crypto, layout)

    window = sg.Window(str(class_name), layout,
                       default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       element_justification='c', finalize=True)

    window._crypto = _crypto

    return window


def main():
    sg.ChangeLookAndFeel('LightGreen')
    # sg.SetOptions(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Exit']],
                ['Encrypt/Decrypt', ['Cesar'], ],
                ['Analysis', ['Frequency']],
                ['Crack', ['Cesar frequency']]]

    # ------ GUI Defintion ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10))]
    ]

    main_window = sg.Window("CryptoTool v0.01", layout,
                            default_element_size=(12, 1), auto_size_text=False,
                            auto_size_buttons=False,
                            default_button_element_size=(12, 1), finalize=True)

    encrypt_decrypt = {'Cesar': CesarCypher}
    analyzers = {'Frequency': FrequencyAnalyzer}

    # ------ Loop & Process button menu choices ------ #

    while True:
        try:
            window, event, values = sg.read_all_windows()
            if window == main_window:
                if event == sg.WIN_CLOSED or event == 'Exit':
                    break
                print('Button = ', event)
                # ------ Process menu choices ------ #
                if event in encrypt_decrypt:
                    create_encrypt_decrypt_window(encrypt_decrypt[event])

                if event in analyzers:
                    create_analyzer_window(analyzers[event])

            else:
                if event == sg.WIN_CLOSED or event == 'Exit':
                    window.close()

                if event == 'Open':
                    path = sg.popup_get_file('Input file', no_window=True)
                    try:
                        with open(path) as file:
                            window['-INPUT-'].update(file.read())
                    except:
                        sg.popup('Invalid file')

                if event == 'Encrypt':
                    window['-OUTPUT-'].update(
                        window._crypto.encrypt(values['-INPUT-']))
                if event == 'Decrypt':
                    window['-INPUT-'].update(
                        window._crypto.decrypt(values['-OUTPUT-']))

                option = list(
                    filter(lambda x: x[0] == event, window._crypto.options))
                if len(option) > 0:
                    option = option[0]
                    if option[1] == 'text' or is_number(values[option[0]]):
                        setattr(window._crypto, option[0],
                                values[option[0]] if option[1] == 'test' else int(
                                    values[option[0]]))

                if event == 'Analyze':
                    x, data = window._crypto.analyze(values['-INPUT-'])
                    plt.bar(x, data)
                    plt.show()
        except Exception as e:
            print('Error:', e)


if __name__ == "__main__":
        main()

