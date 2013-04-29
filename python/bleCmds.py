
class BLECommands:
  def GAP_DeviceInit( taskID, profileRole, maxScanResponses, irk, srk, signCounter ):
    buf = '\x01'                       # -Type    : 0x01 (Command)
    buf = buf + '\x00'                 # -Opcode  : 0xFE00 (GAP_DeviceInit)
    buf = buf + '\xFE'

    buf = buf + '\x26'                 # -Data Length
    buf = profileRole                  #  Profile Role
    buf = maxScanResponses             #  MaxScanRsps
    buf = buf + irk                    #
    buf = buf + srk                    #
    buf = buf + signCounter            #

    Serial.write(buf)

    # ToDo: here should wait for command status
    return TRUE

