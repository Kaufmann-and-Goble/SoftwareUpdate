import paramiko


with open('targets.txt', 'r') as f:
    myNames = f.readlines()
myNames = [x.replace('\n', '') for x in myNames]
selected = ""
print(myNames)


def getUpdateList(machine):
    command = '/Volumes/Shared/Andrew/list.sh'
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.connect(machine, username='softwareupdate')
    print('Connected to: ' + machine + ' [COMPLETED]')
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    lines = stdout.readlines()
    for line in lines:
        print(line)
    client.close()


def getMachine():
    count = 0
    while count < len(myNames):
        selected = str(myNames[count])
        count += 1
        print(selected)
        getUpdateList(selected)


getMachine()
