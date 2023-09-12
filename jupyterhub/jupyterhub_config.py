# Configuration file for jupyterhub.

c = get_config()  

c.JupyterHub.admin_users = {'bigred'}
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_port = 8081
c.JupyterHub.port = 8000
c.JupyterHub.spawner_class = 'docker'
c.DockerSpawner.image='jupyter/scipy-notebook:hub-4.0.2'
c.DockerSpawner.network_name = 'jupyterhub'
