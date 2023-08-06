echo "================================ killing old docker processes ==============================";
docker stop __viper___app_container;
docker rm __viper___app_container;
echo "================================= running container ==========================================";
cd "../";
cd "../";
docker run -e TZ=UTC+5:30 -d --restart=always --workdir="/__viper__/code_mount" -v "$(pwd)/code_mount":"/__viper__/code_mount" -v "$(pwd)/data_mount":"/__viper__/data_mount" -p 5000:5000 --name __viper___app_container __viper___app "conda" "run" "-n" "__viper__" "gunicorn" "-w" "1" "-b" "0.0.0.0:5000" "app:app";
cd execute;
cd Linux;