<h1 align="center"><img src="./docs/images/banner_cli.png" alt="Testing as a service"></h1>  

Support project: <a href="https://paypal.me/catalindinuta?locale.x=en_US"><img src="https://lh3.googleusercontent.com/Y2_nyEd0zJftXnlhQrWoweEvAy4RzbpDah_65JGQDKo9zCcBxHVpajYgXWFZcXdKS_o=s180-rw" height="40" width="40" align="center"></a>    

# estuary-cicd
Estuary CI/CD CLI will run your CI/CD flow and stream back the events real-time as they happen.

## Code quality
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/086f5a66ac0841c4800dcddfdc9fb3c2)](https://www.codacy.com/gh/estuaryoss/estuary-cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=estuaryoss/estuary-cli&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/8fffe56fb66038d7fa2d/maintainability)](https://codeclimate.com/github/estuaryoss/estuary-cli/maintainability)

## Linux status
[![Build Status](https://travis-ci.org/estuaryoss/estuary-cli.svg?branch=master)](https://travis-ci.org/estuaryoss/estuary-cli)

## Win status
[![CircleCI](https://circleci.com/gh/estuaryoss/estuary-cli.svg?style=svg)](https://circleci.com/gh/estuaryoss/estuary-cli)

## Steps
-  deploy [estuary-agent](https://github.com/dinuta/estuary-agent) or [estuary-agent-java](https://github.com/dinuta/estuary-agent-java)  on the target machine (metal/VM/Docker/IoT device)
-  define your yaml configuration 
-  start your CI/CD flow

## Usage
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --cmds="dir;;-trump"
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --cmds="dir;;cat requirements.txt;;-trump"
```

The default endpoint is */command*. The endpoint can be overridden (E.g. Estuary deployer):
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --endpoint=/docker/command --cmds="dir;;cat requirements.txt;;-trump"
python .\main.py --ip=localhost --port=8080 --token=None --protocol=https --cmds="dir;;-get --args README.md;altcva.md;;-quit"
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --endpoint=/kubectl/command --cmds="dir;;cat requirements.txt;;-trump"
```

## File download and upload
CLI supports file upload and download similar to sftp transfers.

*-put --args LOCAL_PATH;REMOTE_PATH*
*-get --args REMOTE_PATH;LOCAL_PATH*

```bash
-put --args C:\Users\Dinuta\Downloads\669564.pdf;/tmp/remote/669564.pdf
-get --args /tmp/remote/669564.pdf;C:\Users\Dinuta\Downloads\669564.pdf
```

## Params
```bash
PS > python main.py --help
Usage: main.py [OPTIONS]

Options:
  --ip TEXT        The IP/hostname of the target machine where estuary-agent
                   is deployed
  --port TEXT      The port number of the target machine where estuary-agent
                   is deployed
  --token TEXT     The authentication token that will be sent via 'Token'
                   header. Use 'None' if estuary-agent is deployed unsecured
  --protocol TEXT  The protocol with which the estuary-agent was deployed.
                   Default is http. E.g. https
  --cert TEXT      The certificate with which the estuary-agent was deployed.
                   E.g. https/cert.pem
  --endpoint TEXT  The endpoint to sent the request. Default is "/command"
  --cmds TEXT      The commands to be sent separated by ";". Useful for non-
                   interactive mode.
  --help           Show this message and exit.

```

## Stateless cli example  
![image](https://user-images.githubusercontent.com/43060213/79952987-e1142f00-8483-11ea-8fdc-8bef2b7f8d2a.png)  

## Use cases
-  Remote IoT device control
-  Remote machine control
-  Remote software settings
-  Remote debugging

## Exit cli
ctrl + c  
-quit  
-trump  
  
