import time
import telebot
from telebot import types
import pickle
import numpy as np


from google.cloud import storage

storage_client = storage.Client('calcium-spanner-264710')
bucket = storage_client.get_bucket('stablemodelpickle')
blob = bucket.blob('pickle_model.pkl')
with open("./pickle_model.pkl", "wb") as file_obj:
    blob.download_to_file(file_obj)

model = pickle.load(open('pickle_model.pkl','rb'))

TOKEN = '1263868956:AAFAeMo-CGLvTjB7WfytwphqBZQBD43efZE'

knownUsers = []  # todo: save these in a file,
userStep = {}  # so they won't reset every time the bot restarts

userResponses = {}

commands = {  # command description used in the "help" command
    'start'       : 'Para iniciar la predicción',
    'help'        : 'Da información sobre los comandos disponibles',
    'instrucciones': 'Instrucciones de como proceder para hallar las predicciones'
}

genero = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
genero.add('Hombre', 'Mujer')

hideBoard = types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard


edad = types.ReplyKeyboardMarkup(one_time_keyboard=True)
edad.add('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
         '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
         '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
         '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
         '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
         '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
         '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
         '80', '81', '82', '83', '84', '85', '86', '87', '88', '89')

hideBoard = types.ReplyKeyboardRemove()

diaviaje = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
diaviaje.add('LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO')

hideBoard = types.ReplyKeyboardRemove()

distrito = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
distrito.add('CHAMARTIN', 'SALAMANCA', 'CENTRO', 'CIUDAD LINEAL',
            'PUENTE DE VALLECAS', 'CARABANCHEL', 'CHAMBERI', 'RETIRO',
            'FUENCARRAL-EL PARDO', 'TETUAN', 'MONCLOA-ARAVACA', 'ARGANZUELA',
            'SAN BLAS', 'LATINA', 'USERA', 'HORTALEZA', 'VILLAVERDE',
            'MORATALAZ', 'VILLA DE VALLECAS', 'VICALVARO', 'BARAJAS',
            'VILLA DE VALLECAS')

hideBoard = types.ReplyKeyboardRemove()

vehiculo = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
vehiculo.add('TURISMO', 'MOTOCICLETA', 'FURGONETA', 'AUTO-TAXI',
             'AUTOBUS-AUTOCAR', 'CICLOMOTOR', 'BICICLETA', 
             'CAMION', 'VARIOS', 'AMBULANCIA', 'VEH.3 RUEDAS')

hideBoard = types.ReplyKeyboardRemove()

conductor = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
conductor.add('CONDUCTOR', 'VIAJERO', 'PEATON')

hideBoard = types.ReplyKeyboardRemove()

hora = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
hora.add('00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
         '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
         '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
         '18:00', '19:00', '20:00', '21:00', '22:00', '23:00')

hideBoard = types.ReplyKeyboardRemove()

# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        userResponses[uid] = {
            'sexo': 0, 
            'edad': 0, 
            'barrio': 0, 
            'diasemana': 0, 
            'vehiculo': 0,
            'tipo': 0
            }
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = 0  # save user id and his current "command level", so he can use the "/getImage" command
        userResponses[cid] = {
            'sexo': 0, 
            'edad': 0, 
            'barrio': 0, 
            'diasemana': 0, 
            'vehiculo': 0,
            'tipo': 0
            }
        bot.send_message(cid, "Hola, bienvenido.")
        command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "Presione /genero para comenzar el test")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "Las siguientes opciones están disponibles: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['instrucciones'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "Para comenzar pulse en /start")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    bot.send_message(cid, "A continuación le haremos unas preguntas para conocerle mejor e indicarle la probabilidad de accidente y en este caso la lesividad más probable.")


# user can chose an image (multi-stage command example)
@bot.message_handler(commands=['genero'])
def command_image(m):
    cid = m.chat.id
    bot.send_message(cid, "Por favor, elija su género.", reply_markup=genero)  # show the keyboard
    userStep[cid] = 1  # set the user to the next step (expecting a reply in the listener now)


# if the user has issued the "/getImage" command, process the answer
@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def msg_image_select(m):
    cid = m.chat.id
    text = m.text
    
    # for some reason the 'upload_photo' status isn't quite working (doesn't show at all)
    bot.send_chat_action(cid, 'typing')
    if m.chat.id not in userResponses:
        userResponses[m.chat.id] = {}
    print(userResponses)
    if text == 'Hombre':  # send the appropriate image based on the reply to the "/getImage" command
        userResponses[m.chat.id]['sexo'] = 1
        bot.send_message(cid, "Perfecto, indíquenos su edad.", reply_markup=edad)  # send file and hide keyboard, after image is sent
        userStep[cid] = 0  # reset the users step back to 0
    elif text == 'Mujer':
        userResponses[m.chat.id]['sexo'] = 0
        bot.send_message(cid, "Perfecto, indíquenos su edad.", reply_markup=edad)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Por favor, use el teclado predefinido")
        bot.send_message(cid, "Por favor, inténtelo de nuevo")
        

@bot.message_handler(func=lambda message: message.text in ['0',
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
         '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
         '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
         '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
         '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
         '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
         '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
         '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
         '80', '81', '82', '83', '84', '85', '86', '87', '88', '89'])
def command_text_hi(m):
    userResponses[m.chat.id]['edad'] = int(m.text)
    bot.send_message(m.chat.id, "Genial, ¿cuándo vas a viajar?", reply_markup=diaviaje)

@bot.message_handler(func=lambda message: message.text in [
    'LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO'])
def command_text_hi(m):
    cid = m.chat.id
    text = m.text
    userResponses[m.chat.id]['diasemana'] = m.text

    if text == 'LUNES': 
        userResponses[m.chat.id]['diasemana'] = 1
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0 
    elif text == 'MARTES':
        userResponses[m.chat.id]['diasemana'] = 2
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0
    elif text == 'MIERCOLES':
        userResponses[m.chat.id]['diasemana'] = 3
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0
    elif text == 'JUEVES':
        userResponses[m.chat.id]['diasemana'] = 4
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0
    elif text == 'VIERNES':
        userResponses[m.chat.id]['diasemana'] = 5
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0
    elif text == 'SABADO':
        userResponses[m.chat.id]['diasemana'] = 6
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0
    elif text == 'DOMINGO':
        userResponses[m.chat.id]['diasemana'] = 7
        bot.send_message(cid, "Muy bien, ¿por qué distrito?", reply_markup=distrito)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Por favor, use el teclado predefinido")
        bot.send_message(cid, "Por favor, inténtelo de nuevo")

@bot.message_handler(func=lambda message: message.text in [
            'CHAMARTIN', 'SALAMANCA', 'CENTRO', 'CIUDAD LINEAL',
            'PUENTE DE VALLECAS', 'CARABANCHEL', 'CHAMBERI', 'RETIRO',
            'FUENCARRAL-EL PARDO', 'TETUAN', 'MONCLOA-ARAVACA', 'ARGANZUELA',
            'SAN BLAS', 'LATINA', 'USERA', 'HORTALEZA', 'VILLAVERDE',
            'MORATALAZ', 'VILLA DE VALLECAS', 'VICALVARO', 'BARAJAS',
            'VILLA DE VALLECAS'])
def command_text_hi(m):
    cid = m.chat.id
    text = m.text
    userResponses[m.chat.id]['barrio'] = m.text

    if text == 'CHAMARTIN': 
        userResponses[m.chat.id]['barrio'] = 0.538136
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0 
    elif text == 'SALAMANCA':
        userResponses[m.chat.id]['barrio'] = 0.52661
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'CENTRO':
        userResponses[m.chat.id]['barrio'] = 0.520044
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'CIUDAD LINEAL':
        userResponses[m.chat.id]['barrio'] = 0.542599
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'PUENTE DE VALLECAS':
        userResponses[m.chat.id]['barrio'] = 0.528020
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'CARABANCHEL':
        userResponses[m.chat.id]['barrio'] = 0.529012
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'CHAMBERI':
        userResponses[m.chat.id]['barrio'] = 0.539454
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'RETIRO':
        userResponses[m.chat.id]['barrio'] = 0.542946
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'FUENCARRAL-EL PARDO':
        userResponses[m.chat.id]['barrio'] = 0.559222
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'TETUAN':
        userResponses[m.chat.id]['barrio'] = 0.544002
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'MONCLOA-ARAVACA':
        userResponses[m.chat.id]['barrio'] = 0.562741
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'ARGANZUELA':
        userResponses[m.chat.id]['barrio'] = 0.527174
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'SAN BLAS':
        userResponses[m.chat.id]['barrio'] = 0.537926
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'LATINA':
        userResponses[m.chat.id]['barrio'] = 0.535205
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'USERA':
        userResponses[m.chat.id]['barrio'] = 0.514768
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'HORTALEZA':
        userResponses[m.chat.id]['barrio'] = 0.552982 
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'VILLAVERDE':
        userResponses[m.chat.id]['barrio'] = 0.537729 
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'MORATALAZ':
        userResponses[m.chat.id]['barrio'] = 0.546963
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'VILLA DE VALLECAS':
        userResponses[m.chat.id]['barrio'] = 0.541587
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'VICALVARO':
        userResponses[m.chat.id]['barrio'] = 0.573143
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    elif text == 'BARAJAS':
        userResponses[m.chat.id]['barrio'] = 0.543067
        bot.send_message(cid, "Excelente, ¿cómo vas a ir?", reply_markup=vehiculo)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Por favor, use el teclado predefinido")
        bot.send_message(cid, "Por favor, inténtelo de nuevo")
    
@bot.message_handler(func=lambda message: message.text in [
             'TURISMO', 'MOTOCICLETA', 'FURGONETA', 'AUTO-TAXI',
             'AUTOBUS-AUTOCAR', 'CICLOMOTOR', 'BICICLETA', 
             'CAMION', 'VARIOS', 'AMBULANCIA', 'VEH.3 RUEDAS'])
def command_text_hi(m):
    cid = m.chat.id
    text = m.text
    userResponses[m.chat.id]['vehiculo'] = m.text

    if text == 'TURISMO': 
        userResponses[m.chat.id]['vehiculo'] = 0.932760
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0 
    elif text == 'MOTOCICLETA':
        userResponses[m.chat.id]['vehiculo'] = 1.035363
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'FURGONETA':
        userResponses[m.chat.id]['vehiculo'] = 0.291403
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'AUTO-TAXI':
        userResponses[m.chat.id]['vehiculo'] = 0.390084
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'AUTOBUS-AUTOCAR':
        userResponses[m.chat.id]['vehiculo'] = 0.501497
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'CICLOMOTOR':
        userResponses[m.chat.id]['vehiculo'] = 1.018205
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'BICICLETA':
        userResponses[m.chat.id]['vehiculo'] = 1.017821
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'CAMION':
        userResponses[m.chat.id]['vehiculo'] = 0.166977
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'VARIOS':
        userResponses[m.chat.id]['vehiculo'] = 0.932760
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'AMBULANCIA':
        userResponses[m.chat.id]['vehiculo'] = 0.507205
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    elif text == 'VEH.3 RUEDAS':
        userResponses[m.chat.id]['vehiculo'] = 1.121212
        bot.send_message(cid, "Maravilloso, vas a ir de...", reply_markup=conductor)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Por favor, use el teclado predefinido")
        bot.send_message(cid, "Por favor, inténtelo de nuevo")

    
@bot.message_handler(func=lambda message: message.text in [
             'CONDUCTOR', 'VIAJERO', 'PEATON'])
def command_text_hi(m):
    cid = m.chat.id
    text = m.text
    userResponses[m.chat.id]['tipo'] = m.text

    if text == 'CONDUCTOR': 
        userResponses[m.chat.id]['tipo'] = 0.523581
        bot.send_message(cid, "Por último, ¿sobre qué hora irás?", reply_markup=hora)
        userStep[cid] = 0 
    elif text == 'VIAJERO':
        userResponses[m.chat.id]['tipo'] = 0.584713
        bot.send_message(cid, "Por último, ¿sobre qué hora irás?", reply_markup=hora)
        userStep[cid] = 0
    elif text == 'PEATON':
        userResponses[m.chat.id]['tipo'] = 1.333333
        bot.send_message(cid, "Por último, ¿sobre qué hora irás?", reply_markup=hora)
        userStep[cid] = 0
    else:
        bot.send_message(cid, "Por favor, use el teclado predefinido")
        bot.send_message(cid, "Por favor, inténtelo de nuevo")


@bot.message_handler(func=lambda message: message.text in [
             '00:00', '01:00', '02:00', '03:00', '04:00', '05:00',
             '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
             '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
             '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'])
def command_text_hi(m):
    (h, mn) = m.text.split(':')
    m.text = int(h)
    userResponses[m.chat.id]['hora'] = m.text
    cid = m.chat.id
    
    print(userResponses)

    bot.send_message(m.chat.id, "Genial, ya hemos terminado, espere unos segundos que estamos preparando sus resultados.")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(5)
    inputs = [userResponses[m.chat.id]['hora'],
                userResponses[m.chat.id]['diasemana'],
                userResponses[m.chat.id]['barrio'],
                0.5380060943021453,
                0.0008329342190200529,
                0.880404528385704,
                0.8591577646822008,
                0.5380169386909265,
                userResponses[m.chat.id]['vehiculo'],
                userResponses[m.chat.id]['tipo'],
                userResponses[m.chat.id]['sexo'],
                userResponses[m.chat.id]['edad'],
                40.423824710590075,
                -3.6853542365934526,
                1.5205403997258262,
                1.790968216618426,
                2.6636972051051093,
                2.6796951460758387,
                2014.1422096356607,
                6.6167183779994305,
                15.766549361764154,
                0.7519174839833691,
                0.13795473002519626]
    new_inputs = np.array([inputs])
    prediction = model.predict(new_inputs)
    print(prediction[0])
    
    if prediction==0:
        p="ILESO"
    elif prediction==1:
        p="HERIDO LEVE"
    elif prediction==2:
        p="HERIDO GRAVE"
    else:
        p="FALLECIDO"
    bot.send_message(m.chat.id, "Hola, su resultado de Lesividad es:")
    bot.send_message(m.chat.id, p)

texto = open('./resultado.txt', 'rt', encoding = 'UTF-8')
text  = texto.read()

@bot.message_handler(func=lambda message: message.text == "/Resultados")
def command_text_hi(m):
    cid = m.chat.id
    bot.send_message(m.chat.id, "Hola, su resultado de Lesividad es:")
    bot.send_message(m.chat.id, text)

# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hola")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Hola, ¿qué tal? Para empezar pulse en /start")
    
# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "Hola")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Hola, ¿qué tal? Para empezar pulse en /start")
    
# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "Buenas tardes")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Buenas tardes, ¿qué tal? Para empezar pulse en /start")

@bot.message_handler(func=lambda message: message.text == "Buenos días")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Buenos días, ¿qué tal? Para empezar pulse en /start")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No entiendo que significa \"" + m.text + "\"\nInténtelo con /help")


bot.polling()
