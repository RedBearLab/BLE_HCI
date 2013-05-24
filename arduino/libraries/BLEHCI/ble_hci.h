
#ifndef BLE_H
#define BLE_H

#include "typedef.h"

#if defined(__AVR_ATmega328P__)
#include <AltSoftSerial.h>
uint8 ble_hci_init(AltSoftSerial *ser);
#else
uint8 ble_hci_init();
#endif

bStatus_t GAP_DeviceInit( uint8 taskID, uint8 profileRole, uint8 maxScanResponses, uint8 *pIRK, uint8 *pSRK, uint32 *pSignCounter );
bStatus_t GAP_DeviceDiscoveryRequest( gapDevDiscReq_t *pParams );
bStatus_t GAP_EstablishLinkReq( gapEstLinkReq_t *pParams );
bStatus_t GATT_WriteCharValue( uint16 connHandle, attWriteReq_t *pReq, uint8 taskId );
bStatus_t GATT_WriteNoRsp( uint16 connHandle, attWriteReq_t *pReq, uint8 taskId );

#endif /* BLE_H */

