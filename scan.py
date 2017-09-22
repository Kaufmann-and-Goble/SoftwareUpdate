import os

with open('targets.txt', 'r') as f:
    myNames = f.readlines()
myNames = [x.replace('\n', '') for x in myNames]
targetFile = '/Users/azimdars/Desktop/SoftwareUpdate/targets.txt'
errorFolder = '/Users/azimdars/Desktop/output/errors/'
outputFolder = '/Users/azimdars/Desktop/output/outputs/'
combineFolder = '/Users/azimdars/Desktop/output/combined/'
hostnameFolder = '/Users/azimdars/Desktop/output/hostnames/'


def prep():
    print('\nRemoving old Temp files...\t', end='\t\t')
    os.system('rm -f ' + errorFolder + '* ' + outputFolder + '* ' + combineFolder + '* ' + hostnameFolder + '*')
    print('[SUCCESS]\n')


def execute():
    print('Checking for updates...\n')
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -e ' + errorFolder + ' -o ' + outputFolder + ' softwareupdate -l')
    print('\n[SUCCESS]\n')


def hostname():
    print('Getting hostnames...\n')
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + hostnameFolder + ' hostname')
    print('\n[SUCCESS]\n')


def cleanup():
    count = 0
    while count < len(myNames):
        machine = str(myNames[count])
        print("Cleaning up " + machine + "'s output...")

        os.system('cat ' + hostnameFolder + machine + ' ' + outputFolder + machine + ' ' + errorFolder + machine + ' >> ' + combineFolder + machine + '.txt')
        count += 1

    print('\n[SUCCESS]\n')
    print('**********************************************\n')


def check4updates():
    count = 0
    while count < len(myNames):
        with open(combineFolder + str(myNames[count]) + '.txt') as x:
            storage = x.readlines()
        if 'No new software available.\n' in storage:
            print('-----------------------------\n')
            print(myNames[count] + '\t= [UP TO DATE]')
            print(str(storage[0]))
        else:
            print('-----------------------------\n')
            print(myNames[count] + '\t= [WARNING: THIS SYSTEM NEEDS UPDATES]')
            linecheck = 0
            print(str(storage[0]) + '\n')
            while linecheck < len(storage):
                str(storage).replace('\n', '')
                if '*' in str(storage[linecheck]):
                    line = str(storage[linecheck + 1])
                    print(line)
                linecheck += 1
            print('\n')
        count += 1
    print('**********************************************\n')
    print('[DONE]')


prep()
execute()
hostname()
cleanup()
check4updates()
