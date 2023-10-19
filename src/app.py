from fastapi import FastAPI, Request,HTTPException,Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


import pickle
import pandas as pd

from lung_features import LungFeatures

app=FastAPI()

templates=Jinja2Templates(directory='templates')

model=pickle.load(open('model.pkl','rb'))
preprocessor=pickle.load(open('preprocessor.pkl','rb'))


def get_valuess(data):
    return [getattr(data,field) for field in data.__annotations__.keys()]

@app.get('/',response_class=HTMLResponse)
async def home(request: Request):
     return templates.TemplateResponse('home.html',{'request':request})

@app.post('/predict')
async def predict(request: Request,
                    gender:str=Form(...),
                    age:int=Form(...),
                    smoking:str=Form(...),
                    yellow_fingers:str=Form(...),
                    anxiety:str=Form(...),
                    peer_pressure:str=Form(...),
                    chronic_disease:str=Form(...),
                    fatigue:str=Form(...),
                    allergy:str=Form(...),
                    wheezing:str=Form(...),
                    alcohol_consuming:str=Form(...),
                    coughing:str=Form(...),
                    shortness_of_breath:str=Form(...),
                    swallowing_difficulty:str=Form(...),
                    chest_pain:str=Form(...),
                ):


        data= LungFeatures(
                age=age,
                gender=gender,         
                smoking=smoking,
                yellow_fingers=yellow_fingers,
                anxiety=anxiety,
                peer_pressure=peer_pressure,
                chronic_disease=chronic_disease,
                fatigue=fatigue,
                allergy=allergy,
                wheezing=wheezing,
                alcohol_consuming=alcohol_consuming,
                coughing=coughing,
                shortness_of_breath=shortness_of_breath,
                swallowing_difficulty=swallowing_difficulty,
                chest_pain=chest_pain)
        
        data_df = pd.DataFrame([get_valuess(data)], columns=data.__annotations__.keys())
       
        data_df=preprocessor.transform(data_df)
        print(data_df)
        prediction = model.predict(data_df)
        proba=model.predict_proba(data_df)
        probability=f"{proba.tolist()[0][1]*100:.2f}% {proba.tolist()[0][0]*100:.2f}%"
        if prediction[0] == 0:
            pred='Negative'
        else:
            pred='Positive'
        return templates.TemplateResponse("predict.html", {"request": request, "prediction": pred, "probability":probability} )
            
