@echo off


cd ../
cd ../

cd Dockers_file

echo . 
echo ================================ killing old docker processes ==============================
echo .  

@REM docker stop (docker ps -f name=kec_flask_app -q)
@REM docker stop $(docker ps -f name=private-kec-autocal -q)

@REM FOR /f "tokens=*" %i IN ('docker ps -f name=kec_flask_app -q') DO docker stop %i
@REM FOR /f "tokens=*" %i IN ('docker ps -f name=private-kec-autocal -q') DO docker stop %i

@REM FOR /f "tokens=*" %%i IN ("docker ps -f name=kec_flask_app -q") DO docker stop %%i
@REM FOR /f "tokens=*" %%i IN ("docker ps -f name=private-kec-autocal -q") DO docker stop %%i

docker rm -f kec_flask_app
docker rm -f private-kec-autocal


@REM pause

echo .  
echo ============================== building ubuntu image ======================================
echo .
cd ubuntu_image
docker image build -t ubuntu_image .
cd ../


@REM pause

echo . 
echo ================================ building kec_flask_app image ======================================
echo . 
@REM cd kec_flask_app

docker build --progress=plain -f "./kec_flask_app_initiatory/Dockerfile" -t kec_flask_app .

@REM cd ../


@REM pause

echo .

echo ================================ building kec_flask_app_backup image ======================================
echo . 


docker image build -f "./kec_flask_app_backup/Dockerfile" -t kec_flask_app_backup .


@REM pause

echo .  



@REM echo ===================================== building nginx ============================================
@REM echo . 
@REM cd nginx
@REM @REM docker image build -t flask_nginx .
@REM cd ../

@REM pause

cd ../

cd execute
cd Windows  

echo .
echo .
echo ===================================== Completed ============================================
echo ********************************************************************************************
