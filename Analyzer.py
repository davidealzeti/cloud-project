import pandas as pd
import requests


class Analyzer:
    __supported_formats__ = ['txt', 'csv', 'json']
    __file_url__ = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.csv'

    def __init__(self, path_to_csv: str = "data/consegne-vaccini-latest.csv", get_file_from_web: bool = False):
        if get_file_from_web is False:
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
        return

    def save_df_as_file(self, data_frame: pd.DataFrame, file_name: str, file_format: str = 'json'):
        file_path = file_name + '.' + file_format
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

    # def get_data_media_cons_per_area(self, save_file: bool = False, file_format: str = 'json'):
    #     data_consegna_media = self.df.groupby(['area', 'fornitore']).agg({'numero_dosi': 'sum',
    #                                                                    'data_consegna': 'mean'})
    #                                                                    .sort_values("numero_dosi", ascending=False)
    #     if save_file is True:
    #         self.save_df_as_file(data_consegna_media, 'data_consegna_media_per_area', file_format)
    #
    #     return self.get_df_as_format(data_consegna_media, file_format)

    def get_vaccini_per_mese(self, save_file: bool = False, file_format: str = 'json'):
        new_df = self.df
        new_df['Anno'] = pd.DatetimeIndex(new_df['data_consegna']).year
        new_df['Mese'] = pd.DatetimeIndex(new_df['data_consegna']).month
        new_df = new_df.groupby(by=['Mese', 'Anno']).agg({'numero_dosi': 'sum'}).sort_values(["Anno", "Mese"])
        new_df = new_df.rename(columns={'numero_dosi': 'Dosi Totali'})

        if save_file is True:
            self.save_df_as_file(new_df, 'dosi_per_mese', file_format)

        return self.get_df_as_format(new_df, file_format)



