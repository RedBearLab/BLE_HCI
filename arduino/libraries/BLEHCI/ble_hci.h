
#ifndef BLE_H
#define BLE_H

#include "typedef.h"

bStatus_t GAP_DeviceInit( uint8 taskID, uint8 profileRole, uint8 maxScanResponses, uint8 *pIRK, uint8 *pSRK, uint32 *pSignCounter );
bStatus_t GAP_DeviceDiscoveryRequest( gapDevDiscReq_t *pParams );
bStatus_t GAP_EstablishLinkReq( gapEstLinkReq_t *pParams );
bStatus_t GATT_WriteCharValue( uint16 connHandle, attWriteReq_t *pReq, uint8 taskId );

#endif /* BLE_H */

