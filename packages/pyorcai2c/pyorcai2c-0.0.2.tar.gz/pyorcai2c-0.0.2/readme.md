# PYORCAI2C

## quickstart (ORCA DEVELOPMENT TEAM ONLY)
1. clone the repository locally
```
    git clone git@github.com:orcasemi/pyorcai2c.git
```
if you get an error about not having enough clearance to clone it please follow <a href="https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent">this tutorial</a> to setup a github ssh-key and contact orcasemi github organization to be added as a member 

2. setup and activate virtual envinroment
```
    cd pyorcai2c
    python -m venv
```

3. if you are on windows and you have never done that before you need to enable powershell to run scripts in order to activate the newly created virtual envinroment
```
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
run that from an admin elevated powershell

4. activate the virtual envinroment
```
    .\venv\Scripts\activate 
```