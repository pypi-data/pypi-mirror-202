import doctest


def test_braintv_camstim_agent():
    """
    >>> test_braintv_camstim_agent()
    """
    from np_zro import DeviceProxy as Proxy
    proxy = Proxy('w10sv111814', port=5000, serialization='json')
    assert proxy.uptime, 'Failed to query Camstim Agent on BTVTest.1-Stim'
    
    
if __name__ == '__main__':
    doctest.testmod(verbose=True) 