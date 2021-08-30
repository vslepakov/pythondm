# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import sys
import asyncio
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse


async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception(
                "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version)
        print("IoT Hub Client for Python")

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # Define behavior for receiving methods
        async def method_handler(method_request):
            if method_request.name == "get_data":
                print("Received request for data")
                method_response = MethodResponse.create_from_method_request(
                    method_request, 200, "some data"
                )
                await module_client.send_method_response(method_response)
            else:
                print("Unknown method request received: {}".format(
                    method_request.name))
                method_response = MethodResponse.create_from_method_request(
                    method_request, 400, None)
                await module_client.send_method_response(method_response)

        def state_machine():
            while True:
                print("In state Initializing...")
                time.sleep(3)
                print("In state Downloading...")
                time.sleep(4)
                print("In state Downloaded")
                time.sleep(2)
                print("Doing some ML stuff...")
                time.sleep(4)

                # define some break condition...

        module_client.on_method_request_received = method_handler

        # Run the state machine in the event loop
        loop = asyncio.get_event_loop()
        finished = loop.run_in_executor(None, state_machine)

        # Wait for user to indicate they are done listening for messages
        await finished

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print("Unexpected error %s " % e)
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    # If using Python 3.7 or above, you can use following code instead:
    # asyncio.run(main())
