import Analyzer
import os


if __name__ == '__main__':
    analyzer = Analyzer.Analyzer()
    print(analyzer.get_vaccines_per_area(os.getenv("SAVE_FILE", False), os.getenv("FILE_FORMAT", "json")))
