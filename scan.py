import os
from termcolor import colored

with open('targets.txt', 'r') as f:
    myNames = f.readlines()
myNames = [x.replace('\n', '') for x in myNames]
targetFile = '/Users/azimdars/Desktop/SoftwareUpdate/targets.txt'
errorFolder = '/Users/azimdars/Desktop/output/errors/'
outputFolder = '/Users/azimdars/Desktop/output/outputs/'
combineFolder = '/Users/azimdars/Desktop/output/combined/'
hostnameFolder = '/Users/azimdars/Desktop/output/hostnames/'
version4DFolder = '/Users/azimdars/Desktop/output/4D/'
updateList = []
version4DList = []


def prep():
    print(colored('\nRemoving old Temp files...\t', 'cyan'))
    os.system('rm -f ' + errorFolder + '* ' + outputFolder + '* ' + combineFolder + '* ' + hostnameFolder + '*' + version4DFolder + '*')
    print(colored('\n[SUCCESS]\n', 'green'))


def execute():
    print(colored('Checking for updates...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -e ' + errorFolder + ' -o ' + outputFolder + ' softwareupdate -l')
    print(colored('\n[SUCCESS]\n', 'green'))


def hostname():
    print(colored('Getting hostnames...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + hostnameFolder + ' hostname')
    print(colored('\n[SUCCESS]\n', 'green'))


def cleanup():
    count = 0
    while count < len(myNames):
        machine = str(myNames[count])
        print("Cleaning up " + machine + "'s output...")

        os.system('cat ' + hostnameFolder + machine + ' ' + outputFolder + machine + ' ' + errorFolder + machine + ' >> ' + combineFolder + machine + '.txt')
        count += 1

    print(colored('\n[SUCCESS]\n', 'green'))
    print('**********************************************\n')


def version4D():
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + version4DFolder + ' find /Applications -maxdepth 1 -iname 4D*')
    print(colored('\n[SUCCESS]\n', 'green'))


def check4updates():
    count = 0
    while count < len(myNames):
        with open(combineFolder + str(myNames[count]) + '.txt') as x:
            storage = x.readlines()
            storage = [worded.replace('\n', '') for worded in storage]
        if 'No new software available.' in storage:
            print('-----------------------------\n')
            print(colored(myNames[count] + '\t = [UP TO DATE]\]', 'green'))
            print(colored('Hostname: ' + str(storage[0]), 'blue'))
            step = 0
            while step < len(myNames):
                with open(version4DFolder + str(myNames[count])) as x:
                    box = x.readlines()
                    box = [word.replace('/Applications/', '') for word in box]
                    box = [word.replace('\n', '') for word in box]
                    box = [word.replace('.app', '') for word in box]
                    box = [word.replace('4D ', '4D') for word in box]
                    box = [word.replace('V', 'v') for word in box]
                    box.sort()
                    step += 1
            print('4D Versions installed: ' + str(box) + '\n')
        else:
            print('-----------------------------\n')
            print(colored(myNames[count] + '\t= [WARNING: THIS SYSTEM NEEDS UPDATES]', 'red'))
            updateList.append(str(myNames[count]))
            linecheck = 0
            print(colored('Hostname: ' + str(storage[0]), 'blue'))
            step = 0
            while step < len(myNames):
                with open(version4DFolder + str(myNames[count])) as x:
                    box = x.readlines()
                    box = [word.replace('/Applications/', '') for word in box]
                    box = [word.replace('\n', '') for word in box]
                    box = [word.replace('.app', '') for word in box]
                    box = [word.replace('4D ', '4D') for word in box]
                    box = [word.replace('V', 'v') for word in box]
                    box.sort()
                    step += 1
            print('4D Versions installed: ' + str(box))
            print('Updates available: ')
            while linecheck < len(storage):
                str(storage).replace('\n', '')
                if '*' in str(storage[linecheck]):
                    line = str(storage[linecheck + 1])
                    print(colored(line, 'red'))
                linecheck += 1
            print('\n')
        count += 1
    print('**********************************************\n')
    print(colored('[DONE]', 'green'))


try:
    # prep()
    # execute()
    # hostname()
    # cleanup()
    check4updates()
    # version4D()
except(IndexError):
    print('Issue present, check IP list.')
print('Machines that need upgrades: \t' + str(updateList))
