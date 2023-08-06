# np_zro

### *For use on internal Allen Institute network*

[![Python
Versions](https://img.shields.io/pypi/pyversions/np_zro.svg)](https://pypi.python.org/pypi/np-zro/)


Just the `zro.Proxy` class extracted from `mpeconfig`, with `zmq` as a dependency.

## Install
```shell
python -m pip install --extra-index-url https://pypi.org/simple np_zro
```


## Basic usage

`Proxy.__getattr__` and `Proxy.__setattr__` are forwarded to remote `zmq` object:  
```python
>>> from np_zro import Proxy

>>> camstim_agent = Proxy('w10sv111814', port=5000, serialization='json') # BTVTest.1-Stim
>>> camstim_agent.mouse_id = '366122'
>>> camstim_agent.mouse_id
'366122'

```
