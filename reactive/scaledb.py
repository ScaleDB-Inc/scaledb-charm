# pylint: disable=unused-argument
from charms.reactive import when, when_not, set_state
from charmhelpers.core.hookenv import status_set
from charms.layer.scaledb import ScaleDB


# Two actions to demonstrate the state transition:
# fetch_resources sets 'scaledb.fetched'
# deploy_scaledb installs the deb packages and sets 'scaledb.deployed'
@when_not('scaledb.fetched')
def fetch_scaledb():
    status_set('maintenance', 'fetching ScaleDB')
    scaledb = ScaleDB()
    result = scaledb.fetch()
    if not result:
        status_set("blocked", "Failed to fetch ScaleDB binaries")
        return

    status_set('waiting', 'waiting for ScaleDB to deploy')
    set_state('scaledb.fetched')


@when_not('scaledb.deployed')
@when('scaledb.fetched')
def deploy_scaledb():
    status_set('maintenance', 'deploying ScaleDB')
    scaledb = ScaleDB()
    scaledb.deploy()
    status_set('active', 'ready')
    set_state('scaledb.deployed')
