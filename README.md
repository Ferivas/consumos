# consumos
Lee los consumos de los DAA de Manta a las 16h30 de todos los días

Es necesario editar el crontab (crontab -e) añadiendo la siguiente línea

15 16 * * * /home/pi/consumos/consumos.sh

10 16 * * * /home/pi/consumos/buscanotx.sh

Para hacer ejecutable los archivo.sh hay que ejecutar el comando

chmod +x consumos.sh
chmod +x buscanotx.sh

Para probar que el archivo sea ejecutable usamos

./consumos.sh
./buscanotx.sh



