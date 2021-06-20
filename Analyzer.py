import pandas as pd


class Analyzer:
    __supported_formats__ = ['txt', 'csv', 'json']

    def __init__(self, path_to_csv: str = "data/consegne-vaccini-latest.csv"):
        self.df = pd.read_csv(path_to_csv)
        return

    # TODO: fare un check sul perché i file json vengono salvati con nomi sbagliati quando non si specifica il formato
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

    def get_vaccines_per_area(self, save_file: bool = False, file_format: str = 'json'):
        vaccines_per_area = self.df.rename(columns={'nome_area': 'Area'})
        vaccines_per_area = vaccines_per_area.groupby('Area').agg({'numero_dosi': 'sum'}).sort_values("numero_dosi",
                                                                                                      ascending=False)
        vaccines_per_area = vaccines_per_area.rename(columns={'numero_dosi': 'Dosi Totali'})

        if save_file:
            self.save_df_as_file(vaccines_per_area, 'vaccines_per_area', file_format)

        if file_format in self.__supported_formats__:
            if file_format == 'txt':
                return vaccines_per_area.to_string()
            elif file_format == 'csv':
                return vaccines_per_area.to_csv()
            elif file_format == 'json':
                return vaccines_per_area.to_json()
        else:
            return vaccines_per_area.to_json()
