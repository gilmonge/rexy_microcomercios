Sistema de comercio electrónico para micro comercios
========

> __Proyecto realizado por:__
> Rexy Studios

> __Copyright (C):__
> Prohibido su distribución, todos los derechos reservados Rexy Studios

> __Última modificación__
> 20 de enero de 2021

---
Instanciamiento en servidor
--------
 1. Se crea un clon del proyecto estando vacío 
    ```sh
     $ git clone --bare microcomercios microcomercios.git
    ``` 
 2. Se sube al servidor y se crea el __post-receive__
    ```sh
     $ touch post-receive
    ``` 
 3. Se da permisos para ejecución a __post-receive__
    ```sh
     $ chmod u+x post-receive
    ``` 
 4. Se agrega repositorio del servidor a publicar
    ```sh
     $ git remote add centos ssh://root@rexystudios.com:/var/www/git_repository/microcomercios.git
    ```
---
Realizar deploy del proyecto en el servidor
--------
 1. Se comprueban los cambios a realizar
    ```sh
     $ git status
    ```
 2. Se agregan los cambios realizados
    ```sh
     $ git add -A
    ```
 3. Se realiza el commit respectivo
    ```sh
     $ git commit -m  "texto"
    ```
 4. Se realiza la carga al servidor
    ```sh
     $ git push centos produccion
    ```
---

---
Ejecutar prueba de NGrok
--------
 1. Se debe ejecutar
    ```sh
     $ ngrok http 8000
    ```