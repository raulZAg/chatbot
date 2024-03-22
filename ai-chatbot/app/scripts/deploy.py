#!/usr/bin/python3

# Deploy script for ubuntu
import os
import sys
from subprocess import call
import subprocess

version = sys.version_info
GIT_REPO = 'https://github.com/K4rlosReyes/ai-dashbot'


# Step 1: Dependencies

def check_dependencies():
	print('Checking dependencies...')

	deps = [ 'python3.8', 'git' ]
	missing =  [False] * len(deps)

	to_install = ''

	for i in range(len(deps)):
		s = subprocess.check_output( ['which', deps[i]] )
		if len(s) == 0:
			missing[i] = True
			to_install += deps[i] + ' '
	return to_install

def install_dependencies(to_install):
	print('Installing dependencies...')
	os.system( 'sudo apt update' )
	os.system( 'sudo apt install ' + to_install + ' -y' )


#Step 2: Clone repository

def clone_repository(folder:str):
	os.system(f'git clone {GIT_REPO} {folder}' )


#Step 3: Build environment

def create_venv(folder:str):

	print( 'Creating environment...' )
	if folder[-1] != '/':
		folder += '/'
	folder_env = folder + 'env/'

	os.system( f'python3.8 -m venv {folder_env}' )

	print( 'Installing environment deps...' )
	os.system( f'{folder_env}/bin/pip3.8 install -r {folder}requirements.txt' )
	return folder_env


#Step 4: Create daemon
def create_deamon():
	pass

if __name__ == '__main__':
	if len(sys.argv)<2:
		print('Example: deploy.py /home/apps/chatAI')
		exit()
	pending = check_dependencies()

	if len(pending)>0:
		install_dependencies(pending)
	
	clone_repository(sys.argv[1])
	env_folder = create_venv(sys.argv[1])
#	print(env_folder)
