# Simple mqtt django

Esta aplicación es un manejador de conexiones MQTT.  Tiene un menu que permite agregar conexiones, borrar, editar y actualizar.  

Cada conexión tiene la opción de conectarse a la configuración especifica y consultar valores en tiempo real desde el broker configurado. (EN PROGRESO)

Para poder manejar conexiones es necesario estar registrado y logeado.



## Iniciar aplicación

cd /myenv

source bin/activate

python manage.py migrate

mython manage.py runserver
