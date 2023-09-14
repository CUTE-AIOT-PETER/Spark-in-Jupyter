# Jupyter Hub 

## Reference

[Docker spawner 官方範例](https://github.com/jupyterhub/dockerspawner/tree/main/examples/simple)


## 架構圖

JupyterHub 共分幾個組件 :
Hub, HTTP Proxy Config.py, Authenticator, Spawners, Admin, Database

TODO...

## 使用版本

Jupyterhub 4.0.2
JupyterNotebook 4.0.2

## Usage

產生 jupyterhub + dockerspawner image

```bash
$ docker build -t jupyterhub .
```

建立 JupyterHub 專用的 docker network

```bash
docker network create jupyterhub
```

啟動 jupyterhub

```bash
docker compose up -d 
```

建立 jupyterhub 管理員 (需再 jupyterhub_config.py 參數設定管理員帳號)

```bash
$ docker exec -it jupyterhub bash
> adduser bigred
```


## jupyterhub_config.py 說明

```
c = get_config()  

c.JupyterHub.admin_users = {'bigred'} : 設定哪個 user 為管理員帳號
c.JupyterHub.hub_connect_ip = 'jupyterhub' : JupyterHub 的 IP，這邊使用 cotainer 名稱
c.JupyterHub.hub_ip = 'jupyterhub' : JupyterHub 的 IP，這邊使用 cotainer 名稱
c.JupyterHub.hub_port = 8081 : JupyterHub 的 Hub port
c.JupyterHub.port = 8000 : JupyterHub 的 Http proxy 的 Port
c.JupyterHub.spawner_class = 'docker' 
c.DockerSpawner.image='jupyter/scipy-notebook:hub-4.0.2'
c.DockerSpawner.network_name = 'jupyterhub'
```

