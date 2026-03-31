import os
import joblib
import pandas as pd
from django.conf import settings

MODELS_DIR = os.path.join(settings.BASE_DIR, 'air_quality', 'ml_models')

AI_MODELS = {}
FEATURES =[]
CITY_MAPPING = {}

def load_models():
    global AI_MODELS, FEATURES, CITY_MAPPING
    try:
        pm25_data = joblib.load(os.path.join(MODELS_DIR, 'airguard_pm25_ensemble.joblib'))
        
        if isinstance(pm25_data, dict) and 'model' in pm25_data:
            AI_MODELS['pm25'] = pm25_data['model']
            FEATURES = pm25_data.get('features',[])
            CITY_MAPPING = pm25_data.get('city_mapping', {})
        else:
            AI_MODELS['pm25'] = pm25_data
            
        def extract_model(filename):
            data = joblib.load(os.path.join(MODELS_DIR, filename))
            return data['model'] if isinstance(data, dict) and 'model' in data else data

        AI_MODELS['heat_index'] = extract_model('airguard_heat_index.joblib')
        AI_MODELS['water_stress'] = extract_model('airguard_deficit_eau_cumule.joblib')
        AI_MODELS['flood_risk'] = extract_model('airguard_risque_inondation.joblib')
        AI_MODELS['extreme_heat'] = extract_model('airguard_chaleur_extreme.joblib')

        print("Les  modèles IA ont été chargés")
    except Exception as e:
        print(f"ERREUR: Impossible de charger les modèles: {e}")

load_models()

def get_aqi_category(pm25_value):
    if pm25_value <= 12.0: return 50, "Bon", "🟢"
    elif pm25_value <= 35.4: return 100, "Modéré", "🟡"
    elif pm25_value <= 55.4: return 150, "Sensible", "🟠"
    elif pm25_value <= 150.4: return 200, "Malsain", "🔴"
    elif pm25_value <= 250.4: return 300, "Très mauvais", "🟣"
    else: return 500, "Dangereux", "🟤"

def get_flood_category(val):
    if val <= 2: return "Risque faible"
    if val <= 4: return "Risque modéré"
    if val <= 6: return "Risque élevé"
    return "Alerte inondation"

def predire_tous_les_indicateurs(ville_nom, meteo_data):
    
    if not AI_MODELS:
        return {"error": "Les modèles ML ne sont pas disponibles sur le serveur."}
        
    if ville_nom not in CITY_MAPPING:
        return {"error": f"La ville '{ville_nom}' n'est pas reconnue."}
        
    # 1. Construction du DataFrame d'entrée
    input_dict = {'city_enc': CITY_MAPPING[ville_nom]}
    for feature in FEATURES:
        if feature != 'city_enc':
            input_dict[feature] = meteo_data.get(feature, 0.0) 
            
    df_input = pd.DataFrame([input_dict])[FEATURES]
    
    # 2. Prédictions Multiples
    try:
        pred_pm25 = AI_MODELS['pm25'].predict(df_input)[0]
        pred_heat = AI_MODELS['heat_index'].predict(df_input)[0]
        pred_water = AI_MODELS['water_stress'].predict(df_input)[0]
        pred_flood = AI_MODELS['flood_risk'].predict(df_input)[0]
        pred_extreme = AI_MODELS['extreme_heat'].predict(df_input)[0]
    except Exception as e:
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}

    # 3. Formatage des résultats 
    aqi_val, aqi_label, aqi_color = get_aqi_category(pred_pm25)
    
    return {
        "ville": ville_nom,
        "predictions": {
            "qualite_air": {
                "pm25_proxy_ugm3": round(pred_pm25, 2),
                "aqi_estime": aqi_val,
                "categorie": aqi_label,
                "alerte_couleur": aqi_color
            },
            "chaleur_sante": {
                "heat_index_ressenti": round(pred_heat, 2),
                "chaleur_extreme_0_10": round(pred_extreme, 2),
                "avertissement": "Danger" if pred_extreme > 7 else "Normal"
            },
            "risques_naturels": {
                "stress_hydrique_agricole": round(pred_water, 2),
                "risque_inondation_0_10": round(pred_flood, 2),
                "categorie_inondation": get_flood_category(pred_flood)
            }
        }
    }