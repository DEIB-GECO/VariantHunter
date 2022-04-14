cd frontend
npm run build
cd ..
rm -rf docker
mkdir docker
cp requirements.txt ./docker/
cp Dockerfile ./docker/

cp -r ./backend ./docker/
mkdir ./docker/frontend
cp -r ./frontend/dist ./docker/frontend/dist
rm -f docker/backend/varianthunter.db
cd docker
DOCKER_BUILDKIT=0 docker build -t gecopolimi/varianthunter  -f Dockerfile .