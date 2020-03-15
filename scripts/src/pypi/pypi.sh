#!/bin/bash
hr="$( dirname "$( realpath "${0}" )" )"

RED='\033[0;31m'
ORANGE='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
function succeed() {
	echo -e "${CYAN}[LIT] ${NC}${@}"
}
function warn() {
	echo -e "${ORANGE}[WARNING] ${NC}${@}"
}
function wait() {
	read -p $'\e[34m[PRESS ENTER]\e[0m to continue.'
}
function error() {
	echo -e "${RED}[ERROR] ${NC}${@}"
	exit 1
}

comp="${hr}/components"
help="${hr}/help"

while getopts ":h" opt; do
	case "${opt}" in
		h ) 
			cat "${help}"
			exit 0
			;;
		\? )
			error "Invalid Option: -${OPTARG}"
			;;
	esac
done
shift $((OPTIND -1)) # remove the package flag (if exists)

# Handle case no arguments
if [[ $# -eq 0 ]] ; then
	cat "${help}"
	exit 0
fi

# handle case being run from outside pypi directory
check_file="${PWD}/setup.py"
function check_directory() {
	if [ ! -f "${check_file}" ]; then
		error 'script must be run in a pypi package directory'
	fi
}

function build() {
	check_directory
	python3 setup.py sdist bdist_wheel
	succeed 'built successfully'
	echo
}

function clean() {
	check_directory
	rm -rf build/*
	rm -rf dist/*
	rm -rf syspy.egg-info/
	if [ $? -eq 0 ]; then
		succeed 'cleaned successfully'
	else
		error 'could not clean the build history'
	fi
	echo
}

function init() {
	cp "${comp}/license" "${PWD}"
	cp "${comp}/setup.py" "${PWD}"
	succeed 'moved license and generic setup file'
	echo
}

function pull() {
	warn 'we will now attempt to update your package locally.'
	echo 'If your system claims it is up to date, check the version #.'
	echo 'Sometimes it takes time for the pypi index to update after a push.'
	echo 'Try again after a few seconds: pypi pull <packageName>'
	wait
	echo
	sudo -EH pip3 install --upgrade -i https://test.pypi.org/simple/ "${@}"
	echo
	succeed 'connection to PYPI test successful. see output above for results of upgrade'
	echo 'Push your local git repo to keep everything up to date.'
	echo
}

function push() {
	if [ -z "${PYPI_PASSWORD}" ] || [ -z "${PYPI_USERNAME}" ]; then
		error 'must export environment variables for PYPI_USERNAME & PYPI_PASSWORD'
	fi
	python3 -m twine upload -u "${PYPI_USERNAME}" -p "${PYPI_PASSWORD}" --repository-url https://test.pypi.org/legacy/ dist/*
	echo
	succeed 'connection to PYPI test successful. see output above for results of deployment'
	echo
}

function setup() {
	python3 -m pip install --user --upgrade setuptools wheel
	python3 -m pip install --user --upgrade twine
}

cmd="${1}"; shift # remove package name from the inputs
case "${cmd}" in
	"all")
		if [ -z "${@}" ]; then
			error 'not enough input arguments'
		fi
		check_directory
		echo "Now change the version of the package."
		wait
		echo
		vim "${check_file}"
		clean
		build
		push
		pull "${@}"
		;;
	"build")
		build
		;;
	"clean")
		clean
		;;
	"init")
		init
		;;
	"pull")
		if [ -z "${@}" ]; then
			error 'not enough input arguments'
		fi
		pull "${@}"
		;;
	"push")
		push
		;;
	"setup")
		setup
		;;
	*)
		error "Not a recognized command: ${cmd}"
		;;

esac
