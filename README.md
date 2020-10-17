<h1 align="center"><img src="./docs/images/banner_cli.png" alt="Testing as a service"></h1>  

Support project: <a href="https://paypal.me/catalindinuta?locale.x=en_US"><img src="https://lh3.googleusercontent.com/Y2_nyEd0zJftXnlhQrWoweEvAy4RzbpDah_65JGQDKo9zCcBxHVpajYgXWFZcXdKS_o=s180-rw" height="40" width="40" align="center"></a>    

# estuary-cicd
Estuary CI/CD CLI will run your CI/CD flow and stream back the events real-time as they happen.

## Code quality
[![Maintainability](https://api.codeclimate.com/v1/badges/315fdb698ad782505c96/maintainability)](https://codeclimate.com/repos/5f8b3da35a75ce3a01000c4c/maintainability)

## Linux status
[![Build Status](https://travis-ci.org/estuaryoss/estuary-cicd.svg?branch=master)](https://travis-ci.org/estuaryoss/estuary-cicd)

## Win status
[![CircleCI](https://circleci.com/gh/estuaryoss/estuary-cicd.svg?style=svg)](https://circleci.com/gh/estuaryoss/estuary-cicd)

## Steps
-  deploy [estuary-agent](https://github.com/dinuta/estuary-agent) or [estuary-agent-java](https://github.com/dinuta/estuary-agent-java)  on the target machine (metal/VM/Docker/IoT device)
-  define your yaml configuration 
-  start your CI/CD flow

## Usage
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --file="config.yaml"
```

The default endpoint is */commanddetachedyaml*. The endpoint can be overridden (E.g. Estuary deployer):
```bash
python .\main.py --ip=192.168.0.10 --port=8080 --token=None --endpoint=/docker/command --file="config.yaml"
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
  --endpoint TEXT  The endpoint to sent the request. Default is
                   "/commanddetachedyaml"
  --file TEXT      The yaml file path on disk. Default is "./config.yaml"
  --help           Show this message and exit.

```

## Use cases
-  app download and installation
-  CI/CD flows
  
