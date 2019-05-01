# Builder Project:

***This source code for help deploy code from git into server with each branch a folder code***

```
Fullname: Nguyen Minh Thang
Skype: nguyenthang.93
Website: https://thangnm.info
Email:  minhthang0403@gmail.com
```

## 1. Install

* Docker
* Docker Composer

## 2. Need to setup firsts

- For GIT : put your id_rsa, id_rsa.pub => ./key folder
- For SSH EC2 or AWS: put key.pem => ./key folder
- Copy file `env.yml.sample` to `env.yml` and update the information for host you want to deploy to


## 3. Setup project

```
cd <path-to-source-code>

docker-compose up -d

or 

docker-compose.exe up -d
```

## 4. Run

- Check connection to host :

```
fab role:[ROLE] test_host

# ROLE is defined in env.yml
# ex : fab role:staging test_host
```

- Deploy with branch :

```
fab role:[ROLE] deploy:[BRANCH]

# ROLE is defined in env.yml
# ex : fab role:staging deploy:develop
```

- Delete source code for branch :

```
fab role:[ROLE] destroy:[BRANCH]

# ROLE is defined in env.yml
# ex : fab role:staging destroy:develop
```

- Deploy without execute in docker container:

```
docker-compose exec builder fab role:[ROLE] deploy:[BRANCH]

# ROLE is defined in env.yml
# ex : docker-compose exec builder fab role:staging deploy:develop
```

## 5. Link for docs

- https://docs.fabfile.org/en/1.14/tutorial.html
- https://docs.docker.com/docker-for-windows/install/
- https://docs.docker.com/compose/install/
- https://blogs.msdn.microsoft.com/stevelasker/2016/06/14/configuring-docker-for-windows-volumes/
- https://www.isunshare.com/windows-10/5-ways-to-open-local-users-and-groups-in-windows-10.html
- https://blogs.technet.microsoft.com/canitpro/2015/09/08/step-by-step-enabling-hyper-v-for-use-on-windows-10/