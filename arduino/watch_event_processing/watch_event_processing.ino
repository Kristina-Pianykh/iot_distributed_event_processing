#include <HTTPClient.h>
#include <WiFi.h>
#include <SPI.h>
#include "config.h"


const char* ssid = "Beta Centauri";
const char* password = "HEtV24c7j6vz";
const char* serverURL = "http://192.168.0.6:8000";


// WiFiClient wifiClient;
HTTPClient httpClient;
TTGOClass *ttgo;

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

static void event_handler(lv_obj_t *obj, lv_event_t event)
{
    if (event == LV_EVENT_CLICKED) {
        sendHTTPRequest("{\"Event\": \"Clicked\"}");
        Serial.printf("Clicked\n");

    } else if (event == LV_EVENT_VALUE_CHANGED) {
        sendHTTPRequest("{\"Event\": \"Toggled\"}");
        Serial.printf("Toggled\n");
    }
}

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Wi-Fi connected
  Serial.println("Connected to WiFi!");

  // Print the ESP32's IP address
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // TTGO Watch LVLG Button example setup
  ttgo = TTGOClass::getWatch();
  ttgo->begin();
  ttgo->openBL();
  ttgo->lvgl_begin();

  lv_obj_t *label;

  lv_obj_t *btn1 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn1, event_handler);
  lv_obj_align(btn1, NULL, LV_ALIGN_CENTER, 0, -40);

  label = lv_label_create(btn1, NULL);
  lv_label_set_text(label, "Button");

  lv_obj_t *btn2 = lv_btn_create(lv_scr_act(), NULL);
  lv_obj_set_event_cb(btn2, event_handler);
  lv_obj_align(btn2, NULL, LV_ALIGN_CENTER, 0, 40);
  lv_btn_set_checkable(btn2, true);
  lv_btn_toggle(btn2);
  lv_btn_set_fit2(btn2, LV_FIT_NONE, LV_FIT_TIGHT);

  label = lv_label_create(btn2, NULL);
  lv_label_set_text(label, "Toggled");
  // end of the example
  
  delay(5000); // Wait for 5 seconds before sending the next request
}

void loop() {
    lv_task_handler();
    delay(5);
}
