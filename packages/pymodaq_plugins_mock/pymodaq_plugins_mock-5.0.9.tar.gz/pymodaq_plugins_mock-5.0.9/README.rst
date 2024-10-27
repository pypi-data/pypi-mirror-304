PyMoDAQ Plugins Mock
####################

.. image:: https://img.shields.io/pypi/v/pymodaq_plugins_mock.svg
   :target: https://pypi.org/project/pymodaq_plugins_mock/
   :alt: Latest Version

.. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
   :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_mock/workflows/Upload%20Python%20Package/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_mock

.. image:: https://github.com/PyMoDAQ/pymodaq_plugins_mock/actions/workflows/Test.yml/badge.svg
    :target: https://github.com/PyMoDAQ/pymodaq_plugins_mock/actions/workflows/Test.yml


Plugins initially developed with PyMoDAQ. Includes Mock plugins that are plugins of virtual instruments dedicated
to code testing for new functionalities or development. From version 4.0.0 onwards, these plugins will only work with
pymodaq > 4.0.0


Authors
=======

* Sebastien J. Weber

Instruments
===========
Below is the list of instruments included in this plugin

Actuators
+++++++++

* **Mock** actuator to test PyMoDAQ functionalities
* **MockTau** mock actuator with characteristic time to reach set value
* **TCP server** to communicate with other DAQ_Move or third party applications
* **LECO director** to communicate with other DAQ_Move or third party applications

Viewer0D
++++++++

* **Mock 0D** detector to test PyMoDAQ functionalities
* **Mock Adaptive** detector to test PyMoDAQ adaptive scan mode
* **TCP server** to communicate with other DAQ_Viewer or third party applications
* **LECO director** to communicate with other DAQ_Viewer or third party applications

Viewer1D
++++++++

* **Mock 1D** detector to test PyMoDAQ functionalities
* **Mock Spectro** detector to test pymodaq_spectro functionalities
* **TCP server** to communicate with other DAQ_Viewer or third party applications
* **LECO director** to communicate with other DAQ_Viewer or third party applications

Viewer2D
++++++++

* **Mock 2D** detector to test PyMoDAQ functionalities
* **TCP server** to communicate with other DAQ_Viewer or third party applications
* **LECO director** to communicate with other DAQ_Viewer or third party applications

ViewerND
++++++++

* **Mock ND** detector to test PyMoDAQ functionalities
* **LECO director** to communicate with other DAQ_Viewer or third party applications
