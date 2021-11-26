<h1 align="center"><img src="./docs/images/banner_cli.png" alt="Testing as a service"></h1>  

# Estuary CI/CD
Estuary CI/CD CLI will run your CI/CD flow and stream back the events real-time as they happen.

## Code quality
[![Maintainability](https://api.codeclimate.com/v1/badges/315fdb698ad782505c96/maintainability)](https://codeclimate.com/repos/5f8b3da35a75ce3a01000c4c/maintainability)

## Linux status
[![Build Status](https://travis-ci.com/estuaryoss/estuary-cicd.svg?token=UC9Z5nQSPmb5vK5QLpJh&branch=main)](https://travis-ci.com/estuaryoss/estuary-cicd)

## Win status
[![CircleCI](https://circleci.com/gh/estuaryoss/estuary-cicd.svg?style=svg&circle-token=cd4dd66d5683d534ca44f5a64a644720149d8578)](https://circleci.com/gh/estuaryoss/estuary-cicd)

## Steps
-  deploy [estuary-agent-java](https://github.com/estuaryoss/estuary-agent-java)  on the target machine (metal/VM/Docker/IoT device)
-  define your yaml configuration 
-  start your CI/CD flow

!Obs: Compatible with Agent version >= 4.2.4 

## Usage
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --username=admin --password=yourSecret --file="config.yaml"
```

The default endpoint is */commanddetachedyaml*. The endpoint can be overridden:
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --username=admin --password=yourSecret --endpoint=/docker/command --file="config.yaml"
```

## Params
```bash
PS > python main.py --help
Usage: main.py [OPTIONS]

Options:
  --ip TEXT        The IP/hostname of the target machine where Estuary Agent
                   is deployed
  --port TEXT      The port number of the target machine where Estuary Agent
                   is deployed
  --username TEXT  The username used for the Basic authentication
  --password TEXT  The password used for the Basic authentication
  --protocol TEXT  The protocol with which the estuary-agent was deployed.
                   Default is http. E.g. https
  --cert TEXT      The certificate with which the estuary-agent was deployed.
                   E.g. https/cert.pem
  --endpoint TEXT  The endpoint to sent the request. Default is
                   "/commandsyaml"
  --file TEXT      The yaml file path on disk. Default is "./config.yaml"
  --batch TEXT     If batch is "true", the server will execute all commands in
                   batch. If batch is "false" the commands will be executed
                   one by one and the CLI exits when the first failure is
                   detected. Default is "false"
  --help           Show this message and exit.


```

## Use cases
-  App download and installation
-  CI/CD flows
  
Support project: <a href="https://paypal.me/catalindinuta?locale.x=en_US"><img src="https://lh3.googleusercontent.com/Y2_nyEd0zJftXnlhQrWoweEvAy4RzbpDah_65JGQDKo9zCcBxHVpajYgXWFZcXdKS_o=s180-rw" height="40" width="40" align="center"></a>    
