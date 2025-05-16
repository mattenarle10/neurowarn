#include "Adafruit_VL53L1X.h"
#include "ArduinoJson.h"

// address we will assign if dual sensor is present
#define LOX1_ADDRESS 0x30
#define LOX2_ADDRESS 0x31



// set the pins to shutdown
#define SHT_LOX1 6
#define SHT_LOX2 7

// objects for the vl53l0x
Adafruit_VL53L1X lox1 = Adafruit_VL53L1X();
Adafruit_VL53L1X lox2 = Adafruit_VL53L1X();

int data_interval = 100;
int servo_sections = 6;  //should be factor of 180
int servo_stride = 180 / servo_sections;
int max_distance = 200;

long prev = 0;


int servo1_angle = 0;
int servo1_direction = servo_stride;

float servo2_angle = 0;
float servo2_direction = servo_stride;



/*
    Reset all sensors by setting all of their XSHUT pins low for delay(10), then set all XSHUT high to bring out of reset
    Keep sensor #1 awake by keeping XSHUT pin high
    Put all other sensors into shutdown by pulling XSHUT pins low
    Initialize sensor #1 with lox.begin(new_i2c_address) Pick any number but 0x29 and it must be under 0x7F. Going with 0x30 to 0x3F is probably OK.
    Keep sensor #1 awake, and now bring sensor #2 out of reset by setting its XSHUT pin high.
    Initialize sensor #2 with lox.begin(new_i2c_address) Pick any number but 0x29 and whatever you set the first sensor to
 */
void setID() {
  // all reset
  Wire.begin();
  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(10);
  // all unreset
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);

  // activating LOX1 and resetting LOX2
  digitalWrite(SHT_LOX1, HIGH);
  digitalWrite(SHT_LOX2, LOW);

  // initing LOX1
  if (!lox1.begin(LOX1_ADDRESS)) {
    Serial.println(F("Failed to boot first VL53L0X"));
    while (1)
      ;
  }
  delay(10);
  if (!lox1.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(lox1.vl_status);
    while (1) delay(10);
  }
  // Serial.println(F("sensor1 Ranging started"));




  // activating LOX2
  digitalWrite(SHT_LOX2, HIGH);
  delay(10);
  
  //initing LOX2
  if (!lox2.begin(LOX2_ADDRESS)) {
    Serial.println(F("Failed to boot second VL53L0X"));
    while (1)
      ;
  }

  if (!lox2.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(lox2.vl_status);
    while (1) delay(10);
  }
  // Serial.println(F("sensor2 Ranging started"));
}


void setup() {
  Serial.begin(115200);

  // wait until serial port opens for native USB devices
  while (!Serial) { delay(1); }


  pinMode(SHT_LOX1, OUTPUT);
  pinMode(SHT_LOX2, OUTPUT);

  // Serial.println(F("Shutdown pins inited..."));

  digitalWrite(SHT_LOX1, LOW);
  digitalWrite(SHT_LOX2, LOW);
  delay(10);
  // Serial.println(F("Both in reset mode...(pins are low)"));


  // Serial.println(F("Starting..."));
  setID();
  delay(10);

  // Valid timing budgets: 15, 20, 33, 50, 100, 200 and 500ms!
  // lox1.setTimingBudget(100);
  // Serial.print(F("Timing budget (ms): "));
  // Serial.println(lox1.getTimingBudget());
  lox1.VL53L1X_SetDistanceMode(2);
  lox2.VL53L1X_SetDistanceMode(1);
  /*==
  vl.VL53L1X_SetDistanceThreshold(100, 300, 3, 1);
  vl.VL53L1X_SetInterruptPolarity(0);
  */
  delay(500);
}

void loop() {
  int16_t distance1, distance2;

  if (millis() - prev > data_interval) {

    JsonDocument doc;
    JsonArray lidar1, lidar2;
    if (lox1.dataReady()) {

      // new measurement for the taking!
      distance1 = lox1.distance();
      // Serial.println(distance1);
      if (distance1 == -1 || distance1 > max_distance) {

        lidar1 = doc["lidar1"].to<JsonArray>();
        lidar1.add(false);
        lidar1.add(servo1_angle / servo_stride);


      } else {

        lidar1 = doc["lidar1"].to<JsonArray>();
        lidar1.add(true);
        lidar1.add(servo1_angle / servo_stride);
      }

      if (servo1_angle == 0 || servo1_angle == 180) servo1_direction = -1 * servo1_direction;
      servo1_angle += servo1_direction;
      servo1_angle = constrain(servo1_angle, 0, 180);
      delay(5);
    }


    if (lox2.dataReady()) {


      // new measurement for the taking!
      distance2 = lox2.distance();
      // Serial.println(distance2);
      if (distance2 == -1 || distance2 > max_distance) {

        lidar2 = doc["lidar2"].to<JsonArray>();
        lidar2.add(false);
        lidar2.add(servo2_angle / servo_stride);


      } else {

        lidar2 = doc["lidar2"].to<JsonArray>();
        lidar2.add(true);
        lidar2.add(servo1_angle / servo_stride);
      }


      if (servo2_angle == 0 || servo2_angle == 180) servo2_direction = -1 * servo2_direction;
      servo2_angle += servo2_direction;
      servo2_angle = constrain(servo2_angle, 0, 180);
      delay(5);
    }



    char buffer[256];
    size_t n = serializeJson(doc, buffer);
    Serial.write(buffer, n);
    Serial.println();  // Send a newline character to end the lineF
    prev = millis();

    delay(5);
  }
}
