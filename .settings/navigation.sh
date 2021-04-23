alias t='clear; tree -L 1 --dirsfirst'
alias r='clear; tree --dirsfirst'
alias c='clear'
set -o vi

function dn() {
    new_directory="$*";
    if [ $# -eq 0 ]; then 
        new_directory=${HOME};
    fi;
    builtin cd "${new_directory}"; c; t
}
alias up="cd ..; c; t"

