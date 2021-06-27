import Analyzer
import os


if __name__ == '__main__':
    analyzer = Analyzer.Analyzer(get_file_from_web=os.getenv("GET_FILE_FROM_GITHUB", False))
    print(analyzer.make_analysis(os.getenv("SELECTED_ANALYSIS", 0), os.getenv("SAVE_FILE", False), os.getenv("FILE_FORMAT", 'json')))
