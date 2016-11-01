from charmhelpers.core.hookenv import resource_get, log, open_port
from jujubigdata import utils
from charmhelpers.core import unitdata


class ScaleDB(object):
    """
    This class manages the ScaleDB deployment.

    :param DistConfig dist_config: The configuration container object needed.
    """
    def fetch(self):
        '''
        Get the resources from the controller.
        Returns: True if the resources are available, False if not.

        '''
        result = resource_get('scaledb-ude')
        if not result:
            log("Failed to fetch ScaleDB UDE resource")
            return False

        unitdata.kv().set("udedeb", result)
        log("ScaleDB UDE deb is {}".format(result))

        result = resource_get('scaledb-maria')
        if not result:
            log("Failed to fetch ScaleDB Maria resource")
            return False

        unitdata.kv().set("mariadeb", result)
        log("ScaleDB Maria deb is {}".format(result))

        # Usually you would open some ports so that outside cloud customers
        # would be able to reach your service.
        # https://jujucharms.com/docs/2.0/charms-exposing
        # self.open_ports()
        return True

    def deploy(self):
        '''
        Just install the two deb packages. Should throw an exception in case
        installation fails.
        '''
        udedeb = unitdata.kv().get("udedeb")
        utils.run_as('root', 'dpkg', '-i', '{}'.format(udedeb))

        mariadeb = unitdata.kv().get("mariadeb")
        utils.run_as('root', 'dpkg', '-i', '{}'.format(mariadeb))

    def open_ports(self):
        # Don't we need to open some ports?
        open_port(8080)
