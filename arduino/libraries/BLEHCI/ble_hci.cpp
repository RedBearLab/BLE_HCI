
#include "typedef.h"
#include "ble_hci.h"
#include <SoftwareSerial.h>

bStatus_t GAP_DeviceInit( uint8 taskID, uint8 profileRole, uint8 maxScanResponses, uint8 *pIRK, uint8 *pSRK, uint32 *pSignCounter )
{
  uint8 buf[42];
  uint8 len = 0;
    
  buf[len++] = 0x01;                  // -Type    : 0x01 (Command)
  buf[len++] = 0x00;                  // -Opcode  : 0xFE00 (GAP_DeviceInit)
  buf[len++] = 0xFE;
  
  buf[len++] = 0x26;                  // -Data Length
  buf[len++] = profileRole;           //  Profile Role
  buf[len++] = maxScanResponses;      //  MaxScanRsps
  memcpy(&buf[len], pIRK, 16);        //  IRK
  len += 16;
  memcpy(&buf[len], pSRK, 16);        //  SRK
  len += 16;
  memcpy(&buf[len], pSignCounter, 4); //  SignCounter
  len += 4;

  Serial1.write(buf, len);
  return 1;
}

bStatus_t GAP_DeviceDiscoveryRequest( gapDevDiscReq_t *pParams )
{
  uint8 buf[20];
  uint8 len = 0;
    
  buf[len++] = 0x01;                  // -Type    : 0x01 (Command)
  buf[len++] = 0x04;                  // -Opcode  : 0xFE04 (GAP_DeviceDiscoveryRequest)
  buf[len++] = 0xFE;
    
  buf[len++] = 0x03;                 // -Data Length
  buf[len++] = pParams->mode;        //  Mode
  buf[len++] = pParams->activeScan;  //  ActiveScan
  buf[len++] = pParams->whiteList;   //  WhiteList
  
//  hci_tl_write(buf, len);
//  hci_tl_wait_for_response();
  
  Serial1.write(buf, len);
  return 1;
}

bStatus_t GAP_EstablishLinkReq( gapEstLinkReq_t *pParams )
{
  uint8 buf[20];
  uint8 len = 0;
    
  buf[len++] = 0x01;
  memcpy(&buf[len], "\x09\xFE", 2);
  len += 2;
  
  buf[len++] = 0x03 + B_ADDR_LEN;
  
  buf[len++] = pParams->highDutyCycle;
  buf[len++] = pParams->whiteList;    
  buf[len++] = pParams->addrTypePeer;
  memcpy(&buf[len], pParams->peerAddr, B_ADDR_LEN);
  len+=B_ADDR_LEN;

  Serial1.write(buf, len);
  return 1;
}

bStatus_t GATT_WriteCharValue( uint16 connHandle, attWriteReq_t *pReq, uint8 taskId )
{
  uint8 buf[20];
  uint8 len = 0;
  
  buf[len++] = 0x01;
  memcpy(&buf[len], "\x92\xFD", 2);
  len += 2;
  
  buf[len++] = 0x04 + pReq->len;
  
  memcpy(&buf[len], &connHandle, 2);
  len += 2;
  memcpy(&buf[len], &pReq->handle, 2);
  len += 2;
  memcpy(&buf[len], pReq->value, pReq->len);
  len += pReq->len;
  
  Serial1.write(buf, len);
  return 1;
}

/*
bStatus_t GAP_TerminateLinkReq( uint8 taskID, uint16 connectionHandle )
{
}
*/


