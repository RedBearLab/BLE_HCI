
#ifndef TYPEDEF_H
#define TYPEDEF_H

#include "Arduino.h"

/* ------------------------------------------------------------------------------------------------
 *                                        Standard Defines
 * ------------------------------------------------------------------------------------------------
 */
#ifndef TRUE
#define TRUE 1
#endif

#ifndef FALSE
#define FALSE 0
#endif

#ifndef NULL
#define NULL 0
#endif

#define BUILD_UINT32(Byte0, Byte1, Byte2, Byte3) \
          ((uint32)((uint32)((Byte0) & 0x00FF) \
          + ((uint32)((Byte1) & 0x00FF) << 8) \
          + ((uint32)((Byte2) & 0x00FF) << 16) \
          + ((uint32)((Byte3) & 0x00FF) << 24)))

#define BUILD_UINT16(loByte, hiByte) \
          ((uint16)(((loByte) & 0x00FF) + (((hiByte) & 0x00FF) << 8)))

#define HI_UINT16(a) (((a) >> 8) & 0xFF)
#define LO_UINT16(a) ((a) & 0xFF)

#define BUILD_UINT8(hiByte, loByte) \
          ((uint8)(((loByte) & 0x0F) + (((hiByte) & 0x0F) << 4)))

#define HI_UINT8(a) (((a) >> 4) & 0x0F)
#define LO_UINT8(a) ((a) & 0x0F)

/** @defgroup GAP_DEVDISC_MODE_DEFINES GAP Device Discovery Modes
 * @{
 */
#define DEVDISC_MODE_NONDISCOVERABLE  0x00    //!< No discoverable setting
#define DEVDISC_MODE_GENERAL          0x01    //!< General Discoverable devices
#define DEVDISC_MODE_LIMITED          0x02    //!< Limited Discoverable devices
#define DEVDISC_MODE_ALL              0x03    //!< Not filtered
/** @} End GAP_DEVDISC_MODE_DEFINES */

/** @defgroup GAP_PROFILE_ROLE_DEFINES GAP Profile Roles
 * Bit mask values
 * @{
 */
#define GAP_PROFILE_BROADCASTER   0x01 //!< A device that sends advertising events only.
#define GAP_PROFILE_OBSERVER      0x02 //!< A device that receives advertising events only.
#define GAP_PROFILE_PERIPHERAL    0x04 //!< A device that accepts the establishment of an LE physical link using the connection establishment procedure
#define GAP_PROFILE_CENTRAL       0x08 //!< A device that supports the Central role initiates the establishment of a physical connection
/** @} End GAP_PROFILE_ROLE_DEFINES */

//! Default key length
#define KEYLEN                                    16

#define B_ADDR_LEN                                6 

// Minimum supported information payload for the Basic information frame (B-frame)
#define L2CAP_MTU_SIZE                   23

// The Exchanging MTU Size is defined as the maximum size of any packet 
// transmitted between a client and a server. A higher layer specification
// defines the default ATT MTU value. The ATT MTU value should be within
// the range 23 to 517 inclusive.
#define ATT_MTU_SIZE                     L2CAP_MTU_SIZE //!< Minimum ATT MTU size
#define ATT_MAX_MTU_SIZE                 517            //!< Maximum ATT MTU size

// Size of 16-bit Bluetooth UUID
#define ATT_BT_UUID_SIZE                 2
  
// Size of 128-bit UUID
#define ATT_UUID_SIZE                    16

typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;

typedef uint8 Status_t;
typedef Status_t bStatus_t;

/**
 * Type of device discovery (Scan) to perform.
 */
typedef struct
{
  uint8 taskID;       //!< Requesting App's Task ID, used to return results
  uint8 mode;         //!< Discovery Mode: @ref GAP_DEVDISC_MODE_DEFINES
  uint8 activeScan;   //!< TRUE for active scanning
  uint8 whiteList;    //!< TRUE to only allow advertisements from devices in the white list.
} gapDevDiscReq_t;

/**
 * Establish Link Request parameters
 */
typedef struct
{
  uint8 taskID;               //!< Requesting App/Profile's Task ID
  uint8 highDutyCycle;        //!< TRUE to high duty cycle scan, FALSE if not.
  uint8 whiteList;            //!< Determines use of the white list: @ref GAP_WHITELIST_DEFINES
  uint8 addrTypePeer;         //!< Address type of the advertiser: @ref GAP_ADDR_TYPE_DEFINES
  uint8 peerAddr[B_ADDR_LEN]; //!< Advertiser's address
} gapEstLinkReq_t;

/**
 * Attribute Type format (2 or 16 octet UUID).
 */
typedef struct
{
  uint8 len;                 //!< Length of UUID
  uint8 uuid[ATT_UUID_SIZE]; //!< 16 or 128 bit UUID
} attAttrType_t;

/**
 * Read By Type Request format.
 */
typedef struct
{
  uint16 startHandle; //!< First requested handle number (must be first field)
  uint16 endHandle;   //!< Last requested handle number
  attAttrType_t type; //!< Requested type (2 or 16 octet UUID)
} attReadByTypeReq_t;

/**
 * Write Request format.
 */
typedef struct
{
  uint16 handle;               //!< Handle of the attribute to be written (must be first field)
  uint8 len;                   //!< Length of value
  uint8 value[ATT_MTU_SIZE-3]; //!< Value of the attribute to be written
  uint8 sig;                   //!< Authentication Signature status (not included (0), valid (1), invalid (2))
  uint8 cmd;                   //!< Command Flag
} attWriteReq_t;

#endif /* TYPEDEF_H */

