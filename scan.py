import os
from termcolor import colored

with open('targets.txt', 'r') as f:
    myNames = f.readlines()
myNames = [x.replace('\n', '') for x in myNames]
targetFile = './targets.txt'
errorFolder = './errors/'
outputFolder = './outputs/'
combineFolder = './combined/'
hostnameFolder = './hostnames/'
version4DFolder = './version4D/'
mountFolder= './mounts/'
updateList = []
backupList = []
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
    print(colored('Cleaning up output...\n', 'cyan'))
    while count < len(myNames):
        machine = str(myNames[count])
        # print("Cleaning up " + machine + "'s output...")
        os.system('cat ' + hostnameFolder + machine + ' ' + outputFolder + machine + ' ' + errorFolder + machine + ' >> ' + combineFolder + machine + '.txt')
        count += 1
    print(colored('\n[SUCCESS]\n', 'green'))


def version4D():
    print(colored('Getting 4D Versions...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + version4DFolder + ' find /Applications -maxdepth 1 -iname 4D*')
    print(colored('\n[SUCCESS]\n', 'green'))
    print('**********************************************\n')


def mountCheck():
    print(colored('Getting mounted drives...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + mountFolder + ' ls /Volumes/')
    print(colored('\n[SUCCESS]\n', 'green'))


def printMounts(count):
    while count < len(myNames):
        with open(mountFolder + str(myNames[count])) as z:
            hold = z.readlines()
            hold = [words.replace('\n', '') for words in hold]
            hold = str(hold).lower()
        if 'time' in str(hold):
            return '[YES]'
        elif 'backup' in str(hold):
            return '[YES]'
        else:
            return '[NO]'


def check4updates():
    count = 0
    while count < len(myNames):
        with open(combineFolder + str(myNames[count]) + '.txt') as x:
            storage = x.readlines()
            storage = [worded.replace('\n', '') for worded in storage]
            x.close()
        if 'No new software available.' in storage:
            print('-----------------------------'
                  '')
            print(colored(myNames[count] + '\t\t\t= [UP TO DATE]]', 'green'))
            print(colored('Hostname\t\t\t\t= ' + str(storage[0]), 'blue'))
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
                    x.close()
            print('4D Versions installed\t= ' + str(box))
            print('Time Machine / Backup\t= ' + printMounts(count))
            if printMounts(count) == '[NO]':
                backupList.append(myNames[count])
        else:
            print('-----------------------------')
            print(colored(myNames[count] + '\t\t\t= [WARNING: THIS SYSTEM NEEDS UPDATES]', 'red'))
            updateList.append(str(myNames[count]))
            linecheck = 0
            print(colored('Hostname\t\t\t\t= ' + str(storage[0]), 'blue'))
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
                    x.close()
                    step += 1
            print('4D Versions installed\t= ' + str(box))
            print('Time Machine / Backup\t= ' + printMounts(count))
            if printMounts(count) == '[NO]':
                backupList.append(myNames[count])
            print('\nUpdates available ')
            while linecheck < len(storage):
                str(storage).replace('\n', '')
                if '*' in str(storage[linecheck]):
                    line = str(storage[linecheck + 1])
                    print(colored('\t\t\t\t\t' + '    =' + line, 'red'))
                linecheck += 1
            print('\n')
        count += 1
    print('**********************************************\n')
    print(colored('[DONE]\n', 'green'))


try:
    prep()
    execute()
    hostname()
    cleanup()
    mountCheck()
    version4D()
    check4updates()
except IndexError:
    print('Issue present, check IP list.')
print('Machines that need upgrades\t:\t' + str(updateList))
print('Machines that need backup\t:\t' + str(backupList))
