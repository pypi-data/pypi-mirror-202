##%%
#from SSOPDataBase import wMqttService 
#from SSOPDataBase import gCentralComponentDB as CC
#
## %%
#wMqttService.launchMqttService()
#
## %%
#

from SSOPDataBase.wMqttService import launchMqttService


if __name__ == '__main__':
    launchMqttService()