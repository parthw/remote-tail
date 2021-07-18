# remote-tail

Agent and CLI for real time sharing of log files.

## Architecture

Tail Agent is a python application which will tail the file content of the input file and send the content to kafka server.
Tail CLI is a python applicaton which consumes the file content from kafka server and show them on console.

<p align="center">
<a href="https://raw.githubusercontent.com/parthw/remote-tail/main/arch.png">
<img src="https://raw.githubusercontent.com/parthw/remote-tail/main/arch.png" alt="arch image" />
</a>
</p>

## Acceptance Criteria

1. Real time file content should be shared 👍
2. If file is rotated, then it must get truncated. Truncate case handling. 👍
3. If file is moved, the OS itself will give error saying - "Device or Resource is in use." 👍

## Installation

### Pre-requisities

1. Kafka setup is required. For local kafka setup please refer - https://kafka.apache.org/quickstart
2. Execute the following command to create remote-tail kafka topic

```
bin/kafka-topics.sh --create --topic remote-tail --bootstrap-server <Kafka-server-endpoint>:<kafka-server-port>
```

3. It is recommended to use conda or python virtual-env. To setup miniconda please refer - https://docs.conda.io/en/latest/miniconda.html

### Tail Agent and CLI Setup

1. To setup tail agent or cli please clone the repo using -

```
git clone https://github.com/parthw/remote-tail.git
cd remote-tail
make install-agent
make install-cli
```

2. Edit the configuration file of tail-agent and tail-cli in config directory.
3. To start the tail-agent please execute -

```
make start-agent
```

4. To start the cli please execute -

```
python3 tail-cli/main.py <ip address> <filename>
```

5. To execute pylint or unittests please check make help using -

```
make help
```

## Deployment of Tail Agent

### Deployment Files

1. Dockerfile.build - To execute the pylint, unittests or security tools on Tail Agent
2. Dockerfile - To build the tail-agent image
3. kuberentes-deployment.yaml - Manifest to deploy the image to kuberentes
4. Jenkinsfile - To perform the CI/CD

### Deployment

1. Setup Jenkins
2. Create a new pipeline type job and configure the jenkinsfile.
3. Click on Build.

## Further Enhancements

1. While creating topic, number partition and replication can be configured.
2. Currently, the code supports single file tail. We can enhance the multi-process setup in tail-agent to support multiple file tailing.
3. Currently, tail-cli is sending request via IP to one server, in case of multiple servers we can broadcast the messages to multiple servers. [That is needed to look into]

## Feedback

If you have suggestions, please open an issue or better yet, a pull request.

Be nice. 😄
