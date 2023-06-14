#include <HTTPClient.h>
#include <WiFiServer.h>
#include "ESPAsyncWebServer.h"
#include <WiFi.h>
#include <SPI.h>
#include "config.h"
#include "sensors.h"
#include "http_requests.h"
#include "lvgl.h"

// home Wi-Fi config
const char* ssid = "Beta Centauri";
const char* password = "HEtV24c7j6vz";
// const char* serverURL = "http://192.168.0.6:8000";

// Iphone hotspot config
// const char* ssid = "iPhone (Kris)";
// const char* password = "123456789km";
// const char* serverURL = "http://172.20.10.6:8000";


AsyncWebServer server(80);
TTGOClass *ttgo_watch;


// for time synchronization
const char *ntpServer       = "pool.ntp.org";
const long  gmtOffset_sec   = 3600;
const int   daylightOffset_sec = 3600;
// Global variable to store the synchronized time
PCF8563_Class *rtc; //real time clock

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
  cfg.odr = BMA4_OUTPUT_DATA_RATE_100HZ;
  cfg.range = BMA4_ACCEL_RANGE_2G;
  cfg.bandwidth = BMA4_ACCEL_NORMAL_AVG4;
  cfg.perf_mode = BMA4_CONTINUOUS_MODE;

  // Configure the BMA423 accelerometer
  sensor->accelConfig(cfg);
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
  server.on(
    "/post",
    HTTP_POST,
    [](AsyncWebServerRequest * request){},
    NULL,
    [](AsyncWebServerRequest * request, uint8_t *data, size_t len, size_t index, size_t total) {

      Serial.println("Incoming request:");
      for (size_t i = 0; i < len; i++) {
        Serial.write(data[i]);
      }

      Serial.println();

      request->send(200);
  });
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
    lv_task_handler();
    sensor_event_handler(ttgo_watch);
    server.handleClient();
    
    // // Check if a client has connected
    // WiFiClient client = server.available();
    // if (client) {
    //   Serial.println("New HTTP request");

    //   // Read the request
    //   String request = client.readStringUntil('\r');
    //   client.flush();

    //   // Print the request payload
    //   Serial.println("Request Payload:");
    //   while (client.available()) {
    //     String line = client.readStringUntil('\r');
    //     Serial.println(line);
    //   }
    //   // Send the response
    //   client.println("HTTP/1.1 200 OK");
    //   client.println("Content-type:text/html");
    //   client.println();
    //   client.println("<html><body><h1>HTTP Request Received</h1></body></html>");


    //   // Close the connection
    //   delay(1);
    //   // client.stop();
    //   // Serial.println("Client disconnected");
    // }
    // delay(5);
}
