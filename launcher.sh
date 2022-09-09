#
#     VARIANT HUNTER DOCKER LAUNCHER UTILITY
#     This script will periodically adjust the size of the Docker volumes
#     during the execution of Docker in order to prevent it from filling the disk.
#
#     Run this script with the following command:
#     /bin/zsh ./launcher.sh {parameters_list}
#
#     More details at http://cerilab.deib.polimi.it/variant_hunter/about#docker
#

trap 'kill 0' EXIT

Clean() {
  trap 'kill 0' EXIT
  while [ true ]; do
    docker volume prune --filter label=varianthunter_app_1 -f >/dev/null
    sleep 200
  done
}

RunDocker() {
  trap 'echo "\nPress again Ctrl+C to exit."; kill 0' EXIT
  docker pull gecopolimi/varianthunter
  bash -c " ${DOCKER_PARAM} Docker-compose up"
}

for str in "${@}" ; do
    # try to figure out if quoting was required for the $x
    if [[ "$str" != "${str%[[:space:]]*}" ]]; then
        var1=$(echo "$str" | cut -d "=" -f 1)
        var2=$(echo "$str" | cut -d "=" -f 2)
        str=${var1}"=""\""${var2}"\""
    fi
    _args=$_args" "$str
done
DOCKER_PARAM=$_args
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No color tag

echo "
${BLUE}** VARIANT HUNTER DOCKER LAUNCHER UTILITYYY **
     ${NC}This script will periodically adjust the size of the Docker volumes during the execution of Docker in order to prevent it from filling the disk."
echo "
     ${RED}WARNING! This may remove all Docker volumes not used by at least one container.
     ${NC}Are you sure you want to continue? [y/N]"
read answer

if [ "$answer" = 'y' ]; then
  Clean &
  RunDocker &
  wait
fi
