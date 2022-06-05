import pickle
import flask
from flask import Flask , request ,app,jsonify

from flask import Response

from flask_cors import CORS

import pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
from feature_extraction import features_selection
from Load_from_mongodb import  extract_data_mongodb
from sklearn.preprocessing import StandardScaler
import logger_Forest
std_scaler = StandardScaler()
app = Flask(__name__)
model_1 = pickle.load(open('decision_tree.pkl.pkl', 'rb'))
model_2 = pickle.load(open('RFregression_model.pkl','rb'))

@app.route('/')
def home():
    # return 'Hello World'
    return render_template('home.html')


@app.route('/single_prediction')
def single_prediction():
    return render_template('Sin_Class.html')

@app.route('/individual_reg_prediction')
def individual_reg_prediction():
    return render_template('Sin_Reg.html')

@app.route('/bulk_data_predict_class')
def bulk_data_predict_class():
    return render_template('Bul_Class.html')

@app.route('/bulk_data_predict_regress')
def bulk_data_predict_regress():
    return render_template('Bul_Regre.html')

@app.route('/single_classifier', methods=['POST'])
def single_classifier():
    data = [float(x) for x in request.form.values()]
    feature_sel_obj = features_selection(data)
    scaled_features = feature_sel_obj.scal_trans()
    output = model_1.predict(scaled_features)[0]
    print(output)
    # output = round(prediction[0], 2)
    if output ==1:
        print("The datas tends to predict Fire")
        return render_template('Sin_Class.html', prediction_text="The data tends to show that   {}".format('no_fire'))
    elif output ==0:
        print("the datas shows that there is no fire")
        return render_template('Sin_Class.html', prediction_text="The data tends to show that   {}".format('fire'))

@app.route('/single_regressor', methods=['POST'])
def single_regressor():
    if request.method=='POST':
        try:
            data = [float(x) for x in request.form.values()]
        except Exception as err:
            logger_Forest.logging_error("The data entered was not in correct format"+str(err))
            return render_template('Sin_Reg.html', prediction_text="The data tends to show that you entered incorrect datatype {}".format(output))
        else:
            input_value = np.array(data).reshape(1,-1)
            output = model_2.predict(input_value)[0]
            print(output)
            return render_template('Sin_Reg.html', prediction_text="The data tends to show that  Temperature will be {}".format(output))
    else:
        return render_template("Sin_Reg.html")


@app.route('/bulk_Classifier', methods=['POST'])
def bulk_Classifier():
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['mypassword']
            data_base_name = request.form['DBname']
            collection_name = request.form['collec_name']
            e1 = extract_data_mongodb(username, password)
    else:
        return render_template("Bul_Class.html")

    if e1.check_login_mongodb(data_base_name, collection_name)==True:
        data_frame = e1.read_classi_data()
        #using random forest models so no scaling is required
        X_to_predict = data_frame
        output = model_1.predict(X_to_predict)
        con_output = np.where(output>0,'fire','no_fire')

        data_frame["output"] = con_output.reshape(-1,1)
        print(data_frame)
        logger_Forest.logging_info("Model predicted the output successfully")
        try:
            return render_template('index.html', column_names=data_frame.columns.values, row_data=list(data_frame.values.tolist()), zip=zip)
        except Exception as err:
            logger_Forest.logging_info("Unable to show results in html page")
            return render_template('Bul_Class.html',prediction_text="The connection was not established with mongodb enter details again")
    else:
        logger_Forest.logging_info("Connection was not established thus")
        return render_template('Bul_Class.html', prediction_text="The connection was not established with mongodb enter details again")

@app.route('/bulk_regression', methods=['POST'])
def bulk_regression():
    if request.method=='POST':
            username = request.form['username']
            password = request.form['mypassword']
            data_base_name = request.form['DBname']
            collection_name = request.form['collec_name']
            e1 = extract_data_mongodb(username, password)
    else:
        return render_template("Bul_Regre.html",prediction_text="The connection was not established with mongodb enter details! again ")
    if e1.check_login_mongodb(data_base_name, collection_name):
        data_frame = e1.read_regression_data()
        # using random forest models so no scaling is required
        X_to_predict = data_frame
        output = np.round(model_2.predict(X_to_predict),3)
        data_frame["Temperature_predicted"]= output.reshape(-1,1)
        logger_Forest.logging_info("Model predicted  the temperature output successfully")
        try:
            return render_template('index.html', column_names=data_frame.columns.values, row_data=list(data_frame.values.tolist()), zip=zip)
        except Exception as err:
            logger_Forest.logging_info("Unable to show results in html page")
            return render_template('Bul_Regre.html',prediction_text="The connection was not established with mongodb enter details again")
    else:
        logger_Forest.logging_info("Connection was not established thus enter details again")
        return render_template('Bul_Regre.html', prediction_text="The connection was not established with mongodb enter details again!")


if __name__ == "__main__":
    app.run(debug=True)
