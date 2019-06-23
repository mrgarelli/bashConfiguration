PROMPT_COMMAND="history -a; history -c" # add to ~/.bash_history after each command
export EDITOR='vim'

export ANDROID_SDK_ROOT="${HOME}/Projects/android/tools"
export ANDROID_HOME="${HOME}/.android"

source ${HOME}/Scripts/colorSettings.sh

#________________________________________________________________________________
#__________Local (not trackable)
source ${HOME}/.locrc

#________________________________________________________________________________
#__________File
alias c='clear'
function cd() {
    new_directory="$*";
    if [ $# -eq 0 ]; then 
        new_directory=${HOME};
    fi;
    builtin cd "${new_directory}" && t
}
alias up="cd ..; t"

alias copy='bash ~/Scripts/edit/copy.sh'
alias view='bash ~/Scripts/edit/view.sh'
alias apps='cd /usr/share/applications'
alias fnd='bash ~/Scripts/fnd/run.sh'
alias search='bash ~/Scripts/search.sh'

#________________________________________________________________________________
#__________System
alias linuxDrive='sudo mkfs.ext4'
alias mouse='bash ~/Scripts/mouse.sh'
alias apt-size='bash ~/Scripts/apt-size.sh'
alias battery='upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -E "state:|percentage:|time to empty:"'
alias get='sudo apt-get install'
alias upgrade='sudo apt-get update; sudo apt-get upgrade; sudo apt update; sudo apt upgrade'
alias u-grub='sudo update-grub'
alias mem='python3.7 ~/Scripts/mem/run.py'
alias dsk='python3.7 ~/Scripts/dsk/run.py'

alias fixBackground='dbus-send --type=method_call --dest=org.gnome.Shell /org/gnome/Shell org.gnome.Shell.Eval "string:global.reexec_self()"'
alias src="source ${HOME}/.bashrc; source ${HOME}/.profile"


#________________________________________________________________________________
#__________Programs
alias weather='sudo curl wttr.in'
alias chrome='/usr/bin/chromium-browser &>/dev/null'
alias render='bash ~/Scripts/render.sh &>/dev/null'
alias g='bash ~/Scripts/git/g.sh'
alias cg='bash ~/Scripts/git/cg.sh'
alias ve='/usr/local/bin/virtualenv'
alias fetch='bash ~/Scripts/fetch.sh'
alias sl='sudo bash ~/Scripts/symlinks/sl.sh'
alias C='bash ~/Scripts/gcc/C.sh'
alias todo='bash ~/Scripts/todo/run.sh'
alias settings='bash ~/Scripts/settings/run.sh'
alias clk='bash ~/Scripts/clk/run.sh'
alias dsp='bash ~/Scripts/dsp/run.sh'
alias pypi='bash ~/Scripts/pypi/run.sh'
alias rct='/usr/local/bin/react-native'

#________________________________________________________________________________
#__________Open
alias pdf="bash ~/Scripts/pdf.sh"
alias image='/usr/bin/xdg-open'

# p equates to whichever python is active
alias p='python3.7'
alias pin='sudo python3.7 -m pip install'
alias create='python3.7 -m virtualenv env'
alias activate='source env/bin/activate'
