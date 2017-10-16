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
osFolder = './os/'
updateList = []
backupList = []
version4DList = []
osList = []

####################################################################################################
######################################## Get inforamtion ###########################################
####################################################################################################


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
        print("Cleaning up " + machine)
        os.system('cat ' + hostnameFolder + machine + ' ' + outputFolder + machine + ' ' + errorFolder + machine + ' >> ' + combineFolder + machine + '.txt')
        count += 1
    print(colored('\n[SUCCESS]\n', 'green'))


def version4D():
    print(colored('Getting 4D Versions...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + version4DFolder + ' find /Applications -maxdepth 1 -iname 4D*')
    print(colored('\n[SUCCESS]\n', 'green'))


def mountCheck():
    print(colored('Getting backup info...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + mountFolder + ' tmutil listbackups')
    print(colored('\n[SUCCESS]\n', 'green'))


def printMounts(count):
    while count < len(myNames):
        with open(mountFolder + str(myNames[count])) as z:
            hold = z.readlines()
            if len(hold) <= 1:
                return 'No Backup Located'
            else:
                length = len(hold)
                return str(hold[length - 1])


def osinfo():
    print(colored('Getting macOS Info...\n', 'cyan'))
    os.system('pssh -h ' + targetFile + ' -l softwareupdate -o ' + osFolder + ' sw_vers')
    print(colored('\n[SUCCESS]\n', 'green'))
    print('********************************************************************************************\n')


def printos(count):
    with open(osFolder + str(myNames[count])) as g:
        for line in g:
            osList.append(line)
            print(line)


def check4updates():
    count = 0
    while count < len(myNames):
        with open(combineFolder + str(myNames[count]) + '.txt') as x:
            storage = x.readlines()
            storage = [worded.replace('\n', '') for worded in storage]
            x.close()
        if 'No new software available.' in storage:
            print('---------------------------------------------------------------------------------------'
                  '')
            print(colored(myNames[count] + '\t\t\t= [UP TO DATE]]', 'green'))
            print('Hostname\t\t\t\t= ' + str(storage[0]))
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
            if printMounts(count) == 'No Backup Located':
                backupList.append(myNames[count])
                print('Time Machine / Backup\t= ' + printMounts(count) + '\n')
            else:
                print('Time Machine / Backup\t= ' + printMounts(count))
            str(printos(count))
        else:
            print('---------------------------------------------------------------------------------------')
            print(colored(myNames[count] + '\t\t\t= [WARNING: THIS SYSTEM NEEDS UPDATES]', 'red'))
            updateList.append(str(myNames[count]))
            linecheck = 0
            print('Hostname\t\t\t\t= ' + str(storage[0]))
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
            if printMounts(count) == 'No Backup Located':
                backupList.append(myNames[count])
                print('Time Machine / Backup\t= ' + printMounts(count) + '\n')
            else:
                print('Time Machine / Backup\t= ' + printMounts(count))
            str(printos(count))
            print('\nUpdates available ')
            while linecheck < len(storage):
                str(storage).replace('\n', '')
                if '*' in str(storage[linecheck]):
                    line = str(storage[linecheck + 1])
                    print('\t\t\t\t\t' + '    =' + line)
                linecheck += 1
            print('\n')
        count += 1
    print('********************************************************************************************\n')
    print(colored('[DONE]\n', 'green'))


####################################################################################################
######################################## Do Something ##############################################
####################################################################################################


def moveFile():
    print('\n1 = Move File\n\n2 = Run Update\n\n3 = Quit\n')
    question = input('Selection : ')
    if question == '1':
        location = input('Enter the path of the file you would like to move. : ')
        if os.path.isfile(location) == False:
            print('That is not a file, try again.')
            moveFile()
        allmove = input('Which device would you like to move to [IP Address]? [Enter all for all devices]: ')
        if allmove == 'all':
            print('All move selected')
            print(location)
        else:
            print('Single Selected')
            print(location)

    elif question == '2':
        allupdate = input('Would you like to update all? [Yes / No] : ')
        if allupdate == 'Yes':
            print('All update selected')
        else:
            print('Single Selected')


####################################################################################################
######################################## Initiate ##################################################
####################################################################################################


def run():
    try:
        prep()
        execute()
        hostname()
        cleanup()
        mountCheck()
        version4D()
        osinfo()
        check4updates()
    except IndexError as e:
        print('Issue present, check IP list.')
        print(e)
    print('Machines that need updates\t: ' + '[' + str(len(updateList)) + ']\t' + str(updateList))
    print('Machines that need backup\t: ' + '[' + str(len(backupList)) + ']\t' + str(backupList))

run()
#moveFile()

