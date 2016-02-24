#simple prototype to read from string lines from a TCP socket
import socket
import time

def transferJsonStreamToTelemetry(telemetryLogger):
    #Listening Port of CANBOAT n2kd stream
    N2KD_STREAM_PORT = 2598
    #Buffer recv size
    BUFFER_RECV = 2048

    #create an INET, STREAMing socket
    s = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    #now connect to the web server on port 80
    # - the normal http port
    s.connect(("localhost", N2KD_STREAM_PORT))

    while True:
        time.sleep(.100)
        recvBuffer = s.recv(2048)
        stringBuffer = str(recvBuffer)
        #This seems a bit ditry, how do I know that I'm not going to truncate a n2k message and get a partial line
        stringBuffer = stringBuffer.split('\n')

        for logLine in stringBuffer:
            telemetryLogger.processLogLine(logLine)