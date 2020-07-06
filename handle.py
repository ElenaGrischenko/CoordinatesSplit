from borneo import NoSQLHandle, NoSQLHandleConfig
from borneo.kv import StoreAccessTokenProvider
from parameters import endpoint


def get_handle():
    """
    Constructs a NoSQLHandle. Additional configuration options can be added
    here. Use the tenant_id as the default compartment for all operations. This
    puts tables in the root compartment of the tenancy.
    """
    provider = StoreAccessTokenProvider()
    config = NoSQLHandleConfig(endpoint)
    config.set_authorization_provider(provider)
    return NoSQLHandle(config)
