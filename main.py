import PySimpleGUI as sg
import matplotlib.pyplot as plt
from Cypher import CesarCypher, VigenereCypher
from Analyzer import FrequencyAnalyzer
from Cracker import CesarCracker, VigenereCracker


def is_number(n):
    try:
        int(n)
        return True
    except:
        return False


def create_options(options, layout, index=1):
    types = {
        'number': sg.InputText,
        'text': sg.InputText,
        'multiline': sg.Multiline,
        'combobox': sg.InputCombo
    }

    for i, option in enumerate(options):

        args = []
        if option[1] == 'combobox':
            args = [option[2]]

        layout.insert(i + index, [sg.Text(option[0]),
                                  types[option[1]](*args, key=option[0],
                                                   enable_events=True)])


def create_encrypt_decrypt_window(class_name):
    menu_def = [['File', ['Open', 'Save', 'Exit']]]

    # ------ GUI Definition ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10), key='-INPUT-')],
        [sg.Button('Encrypt'), sg.Button('Decrypt')],
        [sg.Multiline(size=(60, 10), key='-OUTPUT-')]
    ]

    _crypto = class_name()

    create_options(_crypto.options, layout)

    window = sg.Window(str(class_name), layout,
                       default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       element_justification='c', finalize=True)

    window._crypto = _crypto

    return window


def create_analyzer_window(class_name):
    menu_def = [['File', ['Open', 'Exit']]]

    # ------ GUI Definition ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10), key='-INPUT-')],
        [sg.Button('Analyze')]
    ]

    _crypto = class_name()

    create_options(_crypto.options, layout)

    window = sg.Window(str(class_name), layout,
                       default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(12, 1),
                       element_justification='c', finalize=True)

    window._crypto = _crypto

    return window


def create_cracker_window(class_name):
    menu_def = [['File', ['Open', 'Exit']]]

    # ------ GUI Definition ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10), key='-INPUT-')],
        [sg.Button('Crack')]
    ]

    _crypto = class_name()

    create_options(_crypto.options, layout)
    create_options(_crypto.output_options, layout, len(layout))

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

    encrypt_decrypt = {'Cesar': CesarCypher,
                       'Vigenere': VigenereCypher}
    analyzers = {'Frequency': FrequencyAnalyzer}
    crackers = {'Cesar frequency': CesarCracker,
                'Vigenere (coincidence index)': VigenereCracker}

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Exit']],
                ['Encrypt/Decrypt', list(encrypt_decrypt.keys())],
                ['Analysis', list(analyzers.keys())],
                ['Crack', list(crackers.keys())]]

    # ------ GUI Definition ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Multiline(size=(60, 10))]
    ]

    main_window = sg.Window("CryptoTool v0.01", layout,
                            default_element_size=(12, 1), auto_size_text=False,
                            auto_size_buttons=False,
                            default_button_element_size=(12, 1), finalize=True)

    # ------ Loop & Process button menu choices ------ #

    while True:
        try:
            window, event, values = sg.read_all_windows()
            if window == main_window:
                if event == sg.WIN_CLOSED or event == 'Exit':
                    break

                # ------ Process menu choices ------ #
                if event in encrypt_decrypt:
                    create_encrypt_decrypt_window(encrypt_decrypt[event])

                if event in analyzers:
                    create_analyzer_window(analyzers[event])

                if event in crackers:
                    create_cracker_window(crackers[event])

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

                if event == 'Save':
                    path = sg.popup_get_file('Input file',
                                             save_as=True,
                                             no_window=True)
                    if path:
                        try:
                            with open(path, 'w') as file:
                                file.write(values['-OUTPUT-'])
                        except:
                            sg.popup('Invalid path')

                if event == 'Encrypt':
                    window['-OUTPUT-'].update(
                        window._crypto.encrypt(values['-INPUT-'].strip()))
                if event == 'Decrypt':
                    window['-INPUT-'].update(
                        window._crypto.decrypt(values['-OUTPUT-'].strip()))

                if event == 'Analyze':
                    x, data = window._crypto.analyze(values['-INPUT-'])
                    plt.bar(x, data)
                    plt.show()

                if event == 'Crack':
                    output = window._crypto.crack(values['-INPUT-'])
                    for i, option in enumerate(window._crypto.output_options):
                        window[option[0]].update(output[i])

                option = list(filter(lambda x: x[0] == event,
                                     window._crypto.options))

                if len(option) > 0:
                    option = option[0]
                    if option[1] != 'number' or is_number(values[option[0]]):
                        setattr(window._crypto, option[0],
                                values[option[0]] if option[1] != 'number' else
                                int(values[option[0]]))

        except Exception as e:
            print('Error:', e)


if __name__ == "__main__":
    main()
