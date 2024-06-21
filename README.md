# CareSync-backend

## 版本
Python >= 3.12


## 安裝

1. 設定 .env  
複製 `.env.example` 裡的內容到 `.env`  
    - Django 相關設定
        - SECRET_KEY: Django 的 SECRET_KEY，到[這裡](https://djecrety.ir/)產生一個即可
        - DEBUG: 開發時可以設為 True 方便 debug，若為正式部署則設為 False
    - Database 相關設定
        - DB_USER = 自行設置
        - DB_PASSWORD = 自行設置
        - DB_NAME = 自行設置
2. 確認已安裝 Docker
``` shell
docker --verison
```
3. 進到專案目錄
4. 啟動 Container
``` shell
docker compose up -d
```
5. 確認成功啟動
``` shell
docker compose ps

# NAME      IMAGE
# caresync  ....
# postgres  ....
```
