import time
import datetime
from azure.iot.device import IoTHubDeviceClient, MethodResponse

CONNECTION_STRING = ''

def create_client():
    # Instantiate the client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    # Define the handler for method requests
    def method_request_handler(method_request):
        if method_request.name == 'rebootDevice':
            # Reboot the device
            print('Rebooting device')
            time.sleep(20)
            print('Device rebooted')

            # Patch the reported properties
            current_time = str(datetime.datetime.now())
            reported_props = {'rebootTime': current_time}
            client.patch_twin_reported_properties(reported_props)
            print('Device twins updated with latest rebootTime')

            # Method response indicating the method request was resolved
            resp_status = 200
            resp_payload = {'Response': 'This is the response from the device'}
            method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)
        
        else:
            # Method response indicating the method request was for an unknown method
            resp_status = 404
            resp_payload = {'Response': 'Unknown method'}
            method_response = MethodResponse(method_request.request_id, resp_status, resp_payload)

        # Send the method response
        client.send_method_response(method_response)

    try:
       # Attach the handler to the client
       client.on_method_request_received = method_request_handler
    except:
        # Clean up in the event of failuer
        client.shutdown()
    return client

def main():
    print('Starting the IoT Hub')
    client = create_client()

    print('Waiting for commands, press CTRL-C to exit')
    try:
        # Wait for the program exit
        while True:
            time.sleep(1000)
    except KeyboardInterrupt:
        print('IoTHubDeviceClient sampe stopped')
    finally:
        print('Shutting down IoT Hub Client')
        client.shutdown()

if __name__ == '__main__':
    main()
