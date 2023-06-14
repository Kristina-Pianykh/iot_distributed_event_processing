#ifndef LVGL_UTILS_H
#define LVGL_UTILS_H


#include <Arduino.h>
#include "config.h"


void setup_lvgl(TTGOClass *ttgo_watch);
static void click_event_handler(TTGOClass *ttgo_watch, lv_obj_t *obj, lv_event_t event);

#endif // LVGL_UTILS_H