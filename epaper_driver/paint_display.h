#include "../lib/e-Paper/EPD_IT8951.h"
#include "../lib/Config/DEV_Config.h"

//For all refresh fram buf except touch panel
extern UBYTE *Refresh_Frame_Buf;

UBYTE PaintBitMap(UWORD Panel_Width, UWORD Panel_Height, UDOUBLE Init_Target_Memory_Addr, char* filepath);
