SENSOR=["28-1111111111111"]              # Name of directory in the /sys/bus/w1/devices folder
SENSORPATH="/sys/bus/w1/devices"        # Directory sensor is located in
SUFFIX="w1_slave"                       # File name for sensor

CLIENT_ID="xxxxxxx"                  # Name of the client create in AWS-IoT
ENDPOINT="xxxxxxxxxxxxxxx"   # Endpoing created in AWS-IoT
PATH_TO_CERT="certs/device.pem.crt"     # The cert file created in AWS-IoT
PATH_TO_KEY="certs/private.pem.key"     # The private key file created in AWS-IoT
PATH_TO_ROOT="certs/AmazonRootCA1.pem"  # The AWS Root CA file available here: https://www.amazontrust.com/repository/AmazonRootCA1.pem
TOPIC="iot/temperature"                 # Topic created in AWS-IoT
