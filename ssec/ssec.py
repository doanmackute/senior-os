import subprocess

encrypted_device = '/dev/sdb1'
password = 'komosny1'

subprocess.run('echo "{password}" | cryptsetup luksOpen {encrypted_device} EncHomeFoo -d -', shell=True)