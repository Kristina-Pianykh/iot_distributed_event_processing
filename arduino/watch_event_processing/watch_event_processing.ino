#include <HTTPClient.h>
#include <WiFi.h>
#include <SPI.h>
#include <ctime>
#include "config.h"


const char* ssid = "Beta Centauri";
const char* password = "HEtV24c7j6vz";
const char* serverURL = "http://192.168.0.6:8000";


HTTPClient httpClient;
TTGOClass *ttgo_watch;

// for rotation sensors
TFT_eSPI *tft;
BMA *sensor;
uint8_t prevRotation;

// for time synchronization
const char *ntpServer       = "pool.ntp.org";
const long  gmtOffset_sec   = 3600;
const int   daylightOffset_sec = 3600;
// Global variable to store the synchronized time
PCF8563_Class *rtc; //real time clock
uint8_t hh, mm, ss, mmonth, dday; // H, M, S variables
uint16_t yyear; // Year is 16 bit int
RTC_Date tnow;


void sendHTTPRequest(String requestBody) {
  if (WiFi.status() == WL_CONNECTED) {
    // Set the target URL
    httpClient.begin(serverURL);

    // Set the Content-Type header
    httpClient.addHeader("Content-Type", "application/json");
    
    // Send the HTTP POST request
    int httpResponseCode = httpClient.POST(requestBody);
    
    // Handle the response
    if (httpResponseCode > 0) {
      String response = httpClient.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.println("Error on HTTP request");
    }
      
    // Free resources
    httpClient.end();
  }
}

String format_request_payload(String eventType, RTC_Date tnow) {
  hh = tnow.hour;
  mm = tnow.minute;
  ss = tnow.second;
  mmonth = tnow.month;
  dday = tnow.day;
  yyear = tnow.year;

  String message = "{\"Event\": \"" + eventType + "\", \"Year\": \"" + String(yyear) + "\", \"Month\": \"" + String(mmonth) + "\", \"Day\": \"" + String(dday) + "\", \"Hour\": \"" + String(hh) + "\", \"Minute\": \"" + String(mm) + "\", \"Seconds\": \"" + String(ss) + "\"}";
  return message;
}

static void click_event_handler(lv_obj_t *obj, lv_event_t event)
{
    if (event == LV_EVENT_CLICKED) {
        tnow = ttgo_watch->rtc->getDateTime();
        Serial.println(format_request_payload("Clicked", tnow));
        sendHTTPRequest(format_request_payload("Clicked", tnow));
        Serial.printf("Clicked\n");

    } else if (event == LV_EVENT_VALUE_CHANGED) {
        tnow = ttgo_watch->rtc->getDateTime();
        Serial.println(format_request_payload("Toggled", tnow));
        sendHTTPRequest(format_request_payload("Toggled", tnow));
        Serial.printf("Toggled\n");
    }
}

static void sensor_event_handler() {
  // Obtain the BMA423 direction,
  // so that the screen orientation is consistent with the sensor
  uint8_t rotation = sensor->direction();
  if (prevRotation != rotation) {
      prevRotation = rotation;
      // Serial.printf("tft:%u sens:%u ", tft->getRotation(), rotation);
      switch (rotation) {
      case DIRECTION_DISP_DOWN:
          //No use
          break;
      case DIRECTION_DISP_UP:
          //No use
          break;
      case DIRECTION_BOTTOM_EDGE:
          Serial.printf("WATCH_SCREEN_BOTTOM_EDGE\n");
          tnow = ttgo_watch->rtc->getDateTime();
          Serial.println(format_request_payload("WATCH_SCREEN_BOTTOM_EDGE", tnow));
          sendHTTPRequest(format_request_payload("WATCH_SCREEN_BOTTOM_EDGE", tnow));
          tft->setRotation(WATCH_SCREEN_BOTTOM_EDGE);
          break;
      case DIRECTION_TOP_EDGE:
          Serial.printf("WATCH_SCREEN_TOP_EDGE\n");
          tnow = ttgo_watch->rtc->getDateTime();
          Serial.println(format_request_payload("WATCH_SCREEN_TOP_EDGE", tnow));
          sendHTTPRequest(format_request_payload("WATCH_SCREEN_TOP_EDGE", tnow));
          tft->setRotation(WATCH_SCREEN_TOP_EDGE);
          break;
      case DIRECTION_RIGHT_EDGE:
          Serial.printf("WATCH_SCREEN_RIGHT_EDGE\n");
          tnow = ttgo_watch->rtc->getDateTime();
          Serial.println(format_request_payload("WATCH_SCREEN_RIGHT_EDGE", tnow));
          sendHTTPRequest(format_request_payload("WATCH_SCREEN_RIGHT_EDGE", tnow));
          tft->setRotation(WATCH_SCREEN_RIGHT_EDGE);
          break;
      case DIRECTION_LEFT_EDGE:
          Serial.printf("WATCH_SCREEN_LEFT_EDGE\n");
          tnow = ttgo_watch->rtc->getDateTime();
          Serial.println(format_request_payload("WATCH_SCREEN_LEFT_EDGE", tnow));
          sendHTTPRequest(format_request_payload("WATCH_SCREEN_LEFT_EDGE", tnow));
          tft->setRotation(WATCH_SCREEN_LEFT_EDGE);
          break;
      default:
          break;
      }
  }
}

void setup_lvgl(TTGOClass *ttgo_watch) {
  ttgo_watch->openBL();
  ttgo_watch->lvgl_begin();

  lv_obj_t *label;

  lv_obj_t *btn1 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn1, click_event_handler);
  lv_obj_align(btn1, NULL, LV_ALIGN_CENTER, 0, -40);

  label = lv_label_create(btn1, NULL);
  lv_label_set_text(label, "Button");

  lv_obj_t *btn2 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn2, click_event_handler);
  lv_obj_align(btn2, NULL, LV_ALIGN_CENTER, 0, 40);
  lv_btn_set_checkable(btn2, true);
  lv_btn_toggle(btn2);
  lv_btn_set_fit2(btn2, LV_FIT_NONE, LV_FIT_TIGHT);

  label = lv_label_create(btn2, NULL);
  lv_label_set_text(label, "Toggled");
}

void synchronize_time(TTGOClass *ttgo_watch) {
  //init and get the time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
      tft->println("Failed to obtain time, Restart in 3 seconds");
      Serial.println("Failed to obtain time, Restart in 3 seconds");
      delay(3000);
      esp_restart();
      while (1);
  }
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  Serial.println("Time synchronization succeeded");

  // Sync local time to external RTC
  rtc = ttgo_watch->rtc;
  rtc->syncToRtc();
}

void setup_sensors(TTGOClass *ttgo_watch) {
  // Turn on the backlight
  ttgo_watch->openBL();

  //Receive objects for easy writing
  tft = ttgo_watch->tft;
  sensor = ttgo_watch->bma;

  // Accel parameter structure
  Acfg cfg;
  /*!
      Output data rate in Hz, Optional parameters:
          - BMA4_OUTPUT_DATA_RATE_0_78HZ
          - BMA4_OUTPUT_DATA_RATE_1_56HZ
          - BMA4_OUTPUT_DATA_RATE_3_12HZ
          - BMA4_OUTPUT_DATA_RATE_6_25HZ
          - BMA4_OUTPUT_DATA_RATE_12_5HZ
          - BMA4_OUTPUT_DATA_RATE_25HZ
          - BMA4_OUTPUT_DATA_RATE_50HZ
          - BMA4_OUTPUT_DATA_RATE_100HZ
          - BMA4_OUTPUT_DATA_RATE_200HZ
          - BMA4_OUTPUT_DATA_RATE_400HZ
          - BMA4_OUTPUT_DATA_RATE_800HZ
          - BMA4_OUTPUT_DATA_RATE_1600HZ
  */
  cfg.odr = BMA4_OUTPUT_DATA_RATE_100HZ;
  /*!
      G-range, Optional parameters:
          - BMA4_ACCEL_RANGE_2G
          - BMA4_ACCEL_RANGE_4G
          - BMA4_ACCEL_RANGE_8G
          - BMA4_ACCEL_RANGE_16G
  */
  cfg.range = BMA4_ACCEL_RANGE_2G;
  /*!
      Bandwidth parameter, determines filter configuration, Optional parameters:
          - BMA4_ACCEL_OSR4_AVG1
          - BMA4_ACCEL_OSR2_AVG2
          - BMA4_ACCEL_NORMAL_AVG4
          - BMA4_ACCEL_CIC_AVG8
          - BMA4_ACCEL_RES_AVG16
          - BMA4_ACCEL_RES_AVG32
          - BMA4_ACCEL_RES_AVG64
          - BMA4_ACCEL_RES_AVG128
  */
  cfg.bandwidth = BMA4_ACCEL_NORMAL_AVG4;

  /*! Filter performance mode , Optional parameters:
      - BMA4_CIC_AVG_MODE
      - BMA4_CONTINUOUS_MODE
  */
  cfg.perf_mode = BMA4_CONTINUOUS_MODE;

  // Configure the BMA423 accelerometer
  sensor->accelConfig(cfg);

  // Enable BMA423 accelerometer
  // Warning : Need to use feature, you must first enable the accelerometer
  // Warning : Need to use feature, you must first enable the accelerometer
  // Warning : Need to use feature, you must first enable the accelerometer
  sensor->enableAccel();
}

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(115200);

  ttgo_watch = TTGOClass::getWatch();
  ttgo_watch->begin();

  // Turn on the backlight
  ttgo_watch->openBL();
  // Set up tft for Wi-Fi connection status
  ttgo_watch->setBrightness(128);       // 0~255
  tft = ttgo_watch->tft;
  tft->setTextColor(TFT_GREEN, TFT_BLACK);

  tft->print("Connecting to ");
  tft->println(ssid);
  tft->println();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.printf("Connecting to %s\n", ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
    tft->print(".");
  }

  // Wi-Fi connected
  Serial.println("Connected to WiFi!");

  // Print the ESP32's IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  setup_lvgl(ttgo_watch);
  setup_sensors(ttgo_watch);
  synchronize_time(ttgo_watch);
  
  delay(5000); // Wait for 5 seconds before sending the next request
}

void loop() {
    lv_task_handler();
    sensor_event_handler();
    delay(5);
}
