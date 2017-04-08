import os
import tmallDetailParse as tdp

for i in os.listdir():
    if ('html' in i):
        try:
            tdp.tmallDetailParse(open(i, 'r').read())
        except Exception as _Eall:
            print("Failed: " + i + " " + str(_Eall) + "\n")