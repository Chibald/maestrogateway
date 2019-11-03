# Maestro
 Pilotage des poeles équipés de la technologie Maestro.
 
 Pré-requis :
 ------------
* [Python](http://www.python.org) (3+)
* [Paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [Websocket](https://pypi.org/project/websocket_client/)
	
Installation :
--------------

Pour une installation normale et un essai de lancemend en console :
```sh
git clone https://github.com/Anthony-55/maestro.git
cd maestro
sudo bash install
```
Pour une installation et utilisation en daemon :
```sh
git clone https://github.com/Anthony-55/maestro.git
cd maestro
sudo bash install_daemon
```

Pour démarrer le daemon : :
```sh
sudo systemctl start maestro.service
```

Pour activer le lancement automatique au démarrage du RPI :
```sh
sudo systemctl enable maestro.service
```

Mise à jour :
-------------

```sh
cd maestro
git pull
sudo bash update_daemon
```

