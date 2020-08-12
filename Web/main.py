import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle
from google.cloud import storage

app = Flask(__name__)


#storage_client = storage.Client('calcium-spanner-264710')
#bucket = storage_client.get_bucket('stablemodelpickle')
#blob = bucket.blob('pickle_model.pkl')

#with open("./pickle_model.pkl", "wb") as file_obj:
#    blob.download_to_file(file_obj)
    
model = pickle.load(open('pickle_model.pkl','rb'))



@app.route('/')
def home():
    #return 'Hello World'
    return render_template('home.html')
    #return render_template('index.html')

@app.route('/predict',methods = ['POST'])
def predict():
    #int_features = [int(x) for x in request.form.values()]
    #final_features = [np.array(int_features)]

    def cat_sexo(sexo):
        if sexo == 'HOMBRE':
            return 1
        elif sexo == 'MUJER':
            return 0
        else:
            return 'Error'
    
    def cat_dia(dia_semana):
        if dia_semana == 'LUNES': 
            return 1
        elif dia_semana == 'MARTES':
            return 2
        elif dia_semana == 'MIERCOLES':
            return 3
        elif dia_semana == 'JUEVES':
            return 4
        elif dia_semana == 'VIERNES':
            return 5
        elif dia_semana == 'SABADO':
            return 6
        elif dia_semana == 'DOMINGO':
            return 7
        else:
            return 'Error'

    def cat_distrito(distrito):
        if distrito == 'CHAMARTIN': 
            return 0.538136
        elif distrito == 'SALAMANCA':
            return 0.52661
        elif distrito == 'CENTRO':
            return 0.520044
        elif distrito == 'CIUDAD LINEAL':
            return 0.542599
        elif distrito == 'PUENTE DE VALLECAS':
            return 0.528020
        elif distrito == 'CARABANCHEL':
            return 0.529012
        elif distrito == 'CHAMBERI':
            return 0.539454
        elif distrito == 'RETIRO':
            return 0.542946
        elif distrito == 'FUENCARRAL-EL PARDO':
            return 0.559222
        elif distrito == 'TETUAN':
            return 0.544002
        elif distrito == 'MONCLOA-ARAVACA':
            return 0.562741
        elif distrito == 'ARGANZUELA':
            return 0.527174
        elif distrito == 'SAN BLAS':
            return 0.537926
        elif distrito == 'LATINA':
            return 0.535205
        elif distrito == 'USERA':
            return 0.514768
        elif distrito == 'HORTALEZA':
            return 0.552982 
        elif distrito == 'VILLAVERDE':
            return 0.537729 
        elif distrito == 'MORATALAZ':
            return 0.546963
        elif distrito == 'VILLA DE VALLECAS':
            return 0.541587
        elif distrito == 'VICALVARO':
            return 0.573143
        elif distrito == 'BARAJAS':
            return 0.543067
        else:
            return 'error'

    def cat_vehiculo(vehiculo):
        if vehiculo == 'TURISMO': 
            return 0.932760
        elif vehiculo == 'MOTOCICLETA':
            return 1.035363
        elif vehiculo == 'FURGONETA':
            return 0.291403
        elif vehiculo == 'AUTO-TAXI':
            return 0.390084
        elif vehiculo == 'AUTOBUS-AUTOCAR':
            return 0.501497
        elif vehiculo == 'CICLOMOTOR':
            return 1.018205
        elif vehiculo == 'BICICLETA':
            return 1.017821
        elif vehiculo == 'CAMION':
            return 0.166977
        elif vehiculo == 'VARIOS':
            return 0.932760
        elif vehiculo == 'AMBULANCIA':
            return 0.507205
        elif vehiculo == 'VEH.3 RUEDAS':
            return 1.121212
        else:
            return 'Error'

    def cat_persona(persona):
        if persona == 'CONDUCTOR': 
            return 0.523581
        elif persona == 'VIAJERO':
            return 0.584713
        elif persona == 'PEATON':
            return 1.333333
        else:
            return 'Error'

    def command_text_hi(m):
        (h, mn) = m.split(':')

        return int(h)
    
    inputs = [command_text_hi(request.form["rango_horario"]),
                cat_dia(request.form["dia_semana"]),
                cat_distrito(request.form["distrito"]),
                0.5380060943021453,
                0.0008329342190200529,
                0.880404528385704,
                0.8591577646822008,
                0.5380169386909265,
                cat_vehiculo(request.form["tipo_vehiculo"]),
                cat_persona(request.form["tipo_persona"]),
                cat_sexo(request.form["sexo"]),
                request.form["tramo_edad"],
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

    #output = round(prediction[0], 2)
    return render_template('home.html', prediction_text="En caso de accidente, usted saldrá {}".format(p))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)



if __name__ == '__main__':
    app.run(debug=True)