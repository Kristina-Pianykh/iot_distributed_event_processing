#include "http_requests.h"

String format_request_payload(String eventType, RTC_Date tnow) {
  uint8_t hh, mm, ss, mmonth, dday; // H, M, S variables
  uint16_t yyear; // Year is 16 bit int
  hh = tnow.hour;
  mm = tnow.minute;
  ss = tnow.second;
  mmonth = tnow.month;
  dday = tnow.day;
  yyear = tnow.year;

  String message = "{\"Event\": \"" + eventType + "\", \"Year\": \"" + String(yyear) + "\", \"Month\": \"" + String(mmonth) + "\", \"Day\": \"" + String(dday) + "\", \"Hour\": \"" + String(hh) + "\", \"Minute\": \"" + String(mm) + "\", \"Seconds\": \"" + String(ss) + "\"}";
  return message;
}

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


// time_t generate_unix_timestamp(int year, int month, int day, int hour, int minute, int second) {
//   struct tm timeinfo;

//   timeinfo.tm_year = year - 1900;  // Years since 1900
//   timeinfo.tm_mon = month - 1;     // Months since January (0-11)
//   timeinfo.tm_mday = day;          // Day of the month (1-31)
//   timeinfo.tm_hour = hour;         // Hours since midnight (0-23)
//   timeinfo.tm_min = minute;        // Minutes after the hour (0-59)
//   timeinfo.tm_sec = second;        // Seconds after the minute (0-61)

//   return mktime(&timeinfo);
// }
