#!/bin/bash

hr="${HOME}/Code/bash/file/multiLineEdit"

# __________________________________________________ cntlm wrapper
pwFix="${hr}/awkScripts/pwFix"
getUserName="${hr}/awkScripts/getUserName"

bash='/bin/bash'
cntlm='/usr/sbin/cntlm'
awk='/usr/bin/awk'

# Check for imput arguments
if [ $# -eq 0 ]; then
	echo 'Must enter a username to authenticate'
	exit 1
fi

echo 'Enter Password:'
cntlmOut="$(${cntlm} -H -a 'NTLMv2' -d 'nam.corp.gm.com' -u "${@}")"

cntlmOut=$(tail -n 3 <(echo "${cntlmOut}"))

# echo "${cntlmOut}"

echo "${cntlmOut}" | cut -d'#' -f 1

exit # REMOVE TO RUN WHOLE PROGRAM

# fix password and username formatting
pw="$(${awk} -f ${pwFix} <(echo ${cntlmOut}))"
userName="$(${awk} -f ${getUserName} <(echo ${cntlmOut}))"
userName="${userName/\'/}"
userName="${userName/\',/}"
userName="Username	${userName}"

# NOTE: output must have quotations around it!! ex. "${pw}"
# echo "${pw}"
# echo "${userName}"

# __________________________________________________ config file password
configEditor="${hr}/configEditor/run.sh"

function replaceInConfig () {
	${bash} ${configEditor}\
	 "${new_section}"\
	 "${begin_marker}"\
	 "${end_marker}"\
	 "${confFile}"

}

new_section="${pw}"
begin_marker='# Password BEGIN AUTOMATICALLY EDITED PART, DO NOT EDIT'
end_marker='# Password END AUTOMATICALLY EDITED PART'
confFile="${hr}/testConfig"

replaceInConfig

# __________________________________________________ config file username
configEditor="${hr}/configEditor/run.sh"

new_section="${userName}"
begin_marker='# UserName BEGIN AUTOMATICALLY EDITED PART, DO NOT EDIT'
end_marker='# UserName END AUTOMATICALLY EDITED PART'

replaceInConfig
