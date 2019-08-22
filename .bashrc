# PROMPT_COMMAND="history -a; history -c" # add to ~/.bash_history after each command
export EDITOR='vim'

source ${HOME}/.settings/colorSettings.sh

#________________________________________________________________________________
#__________Android SDK Setup
androidsdk="${HOME}/Projects/android/sdk"
PATH=${PATH}:"${androidsdk}/platform-tools"
PATH=${PATH}:"${androidsdk}/emulator"
PATH=${PATH}:"${androidsdk}/tools"
PATH=${PATH}:"${androidsdk}/tools/bin"

export ANDROID_SDK_ROOT="${HOME}/Projects/android/sdk"
export ANDROID_HOME="${HOME}/Projects/android/sdk"
export ANDROID_AVD_HOME="${HOME}/.android/avd"

#________________________________________________________________________________
#__________Aliases
function dn() {
    new_directory="$*";
    if [ $# -eq 0 ]; then 
        new_directory=${HOME};
    fi;
    builtin cd "${new_directory}"; t
}
alias up="cd ..; t"
alias c='clear'
alias src="source ${HOME}/.bashrc; ${HOME}/scripts/scripts.py; ${HOME}/Local/scripts.py"
alias settings='bash ~/.settings/settings.sh'

#________________________________________________________________________________
#__________bin
export PATH="${HOME}/scripts/bin:${PATH}"
export PATH="${HOME}/Local/bin:${PATH}" # not tracked

#________________________________________________________________________________
#__________Python Environment
alias ve='/usr/local/bin/virtualenv'
alias p='python3'
alias create='python3 -m virtualenv env'
alias activate='source env/bin/activate'

#________________________________________________________________________________
#__________Local (not trackable)
echo '. ~/.bashrc'
source ${HOME}/.platform.sh
source ${HOME}/.locrc.sh
