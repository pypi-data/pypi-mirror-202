## PyIMCtrans

This tool reads the IMC schema from a XML file, locally creates files containing the messages and connects (imports) the main global machinery.

See `/example` to check an example implementation of the Follow Reference maneuver.

### End-User
- Fancying a virtual env? (Not needed. Just in case you want to isolate it from your python setup)
```shell
$ sudo apt install python3.8-venv
$ python3 -m venv tutorial_env
$ source tutorial_env/bin/activate
```
- To use:
```shell
$ pip3 install pyimclsts
$ # or, if you are cloning the repo, from the folder pyproject.toml is located:
$ pip3 install .
```
- Choose a folder and have a version of the IMC schema. Otherwise, it will fetch the latest IMC version from the LSTS git repository. Extract messages locally, with:
```shell
$ python3 -m pyimclsts.extract
```
Check how to provide a black- or whitelist using:
```shell
$ python3 -m pyimclsts.extract --help
```
This will locally extract the IMC.xml as python classes. You will see a folder called `pyimc_generated` which contains base messages, bitfields and enumerations from the IMC.xml file. They can be locally loaded using, for example:
```python
import pyimc_generated as pg
```
In the top-level module, you will find some functions to allow you to connect to a vehicle and subscribe to messages, namely, a subscriber class.
```python
import pyimclsts.network as n

conn = n.tcp_interface('localhost', 6006)
sub = n.subscriber(conn)

# for example:
sub.subscribe_async(myfunction, pg.messages.Announce)
```
Check `/example` for further details.

### Change log:
#### Version 0.1.1.4
    - Fix extract logic bug

#### Version 0.1.1.3

    - Hide imports and variables of core.py
    - Move IO interface classes to core.py
    - Implement .block_outgoing() through an injected dependency in the message bus
    - Improve subscriber class:
        - Exits when Abort message is received
        - Queries Entity List when started
        - Tracks src and src_ent and their corresponding names
        - Removed .subscribe_all
            - Same functionality can be achieved with .subscribe_async()
    