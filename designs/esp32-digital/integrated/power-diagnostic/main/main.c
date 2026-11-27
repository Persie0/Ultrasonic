#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_system.h"

static const char *TAG = "power_diag";

/*
 * Dedicated power-only diagnostic. Deliberately no PWM, Bluetooth, Wi-Fi,
 * audio service or load activation. Both output pins are held low.
 * Physical arm bridge must remain open and all acoustic positions DNP.
 */
void app_main(void)
{
    ESP_ERROR_CHECK(gpio_reset_pin(GPIO_NUM_25));
    ESP_ERROR_CHECK(gpio_reset_pin(GPIO_NUM_26));
    ESP_ERROR_CHECK(gpio_set_level(GPIO_NUM_25, 0));
    ESP_ERROR_CHECK(gpio_set_level(GPIO_NUM_26, 0));
    const gpio_config_t cfg = {
        .pin_bit_mask = (1ULL << GPIO_NUM_25) | (1ULL << GPIO_NUM_26),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_ENABLE,
        .intr_type = GPIO_INTR_DISABLE
    };
    ESP_ERROR_CHECK(gpio_config(&cfg));
    ESP_ERROR_CHECK(gpio_set_level(GPIO_NUM_25, 0));
    ESP_ERROR_CHECK(gpio_set_level(GPIO_NUM_26, 0));
    ESP_LOGI(TAG, "POWER ONLY; arm open; reset reason=%d", (int)esp_reset_reason());
    unsigned long tick = 0;
    for (;;) {
        ESP_LOGI(TAG, "idle heartbeat %lu; no voltage or temperature sensor", tick++);
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
