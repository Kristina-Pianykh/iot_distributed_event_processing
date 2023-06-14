#include "sensors.h"
#include "http_requests.h"


static void sensor_event_handler(TTGOClass *ttgo_watch) {
  // Obtain the BMA423 direction,
  // so that the screen orientation is consistent with the sensor
  RTC_Date tnow;
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
