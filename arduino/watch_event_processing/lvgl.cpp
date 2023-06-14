#include "http_requests.h"
#include "lvgl.h"

static void click_event_handler(lv_obj_t *obj, lv_event_t event)
{
    RTC_Date tnow;
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
