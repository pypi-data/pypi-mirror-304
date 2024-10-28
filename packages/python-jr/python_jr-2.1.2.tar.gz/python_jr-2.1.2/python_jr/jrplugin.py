"""
This module implements the basic classes for a plugin that can be run in the JR plugin system.
"""
import abc
import sys
import logging
from concurrent import futures
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from io import StringIO
import grpc
from . import producer_pb2_grpc
from . import grpc_controller_pb2
from . import grpc_controller_pb2_grpc
from . import grpc_stdio_pb2_grpc
from . import grpc_stdio_pb2


from grpc_health.v1.health import HealthServicer
from grpc_health.v1 import health_pb2, health_pb2_grpc


class Logger:
    """
    Custom logger to handle logging in the plugin process.
    """
    def __init__(self,
                 logging_level=logging.ERROR,
                 log_format='%(asctime)s %(levelname)s  %(name)s %(pathname)s:%(lineno)d - %(message)s'):
        """
        Initialize the logger with the given logging level and format.
        """
        self.stream = StringIO()
        que = Queue(-1)
        self.queue_handler = QueueHandler(que)
        self.handler = logging.StreamHandler()
        self.listener = QueueListener(que, self.handler)
        self.log = logging.getLogger('jrplugin')
        self.log.setLevel(logging_level)
        self.log_formatter = logging.Formatter(log_format)
        self.handler.setFormatter(self.log_formatter)
        for handler in self.log.handlers:
            self.log.removeHandler(handler)
        self.log.addHandler(self.queue_handler)
        self.listener.start()

    def __del__(self):
        """
        Remove the handler and stop the listener.
        """
        self.listener.stop()

    def read(self):
        """
        Read the log from the listener queue and return it.
        """
        self.handler.flush()
        ret = self.log_formatter.format(self.listener.queue.get()) + "\n"
        return ret.encode("utf-8")


class GRPCController(grpc_controller_pb2_grpc.GRPCControllerServicer):
    """
    GRPController is  a controller that can be used to shutdown the plugin process.
    """
    def __init__(self, _logger, health, server):
        """
        Initialize the controller with the logger and the server.
        """
        self.logger = _logger
        self.server = server
        self.health = health

    def Shutdown(self, request, context):
        """
        Execute what ever needs to be done to clean up and exit the plugin process gracefully
        """
        self.logger.log.debug("shutting down jr plugin grpc server")
        self.health.enter_graceful_shutdown()
        self.server.stop(1)
        self.logger.log.debug("stopped jr plugin grpc server")
        return grpc_controller_pb2.Empty()


class GRPCStdioServicer(object):
    """
    GRPCStdio is a service that is automatically run by the plugin process
    to stream any stdout/err data so that it can be mirrored on the plugin
    host side.
    """
    def __init__(self, _logger):
        self.logger = _logger

    def StreamStdio(self, request, context):
        """
        StreamStdio returns a stream that contains all the stdout/stderr.
        This RPC endpoint must only be called ONCE. Once stdio data is consumed
        it is not sent again.

        Callers should connect early to prevent blocking on the plugin process.
        """
        while True:
            sd = grpc_stdio_pb2.StdioData(channel=1, data=self.logger.read())
            yield sd


def serve(producer, logger):
    """
    Starts the GRPC server
    """
    health = HealthServicer()
    health.set("plugin", health_pb2.HealthCheckResponse.ServingStatus.Value('SERVING'))

    # Start the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    producer_pb2_grpc.add_ProducerServicer_to_server(producer, server)
    grpc_controller_pb2_grpc.add_GRPCControllerServicer_to_server(GRPCController(logger, health, server), server)
    grpc_stdio_pb2_grpc.add_GRPCStdioServicer_to_server(GRPCStdioServicer(logger), server)
    health_pb2_grpc.add_HealthServicer_to_server(health, server)
    server.add_insecure_port('127.0.0.1:1234')
    server.start()
    # Output information
    print("1|1|tcp|127.0.0.1:1234|grpc")
    sys.stdout.flush()
    server.wait_for_termination()



class JRProducer(producer_pb2_grpc.ProducerServicer):
    """
    Abstract class for a producer
    """
    @abc.abstractmethod
    def Produce(self, request, context):
        pass
