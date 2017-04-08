#!/bin/sh
#

if [ "$SHELL" = "/bin/bash" ];then
	rc=~/.bashrc
elif [ "$SHELL" = "/usr/bin/zsh" ];then
	rc=~/.zshrc	
else
	echo "Not support."
	exit
fi
#first install git
if [ -x "/usr/bin/git" ];then
	echo "git already installed..."
else
	sudo apt-get install git
	if [ "$?" = "0" ];then
		echo "git installed..."
	fi
fi
#pyenv && python3.6.0
if [ -n "$PYENV_ROOT" ];then
	echo "Already install pyenv..."
else
	git clone https://github.com/pyenv/pyenv.git ~/.pyenv
	if [ "$?" = "0" ];then
		echo 'export PYENV_ROOT="$HOME/.pyenv"' >> $rc
		echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> $rc
		echo 'eval "$(pyenv init -)"' >> ~$rc
		echo "installed pyenv ok..."
	else
		echo "Error when install pyenv."
	fi

	source $rc
	sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev
	if [ "$?" = "0" ];then
		pyenv install 3.6.0
		if [ "$?" = "0" ];then
			echo "installed python3 ok..."
		fi
	else
		echo "Error when install python3 dependencies..."
	fi
fi


#slacker(0.9.30)
pip install slacker==0.9.30
if [ "$?" != "0" ];then
	echo "Error when pip install slacker."
else
	echo "installed slacker ok..."
fi

#pymongo 3.4.0
pip install pymongo==3.4.0
if [ "$?" != "0" ];then
	echo "Error when pip install pymongo."
else
	echo "installed pymongo ok..."
fi

#redis 2.10.5
pip install redis==2.10.5
if [ "$?" != "0" ];then
	echo "Error when pip install redis."
else
	echo "installed redis ok..."
fi

#selenium (3.3.1)
pip install selenium==3.3.1
if [ "$?" != "0" ];then
	echo "Error when pip install selenium."
else
	echo "installed selenium ok..."
fi

#pyvirtualdisplay (0.2.1)
pip install pyvirtualdisplay==0.2.1
if [ "$?" != "0" ];then
	echo "Error when pip install pyvirtualdisplay."
else
	echo "installed pyvirtualdisplay ok..."
fi

#Xvfb
sudo apt-get install Xvfb
if [ "$?" != "0" ];then
	echo "Error when apt-get install Xvfb."
else
	echo "installed Xvfb ok..."
	echo 'export DISPLAY=:66' >> $rc
	echo "use sudo Xvfb :66 -ac to create a DISPLAY..."
fi
#Firefox
if [ -x "/usr/bin/firefox" ];then
	echo "firefox is already installed."
else
	sudo apt-get install firefox 
	if [ "$?" != "0" ];then
		echo "Error when apt-get install firefox."
	else
		echo "installed firefox ok..."
	fi
fi

#geckodriver
if [ -x "/usr/bin/geckodriver" ];then
	echo "geckodriver is already installed"
else
	wget http://onns.xyz/temp/geckodriver.tar.gz
	if [ "$?" = "0" ];then
		tar -xf geckodriver.tar.gz
		sudo cp geckodriver /usr/bin/
		echo "installed geckodriver ok..."
	else
		echo "Error when pip install slacker."
	fi
fi
