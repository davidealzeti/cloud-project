import Analyzer
import os


if __name__ == '__main__':
    analyzer = Analyzer.Analyzer()
    print(analyzer.get_vaccines_per_area(os.getenv("SAVE_FILE", False), os.getenv("FILE_FORMAT", "json")))
    print(analyzer.get_n_dosi_per_fornitore(save_file=True))
    print(analyzer.get_vaccini_per_mese(save_file=True, file_format='txt'))
