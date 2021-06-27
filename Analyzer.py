import pandas as pd
import requests


class Analyzer:
    __supported_formats__ = ['txt', 'csv', 'json']
    __file_url__ = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv'

    def __init__(self, path_to_csv: str = "data/consegne-vaccini-latest.csv", get_file_from_web: bool = False):
        control = True if str(get_file_from_web) == 'True' else False
        if not control:
            self.df = pd.read_csv(path_to_csv)
        else:
            try:
                response = requests.get(Analyzer.__file_url__).text

                file = open('data/vax_file_web.txt', "w")
                file.write(response)
                file.close()

                self.df = pd.read_csv('data/vax_file_web.txt')
            except Exception as e:
                print(e)
                self.df = pd.read_csv(path_to_csv)

    def make_analysis(self, analysis_id: int, save_file: bool, file_format: str):
        control = True if str(save_file) == 'True' else False

        try:
            id_control = int(analysis_id)
        except Exception as e:
            id_control = 0

        if id_control == 0:
            return self.get_vaccines_per_area(save_file=control, file_format=file_format)
        elif id_control == 1:
            return self.get_n_dosi_per_fornitore(save_file=control, file_format=file_format)
        elif id_control == 2:
            return self.get_vaccini_per_mese(save_file=control, file_format=file_format)
        elif id_control == 3:
            return self.get_percentuale_dosi_per_area(save_file=control, file_format=file_format)
        else:
            return self.get_vaccines_per_area(save_file=control, file_format=file_format)

    def save_df_as_file(self, data_frame: pd.DataFrame, file_name: str, file_format: str = 'json'):
        file_path = 'saved_files/' + file_name + '.' + file_format
        file = open(file_path, "w")

        if file_format in self.__supported_formats__:
            if file_format == 'txt':
                file.write(data_frame.to_string())
            elif file_format == 'csv':
                file.write(data_frame.to_csv())
            elif file_format == 'json':
                file.write(data_frame.to_json())
        else:
            file.write(data_frame.to_json())

        file.close()

    def get_df_as_format(self, df: pd.DataFrame, df_format: str = 'json'):
        if df_format in self.__supported_formats__:
            if df_format == 'txt':
                return df.to_string()
            elif df_format == 'csv':
                return df.to_csv()
            elif df_format == 'json':
                return df.to_json()
        else:
            return df.to_json()

    def get_vaccines_per_area(self, save_file: bool = False, file_format: str = 'json'):
        vaccines_per_area = self.df.rename(columns={'nome_area': 'Area'})
        vaccines_per_area = vaccines_per_area.groupby('Area').agg({'numero_dosi': 'sum'}).sort_values("numero_dosi",
                                                                                                      ascending=False)
        vaccines_per_area = vaccines_per_area.rename(columns={'numero_dosi': 'Dosi Totali'})

        if save_file is True:
            print("vaccines per area method: save file = " + str(save_file))
            self.save_df_as_file(vaccines_per_area, 'vaccines_per_area', file_format)

        return self.get_df_as_format(vaccines_per_area, file_format)

    def get_n_dosi_per_fornitore(self, save_file: bool = False, file_format: str = 'json'):
        n_dosi_per_fornitore = self.df.groupby('fornitore').agg({'numero_dosi': 'sum'}).sort_values("numero_dosi",
                                                                                                 ascending=False)
        if save_file is True:
            self.save_df_as_file(n_dosi_per_fornitore, 'dosi_per_fornitore', file_format)

        return self.get_df_as_format(n_dosi_per_fornitore, file_format)

    def get_vaccini_per_mese(self, save_file: bool = False, file_format: str = 'json'):
        new_df = self.df
        new_df['Anno'] = pd.DatetimeIndex(new_df['data_consegna']).year
        new_df['Mese'] = pd.DatetimeIndex(new_df['data_consegna']).month
        new_df = new_df.groupby(by=['Mese', 'Anno']).agg({'numero_dosi': 'sum'}).sort_values(["Anno", "Mese"])
        new_df = new_df.rename(columns={'numero_dosi': 'Dosi Totali'})

        if save_file is True:
            self.save_df_as_file(new_df, 'dosi_per_mese', file_format)

        return self.get_df_as_format(new_df, file_format)

    def get_percentuale_dosi_per_area(self, save_file: bool = False, file_format: str = 'json'):
        dosi_per_area = self.df.groupby('nome_area').agg({'numero_dosi': 'sum'}).sort_values(
            ['numero_dosi'], ascending=False)

        total_vaccines = dosi_per_area.agg({'numero_dosi': 'sum'})
        total_vaccines = total_vaccines['numero_dosi']

        dosi_per_area.reset_index(inplace=True)
        dosi_per_area['percentuale_dosi_ricevute'] = dosi_per_area['numero_dosi'].div(total_vaccines).mul(100).round(2).astype(str) + '%'

        dosi_per_area.rename(columns={"nome_area": "Area", "numero_dosi": "Dosi Totali", 'percentuale_dosi_ricevute': 'Percentuale dosi ricevute'}, inplace=True)
        final_df = {'Area': 'Totale', 'Dosi Totali': total_vaccines, 'Percentuale dosi ricevute': '100%'}

        dosi_per_area_final = dosi_per_area.append(final_df, ignore_index=True)

        if save_file is True:
            self.save_df_as_file(dosi_per_area_final, 'dosi_per_mese', file_format)

        return self.get_df_as_format(dosi_per_area_final, file_format)




