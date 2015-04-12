#include <Wire.h>
//#include <EEPROM.h>

static long count=0;

//plug the encoder to ping 2 and 3

//#include <ZigduinoRadio.h>

//#define RF_DEVICE_ID 0x11

//remove comment to enable local serial printing
//#define LOCALDEBUG

//int rfChannel = 11;

//int node_id;

#define BNO055_I2C_H_SLAVE_ADDR   0x29
#define BNO055_I2C_ADDR   0x28
#define BNO055_I2C_HID_SLAVE_ADDR 0x40

// BNO055 Registers
#define MAG_RADIUS_MSB 0x6A // R/W
#define MAG_RADIUS_LSB 0x69 // R/W
#define ACC_RADIUS_MSB 0x68 // R/W
#define ACC_RADIUS_LSB 0x67 // R/W

#define GYR_OFFSET_Z_MSB 0x66 // R/W
#define GYR_OFFSET_Z_LSB 0x65 // R/W
#define GYR_OFFSET_Y_MSB 0x64 // R/W
#define GYR_OFFSET_Y_LSB 0x63 // R/W 
#define GYR_OFFSET_X_MSB 0x62 // R/W
#define GYR_OFFSET_X_LSB 0x61 // R/W

#define MAG_OFFSET_Z_MSB 0x60 // R/W
#define MAG_OFFSET_Z_LSB 0x5F // R/W
#define MAG_OFFSET_Y_MSB 0x5E // R/W
#define MAG_OFFSET_Y_LSB 0x5D // R/W
#define MAG_OFFSET_X_MSB 0x5C // R/W
#define MAG_OFFSET_X_LSB 0x5B // R/W

#define ACC_OFFSET_Z_MSB 0x5A // R/W
#define ACC_OFFSET_Z_LSB 0x59 // R/W
#define ACC_OFFSET_Y_MSB 0x58 // R/W
#define ACC_OFFSET_Y_LSB 0x57 // R/W
#define ACC_OFFSET_X_MSB 0x56 // R/W
#define ACC_OFFSET_X_LSB 0x55 // R/W

// Registers 43-54 reserved for Soft Iron Calibration Matrix

#define AXIS_MAP_SIGN   0x42 // Bits0-2: R/W; Bits3-7: reserved 
#define AXIS_MAP_CONFIG 0x41 // Bits0-5: R/W; Bits6-7: reserved
#define TEMP_SOURCE     0x40 // Bits0-1: R/W; Bits2-7: reserved

#define SYS_TRIGGER 0x3F
#define PWR_MODE    0x3E
#define OPR_MODE    0x3D //default = 0x1C

// Register 3C Reserved

#define UNIT_SEL       0x3B //RO
#define SYS_ERR        0x3A //RO
#define SYS_STATUS     0x39 //RO 
#define SYS_CLK_STATUS 0x38 //RO
#define INT_STATUS     0x37	//RO
#define ST_RESULT      0x36 //RO
#define CALIB_STAT     0x35 //RO
#define TEMP           0x34 //RO

#define GRV_DATA_Z_MSB 0x33 //RO
#define GRV_DATA_Z_LSB 0x32 //RO
#define GRV_DATA_Y_MSB 0x31 //RO
#define GRV_DATA_Y_LSB 0x30 //RO
#define GRV_DATA_X_MSB 0x2F //RO
#define GRV_DATA_X_LSB 0x2E //RO

#define LIA_DATA_Z_MSB 0x2D //RO
#define LIA_DATA_Z_LSB 0x2C //RO
#define LIA_DATA_Y_MSB 0x2B //RO
#define LIA_DATA_Y_LSB 0x2A //RO
#define LIA_DATA_X_MSB 0x29 //RO
#define LIA_DATA_X_LSB 0x28 //RO

#define QUA_DATA_Z_MSB 0x27 //RO
#define QUA_DATA_Z_LSB 0x26 //RO
#define QUA_DATA_Y_MSB 0x25 //RO
#define QUA_DATA_Y_LSB 0x24 //RO
#define QUA_DATA_X_MSB 0x23 //RO
#define QUA_DATA_X_LSB 0x22 //RO
#define QUA_DATA_W_MSB 0x21 //RO
#define QUA_DATA_W_LSB 0x20 //RO

#define EUL_PITCH_MSB   0x1F //RO
#define EUL_PITCH_LSB   0x1E //RO
#define EUL_ROLL_MSB    0x1D //RO
#define EUL_ROLL_LSB    0x1C //RO
#define EUL_HEADING_MSB 0x1B //RO
#define EUL_HEADING_LSB 0x1A //RO

#define GYR_DATA_Z_MSB 0x19 //RO
#define GYR_DATA_Z_LSB 0x18 //RO
#define GYR_DATA_Y_MSB 0x17 //RO
#define GYR_DATA_Y_LSB 0x16 //RO
#define GYR_DATA_X_MSB 0x15 //RO
#define GYR_DATA_X_LSB 0x14 //RO

#define MAG_DATA_Z_MSB 0x13 //RO
#define MAG_DATA_Z_LSB 0x12 //RO
#define MAG_DATA_Y_MSB 0x11 //RO
#define MAG_DATA_Y_LSB 0x10 //RO
#define MAG_DATA_X_MSB 0x0F //RO
#define MAG_DATA_X_LSB 0x0E //RO

#define ACC_DATA_Z_MSB 0x0D //RO
#define ACC_DATA_Z_LSB 0x0C //RO
#define ACC_DATA_Y_MSB 0x0B //RO
#define ACC_DATA_Y_LSB 0x0A //RO
#define ACC_DATA_X_MSB 0x09 //RO
#define ACC_DATA_X_LSB 0x08 //RO

#define PAGE_ID       0x07 //RO
#define BL_REV_ID     0x06 //RO
#define SW_REV_ID_MSB 0x05 //RO
#define SW_REV_ID_LSB 0x04 //RO

#define GYR_ID  0x03 // RO; Default = 0x0F
#define MAG_ID  0x02 // RO; Default = 0x32
#define ACC_ID  0xFB // RO; Default = 0xFB
#define CHIP_ID 0x00 // RO; Default 0xA0

// PAGE 1 (All unreserved registers in Page 1 are READ ONLY)
// Registers 7F-60 reserved
// Registers 5F-50 are named UNIQUE_ID and are READ ONLY
// Registers 4F-20 reserved

#define GYR_AM_SET     0x1F // Default = 0x0A
#define GYR_AM_THRES   0x1E	// Default = 0x04
#define GYR_DUR_Z      0x1D	// Default = 0x19
#define GYR_HR_Z_SET   0x1C	// Default = 0x01
#define GYR_DUR_Y      0x1B	// Default = 0x19
#define GYR_HR_Y_SET   0x1A	// Default = 0x01
#define GYR_DUR_X      0x19	// Default = 0x19
#define GYR_HR_X_SET   0x18	// Default = 0x01
#define GYR_INT_SETING 0x17 // Default = 0x00

#define ACC_NM_SET       0x16 // Default = 0x0B
#define ACC_NM_THRE      0x15 // Default = 0x0A
#define ACC_HG_THRE      0x14 // Default = 0xC0
#define ACC_HG_DURATION  0x13 // Default = 0x0F
#define ACC_INT_SETTINGS 0x12 // Default = 0x03
#define ACC_AM_THRES     0x11 //Default = 0x14

#define INT_EN   0x10
#define INT_MASK 0x0F

// Register 0x0E reserved

#define GYR_SLEEP_CONFIG 0x0D 
#define ACC_SLEEP_CONFIG 0x0C
#define GYR_CONFIG_1     0x0B
#define GYR_CONFIG_0     0x0A
#define MAG_CONFIG       0x09
#define ACC_CONFIG       0x08

// PAGE_ID still mapped to 0x07
// Registers 6-0 reserved

#define PWR_MODE_SEL_BIT    0
#define PWR_MODE_SEL_LENGTH 2

#define PWR_MODE_NORMAL  0x00
#define PWR_MODE_LOW	 0x01
#define PWR_MODE_SUSPEND 0x02

#define OPR_MODE_SEL_BIT 0
#define OPR_MODE_LENGTH  4

#define OPR_MODE_CONFIG_MODE  0x00
#define OPR_MODE_ACCONLY 	  0x01
#define OPR_MODE_MAGONLY 	  0x02
#define OPR_MODE_GYROONLY 	  0x03
#define OPR_MODE_ACCMAG 	  0x04
#define OPR_MODE_ACCGYRO 	  0x05
#define OPR_MODE_MAGGYRO 	  0x06
#define OPR_MODE_AMG	 	  0x07
#define OPR_MODE_IMU	 	  0x08
#define OPR_MODE_COMPASS 	  0x09
#define OPR_MODE_M4G	 	  0x0A
#define OPR_MODE_NDOF_FMC_OFF 0x0B
#define OPR_MODE_NDOF 		  0x0C

#define DATA_RATE_SEL_BIT    4
#define DATA_RATE_SEL_LENGTH 3

#define FASTEST_MODE     0x10
#define GAME_MODE	 0x20
#define UI_MODE		 0x30
#define NORMAL_MODE      0x40

#define X_AXIS_REMAP_BIT  0
#define Y_AXIS_REMAP_BIT  2
#define Z_AXIS_REMAP_BIT  4
#define AXIS_REMAP_LENGTH 2

#define AXIS_REP_X 0x00
#define AXIS_REP_Y 0x01
#define AXIS_REP_Z 0x02

#define AXIS_SIGN_REMAP_BIT	   0
#define AXIS_SIGN_REMAP_LENGTH 3

#define ACC_RANGE_SEL_BIT	  0
#define ACC_RANGE_SEL_LENGTH  2
#define ACC_BW_SEL_BIT        2 //Auto controlled in fusion mode
#define ACC_BW_SEL_LENGTH     3 //Auto controlled in fusion mode
#define ACC_OPMODE_SEL_BIT    5 //Auto controlled in fusion mode
#define ACC_OPMODE_SEL_LENGTH 3 //Auto controlled in fusion mode

#define ACC_RANGE_2G  0x00
#define ACC_RANGE_4G  0x01 // Default
#define ACC_RANGE_8G  0x02
#define ACC_RANGE_16G 0x03

#define GYR_RANGE_SEL_BIT	  0 //Auto controlled in fusion mode
#define GYR_RANGE_SEL_LENGTH  3 //Auto controlled in fusion mode
#define GYR_BW_SEL_BIT        3 //Auto controlled in fusion mode
#define GYR_BW_SEL_LENGTH     3 //Auto controlled in fusion mode
#define GYR_OPMODE_SEL_BIT    6 //Auto controlled in fusion mode
#define GYR_OPMODE_SEL_LENGTH 2 //Auto controlled in fusion mode

#define MAG_RANGE_SEL_BIT	  0 //Auto controlled in fusion mode
#define MAG_RANGE_SEL_LENGTH  3 //Auto controlled in fusion mode
#define MAG_BW_SEL_BIT        3 //Auto controlled in fusion mode
#define MAG_BW_SEL_LENGTH     2 //Auto controlled in fusion mode
#define MAG_OPMODE_SEL_BIT    5 //Auto controlled in fusion mode
#define MAG_OPMODE_SEL_LENGTH 2 //Auto controlled in fusion mode

#define ACC_UNIT_SEL_BIT          0
#define ANGULAR_RATE_UNIT_SEL_BIT 1
#define EULER_ANGLE_UNIT_SEL_BIT  2
#define TEMP_UNIT_SEL_BIT         4
#define UNIT_SEL_LENGTH           1

#define ACC_UNIT_M_SSQ        0
#define ACC_UNIT_MG           1
#define ANGULAR_RATE_UNIT_DPS 0
#define ANGULAR_RATE_UNIT_RPS 1
#define EULER_ANGLE_UNIT_DEG  0
#define EULER_ANGLE_UNIT_RAD  1
#define TEMP_UNIT_C           0
#define TEMP_UNIT_F           1



void setup()
{
  // Initialize the Serial Bus for printing data.
  Serial.begin(115200);
  
  /* Setup encoder pins as inputs */
  attachInterrupt(0, enc_isr, CHANGE);
  
//  RF.begin(11);
 // RF.setParam(RP_TXPWR(3));
 // RF.setParam(RP_DATARATE(MOD_OQPSK_1000));
//  RF.attachError(errHandle);
/*
  pinMode(35,OUTPUT);
  digitalWrite(35,HIGH);
  pinMode(3,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  analogWrite(3,254);
  analogWrite(5,254);
  analogWrite(6,254);
  */

  // Initialize the 'Wire' class for the I2C-bus.
  Wire.begin();//OnPins(7,30);
//Wire.begin();
  BNO055_write(OPR_MODE, FASTEST_MODE|OPR_MODE_NDOF);
  
 // EEPROM.write(1, 53); //to program node id
  
  //node_id = EEPROM.read(1); // to read the node id

}

void loop()
{
 // freeCube();
  stellarium();
  
  delay(5);
}

void enc_isr()
{
  if(digitalRead(2))
    count+= digitalRead(3)? -1: 1;
}

void stellarium(){
 // float q[4];
 float temp[3];
  BNO055_3_vec(EUL_HEADING_LSB ,&temp[0]);
  Serial.print(temp[0]/16.0);
  Serial.print(",");
  Serial.print(temp[1]/16.0);
  Serial.print(","); 
  Serial.print(temp[2]/16.0);// BNO055_4_vec(QUA_DATA_W_LSB, &q[0]);
  Serial.print(",");
  Serial.println(count);
  //StellariumOut(&q[0],count);
}

void acc(){
  print_3_vec(ACC_DATA_X_LSB);
}

void gyro(){
  print_3_vec(GYR_DATA_X_LSB);
}

/*
void AccRF(){
  print_3_vec_RF(ACC_DATA_X_LSB);
}
*/
void mag(){
  print_3_vec(MAG_DATA_X_LSB);
}

void eulerHead(){
  print_3_vec(EUL_HEADING_LSB);
}

void gravityVec(){
  print_3_vec(GRV_DATA_X_LSB);
}
/*
void linearAccRF(){
  print_3_vec_RF(LIA_DATA_X_LSB);
}*/

void linearAcc(){
  print_3_vec(LIA_DATA_X_LSB);
}

void print_3_vec(int8_t addr){
  float temp[3];
  BNO055_3_vec(addr ,&temp[0]);
  Serial.print((int)temp[0]);
  Serial.print(",");
  Serial.print((int)temp[1]);
  Serial.print(","); 
  Serial.print((int)temp[2]);
}
/*
void print_3_vec_RF(int8_t addr){
  float temp[3];
  char str[20];
  BNO055_3_vec(addr ,&temp[0]);
  RF.beginTransmission();
  RF.write(dtostrf(temp[0], 2, 2, str));
  RF.write(", ");
  RF.write(dtostrf(temp[1], 2, 2, str));
  RF.write(", "); 
  RF.write(dtostrf(temp[2], 2, 2, str));
  RF.write(" \n\r");
  RF.endTransmission();
}

void freeCubeRF_multi(int node){
  float q[4];
  BNO055_4_vec(QUA_DATA_W_LSB, &q[0]);
  freeIMUOutRF_multi(&q[0], node);
}

void freeCubeRF_unity(int node){
  float q[4];
  BNO055_4_vec(QUA_DATA_W_LSB, &q[0]);
  freeIMUOutRF_unity(&q[0], node);
}
*/
void freeCube_unity(int node){
  float q[4];
  BNO055_4_vec(QUA_DATA_W_LSB, &q[0]);
  freeIMUOut_unity(&q[0], node);
}
/*
void freeCubeRF(){
  float q[4];
  BNO055_4_vec(QUA_DATA_W_LSB, &q[0]);
  freeIMUOutRF(&q[0]);
}
*/
void freeCube(){
  float q[4];
  BNO055_4_vec(QUA_DATA_W_LSB, &q[0]);
  freeIMUOut(&q[0]);
}

void BNO055_3_vec(int8_t addr, float *vec){
  Wire.beginTransmission(BNO055_I2C_ADDR);
  Wire.write(addr);
  Wire.endTransmission(false);

  Wire.requestFrom(BNO055_I2C_ADDR, 6, false);
  int16_t b_data[6];
  for(int i=0;i<6;i++)
    b_data[i]=Wire.read();
  
  vec[0] = b_data[1]<<8|b_data[0];
  vec[1] = b_data[3]<<8|b_data[2];
  vec[2] = b_data[5]<<8|b_data[4];
}

void BNO055_4_vec(int8_t addr, float *vec){
  float norm;
  Wire.beginTransmission(BNO055_I2C_ADDR);
  Wire.write(addr);
  Wire.endTransmission(false);

  Wire.requestFrom(BNO055_I2C_ADDR, 8, false);
  int16_t b_data[8];
  for(int i=0;i<8;i++)
    b_data[i]=Wire.read();
  
  vec[0] = b_data[1]<<8|b_data[0];
  vec[1] = b_data[3]<<8|b_data[2];
  vec[2] = b_data[5]<<8|b_data[4];
  vec[3] = b_data[7]<<8|b_data[6];
 
 /* //If you need normalization
  norm = sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2] + vec[3] * vec[3]);    
  norm = 1.0f/norm;
  vec[0] *= norm;
  vec[1] *= norm;
  vec[2] *= norm;
  vec[3] *= norm;
*/
}

byte BNO055_read(int addr){
  Wire.beginTransmission(BNO055_I2C_ADDR);
  Wire.write(addr);
  Wire.endTransmission(false);

  Wire.requestFrom(BNO055_I2C_ADDR, 1, true);
  return Wire.read();
}

int BNO055_write(int addr,int data){
  Wire.beginTransmission(BNO055_I2C_ADDR);
  Wire.write(addr);
  Wire.write(data);
  Wire.endTransmission(true);

  return 1;
}

void serialFloatPrint(float f) {
  byte * b = (byte *) &f;
  for(int i=0; i<4; i++) {
    
    byte b1 = (b[i] >> 4) & 0x0f;
    byte b2 = (b[i] & 0x0f);
 
    char c1 = (b1 < 10) ? ('0' + b1) : 'A' + b1 - 10;
    char c2 = (b2 < 10) ? ('0' + b2) : 'A' + b2 - 10;
    
    Serial.print(c1);
    Serial.print(c2);
  }
}

void StellariumOut(float *quat, long encoder_value){
  
  serialFloatPrint(quat[0]);
  Serial.print(",");
  serialFloatPrint(quat[1]);
  Serial.print(",");
  serialFloatPrint(quat[2]);
  Serial.print(",");
  serialFloatPrint(quat[3]);
  Serial.print(",");
  Serial.print(encoder_value);
  Serial.print(",\n");  
}

void freeIMUOut(float *quat){
  
  serialFloatPrint(quat[0]);
  Serial.print(",");
  serialFloatPrint(quat[1]);
  Serial.print(",");
  serialFloatPrint(quat[2]);
  Serial.print(",");
  serialFloatPrint(quat[3]);
  Serial.print(",\n");  
}
/*
void freeIMUOutRF_multi(float *quat, int node){
  RF.beginTransmission();
  serialFloatPrintRF(quat[0]);
  RF.write(",");
  serialFloatPrintRF(quat[1]);
  RF.write(",");
  serialFloatPrintRF(quat[2]);
  RF.write(",");
  serialFloatPrintRF(quat[3]);
  RF.write(",");
  RF.write(node);
  RF.write(",\n");  
  RF.endTransmission();
}
*/
void freeIMUOut_unity(float *quat, int node){
  Serial.print("0,Q,");  //zero indicates version
  Serial.print(node);
  Serial.print(",");    
  serialFloatPrint(quat[0]);
  Serial.print(",");
  serialFloatPrint(quat[1]);
  Serial.print(",");
  serialFloatPrint(quat[2]);
  Serial.print(",");
  serialFloatPrint(quat[3]);
  Serial.print(",\n");  
}
/*
void freeIMUOutRF_unity(float *quat, int node){
  RF.beginTransmission();
  RF.write("0,Q,");  //zero indicates version
  RF.write(((node/10)%10)+48);
  RF.write((node%10)+48);
  RF.write(",");    
  serialFloatPrintRF(quat[0]);
  RF.write(",");
  serialFloatPrintRF(quat[1]);
  RF.write(",");
  serialFloatPrintRF(quat[2]);
  RF.write(",");
  serialFloatPrintRF(quat[3]);
  RF.write(",\n");  
  RF.endTransmission();
}

void freeIMUOutRF(float *quat){
  RF.beginTransmission();
  serialFloatPrintRF(quat[0]);
  RF.write(",");
  serialFloatPrintRF(quat[1]);
  RF.write(",");
  serialFloatPrintRF(quat[2]);
  RF.write(",");
  serialFloatPrintRF(quat[3]);
  RF.write(",\n");  
  RF.endTransmission();
}

void serialFloatPrintRF(float f) {
  byte * b = (byte *) &f;
  for(int i=0; i<4; i++) {
  //for(int i=0; i<2; i++) {
    
    byte b1 = (b[i] >> 4) & 0x0f;
    byte b2 = (b[i] & 0x0f);
    
    char c1 = (b1 < 10) ? ('0' + b1) : 'A' + b1 - 10;
    char c2 = (b2 < 10) ? ('0' + b2) : 'A' + b2 - 10;
    
   // Serial.print(c1);
   // Serial.print(c2);
    

    RF.write(c1);
    RF.write(c2);

  }
}
*/

