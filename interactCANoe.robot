*** Settings ***
Library        CANoeLib
Suite Teardown    Close All


*** Variables ***
${ENV_VAR_NAME_TEMP_ZL}    P_FSG_2_0_0_16_1
${ENV_VAR_NAME_TEMP_ZL_VALUE}    180

${ENV_VAR_NAME_TEMP_ZR}    P_FSG_2_0_0_17_1
${ENV_VAR_NAME_TEMP_ZR_VALUE}    100

${CONFIG_PATH}    C:\\CAN_Simulation\\SIM\\MIB2p_Audi_MLBevo2\\MIB2p_Audi_MLBevo2.cfg
*** Keywords ***
Open Canoe Configuration
    Open Can
    Load Configuration    ${CONFIG_PATH}
    Start Measurement
    sleep  30s


Set Temperature Zone Left
    ${result} =  set canoe environment variable  ${ENV_VAR_NAME_TEMP_ZL}   ${ENV_VAR_NAME_TEMP_ZL_VALUE}
    should be equal as integers  ${result}  ${ENV_VAR_NAME_TEMP_ZL_VALUE}

Set Temperature Zone Right
    ${result} =  set canoe environment variable  ${ENV_VAR_NAME_TEMP_ZR}  ${ENV_VAR_NAME_TEMP_ZR_VALUE}
    should be equal as integers  ${result}  ${ENV_VAR_NAME_TEMP_ZR_VALUE}

Read Temperature Zone Left
    ${result}=  get canoe environment variable   ${ENV_VAR_NAME_TEMP_ZL}
    should be equal as integers  ${result}  ${result}

Read Temperature Zone Right
    ${result}=  get canoe environment variable   ${ENV_VAR_NAME_TEMP_ZR}
    should be equal as integers  ${result}  ${result}

Close All
    Stop Measurement
    sleep  10s
    Close Can

*** Test Cases ***
Test to Open Canoe Configuration
    Open Canoe Configuration

Test to Set Temperature Zone Left
    Set Temperature Zone Left
    sleep  1s

Test to Set Temperature Zone Right
    Set Temperature Zone Right
    sleep  1s

Test to Read Temperature Zone Left
    Read Temperature Zone Left
    sleep  1s

Test to Read Temperature Zone Right
    Read Temperature Zone Right
    sleep  1s





