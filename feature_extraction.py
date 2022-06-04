from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
std_scaler = StandardScaler()
class features_selection:
    def __init__(self,datas):

        self.df = pd.DataFrame(data=np.array(datas).reshape(1, -1),
                          columns=["day", "month", "year", "Temperature", "RH", "Ws", "Rain", "FFMC", "DMC", "DC",
                                   "ISI", "BUI", "FWI"])

    def scal_trans(self):
       self.df.drop(labels=["year", "BUI", "FWI"], axis=1, inplace=True)
       self.df_scaled = std_scaler.fit_transform(self.df)
       return self.df_scaled


if __name__=="__main__":
    arr = [10, 4, 2012, 20, 67, 5, 0.2, 65.7, 3.4, 7.6, 1.3, 3.4, 0.5]
    features_obj = features_selection(arr)
    features_obj.scal_trans()