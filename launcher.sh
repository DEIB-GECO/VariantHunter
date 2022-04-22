#
#     VARIANT HUNTER DOCKER LAUNCHER UTILITY
#     This script will periodically adjust the size of the Docker volumes
#     during the execution of Docker in order to prevent it from filling the disk.
#
#     Run this script with the following command:
#     /bin/zsh /startup.sh {parameters_list}
#
#     More details at http://cerilab.deib.polimi.it/variant_hunter/about#docker
#

trap 'kill 0' EXIT

Clean() {
  trap 'kill 0' EXIT
  while [ true ]; do
    docker volume prune --filter label=varianthunter_app_1 -f >/dev/null
    sleep 240
  done
}

RunDocker() {
  trap 'echo "\nPress again Ctrl+C to exit."; kill 0' EXIT
  bash -c " ${DOCKER_PARAM} Docker-compose up"
}

DOCKER_PARAM=$*
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No color tag

echo "
${BLUE}** VARIANT HUNTER DOCKER LAUNCHER UTILITY **
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
