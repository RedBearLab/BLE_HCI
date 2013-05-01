
#include <central.h>
#include <ble_hci.h>

// Discovey mode (limited, general, all)
#define DEFAULT_DISCOVERY_MODE                DEVDISC_MODE_ALL

// TRUE to use active scan
#define DEFAULT_DISCOVERY_ACTIVE_SCAN         TRUE

// TRUE to use white list during discovery
#define DEFAULT_DISCOVERY_WHITE_LIST          FALSE

// TRUE to use high scan duty cycle when creating link
#define DEFAULT_LINK_HIGH_DUTY_CYCLE          FALSE

// TRUE to use white list when creating link
#define DEFAULT_LINK_WHITE_LIST               FALSE

void biscuit_central_init()
{
  GAPCentralRole_StartDevice();
}

void biscuit_central_start_discovery()
{
  GAPCentralRole_StartDiscovery( DEFAULT_DISCOVERY_MODE,
                                 DEFAULT_DISCOVERY_ACTIVE_SCAN,
                                 DEFAULT_DISCOVERY_WHITE_LIST );
}
                               
void biscuit_central_connect(uint8 *address)
{
  GAPCentralRole_EstablishLink( DEFAULT_LINK_HIGH_DUTY_CYCLE,
                                DEFAULT_LINK_WHITE_LIST,
                                0, address );
}

void biscuit_central_write_bytes(uint8 *buf, uint8 len)
{
  attWriteReq_t writeReq;
  
  writeReq.handle = 0x0019;
  writeReq.len = len;
  memcpy(writeReq.value, buf, len);

  GATT_WriteCharValue( 0x0000, &writeReq, 0 );
}

void biscuit_central_enable_notification()
{
  attWriteReq_t writeReq;
  
  writeReq.handle = 0x0016;
  writeReq.len = 2;
  writeReq.value[0] = 0x01;
  writeReq.value[1] = 0x00;

  GATT_WriteCharValue( 0x0000, &writeReq, 0 );
}

