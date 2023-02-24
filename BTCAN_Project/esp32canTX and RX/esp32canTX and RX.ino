#include "ESP32CAN.h"
#include "CAN_config.h"
#include "BluetoothSerial.h"


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#if !defined(CONFIG_BT_SPP_ENABLED)
#error Serial Bluetooth not available or not enabled. It is only available for the ESP32 chip.
#endif


BluetoothSerial SerialBT;

CAN_device_t CAN_cfg;

uint8_t ID[16];
uint8_t TxID[16];

void setup() {
    Serial.begin(115200);
    Serial.println("iotsharing.com CAN demo");
    SerialBT.begin("ESP32test"); //Bluetooth device name
    Serial.println("The device started, now you can pair it with bluetooth!");
    CAN_cfg.speed=CAN_SPEED_500KBPS;
    CAN_cfg.tx_pin_id = GPIO_NUM_4;
    CAN_cfg.rx_pin_id = GPIO_NUM_23;
    CAN_cfg.rx_queue = xQueueCreate(10,sizeof(CAN_frame_t));
    //initialize CAN Module
    ESP32Can.CANInit();
}

void loop() {
    CAN_frame_t rx_frame,tx_frame;
    //receive next CAN frame from queue
   

    if(xQueueReceive(CAN_cfg.rx_queue,&rx_frame, 3*portTICK_PERIOD_MS)==pdTRUE){

      //do stuff!
      if(rx_frame.FIR.B.FF==CAN_frame_std)
        printf("New standard frame");
      else
        printf("New extended frame");

      if(rx_frame.FIR.B.RTR==CAN_RTR)
        printf(" RTR from 0x%08x, DLC %d\r",rx_frame.MsgID,  rx_frame.FIR.B.DLC);
      else{
        printf(" from 0x%08x, DLC %d\n",rx_frame.MsgID,  rx_frame.FIR.B.DLC);
        //SerialBT.write(rx_frame.MsgID);
        /* convert to upper case and respond to sender */
        // for(int i = 0; i < 8; i++){
        //   if(rx_frame.data.u8[i] >= 'a' && rx_frame.data.u8[i] <= 'z'){
        //     rx_frame.data.u8[i] = rx_frame.data.u8[i] - 32;
        //   }
          
        //  }
          ID[0]=rx_frame.MsgID>>24&0xff;
          ID[1]=rx_frame.MsgID>>16&0xff;
          ID[2]=rx_frame.MsgID>>8&0xff;
          ID[3]=rx_frame.MsgID>>0&0xff;
          ID[4]=rx_frame.FIR.B.DLC>>0&0xff;

          for(int i = 0; i < 8; i++){
            ID[i+5] = rx_frame.data.u8[i];
          }
          
          SerialBT.write(ID,16);
          SerialBT.readBytes(TxID,16);
          tx_frame.MsgID = ((TxID[0] << 24) & 0xff000000) | ((TxID[1] << 16) & 0x00ff0000) | ((TxID[2] << 8) & 0x0000ff00) | ((TxID[3] << 0) & 0xff);
          tx_frame.FIR.B.DLC = TxID[4];
          // tx_frame.MsgID=0x00003001;
          tx_frame.FIR.B.FF=CAN_frame_ext;
          memcpy(tx_frame.data.u8,&TxID[5],8);
          printf(" TX Msg from 0x%08x, DLC %d\n",tx_frame.MsgID,  tx_frame.FIR.B.DLC);
          for (int i=0;i<14;i++)
          {
            printf("0x%x  ",TxID[i]);
          }
          printf("\r\n");
          for (int i=0;i<8;i++)
          {
            printf("0x%x  ",tx_frame.data.u8[i]);
          }
          printf("\r\n");          
          // SerialBT.write(rx_frame.FIR.B.DLC);
          // SerialBT.write(rx_frame.data.u8,rx_frame.FIR.B.DLC);
          ESP32Can.CANWriteFrame(&tx_frame);
          
           
          
          
      }
      //respond to sender
      // ESP32Can.CANWriteFrame(&tx_frame);
    }

   
    

}
