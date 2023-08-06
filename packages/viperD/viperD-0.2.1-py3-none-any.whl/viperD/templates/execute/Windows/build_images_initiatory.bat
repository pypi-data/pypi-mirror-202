@echo off
cd ../
cd ../
cd Dockers_file
echo ================================ killing old docker processes ==============================
docker stop __viper___app_container;
docker rm __viper___app_container
@REM pause
echo ============================== building ubuntu image ======================================
cd ubuntu_image
docker image build -t ubuntu_image .
cd ../
@REM pause
echo ================================ building __viper___app image ======================================
docker build --progress=plain -f "./app_initiatory/Dockerfile" -t __viper___app .
echo ================================ building __viper___app_backup image ======================================
docker image build -f "./app_backup/Dockerfile" -t __viper___app_backup .

cd ../
cd execute
cd Windows  

echo .
echo ===================================== Completed ============================================
echo ********************************************************************************************
