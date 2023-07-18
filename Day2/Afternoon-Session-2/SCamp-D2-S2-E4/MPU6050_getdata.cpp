/*
 * @Author: ELEGOO
 * @Date: 2019-10-22 11:59:09
 * @LastEditTime: 2020-06-19 11:57:50
 * @LastEditors: Changhua
 * @Description: conqueror robot tank
 * @FilePath: 
 */

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"
#include "MPU6050_getdata.h"

#include <stdio.h>
#include <math.h>

MPU6050 accelgyro;
MPU6050_getdata MPU6050Getdata;

// static void MsTimer2_MPU6050getdata(void)
// {
//   sei();
//   int16_t ax, ay, az, gx, gy, gz;
//   accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); 
//   float gyroz = -(gz - MPU6050Getdata.gzo) / 131 * 0.005f;
//   MPU6050Getdata.yaw += gyroz;
// }

bool MPU6050_getdata::MPU6050_dveInit(void)
{
  Wire.begin();
  uint8_t chip_id = 0x00;
  uint8_t cout;
  do
  {
    chip_id = accelgyro.getDeviceID();
    Serial.print("MPU6050_chip_id: ");
    Serial.println(chip_id);
    delay(10);
    cout += 1;
    if (cout > 10)
    {
      return true;
    }
  } while (chip_id == 0X00 || chip_id == 0XFF); 
  accelgyro.initialize();
  // unsigned short times = 100; 
  // for (int i = 0; i < times; i++)
  // {
  //   gz = accelgyro.getRotationZ();
  //   gzo += gz;
  // }
  // gzo /= times; 
  return false;
}
bool MPU6050_getdata::MPU6050_calibration(void)
{
  unsigned short times = 100;
  for (int i = 0; i < times; i++)
  {
    gz = accelgyro.getRotationZ();
    gzo += gz;
  }
  gzo /= times; 

  // gzo = accelgyro.getRotationZ();
  return false;
}
bool MPU6050_getdata::MPU6050_dveGetEulerAngles(float *Yaw)
{
  unsigned long now = millis();   
  dt = (now - lastTime) / 1000.0; 
  lastTime = now;                 
  gz = accelgyro.getRotationZ();
  float gyroz = -(gz - gzo) / 131.0 * dt; 
  if (fabs(gyroz) < 0.05)
  {
    gyroz = 0.00;
  }
  agz += gyroz; //z轴角速度积分
  *Yaw = agz;
  return false;
}
