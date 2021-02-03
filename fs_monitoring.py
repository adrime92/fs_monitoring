import subprocess
import re

def get_fs_usage(filesystem, check_inodes=False):
    '''Execute "df" command on the machine an return a dictionary with the attributes
    and its respective values

    e.g.:

    filesystem = /opt/example
    
    # Filesystem                           Size  Used Avail Use% Mounted on
    # /dev/mapper/example                   99G  5.5G   93G   6% /opt/example

    return value:
    {
    'Filesystem': '/dev/mapper/example',
    'Size': '99G',
    'Used': '5.5G',
    'Avail': '93G',
    'Use%': '6%',
    'Mounted': '/opt/example'
    }
    
    '''

    if check_inodes:
        sp_return = subprocess.run(["df","-khi", filesystem],capture_output=True, check=True)
    else:
        sp_return = subprocess.run(["df","-kh", filesystem],capture_output=True, check=True)
        
    sp_stdout = sp_return.stdout.decode("utf-8")
    list_sp_stdout = sp_stdout.rstrip("\n").split('\n')
    
    return dict(zip(list_sp_stdout[0].split(),list_sp_stdout[1].split()))

def check_percentage_usage(attr, treshold):
    '''Check if a specific attribute exceed the stablished treshold'''

    attr = int(re.findall(r'[0-9]{1,3}', attr)[0])

    if attr == treshold:
        print('Treshold Exceded')
    else:
        return attr
    

if __name__ == "__main__":
    
    disk_usage_label = 'Use%'
    inodes_usage_label = 'IUse%'
    disk_treshold = 80
    inode_treshold = 80
    fs_list = ["/var/atlassian", "/opt/atlassian"]

    for fs in fs_list:
        
        fs_disk_info = get_fs_usage(fs)
        print(fs_disk_info)
        fs_inodes_info = get_fs_usage(fs,check_inodes=True)
        
        print(f'{fs} Disk usage is {check_percentage_usage(fs_disk_info[disk_usage_label], disk_treshold)}%')
        print(f'{fs} Inodes usage is {check_percentage_usage(fs_inodes_info[inodes_usage_label], disk_treshold)}%')
