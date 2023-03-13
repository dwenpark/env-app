apt update && apt install docker docker.io -y

docker swarm init 

docker service create --name db --replicas 1 --publish mode=host,published=33403,target=3306 --env MYSQL_ROOT_PASSWORD="root" dwenup/mysql:0.0.7
docker service create --name backend --replicas 1 --publish mode=host,published=8000,target=8000 --env ADMIN_USER="admin",ADMIN_PASSWORD="admin" --with-registry-auth dwenup/env-app-backend:0.1.12
docker service create --name frontend --replicas 1 --publish mode=host,published=80,target=80 --env VUE_APP_API_IP="http://172.17.0.1:8000" dwenup/env-app-frontend:1.0.2