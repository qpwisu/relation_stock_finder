#!/bin/bash

# 파라미터 체크
if [ "$#" -ne 2 ]; then
    echo "사용법: $0 FILEID FILENAME"
    exit 1
fi

FILEID=$1
FILENAME=$2
COOKIES=~/cookies.txt

# 구글 드라이브에서 대용량 파일 다운로드
wget --load-cookies $COOKIES "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies $COOKIES --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id='${FILEID} -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=${FILEID}" -O ${FILENAME} && rm -rf $COOKIES

