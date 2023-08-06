import argparse
import os
def set_qt_api(api:str="pyqt5",parse:bool=False):
    if parse:
        parser = argparse.ArgumentParser(description='Set Qt API')
        parser.add_argument('--api', type=str)
        args = parser.parse_args()
        if args.api is not None:
            api=args.api
    os.environ["QT_API"]=api