import pickle
import pandas as pd

with open('model_pickle', "rb") as f:
    imported_model = pickle.load(f)
KEYS = ['wind-speed',
        'average-wind-speed-(period)',
        'average-pressure-(period)',
        'humidity',
        'wind-direction']
    
def get_energy_preds(wind_direction, wind_speed, humidity, average_wind_speed, average_pressure):
    zipped = list(zip([wind_direction], [wind_speed], [humidity], [average_wind_speed], [average_pressure]))
    df_ = pd.DataFrame(zipped, columns=KEYS)
    return imported_model.predict(df_)

if __name__ == "__main__":
    print(get_energy_preds(30, 12.1, 93, 8.0, 29.99))