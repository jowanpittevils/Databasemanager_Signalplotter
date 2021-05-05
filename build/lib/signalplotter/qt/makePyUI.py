#%%
def makeUI(uiNames):
    import sys, os
    print('Check the pwd first, It must be at .../SignalPlotter/qt.')
    print(os.getcwd())

    p0 = os.path.dirname(sys.executable)

    for uiName in (uiNames):
        print('===== for: ',uiName,' ======')
        p1 = '"'+p0+'\Scripts\pyuic5.exe'+'" '
        p1 += ' -x "' + uiName + '.ui"'
        p1 += ' -o "' + uiName + '.py"'

        print(p1)

        import subprocess
        res = subprocess.call(p1) != 0
        print('Done.')
        print('Is there any error: ', res)



uiNames = ['plotter_uiDesign']
makeUI(uiNames)

# %%
