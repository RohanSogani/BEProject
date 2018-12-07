import sys, os

def getManifest(pathName):
    command = 'apktool d ' + pathName + ' -f'
    directory = os.path.dirname(pathName)
    os.chdir(directory)
    os.system(command)
    apkName = os.path.basename(pathName)
    apkName = apkName.split('.apk')
    apkName = apkName[0]
    manifestName = directory + '/' + apkName + '/AndroidManifest.xml'
    os.system('cp ' + manifestName + ' /home/nishad/BE_Project/bitbucket/xcalibur/Backend/mysite/appWindow/')
