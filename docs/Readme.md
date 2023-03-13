# ENV-APP

## Use Tool
Frontend: Vue.js, JWT, Bootstrap

Backend: Django, PyJWT, bcrypt

DB: MySQL

## Doc

1. 환경변수는 key-value 형식으로 관리하는 방식이 적절하다고 생각하여 RDB를 이용하기로 결정했고 그 중, 가장 흔하게 사용하는 mysql을 이용했습니다. 
   모든 데이터가 짧은 text이기 때문에 많은 용량이 필요하지 않다고 생각했으며, 인스턴스내에 hostpath로 지정할 수 있어 RDS같은 별도의 데이터베이스 서비스를 이용하지 않았습니다.
   캐시는 별도로 적용하지 않았습니다.

2. 애플리케이션 동작은 Frontend <-> Backend <-> DB

   각각 80, 8000. 33403 포트를 이용하고 있습니다.
	 현재는 포트로 애플리케이션을 구분했는데, 필요하다면 traefik, nginx와 같은 proxy를 통해 포트를 통일하고 url로 구분이 가능할 것 같습니다.

	 보안그룹에서는 ssh 키만으로 로그인 가능하기 때문에 22번 포트는 0.0.0.0으로 열어두었고,
	 80포트도 개방해두었습니다.
	 
	 그 외는 ec2 내부 포트에서 상호 작용하기 때문에 별도로 개방하지 않았습니다.

3. EC2에 docker swarm을 이용하여 애플리케이션을 배포했습니다.

   EC2를 선정한 첫 번째 이유는 가격입니다.

	 MVP 구현단계이기도 하지만 사내 백오피스 서비스로 운영한다는 가정에서도 많은 수의 트래픽이 발생하지 않을 거라고 판단했습니다.
	 또한, scale-up은 쉽게 가능하며 scale-out이 꼭 필요하다면 ec2를 추가 생성하여 swarm worker 노드로 편입도 가능합니다.

	 두 번째는 운영 편리성입니다.

	 k8s는 de facto 오케스트레이션 툴로써 많이 이용하고 있지만, 작은 서비스를 구현하는데는 배보다 배꼽이 더 클 수 있다고 판단했습니다.
	 Docker swarm은 docker service update / inspect 와 같은 명령어를 통해 쉽게 애플리케이션에 대해 알 수 있고 또 업데이트할 수 있습니다.
	 로그도 docker logs -f $(docker ps -qf name=backend) 와 같이 쉽게 볼 수 있으며, 필요하다면 fluent-bit와 같은 로그 수집기를 이용할 수 있습니다.
	 더 나아가 추후 트래픽이 많아지거나 애플리케이션이 고도화될 경우, 모놀리식 서비스보다 k8s로 원활하게 migration 할 수 있다고 생각했습니다.


4. 애플리케이션은 Swarm Service 로 구성해두었기 때문에 container kill할 경우 재시작되며(docker kill -f $(docker ps -qf name=backend)), 로그 확인이 필요할 경우 docker logs -f $(docker ps -qf name=backend)과 같은 방법으로 확인 가능합니다.

5. 아래는 애플리케이션 실행에 필요한 단계입니다.

## 인프라
- aws configure를 통해 키 인증을 한 뒤, /infra 에서 terraform apply 하시면 됩니다.
- 비밀 키는 제가 임의로 생성해둔 pem를 따로 전달드리겠습니다.
- 그 후, init.sh을 이용하여 서비스합니다.

## 애플리케이션
- 처음 서비스를 시작하고 docker exec -it $(docker ps -qf name=backend) bash 에서 python3 manage.py migrate 
- docker exec -it $(docker ps -qf name=db) mysql -u root -p 로 로그인한 뒤 아래 쿼리를 실행하여 admin 팀과 계정을 생성합니다.

USE envapp;

INSERT INTO teams SET name = "admin";

INSERT INTO users 
   SET name = 'admin', password = 'admin',
       team_id = (
       SELECT id
         FROM teams
        WHERE name = 'admin');

- 그리고 필요한 팀이나 계정이 있을 경우, 프론트 페이지로 user가 속한 팀이 admin일 경우 유저 관리 페이지에서 관리할 수 있습니다.
- admin 계정이 아닐 경우, 각 팀의 환경변수 관리 페이지가 보입니다.

- 추후 새로 빌드를 해야하는 경우, 백엔드의 경우 SECRET_KEY, ALGORITHMS, DATABASES값이 포함되어있는 별도의 환경변수 파이썬 파일을 추가해야합니다.
- init.sh에서 마지막에 실행하는 docker service create에서 MYSQL_ROOT_PASSWORD, HOST_IP, ADMIN_USER, ADMIN_PASSWORD는 필수로 지정해야하며, ADMIN_USER, ADMIN_PASSWORD는 상단 쿼리 INSERT INTO users와 동일하게 구성해주시면 됩니다.

## 이용 방법
admin / admin 으로 처음 어드민 페이지로 접속가능합니다.
admin인 팀은 admin 페이지로 접속되며 유저 생성, 팀 생성, 유저 삭제가 가능합니다.

team 을 먼저 생성한 뒤, Team에 user를 생성합니다.
admin이 아닌 팀은 user 페이지로 접속되며 각 팀별 환경변수 생성, 업데이트, 삭제가 가능합니다.