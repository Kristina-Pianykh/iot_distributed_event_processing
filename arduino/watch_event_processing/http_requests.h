#ifndef HTTP_UTILS_H
#define HTTP_UTILS_H


#include <Arduino.h>
#include "config.h"
#include <WiFi.h>
#include <HTTPClient.h>

HTTPClient httpClient;
const char* serverURL = "http://192.168.0.6:8000";

String format_request_payload(String eventType, RTC_Date tnow);
void sendHTTPRequest(String requestBody);
#endif // HTTP_UTILS_H
