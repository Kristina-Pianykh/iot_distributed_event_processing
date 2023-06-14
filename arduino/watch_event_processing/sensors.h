#ifndef SENSOR_UTILS_H
#define SENSOR_UTILS_H


#include <Arduino.h>
#include "config.h"

// for rotation sensors
TFT_eSPI *tft;
BMA *sensor;
uint8_t prevRotation;

static void sensor_event_handler(TTGOClass *ttgo_watch);

#endif // SENSOR_UTILS_H
