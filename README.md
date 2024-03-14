
# backend 배포
git clone https://github.com/qpwisu/relation_stock_finder.git
docker, docker-compose 설치 

# 초기 크롤링 데이터 다운로드 
https://drive.google.com/file/d/1VXeAcmfgfhmCq34V-UA2mVViMHsSdmRa/view?usp=sharing

mkdir data
# 초기 크롤링 데이터 다운
pip install gdown
gdown --id 1VXeAcmfgfhmCq34V-UA2mVViMHsSdmRa -O ./data/stock_backup.sql

docker-compose up -d        
docker exec -it my-mysql-db mysql -u root -p

