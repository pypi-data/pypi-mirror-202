cd "../"; 
cd "../";
cd "Dockers_file"; 
echo "==================================== killing old docker processes =========================================";
docker stop __viper___app_container;
docker rm __viper___app_container;
# pause
echo "======================================== building ubuntu image ===========================================";
cd "ubuntu_image";
docker image build -t ubuntu_image .;
cd "..";
# pause
echo "=================================== building __viper___app image ==========================================";
docker build --progress=plain -f "./app_initiatory/Dockerfile" -t __viper___app .;
# pause
echo "================================ building __viper___app_backup image =====================================";
docker image build -f "./app_backup/Dockerfile" -t __viper___app_backup .;
# pause
# echo ===================================== building nginx ============================================

echo *;
cd .. ;
cd "execute" ;
cd "Linux";
echo *;
echo "============================================== Completed ================================================";
echo ********************************************************************************************;