echo off
echo . 
echo ================================ killing old docker processes ==============================
echo .  
@REM FOR /f "tokens=*" %%i IN ('docker ps -f name=kec_flask_app -q') DO docker stop %%i
@REM FOR /f "tokens=*" %%i IN ('docker ps -f name=private-kec-autocal -q') DO docker stop %%i


docker rm -f kec_flask_app
docker rm -f private-kec-autocal


pause

echo .  
echo ============================== running container ======================================
echo .

cd ../
cd ../
docker run -e TZ=UTC+5:30 -it --workdir="/kec/code_mount" -v "%cd%\code_mount":"/kec/code_mount" -v "%cd%\data_mount":"/kec/data_mount" -p 5000:5000 --name private-kec-autocal kec_flask_app

cd execute 
cd Windows 