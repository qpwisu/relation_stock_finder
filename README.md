### 배포 
Backend, Frontend, Crawler 폴더 각각에 들어가서 dockerfile이 있는 포더에서 아래 명령어 실행해 이미지들을 빌드해 허브에 push 
docker buildx build --platform linux/amd64,linux/arm64 -t 유저명/레포 . --push  



### 서버 빌드 방법 
git clone https://github.com/qpwisu/relation_stock_finder.git
docker, docker-compose 설치 

mkdir data
# 초기 크롤링 데이터 다운
pip install gdown
gdown --id 1VXeAcmfgfhmCq34V-UA2mVViMHsSdmRa -O ./data/stock_backup.sql

vi .env 
    REACT_APP_HOST=외부IP
    SPRING_HOST=http://외부IP:3000,http://도메인:3000


docker-compose up -d  // 허브에 이미지 변경사항있을시 pull하고 up       
# 크롤러 실행, 로그 확인 
docker exec -d <crawler_container_id> sh -c 'python main.py > logfile.log 2>&1'
    docker exec -it <crawler_container_id> cat logfile.log

docker exec -it my-mysql-db mysql -u root -p



