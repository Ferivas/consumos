# consumos
Lee los consumos de los DAA de Manta a las 16h30 de todos los días

Es necesario editar el crontab (crontab -e) añadiendo la siguiente línea

15 16 * * * /home/pi/consumos/consumos.sh

Para hacer ejecutable el archivo.sh hay que ejecutar el comando

chmod +x consumos.sh

Para probar que el archivo sea ejecutable usamos

./consumos.sh
