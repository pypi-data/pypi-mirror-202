echo "=================================================== killing old docker processes =========================================";
docker stop __viper___app_container;
docker rm __viper___app_container;
echo "============================================ running container ===========================================================";
cd "../";
cd "../";
docker run -e TZ=UTC+5:30 -it --workdir="/__viper__/code_mount" -v "$(pwd)/code_mount":"/__viper__/code_mount" -v "$(pwd)/data_mount":"/__viper__/data_mount" -p 5000:5000 -p 8000:8888 --name __viper___app_container __viper___app;
cd "execute";
cd "Linux";