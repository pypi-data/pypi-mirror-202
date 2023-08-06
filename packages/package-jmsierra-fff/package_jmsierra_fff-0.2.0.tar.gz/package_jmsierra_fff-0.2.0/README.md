## Desplegar Airflow en MAC OS Local

1. Correr el siguiente comando en la terminal, para activar el entorno virtual
	```bash
	source venv/bin/activate
	```

2. Correr el siguiente comando en la terminal, para indicarle a _airflow_ donde alojar la carpeta con las configuraciones
	```bash
	export AIRFLOW_HOME=~/airflow
	```

3. Correr el siguiente comando en la terminal, para actualizar _pip_
	```bash
	pip install --upgrade pip
	```

4. Correr el siguiente comando en la terminal, para instalar _airflow_
	```bash
	pip install apache-airflow
	```

5. Correr el siguiente comando en la terminal, para crear carpeta airflow
	``` bash
	airflow info
 	```

6. Correr el siguiente comando en la terminal, para crear carpeta _dags_ en la raiz del proyecto
	``` bash
	mkdir ./dags
	```

7. Abrir _airflow.cfg_, modificar y guardar:
	```python
	dags_folder = path .dags # para que airflow cargue los dags desde esta ruta
	load_example = False # para que no cargue los dags de ejemmplo.
	```

8. Correr el siguiente comando en la terminal, para para iniciar el servidor web de _airflow_. 
	``` bash
	airflow webserver
	```
    ***** _sólo la primera vez_ *****
	```bash
	airflow users create \
	--username admin \
	--password admin \
	--firstname any_name \
	--lastname any_lastname \
	--role Admin \
	--email cualquiercorreo@gmail.com 
	```

9. Correr el siguiente comando en OTRA terminal, para iniciar el planificador de _airflow_
	```bash
	airflow scheduler
	```

10. Acceder a la interfaz de usuario de _airflow_ desde un navegador web: http://localhost:8080/
####
11. Opcionales:
	```bash
	netstat -b -a -n
	 
	lsof -i :8080
	kill -9 $(lsof -t -i:8080)
		
	lsof -i :8793
	kill -9 $(lsof -t -i:8793)
	```
12. Para que el DAG funcione, las rutas _(paths)_ deben tener el **Absolute Path**