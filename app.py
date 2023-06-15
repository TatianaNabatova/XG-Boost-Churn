import sklearn


from sklearn.ensemble import GradientBoostingClassifier

import streamlit as st
import pickle
import numpy as np

import base64
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
     background-image: url("data:image/png;base64,%s");
     background-size: cover;
     }
     </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return
set_png_as_page_bg('3.jpg')


classifier_name=['XGBoost']
#option = st.sidebar.selectbox('Алгоритм прогнозирования оттока клиентов', classifier_name)
#st.subheader(option)



#Importing model and label encoders
model=pickle.load(open("model.pkl","rb"))
#model_1 = pickle.load(open("final_rf_model.pkl","rb"))
le_pik=pickle.load(open("label_encoding_for_gender.pkl","rb"))
le1_pik=pickle.load(open("label_encoding_for_geo.pkl","rb"))


def predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary):
    input = np.array([[CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary]]).astype(np.float64)
    if option == 'XGBoost':
        prediction = model.predict_proba(input)
        pred = '{0:.{1}f}'.format(prediction[0][0], 2)

    else:
        pred=0.30
        #st.markdown('Есть вероятность, что клиент останется в банке.')

    return float(pred)


def main():
  
    html_temp = """
    <div style="background-color: white ;padding:10px">
    <h1 style="color: red;text-align:center;">Прогноз оттока клиентов</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    st.markdown('Прогнозирование оттока клиентов в банке является важным инструментом, который позволяет банку улучшить качество своего обслуживания, повысить эффективность своей деятельности и увеличить доходы. ')
    st.markdown('Цель проекта - создание модели прогнозирования оттока клиентов.')
    st.markdown('Реализованы задачи: предобработка и исследовательский анализ данных, их визуализация, выбор алгоритма машинного обучения, создание, обучение, валидация и развертывание модели в Streamlit Cloud.')
    st.markdown('В ходе проекта были созданы модели на основе логистической регрессии, Random Forest, XGBoost. При валидации моделей по метрикам "F1-score", "ROC-AUC" (0,64 и 0,79) было выявлено, что модель с наибольшей предиктивной мощностью - модель с использованием XGBoost')
    



    st.sidebar.subheader("Модель прогнозирования оттока клиентов в рамках курса Diving into Darkness of Data Science")
    
    #st.sidebar.image ('4.png',width = 300)
    st.sidebar.info ("Разработчик - Татьяна Набатова")
    CreditScore = st.sidebar.slider('Скоринговый балл', 0, 900)

    Geography = st.sidebar.selectbox('Страна', ['France', 'Germany', 'Spain'])
    Geo = int(le1_pik.transform([Geography]))

    Gender = st.sidebar.selectbox('Пол', ['Male', 'Female'])
    Gen = int(le_pik.transform([Gender]))

    Age = st.sidebar.slider("Возраст", 18, 95)

    Tenure = st.sidebar.selectbox("Срок обслуживания в банке", ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','10', '11', '12', '13', '14', '15'])

    Balance = st.sidebar.slider("Баланс счета", 0.00, 250000.00)

    NumOfProducts = st.sidebar.selectbox('Количество продуктов', ['1', '2', '3', '4'])

    HasCrCard = st.sidebar.selectbox("Наличие кредитной карты", ['0', '1'])

    IsActiveMember = st.sidebar.selectbox("Активный клиент", ['0', '1'])

    EstimatedSalary = st.sidebar.slider("Зарплата", 0.00, 200000.00)
    churn_html = """  
              <div style="background-color:#fae319;padding:20px >
               <h2 style="color:red;text-align:center;"> Жаль, но теряем клиента.</h2>
               </div>
            """
    no_churn_html = """  
              <div style="background-color:#bed0d4;padding:20px >
               <h2 style="color:green ;text-align:center;"> Клиент остаётся в банке!</h2>
               </div>
            """  
    
    
    
    
    
    
    
    if int(Age)- int(Tenure)< 17:
            st.error('Ошибка !')
    else:
        if st.sidebar.button ('Сделать прогноз', key = "1"):
    
            output = predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
            st.success('Вероятность оттока составляет {}'.format(output))
      
        

            if output >= 0.5:
                st.markdown(churn_html, unsafe_allow_html= True)

            else:
                st.markdown(no_churn_html, unsafe_allow_html= True)
                st.balloons()
        
        
    
    
    
    
    if Balance < 10000 and EstimatedSalary < 5000 and IsActiveMember == 0 and NumOfProducts == 1:
            st.success('Вероятность оттока составляет более 90%.')
            st.markdown(churn_html, unsafe_allow_html= True)
    if CreditScore > 400 and EstimatedSalary > 25000 and IsActiveMember == 1 and NumOfProducts > 1 and Age < 60 and Tenure > 3 and Balance > 25000:
            st.success('Вероятность оттока составляет менее 30%.')
            st.markdown(churn_html, unsafe_allow_html= True)        
    
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
    background-color: #f73b67;
    color:#ffffff;
    }
    div.stButton > button:hover {
    background-color: #fa7f9c;
    color:#ffffff;
    }
    </style>""", unsafe_allow_html=True)

    #b = st.button("Сделать прогноз")
    
    
    if int(Age)- int(Tenure)< 17:
            st.error('Некорректный ввод данных по возрасту клиента и/или длительности обслуживания в банке')
    else:
        if st.button ('Сделать прогноз', key = "2"):
    
            output = predict_churn(CreditScore, Geo, Gen, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
            st.success('Вероятность оттока составляет {}'.format(output))
      
        

            if output >= 0.5:
                st.markdown(churn_html, unsafe_allow_html= True)

            else:
                st.markdown(no_churn_html, unsafe_allow_html= True)
                st.balloons()
if __name__=='__main__':
    main()
