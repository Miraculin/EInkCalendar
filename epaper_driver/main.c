#include "../lib/Config/DEV_Config.h"
#include "paint_display.h"
#include "../lib/GUI/GUI_BMPfile.h"

#include <stdlib.h>     
#include <signal.h>

//Change to match VCOM of display
UWORD VCOM = 1420;

IT8951_Dev_Info Dev_Info = {0, 0};
UWORD Panel_Width;
UWORD Panel_Height;
UDOUBLE Init_Target_Memory_Addr;
					
void  Handler(int signo){
    Debug("\nHandler:exit\n");
    if(Refresh_Frame_Buf != NULL){
        free(Refresh_Frame_Buf);
        Debug("free Refresh_Frame_Buf\n");
        Refresh_Frame_Buf = NULL;
    }
    if(bmp_src_buf != NULL){
        free(bmp_src_buf);
        Debug("free bmp_src_buf\n");
        bmp_src_buf = NULL;
    }
    if(bmp_dst_buf != NULL){
        free(bmp_dst_buf);
        Debug("free bmp_dst_buf\n");
        bmp_dst_buf = NULL;
    }
	if(Dev_Info.Panel_W != 0){
		Debug("Going to sleep\n");
		EPD_IT8951_Sleep();
	}
    DEV_Module_Exit();
    exit(0);
}


int main(int argc, char *argv[])
{
    //Exception handling:ctrl + c
    signal(SIGINT, Handler);

    //Init the BCM2835 Device
    if(DEV_Module_Init()!=0){
        return -1;
    }
    
    if (argc < 2){
        Debug("Missing mode 0: clear display, 1: (re-)paint image ; Usage: ./epaper_display <0|1> <filename.bmp>\n");
        return -1;
    }

    if (argc < 3){
        Debug("Missing filename; Usage: ./epaper_display 1 <filename.bmp>\n");
        return -1;
    }

    int mode = 0;
    sscanf(argv[1],"%d", &mode);
    char* filepath = argv[2];
    
    Debug("VCOM value:%d\n", VCOM);
    Dev_Info = EPD_IT8951_Init(VCOM);

    //get some important info from Dev_Info structure
    Panel_Width = Dev_Info.Panel_W;
    Panel_Height = Dev_Info.Panel_H;
    Init_Target_Memory_Addr = Dev_Info.Memory_Addr_L | (Dev_Info.Memory_Addr_H << 16);
    
    //10.3inch e-Paper HAT(1872,1404)
    A2_Mode = 6;
    Debug("A2 Mode:%d\n", A2_Mode);

	EPD_IT8951_Clear_Refresh(Dev_Info, Init_Target_Memory_Addr, INIT_Mode);

    //Show a bmp file
    //1bp use A2 mode by default, before used it, refresh the screen with WHITE
    if (mode == 0){
        EPD_IT8951_Clear_Refresh(Dev_Info, Init_Target_Memory_Addr, INIT_Mode);
    } else {
        PaintBitMap(Panel_Width, Panel_Height, Init_Target_Memory_Addr, filepath);
    }
    //EPD_IT8951_Standby();
    EPD_IT8951_Sleep();

    //In case RPI is transmitting image in no hold mode, which requires at most 10s
    DEV_Delay_ms(5000);

    DEV_Module_Exit();
    return 0;
}
