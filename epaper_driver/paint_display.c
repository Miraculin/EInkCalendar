#include "paint_display.h"

#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>

#include "../lib/e-Paper/EPD_IT8951.h"
#include "../lib/GUI/GUI_BMPfile.h"
#include "../lib/Config/Debug.h"
#include "../lib/GUI/GUI_Paint.h"


UBYTE *Refresh_Frame_Buf = NULL;

/******************************************************************************
function: PaintBitMap
parameter:
    Panel_Width: Width of the panel
    Panel_Height: Height of the panel
    Init_Target_Memory_Addr: Memory address of IT8951 target memory address
    filepath: Filepath to BMP to display
******************************************************************************/
UBYTE PaintBitMap(UWORD Panel_Width, UWORD Panel_Height, UDOUBLE Init_Target_Memory_Addr, char* filepath){

    UDOUBLE Imagesize;
    Imagesize = ((Panel_Width * 4 % 8 == 0)? (Panel_Width * 4 / 8 ): (Panel_Width * 4 / 8 + 1)) * Panel_Height;
    
    if((Refresh_Frame_Buf = (UBYTE *)malloc(Imagesize)) == NULL) {
        Debug("Failed to apply for black memory...\n");
        return -1;
    }

    Paint_NewImage(Refresh_Frame_Buf, Panel_Width, Panel_Height, 0, BLACK);
    Paint_SelectImage(Refresh_Frame_Buf);

    //Set correct EPD display mode for display
    Paint_SetRotate(ROTATE_0);
    Paint_SetMirroring(MIRROR_HORIZONTAL);
    
    Paint_SetBitsPerPixel(4);
    Paint_Clear(WHITE);

    GUI_ReadBmp(filepath, 0, 0);

    // Display on has 16 grayscale => 4 bits per pixel displays the full grayscale range
    EPD_IT8951_4bp_Refresh(Refresh_Frame_Buf, 0, 0, Panel_Width,  Panel_Height, false, Init_Target_Memory_Addr,false);
    
    if(Refresh_Frame_Buf != NULL){
        free(Refresh_Frame_Buf);
        Refresh_Frame_Buf = NULL;
    }

    DEV_Delay_ms(5000);

    return 0;
}