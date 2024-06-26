import sys
sys.path.append("src")
import psycopg2


from encriptation_algorithm import encriptation_algorithm
from encriptation_algorithm.encriptation_algorithm import EncriptationEngine
from encriptation_algorithm.encriptation_algorithm import EmptyMessageError
from encriptation_algorithm.encriptation_algorithm import InvalidPublicKey
from encriptation_algorithm.encriptation_algorithm import EmptyPublicKey
from encriptation_algorithm.encriptation_algorithm import NonPrimeNumber
from encriptation_algorithm.encriptation_algorithm import EmptyInputValuesError

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import NumericProperty

class MainScreen(Screen):
    '''
    Class builds and manages the main screen of the application.

    Clase construye y gestiona la pantalla principal de la aplicación.
    '''

    def __init__(self,encriptation_engine, **kwargs):

        '''
        This method creates the mainscreen layout and adds the widgets to the layout.

        Este método crea el layout de la pantalla principal y agrega los widgets al layout.
        '''

        super(MainScreen, self).__init__(**kwargs)
        self.encriptation_engine = encriptation_engine

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.layout = GridLayout(cols=1, padding=20, spacing=20)
        
        # Agregar texto de lo que hace la interfaz directamente en el layout principal
        self.layout.add_widget(Label(text="Bienvenido al motor de encriptación", font_size=50))
        self.layout.add_widget(Label(text="¿Qué desea hacer hoy?", font_size=35))

        # Botones para cambiar de pantalla y manejar la lógica de la aplicación
        self.layout.add_widget(Button(text="Encriptar un mensaje", font_size=50, on_press=self.switch_to_encryption))
        self.layout.add_widget(Button(text='Ver mensajes guardados', font_size=50, on_press=self.switch_to_saved_messages))
        self.layout.add_widget(Button(text="Desencriptar un mensaje", font_size=50, on_press=self.switch_to_decryption))
        self.layout.add_widget(Button(text="Cambiar contraseña", font_size=50, on_press = self.switch_to_change_passcode))
        self.layout.add_widget(Button(text="Cerrar sesión", font_size=50, on_press=self.log_out))
        self.add_widget(self.layout)

    def switch_to_saved_messages(self, instance):
        '''
        This method switches the screen to the saved messages screen.

        Este método cambia la pantalla actual a la pantalla de mensajes guardados.
        '''
        
        app.screen_manager.current = 'saved_messages'

    def switch_to_encryption(self, instance):
        '''
        This method switches the screen to the previous encryption screen.

        Este método cambia la pantalla actual a la pantalla previa de encriptación.
        '''
        app.screen_manager.current = 'pre_encryption'

    def switch_to_decryption(self, instance):
        '''
        This method switches the screen to the decryption screen.

        Este método cambia la pantalla actual a la pantalla de desencriptación.
        '''
        app.screen_manager.current = 'decryption'

    def switch_to_change_passcode(self, instance):
        '''
        This method changes the screen to the change passcode screen.

        Este método cambia la pantalla a la pantalla de cambio de contraseña.
        '''
        app.screen_manager.current = 'change_passcode'
        
    def log_out(self, instance):
        '''
        This method closes the application.

        Este método cierra la aplicación.
        '''

        app.screen_manager.current = 'welcome'


class ChangePasscodeScreen(Screen):

    '''
    Class builds and manages the change passcode screen of the application.

    Esta clase construye y gestiona la pantalla de cambio de contraseña de la aplicación.
        
    '''

    def __init__(self,encriptation_engine : EncriptationEngine, **kwargs):
        super(ChangePasscodeScreen, self).__init__(**kwargs)

        self.encriptation_engine = encriptation_engine
        
        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1, padding=20, spacing=20)

        #Texto principal de la pantalla
        self.main_layout.add_widget(Label(text="Cambiar contraseña", font_size=40))

        #Label para ingresar el nombre de usuario con su respectivo textinput
        self.main_layout.add_widget(Label(text="Ingrese su antigua contraseña", font_size=20))
        self.old_passcode = TextInput(font_size=16, height=300, hint_text='Ingrese su antigua contraseña', password=True)
        self.main_layout.add_widget(self.old_passcode)

        #Label para ingresar la contraseña con su respectivo textinput
        self.main_layout.add_widget(Label(text="Ingrese la nueva contraseña", font_size=20))

        self.new_passcode = TextInput(font_size=16, height=300, hint_text='Ingrese la nueva contraseña', password=True)
        self.main_layout.add_widget(self.new_passcode)

        self.confirm_new_passcode = TextInput(font_size=16, height=300, hint_text='Confirme la contraseña nueva', password=True)
        self.main_layout.add_widget(self.confirm_new_passcode)

        self.show_password_button = Button(text="Mostrar contraseña",font_size=20, on_press=self.show_password)
        self.main_layout.add_widget(self.show_password_button)

        # Grid layout que contiene los 3 botones para volver, registrarse y limpiar los inputs
        self.buttons_layout  = BoxLayout( spacing = 20)

        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.switch_to_main)

        self.change_passcode_button = Button(text="Cambiar contraseña", font_size=20)
        self.change_passcode_button.bind(on_press=self.change_passcode)


        self.clear_inputs_button = Button(text="Limpiar", font_size=20, size_hint=(None, None), size=(100, 50))
        self.clear_inputs_button.bind(on_press=self.clear_text_inputs)

        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.change_passcode_button)
        self.buttons_layout.add_widget(self.clear_inputs_button)

        self.main_layout.add_widget(self.buttons_layout)

        #Se agrega el layout principal al Screen de registro
        self.add_widget(self.main_layout)

    def clear_text_inputs(self, instance):
        '''
        This method clears the text inputs of the screen.

        Este método limpia los text inputs de la pantalla.
        '''
        self.old_passcode.text = ""
        self.new_passcode.text = ""
        self.confirm_new_passcode.text = ""

    def show_password(self, instance):
        '''
        This method shows the password of the user.

        Este método muestra la contraseña del usuario.
        '''
        if self.old_passcode.password == True:
            self.old_passcode.password = False
            self.new_passcode.password = False
            self.confirm_new_passcode.password = False
        else:
            self.old_passcode.password = True
            self.new_passcode.password = True
            self.confirm_new_passcode.password = True

    def switch_to_main(self, instance):
        '''
        This method changes the current screen to the main screen.

        Este método cambia la pantalla actual a la pantalla principal.
        '''
        app.screen_manager.current = 'main'

    def change_passcode(self, instance):
        
        '''
        This method changes the passcode of the user.

        Este método cambia el passcode del usuario.
        '''
        try:
            old_passcode = self.old_passcode.text
            new_passcode = self.new_passcode.text
            confirm_new_passcode = self.confirm_new_passcode.text
            
            if new_passcode != confirm_new_passcode:
                raise ValueError('Las contraseñas no coinciden. Intente ingresando los valores nuevamente')
            
            change_passcode_status = self.encriptation_engine.change_user_passcode(old_passcode,new_passcode)
            if change_passcode_status:
                self.show_popup_succesful_passcode_changed()
                self.clear_text_inputs(None)
        except ValueError as error:
            self.show_popup_passcode_errors(error)
        except Exception as error:
            print(error)
            self.show_popup_passcode_errors(error)

    def show_popup_passcode_errors(error, instance):
        '''
        This method shows a popup with the error message.

        Este método muestra un popup con el mensaje de error.
        '''
        contenido = GridLayout(cols=1)
        error_label = Label(text=str(error))  
        contenido.add_widget(error_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        error_popup = Popup(title='Error', content=contenido)
        boton_cerrar.bind(on_press=error_popup.dismiss)
        error_popup.open()
    
    def show_popup_succesful_passcode_changed(self):
        '''
        This method shows a popup with the success message.

        Este método muestra un popup con el mensaje de éxito.
        '''
        contenido = GridLayout(cols=1)
        success_label = Label(text='Contraseña cambiada exitosamente')
        contenido.add_widget(success_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        success_popup = Popup(title='Contraseña cambiada', content=contenido)
        boton_cerrar.bind(on_press=success_popup.dismiss)
        success_popup.open()
class SavedMessagesScreen(Screen):

    '''
    Shows the saved messages of the user.

    Muestra los mensajes guardados del usuario.
    '''

    def __init__(self,encriptation_engine : EncriptationEngine, **kwargs):
        super(SavedMessagesScreen, self).__init__(**kwargs)

        self.encriptation_engine = encriptation_engine

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1,padding=5)
        self.table_layout_titles = GridLayout(size_hint_y=None,height=30,cols=3)
        self.table_layout_titles.add_widget(Label(text="Llave secreta", font_size=20))
        self.table_layout_titles.add_widget(Label(text="Mensaje encriptado", font_size=20))
        self.table_layout_titles.add_widget(Label(text="Mensaje original", font_size=20))
        
        self.main_layout.add_widget(self.table_layout_titles)



        #Se agrega el layout principal a la pantalla
        self.add_widget(self.main_layout)

    def on_pre_enter(self, *args):
        '''
        This method shows the saved messages of the user.

        Este método muestra los mensajes guardados del usuario.
        '''
        self.show_saved_messages()

    def switch_to_main(self, instance):
        '''
        This method changes the current screen to the main screen.

        Este método cambia la pantalla actual a la pantalla principal.
        '''

        
        self.main_layout.remove_widget(self.table_layout)
        self.main_layout.remove_widget(self.button_layout)
        app.screen_manager.current = 'main'
        
    def show_saved_messages(self):

        '''
        This method shows the saved messages of the user.

        Este método muestra los mensajes guardados del usuario.
        '''
        self.table_layout = GridLayout(cols=3)

        messages = self.encriptation_engine.get_user_messages()
            
        for message in messages:
            secret_key = message[0]
            encrypted_message = message[1]
            original_message = message[2]

            self.table_layout.add_widget(TextInput(multiline=True,text=secret_key, font_size=20,readonly=True))
            self.table_layout.add_widget(TextInput(multiline=True,text=encrypted_message, font_size=20,readonly=True))
            self.table_layout.add_widget(TextInput(multiline=True,text=original_message, font_size=20,readonly=True))

        self.main_layout.add_widget(self.table_layout)

        self.button_layout = GridLayout(padding=10,size_hint_y=None, height=50,cols=2)
        # Botón para volver a la pantalla principal
        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50),halign='center',valign='middle')
        self.back_button.bind(on_press=self.switch_to_main) 

        self.delete_messages_button = Button(background_color='red',text="Eliminar TODOS los mensajes", font_size=20, size_hint=(None, None), size=(300, 50),halign='center',valign='middle')
        self.delete_messages_button.bind(on_press=self.delete_all_messages)

        self.button_layout.add_widget(self.back_button)
        self.button_layout.add_widget(self.delete_messages_button)

        if len(messages) == 0:
            self.delete_messages_button.disabled = True
    
        self.main_layout.add_widget(self.button_layout)

    def delete_all_messages(self, instance):
        '''
        This method deletes all the messages of the user.

        Este método elimina todos los mensajes del usuario.
        '''
        delete_status = self.encriptation_engine.delete_user_messages()
        if delete_status:
            self.show_popup_succesful_deleted_messages()
            self.main_layout.remove_widget(self.table_layout)
            self.main_layout.remove_widget(self.button_layout)
            app.screen_manager.current = 'main'

    def show_popup_succesful_deleted_messages(self):
        '''
        This method shows a popup with the success message.

        Este método muestra un popup con el mensaje de éxito.
        '''
        contenido = GridLayout(cols=1)
        success_label = Label(text='Mensajes eliminados exitosamente')
        contenido.add_widget(success_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        success_popup = Popup(title='Mensajes eliminados', content=contenido)
        boton_cerrar.bind(on_press=success_popup.dismiss)
        success_popup.open()
class EncryptionScreenWithoutInputs(Screen):
    '''
    Class builds and manages the encryption screen with the user inputs.

    Esta clase construye y gestiona la pantalla de encriptación con los inputs del usuario.
    '''
    def __init__(self,encriptation_engine, **kwargs):
        '''
        This method initializes the layout attribute of the class and adds the widgets to the layout.

        Este método inicializa el atributo layout de la clase y agrega los widgets al layout.
        '''
        super(EncryptionScreenWithoutInputs, self).__init__(**kwargs)
        self.encriptation_engine : EncriptationEngine = encriptation_engine

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1, padding=20, spacing=20)
        self.main_layout.add_widget(Label(text="Pantalla de Encriptación", font_size=50))

        # Grid layout para recibir el mensaje a encriptar con su respectivo TextInput y Label
        self.encryption_layout = GridLayout(rows= 2, spacing = 20)
        self.encryption_layout.add_widget(Label(text="Inserte el texto que desea encriptar", font_size=20))
        self.unencripted_message = TextInput(font_size=16, height=300,hint_text='Inserte el texto que desea encriptar')
        self.encryption_layout.add_widget(self.unencripted_message)

        # Grid Layout que contiene el label y el textinput donde se muestra el mensaje encriptado
        self.encrypted_message_layout = GridLayout(rows = 2, spacing = 20)
        self.encrypted_message_layout.add_widget(Label(text="El mensaje encriptado es: ", font_size=20))
        self.text_encrypted_message = TextInput(font_size=16, multiline=False,readonly=True ,height=300,hint_text='Aquí se mostrará el mensaje encriptado') 
        self.encrypted_message_layout.add_widget(self.text_encrypted_message)


        # Grid layout que contiene el label y textinput donde se muestra la clave secreta
        self.secret_key_layout = GridLayout(rows = 2, spacing = 20)
        self.secret_key_label = Label(text="La clave secreta es: ", font_size=20) 
        self.secret_key = TextInput(font_size=16, multiline=False,readonly=True ,height=300,hint_text='Aquí se mostrará la clave secreta')


        # Se agregan los widgets al layout de la clave secreta
        self.secret_key_layout.add_widget(self.secret_key_label)
        self.secret_key_layout.add_widget(self.secret_key)
        


        # Grid layout que contienee el botón para volver y ejecutar la lógica de encriptación
        self.buttons_layout  = BoxLayout( spacing = 20)

        # Botones para volver, encriptar y limpiar los inputs
        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.switch_to_main) 

        self.encrypt_button = Button(text="Encriptar", font_size=20)  
        self.encrypt_button.bind(on_press=self.encrypt_message)

        self.clear_inputs_button = Button(text="Limpiar", font_size=20, size_hint=(None, None), size=(100, 50))
        self.clear_inputs_button.bind(on_press=self.clear_text_inputs)

        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.encrypt_button)
        self.buttons_layout.add_widget(self.clear_inputs_button)

        # Se agregan los layouts de los widgets al layout principal
        self.main_layout.add_widget(self.encryption_layout)
        self.main_layout.add_widget(self.encrypted_message_layout)
        self.main_layout.add_widget(self.secret_key_layout)

        self.save_message_button = Button(disabled=True,size_hint_y=None,height=30 ,text='Guardar mensaje', font_size=20, on_press=self.save_message)
        self.main_layout.add_widget(self.save_message_button)
        self.main_layout.add_widget(self.buttons_layout)

        # Agregamos el layout principal al Screen de encriptación
        self.add_widget(self.main_layout)

    def save_message(self, instance):
        '''
        This method saves the encrypted message in the database.

        Este método guarda el mensaje encriptado en la base de datos.
        '''
        try:
            encrypted_message = self.text_encrypted_message.text
            secret_key = self.secret_key.text
            original_message = self.unencripted_message.text
            self.encriptation_engine.save_user_message(secret_key,encrypted_message,original_message)
            self.show_popup_succesful_saved_message()
            self.save_message_button.disabled = True
        except Exception as error:
            self.show_popup_encryption_errors(error)

    def switch_to_main(self, instance):
        '''
        This method changes the current screen to the main screen.

        Este método cambia la pantalla actual a la pantalla principal.
        '''
        if self.save_message_button.disabled == True:
            self.save_message_button.disabled = False
        app.screen_manager.current = 'main'

    def clear_text_inputs(self, instance):
        '''
        This method clears the text inputs of the screen.

        Este método limpia los text inputs de la pantalla.
        '''
        self.unencripted_message.text = ""
        self.text_encrypted_message.text = ""
        self.secret_key.text = ''

    def encrypt_message(self,message: str):

        '''
        This method calls the encryption algorithm to encode and encrypt the message.
        
        Este método llama al algoritmo de encriptación para codificar y encriptar el mensaje.
        '''
        try:
            # Validates if the inputs arent empty / Valida si los inputs no están vacíos
            self.validate_inputs()


            self.encriptation_engine.fill_prime_set()
            secret_key = self.encriptation_engine.generate_public_and_private_key()
            message : str = str(self.unencripted_message.text)

            encrypted_message = self.encriptation_engine.encode_and_encrypt_message(message)
            
            self.text_encrypted_message.text = str(encrypted_message)
            self.secret_key.text = str(secret_key)
            self.save_message_button.disabled = False

        except EmptyInputValuesError as error:
            self.show_popup_encryption_errors(error)
        except EmptyMessageError as error:
            self.show_popup_encryption_errors(error)
        except InvalidPublicKey as error:
            self.show_popup_encryption_errors(error)
        except EmptyPublicKey as error:
            self.show_popup_encryption_errors(error)
        except NonPrimeNumber as error:
            self.show_popup_encryption_errors(error)
        except TypeError as error:
            self.show_popup_encryption_errors(error)
        except ValueError as error:
            self.show_popup_encryption_errors(error)
        except Exception as error:
            self.show_popup_encryption_errors(error)

    def validate_inputs(self):
        '''
        This method validates the inputs of the user.

        Este método valida los inputs del usuario.
        '''
        if self.unencripted_message.text == "":
            raise EmptyInputValuesError
        
    def show_popup_succesful_saved_message(self):
        '''
        This method shows a popup with the success message.

        Este método muestra un popup con el mensaje de éxito.
        '''
        contenido = GridLayout(cols=1)
        success_label = Label(text='Mensaje guardado exitosamente')
        contenido.add_widget(success_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        success_popup = Popup(title='Mensaje guardado', content=contenido)
        boton_cerrar.bind(on_press=success_popup.dismiss)
        success_popup.open()


    def show_popup_encryption_errors(self, err):
        '''
        This method shows a popup with the error message.

        Este método muestra un popup con el mensaje de error.
        '''
        contenido = GridLayout(cols=1)
        error_label = Label(text=str(err))  
        contenido.add_widget(error_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        error_popup = Popup(title='Error', content=contenido)  # Establecer un tamaño inicial
        boton_cerrar.bind(on_press=error_popup.dismiss)
        error_popup.open()
        
class PreEncryptionScreen(Screen):
    '''
    This class builds and manages the pre-encryption screen of the application.

    Esta clase construye y gestiona la pantalla de pre-encriptación de la aplicación.
    '''

    def __init__(self,encriptation_engine, **kw):

        ''''
        This method initializes the layout of the class and adds the widgets to the layout.

        Método que inicializa el layout de la clase y agrega los widgets al layout.
        '''
        super().__init__(**kw)
        self.encriptation_engine = encriptation_engine


        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.layout = GridLayout(cols=1, padding=20, spacing=20)
        self.layout.add_widget(Label(text='Para encriptar puede utilizar \n dos funcionalidades de la aplicación.' ,halign='center',valign='middle',font_size=50))

        # Grid layout que contiene los botones para seleccionar la funcionalidad de encriptación
        self.decition_buttons_layout = GridLayout(rows=3, padding=20, spacing=20)

        self.button_decition_1 = Button(text='Encriptar mensaje con llave pública generada por el motor y números primos \n seleccionados por el motor.',halign='center',valign='middle', font_size=20)
        self.button_decition_2 = Button(text='Encriptar mensaje con llave pública y números primos ingresados por el usuario.', font_size=20)
        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50))

        self.decition_buttons_layout.add_widget(self.button_decition_1)
        self.decition_buttons_layout.add_widget(self.button_decition_2)
        self.decition_buttons_layout.add_widget(self.back_button)

        # Botones para cambiar de pantalla y manejar la lógica de la aplicación
        self.back_button.bind(on_press=self.switch_to_main)
        self.button_decition_1.bind(on_press=self.switch_to_encryption_without_inputs)
        self.button_decition_2.bind(on_press=self.switch_to_encryption_with_inputs)

        # Se agregan los layouts de los widgets al layout principal
        self.layout.add_widget(self.decition_buttons_layout)

        self.add_widget(self.layout)

    def switch_to_main(self, instance):
        '''
        This method changes the current screen to the main screen.

        Este método cambia la pantalla actual a la pantalla principal.
        '''
        app.screen_manager.current = 'main'

    def switch_to_encryption_with_inputs(self, instance):
        '''
        This method changes the current screen to the encryption screen with the user inputs.

        Este método cambia la pantalla actual a la pantalla de encriptación con los inputs del usuario.
        '''
        app.screen_manager.current = 'encryption_with_inputs'

    def switch_to_encryption_without_inputs(self, instance):
        '''
        This method changes the current screen to the encryption screen without the user inputs.

        Este método cambia la pantalla actual a la pantalla de encriptación sin los inputs del usuario.
        '''
        app.screen_manager.current = 'encryption'

class EncryptionScreenWithInputs(Screen):
    '''
    Class builds and manages the encryption screen of the application.

    Esta clase construye y gestiona la pantalla de encriptación de la aplicación.
    '''
    def __init__(self,encriptation_engine : EncriptationEngine, **kwargs):
        '''
        This method initializes the layout attribute of the class and adds the widgets to the layout.

        Este método inicializa el atributo layout de la clase y agrega los widgets al layout.
        '''

        super(EncryptionScreenWithInputs, self).__init__(**kwargs)
        self.encriptation_engine : EncriptationEngine = encriptation_engine


        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1, padding=20, spacing=10)
        self.main_layout.add_widget(Label(text="Pantalla de Encriptación", font_size=35))

        # Grid layout para recibir el mensaje a encriptar con su respectivo TextInput y Label
        self.encryption_layout = GridLayout(rows= 2, spacing = 20)
        self.encryption_layout.add_widget(Label(text="Inserte el texto que desea encriptar", font_size=20))
        self.unencripted_message = TextInput(font_size=16, height=300,hint_text='Inserte el texto que desea encriptar')
        self.encryption_layout.add_widget(self.unencripted_message)

        #Grid layout para la llave pública con su respectivo label y textinput
        self.public_key_layout = GridLayout(rows = 2, spacing = 20)
        self.public_key_layout.add_widget(Label(text="Inserte la clave pública", font_size=20))
        self.public_key = TextInput(font_size=16, height=300, multiline=False,hint_text='Inserte la clave pública (Número entero)')  
        self.public_key_layout.add_widget(self.public_key)

        # Grid layout que contiene el label y otro grid layout con los textinput de los números primos
        self.primes_numbers_layout = GridLayout(rows = 2, spacing = 20)
        self.primes_numbers_layout.add_widget(Label(text="Inserte los números primos ", font_size=20))

        # Grid layout que contiene los textinput de los números primos
        self.primes_layout = GridLayout(cols = 2, spacing = 20)
        self.prime_number1 = TextInput(font_size=16, height=300,multiline= False,hint_text='Inserte el primer número primo')  
        self.prime_number2 = TextInput(font_size=16, height=300,multiline=False, hint_text='Inserte el segundo número primo')  
        self.primes_layout.add_widget(self.prime_number1)
        self.primes_layout.add_widget(self.prime_number2)
        self.primes_numbers_layout.add_widget(self.primes_layout)

        # Grid Layout que contiene el label y el textinput donde se muestra el mensaje encriptado
        self.encrypted_message_layout = GridLayout(rows = 2, spacing = 20)
        self.encrypted_message_layout.add_widget(Label(text="El mensaje encriptado es: ", font_size=20))
        self.text_encrypted_message = TextInput(font_size=16, multiline=False,readonly=True ,height=300,hint_text='Aquí se mostrará el mensaje encriptado') 
        
        self.encrypted_message_layout.add_widget(self.text_encrypted_message)
        # Grid layout que contienee el botón para volver y ejecutar la lógica de encriptación
        self.buttons_layout  = BoxLayout( spacing = 20)

        self.back_button = Button(text="Volver", font_size=15, size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.switch_to_main) 

        self.encrypt_button = Button(text="Encriptar", font_size=15)  
        self.encrypt_button.bind(on_press=self.encrypt_message)

        self.clear_inputs_button = Button(text="Limpiar", font_size=15, size_hint=(None, None), size=(100, 50))
        self.clear_inputs_button.bind(on_press=self.clear_text_inputs)

        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.encrypt_button)
        self.buttons_layout.add_widget(self.clear_inputs_button)

        # Se agregan los layouts de los widgets al layout principal
        self.main_layout.add_widget(self.encryption_layout)
        self.main_layout.add_widget(self.public_key_layout)
        self.main_layout.add_widget(self.primes_numbers_layout)
        self.main_layout.add_widget(self.encrypted_message_layout)
        self.save_message_button = Button(disabled=True,size_hint_y=None,height=20 ,text='Guardar mensaje', font_size=20, on_press=self.save_message)
        self.main_layout.add_widget(self.save_message_button)
        self.main_layout.add_widget(self.buttons_layout)

        # Agregamos el layout principal al Screen de encriptación
        self.add_widget(self.main_layout)

    def save_message(self, instance):
        '''
        This method saves the encrypted message in the database.

        Este método guarda el mensaje encriptado en la base de datos.
        '''
        try:
            encrypted_message = self.text_encrypted_message.text
            secret_key = f'[{self.public_key.text}, {self.prime_number1.text}, {self.prime_number2.text}]'
            original_message = self.unencripted_message.text
            self.encriptation_engine.save_user_message(secret_key,encrypted_message,original_message)
            self.show_popup_succesful_saved_message()
            self.save_message_button.disabled = True
        except Exception as error:
            self.show_popup_encryption_errors(error)

    def show_popup_succesful_saved_message(self):
        '''
        This method shows a popup with the success message.

        Este método muestra un popup con el mensaje de éxito.
        '''
        contenido = GridLayout(cols=1)
        success_label = Label(text='Mensaje guardado exitosamente')
        contenido.add_widget(success_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        success_popup = Popup(title='Mensaje guardado', content=contenido)
        boton_cerrar.bind(on_press=success_popup.dismiss)
        success_popup.open()

    def switch_to_main(self, instance):
        '''
        This method changes the current screen to the main screen.

        Este método cambia la pantalla actual a la pantalla principal.
        '''
        app.screen_manager.current = 'main'

    def clear_text_inputs(self, instance):
        '''
        This method clears the text inputs of the screen.

        Este método limpia los text inputs de la pantalla.
        '''
        self.unencripted_message.text = ""
        self.public_key.text = ""
        self.prime_number1.text = ""
        self.prime_number2.text = ""
        self.text_encrypted_message.text = ""

    def encrypt_message(self, instance):
        '''
        This method calls the encryption algorithm to encode and encrypt the message.
        
        Este método llama al algoritmo de encriptación para codificar y encriptar el mensaje.
        '''

        try:
            # Validates if the inputs arent empty / Valida si los inputs no están vacíos
            self.validate_inputs()
            # Getting prime numbers / Obteniendo números primos
            prime_number1 : int = int(self.prime_number1.text)
            prime_number2 : int = int(self.prime_number2.text)

            message : str = str(self.unencripted_message.text)
            public_key : int = int(self.public_key.text) 

            encrypted_message = self.encriptation_engine.encode_and_encrypt_message_with_inputs(message, prime_number1, prime_number2, public_key)
            
            self.text_encrypted_message.text = str(encrypted_message)
            self.save_message_button.disabled = False

        except EmptyInputValuesError as error:
            self.show_popup_encryption_errors(error)
        except EmptyMessageError as error:
            self.show_popup_encryption_errors(error)
        except InvalidPublicKey as error:
            self.show_popup_encryption_errors(error)
        except EmptyPublicKey as error:
            self.show_popup_encryption_errors(error)
        except NonPrimeNumber as error:
            self.show_popup_encryption_errors(error)
        except TypeError as error:
            self.show_popup_encryption_errors(error)
        except ValueError as error:
            self.show_popup_encryption_errors(error)
        except Exception as error:
            self.show_popup_encryption_errors(error)
            
    def validate_inputs(self):
        '''
        This method validates the inputs of the user.

        Este método valida los inputs del usuario.
        '''
        
        unencripted_message : bool = self.unencripted_message.text == ""
        public_key : bool = self.public_key.text == ""
        prime_number1 : bool = self.prime_number1.text == ""
        prime_number2 : bool = self.prime_number2.text == ""

        empty_inputs : list[bool]= [unencripted_message, public_key, prime_number1, prime_number2]

        for input in empty_inputs:
            if input:
                raise EmptyInputValuesError
            
        if not self.public_key.text.isnumeric():
            raise InvalidPublicKey('La clave pública debe ser un número entero')
            
    def show_popup_encryption_errors(self, err):
        '''
        This method shows a popup with the error message.

        Este método muestra un popup con el mensaje de error.
        '''
        contenido = GridLayout(cols=1)
        error_label = Label(text=str(err))  # Establecer un alto fijo o usar size_hint_y=None para permitir que el Label defina su propio alto
        contenido.add_widget(error_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        error_popup = Popup(title='Error', content=contenido)  # Establecer un tamaño inicial
        boton_cerrar.bind(on_press=error_popup.dismiss)
        error_popup.open()

class DecryptationScreen(Screen):
    '''
    This class builds and manages the decryption screen of the application.

    Esta clase construye y gestiona la pantalla de desencriptación de la aplicación.
    '''
    def __init__(self,encriptation_engine : EncriptationEngine, **kwargs):
        '''
        This method initializes the layout attribute of the class and adds the widgets to the layout.

        Este método inicializa el atributo layout de la clase y agrega los widgets al layout.
        '''
        super(DecryptationScreen, self).__init__(**kwargs)
        self.encriptation_engine : EncriptationEngine = encriptation_engine

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1, padding=20, spacing=20)
        # Agregar texto de lo que hace la interfaz directamente en el layout principal
        self.main_layout.add_widget(Label(text="Pantalla de Desencriptación", font_size=50))


        # Grid Layout que contiene el label y el textinput donde se socilita el texto a desencriptar
        self.decrypt_grid_layout = GridLayout(rows=2, spacing=20)
        self.decrypt_grid_layout.add_widget(Label(text="Inserte el texto que desea desencriptar", font_size=30))
        self.encripted_message = TextInput(font_size=16, height=300,hint_text='Inserte el texto que desea desencriptar. Ej: [123, 456, 789]')
        self.decrypt_grid_layout.add_widget(self.encripted_message)

        #Grid layout para la llave pública
        self.public_key_grid_layout = GridLayout(rows = 2, spacing = 20)
        self.public_key_grid_layout.add_widget(Label(text="Inserte la clave secreta", font_size=30))
        self.secret_key = TextInput(font_size=16, height=300, multiline=False,hint_text='Inserte la clave secreta. Ej: [123, 456, 789]')
        self.public_key_grid_layout.add_widget(self.secret_key)

        # Grid Layout
        self.decrypted_message_grid_layout = GridLayout(rows=2, spacing=20)
        self.decrypted_message_grid_layout.add_widget(Label(text="El mensaje desencriptado es: ", font_size=30))
        self.decrypted_message = TextInput(font_size=16, height=300, readonly=True, hint_text='Aquí se mostrará el mensaje desencriptado')
        self.decrypted_message_grid_layout.add_widget(self.decrypted_message)

        # Grid layout que contiene los 3 botones para volver, desencriptar y limpiar los inputs
        self.buttons_layout  = BoxLayout( spacing = 20)

        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.switch_to_main) 

        self.dencrypt_button = Button(text="Desencriptar", font_size=20)
        self.dencrypt_button.bind(on_press=self.decrypt_message)

        self.clear_inputs_button = Button(text="Limpiar", font_size=20, size_hint=(None, None), size=(100, 50))
        self.clear_inputs_button.bind(on_press=self.clear_text_inputs)

        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.dencrypt_button)
        self.buttons_layout.add_widget(self.clear_inputs_button)

        #Se agrega cada layout al layout principal
        self.main_layout.add_widget(self.decrypt_grid_layout)
        self.main_layout.add_widget(self.public_key_grid_layout)
        self.main_layout.add_widget(self.decrypted_message_grid_layout)
        self.main_layout.add_widget(self.buttons_layout)

        self.add_widget(self.main_layout)

    def switch_to_main(self, instance):
        '''
        This method changes the current screen to the main screen.

        Este método cambia la pantalla actual a la pantalla principal.
        '''
        app.screen_manager.current = 'main'

    def clear_text_inputs(self, instance):
        '''
        This method clears the text inputs of the screen.

        Este método limpia los text inputs de la pantalla.
        '''
        self.encripted_message.text = ""
        self.secret_key.text = ""
        self.decrypted_message.text = ""

    def decrypt_message(self, instance):
        '''
        This method calls the decryption algorithm to decode and decrypt the message.
        
        Este método llama al algoritmo de desencriptación para decodificar y desencriptar el mensaje.
        '''
        try:
            # Validates if the inputs arent empty / Valida si los inputs no están vacíos
            self.validate_decrypt_inputs()
            # Getting prime numbers / Obteniendo números primos
            encrypted_message  = (self.encripted_message.text)
            secret_key : str = str(self.secret_key.text)


            if not encrypted_message.startswith('[') or not encrypted_message.endswith(']'):
                raise Exception('El mensaje debe ser ingresado como una lista de números separados por comas.')

            elif self.encriptation_engine.secret_key_format_validator(secret_key) == False:
                raise InvalidPublicKey('La clave pública debe ser una cadena de texto con el formato especificado')
            else:
                '''
                Calls the decode_and_decrypt_message method of the EncriptationEngine class to decrypt the message /
                Llama al método decode_and_decrypt_message de la clase EncriptationEngine para desencriptar el mensaje

                '''
                encrypted_message = encrypted_message.strip('[]')

                # Dividir la cadena en elementos individuales
                encrypted_message = encrypted_message.split(', ')
                elementos_hexadecimal = [str(elemento.strip("'")) for elemento in encrypted_message]
                elementos = self.encriptation_engine.convert_hexadecimal_to_decimal(elementos_hexadecimal)

                # Convertir cada elemento en la lista a un entero
                list_encrypted_message = [int(elemento) for elemento in elementos]

                public_key, prime_number1, primer_number2 = secret_key.split(',')
                public_key = int(public_key.strip('[').strip(']').strip())
                prime_number1 = int(prime_number1.strip('[]').strip(']').strip())
                prime_number2 = int(primer_number2.strip('[]').strip(']').strip())

                decrypted_message = self.encriptation_engine.decode_and_decrypt_message(list_encrypted_message, public_key,prime_number1,prime_number2)
                self.decrypted_message.text = str(decrypted_message)

            

        except EmptyInputValuesError as error:
            self.show_popup_decryption_errors(error)
        except EmptyMessageError as error:
            self.show_popup_decryption_errors(error)
        except InvalidPublicKey as error:
            self.show_popup_decryption_errors(error)
        except EmptyPublicKey as error:
            self.show_popup_decryption_errors(error)
        except NonPrimeNumber as error:
            self.show_popup_decryption_errors(error)
        except TypeError as error:
            self.show_popup_decryption_errors(error)
        except ValueError as error:
            self.show_popup_decryption_errors(error)
        except Exception as error:
            self.show_popup_decryption_errors(error)

    def validate_decrypt_inputs(self):

        '''
        This method validates the inputs of the user.

        Este método valida los inputs del usuario.
        '''
        
        encrypted_message : bool = self.encripted_message.text == ""
        public_key : bool = self.secret_key.text == ""

        empty_inputs : list[bool]= [encrypted_message, public_key]

        for input in empty_inputs:
            if input:
                raise EmptyInputValuesError
            
    def show_popup_decryption_errors(self, err):
        '''
        This method shows a popup with the error message.

        Este método muestra un popup con el mensaje de error.
        '''
        contenido = GridLayout(cols=1)
        error_label = Label(text=str(err))
        contenido.add_widget(error_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        error_popup = Popup(title='Error', content=contenido)
        boton_cerrar.bind(on_press=error_popup.dismiss)
        error_popup.open()

class WelcomeScreen(Screen):

    '''
    Class builds and manages the welcome screen of the application.

    Clase construye y gestiona la pantalla de bienvenida de la aplicación.
    '''

    def __init__(self,encriptation_engine, **kwargs):

        '''
        This method creates the mainscreen layout and adds the widgets to the layout.

        Este método crea el layout de la pantalla principal y agrega los widgets al layout.
        '''

        super(WelcomeScreen, self).__init__(**kwargs)

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.layout = GridLayout(cols=1, padding=20, spacing=20)
        
        # Agregar texto de lo que hace la interfaz directamente en el layout principal
        self.layout.add_widget(Label(text="Bienvenido al motor de encriptación", font_size=50))
        self.layout.add_widget(Label(text="¿Qué desea hacer hoy?", font_size=35))

        # Botones para cambiar de pantalla y manejar la lógica de la aplicación
        self.layout.add_widget(Button(text="Registrarse", font_size=50, on_press=self.switch_to_register))
        self.layout.add_widget(Button(text="Iniciar Sesión", font_size=50, on_press=self.switch_to_login))
        self.layout.add_widget(Button(text="Salir", font_size=50, on_press=self.exit_app))
        self.add_widget(self.layout)

    def switch_to_register(self, instance):
        '''
        This method switches the screen to the register screen.

        Este método cambia la pantalla actual a la pantalla de registro.
        '''
        app.screen_manager.current = 'register'

    def switch_to_login(self, instance):
        '''
        This method switches the screen to the login screen.

        Este método cambia la pantalla actual a la pantalla de inicio de sesión.
        '''
        app.screen_manager.current = 'login'

    def exit_app(self, instance):
        '''
        This method closes the application.

        Este método cierra la aplicación.
        '''
        App.get_running_app().stop()

class RegisterScreen(Screen):

    '''
    Class builds and manages the register screen of the application.

    Clase construye y gestiona la pantalla de registro de la aplicación.
    '''

    def __init__(self,encriptation_engine : EncriptationEngine, **kwargs):

        '''
        This method creates the mainscreen layout and adds the widgets to the layout.

        Este método crea el layout de la pantalla principal y agrega los widgets al layout.
        '''

        super(RegisterScreen, self).__init__(**kwargs)
        self.encriptation_engine : EncriptationEngine = encriptation_engine

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1, padding=20, spacing=20)
        

        #Texto principal de la pantalla
        self.main_layout.add_widget(Label(text="Registrarse", font_size=50))

        #Label para ingresar el nombre de usuario con su respectivo textinput
        self.main_layout.add_widget(Label(text="Ingrese su nombre de usuario", font_size=20))
        self.username = TextInput(font_size=16, height=300, hint_text='Ingrese su nombre de usuario')
        self.main_layout.add_widget(self.username)

        #Label para ingresar la contraseña con su respectivo textinput
        self.main_layout.add_widget(Label(text="Ingrese su contraseña", font_size=20))

        self.passcode = TextInput(font_size=16, height=300, hint_text='Ingrese su contraseña', password=True)
        self.main_layout.add_widget(self.passcode)

        self.confirm_passcode = TextInput(font_size=16, height=300, hint_text='Confirme su contraseña', password=True)
        self.main_layout.add_widget(self.confirm_passcode)

        self.show_password_button = Button(text="Mostrar contraseña",font_size=20, on_press=self.show_password)
        self.main_layout.add_widget(self.show_password_button)

        # Grid layout que contiene los 3 botones para volver, registrarse y limpiar los inputs
        self.buttons_layout  = BoxLayout( spacing = 20)

        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.switch_to_welcome)

        self.register_button = Button(text="Registrarse", font_size=20)
        self.register_button.bind(on_press=self.register)


        self.clear_inputs_button = Button(text="Limpiar", font_size=20, size_hint=(None, None), size=(100, 50))
        self.clear_inputs_button.bind(on_press=self.clear_text_inputs)

        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.register_button)
        self.buttons_layout.add_widget(self.clear_inputs_button)

        self.main_layout.add_widget(self.buttons_layout)

        #Se agrega el layout principal al Screen de registro
        self.add_widget(self.main_layout)

    def switch_to_welcome(self, instance):
        '''
        This method changes the current screen to the welcome screen.

        Este método cambia la pantalla actual a la pantalla de bienvenida.
        '''
        app.screen_manager.current = 'welcome'

    def show_password(self, instance):
        '''
        This method shows the password of the user.

        Este método muestra la contraseña del usuario.
        '''
        if self.passcode.password:
            self.passcode.password = False
            self.confirm_passcode.password = False
            self.show_password_button.text = "Ocultar Contraseña"
        else:
            self.passcode.password = True
            self.confirm_passcode.password = True
            self.show_password_button.text = "Mostrar Contraseña"

    def clear_text_inputs(self, instance):
        '''
        This method clears the text inputs of the screen.

        Este método limpia los text inputs de la pantalla.
        '''
        self.username.text = ""
        self.passcode.text = ""
        self.confirm_passcode.text = ""

    def show_popup_register_errors(self, err):
        '''
        This method shows a popup with the error message.

        Este método muestra un popup con el mensaje de error.
        '''
        contenido = GridLayout(cols=1)
        error_label = Label(text=str(err))
        contenido.add_widget(error_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        error_popup = Popup(title='Error', content=contenido)
        boton_cerrar.bind(on_press=error_popup.dismiss)
        error_popup.open()

    def show_popup_register_success(self):
        '''
        This method shows a popup with the success message.

        Este método muestra un popup con el mensaje de éxito.
        '''
        contenido = GridLayout(cols=1)
        success_label = Label(text='Usuario registrado con éxito. Inicie sesión para acceder al programa')
        contenido.add_widget(success_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        success_popup = Popup(title='Éxito', content=contenido)
        boton_cerrar.bind(on_press=success_popup.dismiss)
        success_popup.open()
        
    def register(self, instance):
        '''
        This method registers the user.

        Este método registra al usuario.
        '''
        try:
            if self.username.text == '' or self.passcode.text == '' or self.confirm_passcode.text == '':
                raise Exception('Todos los campos son obligatorios')
            if len(self.username.text) > 16:
                raise Exception('El nombre de usuario debe tener menos de 16 caracteres')
            if len(self.passcode.text) > 20 or len(self.confirm_passcode.text) > 20:
                raise Exception('La contraseña debe tener menos de 20 caracteres')
            if self.passcode.text != self.confirm_passcode.text:
                raise Exception('Las contraseñas no coinciden. Revisa los campos de contraseña.')
            if len(self.passcode.text) < 8 or len(self.confirm_passcode.text) < 8:
                raise Exception('La contraseña debe tener al menos 8 caracteres')
            else:
       
                username = self.username.text
                passcode = self.passcode.text
                
                register_status = self.encriptation_engine.register_user(username, passcode)
                if register_status:
                    self.clear_text_inputs(None)
                    self.show_popup_register_success()
                    app.screen_manager.current = 'login'

        except psycopg2.errors.UniqueViolation as error:
            print(f'Error psycopg2 UniqueViolation: {error}')
            self.show_popup_register_errors(error)
        except Exception as error:
            print(error)
            self.show_popup_register_errors(error)
        
class LoginScreen(Screen):
    
    '''
    Class builds and manages the login screen of the application.

    Clase construye y gestiona la pantalla de inicio de sesión de la aplicación.
    '''

    def __init__(self,encriptation_engine : EncriptationEngine, **kwargs):

        '''
        This method creates the mainscreen layout and adds the widgets to the layout.

        Este método crea el layout de la pantalla principal y agrega los widgets al layout.
        '''

        super(LoginScreen, self).__init__(**kwargs)
        self.encriptation_engine : EncriptationEngine = encriptation_engine

        # Layout principal donde están todos los demás widgets y layouts adicionales
        self.main_layout = GridLayout(cols=1, padding=20, spacing=20)
        

        #Texto principal de la pantalla
        self.main_layout.add_widget(Label(text="Inicio de sesión", font_size=50))

        #Label para ingresar el nombre de usuario con su respectivo textinput
        self.main_layout.add_widget(Label(text="Ingrese su nombre de usuario", font_size=20))
        self.username = TextInput(font_size=16, height=300, hint_text='Ingrese su nombre de usuario')
        self.main_layout.add_widget(self.username)

        #Label para ingresar la contraseña con su respectivo textinput
        self.main_layout.add_widget(Label(text="Ingrese su contraseña", font_size=20))

        self.passcode = TextInput(font_size=16, height=300, hint_text='Ingrese su contraseña', password=True)
        self.main_layout.add_widget(self.passcode)

        self.show_password_button = Button(text="Mostrar contraseña",font_size=20, on_press=self.show_password)
        self.main_layout.add_widget(self.show_password_button)

        # Grid layout que contiene los 3 botones para volver, registrarse y limpiar los inputs
        self.buttons_layout  = BoxLayout( spacing = 20)

        self.back_button = Button(text="Volver", font_size=20, size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.switch_to_welcome)

        self.login_button = Button(text="Iniciar Sesión", font_size=20)
        self.login_button.bind(on_press=self.login)


        self.clear_inputs_button = Button(text="Limpiar", font_size=20, size_hint=(None, None), size=(100, 50))
        self.clear_inputs_button.bind(on_press=self.clear_text_inputs)

        self.buttons_layout.add_widget(self.back_button)
        self.buttons_layout.add_widget(self.login_button)
        self.buttons_layout.add_widget(self.clear_inputs_button)

        self.main_layout.add_widget(self.buttons_layout)

        #Se agrega el layout principal al Screen de registro
        self.add_widget(self.main_layout)

    def switch_to_welcome(self, instance):
        '''
        This method changes the current screen to the welcome screen.

        Este método cambia la pantalla actual a la pantalla de bienvenida.
        '''
        app.screen_manager.current = 'welcome'

    def show_password(self, instance):
        '''
        This method shows the password of the user.

        Este método muestra la contraseña del usuario.
        '''
        if self.passcode.password:
            self.passcode.password = False
            self.show_password_button.text = "Ocultar Contraseña"
        else:
            self.passcode.password = True
            self.show_password_button.text = "Mostrar Contraseña"

    def clear_text_inputs(self, instance):
        '''
        This method clears the text inputs of the screen.

        Este método limpia los text inputs de la pantalla.
        '''
        self.username.text = ""
        self.passcode.text = ""

    def show_popup_login_errors(self, err):
        '''
        This method shows a popup with the error message.

        Este método muestra un popup con el mensaje de error.
        '''
        contenido = GridLayout(cols=1)
        error_label = Label(text=str(err))
        contenido.add_widget(error_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        error_popup = Popup(title='Error', content=contenido)
        boton_cerrar.bind(on_press=error_popup.dismiss)
        error_popup.open()

    def show_popup_login_success(self):
        '''
        This method shows a popup with the success message.

        Este método muestra un popup con el mensaje de éxito.
        '''
        contenido = GridLayout(cols=1)
        success_label = Label(text='Inicio de sesión exitoso')
        contenido.add_widget(success_label)

        boton_cerrar = Button(text='Cerrar')
        contenido.add_widget(boton_cerrar)

        success_popup = Popup(title='Éxito', content=contenido)
        boton_cerrar.bind(on_press=success_popup.dismiss)
        success_popup.open()

    def login(self, instance):
        '''
        This method registers the user.

        Este método registra al usuario.
        '''
        try:
            if self.username.text == '' or self.passcode.text == '':
                raise Exception('Todos los campos son obligatorios')
            else:
       
                username = self.username.text
                passcode = self.passcode.text
                
                login_status = self.encriptation_engine.login_user(username, passcode)

                if login_status:
                    self.show_popup_login_success()
                    self.clear_text_inputs(None)
                    app.screen_manager.current = 'main'
        except Exception as error:
            print(error)
            self.show_popup_login_errors(error)

class EncryptationApp(App):
    '''
    This class builds and manages the application.

    Esta clase construye y gestiona la aplicación.
    '''

    def build(self):
        '''
        This method builds the screen manager and adds the screens to the screen manager.

        Este método construye el screen manager y agrega las pantallas al screen manager.
        '''
        self.encriptation_engine = EncriptationEngine()
        self.screen_manager = ScreenManager()
        self.welcome_screen = WelcomeScreen(self.encriptation_engine,name='welcome')
        self.register_screen = RegisterScreen(self.encriptation_engine,name='register')
        self.login_screen = LoginScreen(self.encriptation_engine,name='login')
        self.main_screen = MainScreen(self.encriptation_engine,name='main')
        self.pre_encryption_screen = PreEncryptionScreen(self.encriptation_engine,name='pre_encryption')
        self.encryption_screen_without_inputs = EncryptionScreenWithoutInputs(self.encriptation_engine,name='encryption')
        self.saved_messages_screen = SavedMessagesScreen(self.encriptation_engine,name='saved_messages')
        self.encryption_screen_with_inputs = EncryptionScreenWithInputs(self.encriptation_engine,name='encryption_with_inputs')
        self.decryption_screen = DecryptationScreen(self.encriptation_engine,name='decryption')
        self.change_passcode_screen = ChangePasscodeScreen(self.encriptation_engine,name='change_passcode')

        self.screen_manager.add_widget(self.welcome_screen)
        self.screen_manager.add_widget(self.register_screen)
        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.pre_encryption_screen)
        self.screen_manager.add_widget(self.encryption_screen_without_inputs)
        self.screen_manager.add_widget(self.saved_messages_screen)
        self.screen_manager.add_widget(self.encryption_screen_with_inputs)
        self.screen_manager.add_widget(self.decryption_screen)
        self.screen_manager.add_widget(self.change_passcode_screen)

        return self.screen_manager



# Run the application / Ejecuta la aplicación
if __name__ == "__main__":
    app = EncryptationApp()
    app.run()
