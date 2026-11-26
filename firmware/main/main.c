#include <stdbool.h>
#include <stdint.h>
#include <stdatomic.h>
#include <stdlib.h>
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_gap_bt_api.h"
#include "esp_a2dp_api.h"
#include "driver/mcpwm_prelude.h"

#define GPIO_A 25
#define GPIO_B 26
#define PERIOD 250
#define HALF 125
#define PCM_OUT_HZ 8000
#define SILENCE_SAMPLES 800
#define QUEUE_SAMPLES 512
#define PREFILL_SAMPLES 160
#define MAX_TICK_GAP_US 1000
static const char *TAG = "ultrasonic";
static QueueHandle_t audio;
static atomic_int rate;
static atomic_bool streaming;
static atomic_uint generation;
static mcpwm_gen_handle_t gen_a, gen_b;
static mcpwm_cmpr_handle_t end_a, end_b;
static bool active;
static unsigned quiet;
static bool primed;
static unsigned consumer_epoch;
static int64_t last_tick_us;
static atomic_bool overrun;

static void mute(void) {
    mcpwm_generator_set_force_level(gen_a, 0, true);
    mcpwm_generator_set_force_level(gen_b, 0, true);
    active = false;
}

static void init_pwm(void) {
    mcpwm_timer_handle_t timer;
    mcpwm_oper_handle_t opa, opb;
    mcpwm_cmpr_handle_t start_b;
    mcpwm_timer_config_t tc = {
        .group_id = 0, .clk_src = MCPWM_TIMER_CLK_SRC_DEFAULT,
        .resolution_hz = 10000000, .period_ticks = PERIOD,
        .count_mode = MCPWM_TIMER_COUNT_MODE_UP
    };
    mcpwm_operator_config_t oc = {.group_id = 0};
    mcpwm_comparator_config_t cc = {.flags.update_cmp_on_tez = true};
    mcpwm_generator_config_t ga = {.gen_gpio_num = GPIO_A};
    mcpwm_generator_config_t gb = {.gen_gpio_num = GPIO_B};
    ESP_ERROR_CHECK(mcpwm_new_timer(&tc, &timer));
    ESP_ERROR_CHECK(mcpwm_new_operator(&oc, &opa));
    ESP_ERROR_CHECK(mcpwm_new_operator(&oc, &opb));
    ESP_ERROR_CHECK(mcpwm_operator_connect_timer(opa, timer));
    ESP_ERROR_CHECK(mcpwm_operator_connect_timer(opb, timer));
    ESP_ERROR_CHECK(mcpwm_new_comparator(opa, &cc, &end_a));
    ESP_ERROR_CHECK(mcpwm_new_comparator(opb, &cc, &start_b));
    ESP_ERROR_CHECK(mcpwm_new_comparator(opb, &cc, &end_b));
    ESP_ERROR_CHECK(mcpwm_comparator_set_compare_value(end_a, 20));
    ESP_ERROR_CHECK(mcpwm_comparator_set_compare_value(start_b, HALF));
    ESP_ERROR_CHECK(mcpwm_comparator_set_compare_value(end_b, HALF+20));
    ESP_ERROR_CHECK(mcpwm_new_generator(opa, &ga, &gen_a));
    ESP_ERROR_CHECK(mcpwm_new_generator(opb, &gb, &gen_b));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_timer_event(gen_a,
        MCPWM_GEN_TIMER_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_TIMER_EVENT_EMPTY, MCPWM_GEN_ACTION_HIGH)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_compare_event(gen_a,
        MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, end_a, MCPWM_GEN_ACTION_LOW)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_timer_event(gen_b,
        MCPWM_GEN_TIMER_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_TIMER_EVENT_EMPTY, MCPWM_GEN_ACTION_LOW)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_compare_event(gen_b,
        MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, start_b, MCPWM_GEN_ACTION_HIGH)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_compare_event(gen_b,
        MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, end_b, MCPWM_GEN_ACTION_LOW)));
    mute();
    ESP_ERROR_CHECK(mcpwm_timer_enable(timer));
    ESP_ERROR_CHECK(mcpwm_timer_start_stop(timer, MCPWM_TIMER_START_NO_STOP));
}

typedef struct { int16_t pcm; unsigned epoch; } frame_t;

// Runs in the esp_timer task, not an ISR. The peripheral generates the carrier.
static void sample_tick(void *arg) {
    (void)arg;
    frame_t f;
    const unsigned epoch = atomic_load(&generation);
    const int64_t now = esp_timer_get_time();
    const bool delayed = last_tick_us && now - last_tick_us > MAX_TICK_GAP_US;
    last_tick_us = now;
    const bool overflow = atomic_exchange(&overrun, false);
    if (consumer_epoch != epoch || delayed || overflow ||
        !atomic_load(&streaming) || atomic_load(&rate) == 0) {
        if (active) mute();
        quiet = SILENCE_SAMPLES;
        primed = false;
        consumer_epoch = epoch;
        // Bounded drain, rather than an unbounded loop in the shared timer task.
        for (unsigned i = 0; i < QUEUE_SAMPLES; ++i)
            if (xQueueReceive(audio, &f, 0) != pdTRUE) break;
        return;
    }
    if (!primed) {
        if (uxQueueMessagesWaiting(audio) < PREFILL_SAMPLES) return;
        primed = true;
    }
    if (xQueueReceive(audio, &f, 0) != pdTRUE || f.epoch != epoch ||
        !atomic_load(&streaming) || epoch != atomic_load(&generation)) {
        if (active) mute();
        quiet = SILENCE_SAMPLES;
        primed = false;
        return;
    }
    int sample = f.pcm;
    if (abs(sample) > 150) quiet = 0;
    else if (quiet < SILENCE_SAMPLES) quiet++;
    if (quiet >= SILENCE_SAMPLES) {
        if (active) mute();
        return;
    }
    // Fixed, conservative bench-only modulation. No full-power mode.
    int width = 20 + sample * 15 / 32768;
    if (width < 5) width = 5;
    if (width > 35) width = 35;
    if (mcpwm_comparator_set_compare_value(end_a, width) != ESP_OK ||
        mcpwm_comparator_set_compare_value(end_b, HALF+width) != ESP_OK) {
        mute();
        return;
    }
    if (!atomic_load(&streaming) || epoch != atomic_load(&generation)) {
        mute();
        primed = false;
        return;
    }
    if (!active) {
        if (mcpwm_generator_set_force_level(gen_a, -1, true) != ESP_OK ||
            mcpwm_generator_set_force_level(gen_b, -1, true) != ESP_OK) {
            mute();
            return;
        }
        active = true;
    }
}

// ESP-IDF v5.4.x decoded interleaved signed 16-bit little-endian PCM.
static int16_t le16(const uint8_t *p) {
    return (int16_t)((uint16_t)p[0] | ((uint16_t)p[1] << 8));
}
static void pcm_callback(const uint8_t *data, uint32_t len) {
    static int last_rate, phase, lp1, lp2;
    static unsigned last_epoch;
    const int fs = atomic_load(&rate);
    const unsigned epoch = atomic_load(&generation);
    if (!atomic_load(&streaming) || fs == 0) return;
    if (fs != last_rate || epoch != last_epoch) {
        phase = lp1 = lp2 = 0;
        last_rate = fs;
        last_epoch = epoch;
    }
    // Two fixed one-pole low-pass stages before downsampling. Speech experiment,
    // not a hi-fi reconstruction filter. SBC stereo only.
    for (uint32_t i = 0; i + 3 < len; i += 4) {
        int mono = ((int)le16(data+i) + (int)le16(data+i+2)) / 2;
        lp1 += (mono-lp1)/5;
        lp2 += (lp1-lp2)/5;
        phase += PCM_OUT_HZ;
        if (phase >= fs) {
            phase -= fs;
            frame_t f = {.pcm = (int16_t)lp2, .epoch = epoch};
            if (xQueueSend(audio, &f, 0) != pdTRUE) atomic_store(&overrun, true);
        }
    }
}

static void a2dp_event(esp_a2d_cb_event_t event, esp_a2d_cb_param_t *p) {
    switch (event) {
    case ESP_A2D_AUDIO_CFG_EVT: {
        atomic_store(&streaming, false);
        atomic_fetch_add(&generation, 1);
        int fs = 0;
        if (p->audio_cfg.mcc.type == ESP_A2D_MCT_SBC) {
            uint8_t b = p->audio_cfg.mcc.cie.sbc[0];
            // Accept normal stereo/joint-stereo/dual-channel 44.1 or 48 kHz.
            if ((b & 0x08) == 0) {
                if (b & 0x20) fs = 44100;
                else if (b & 0x10) fs = 48000;
            }
        }
        atomic_store(&rate, fs);
        ESP_LOGI(TAG, "PCM format: %d Hz (0 = unsupported)", fs);
        break;
    }
    case ESP_A2D_AUDIO_STATE_EVT:
        atomic_store(&streaming, false);
        atomic_fetch_add(&generation, 1);
        atomic_store(&streaming, p->audio_stat.state == ESP_A2D_AUDIO_STATE_STARTED);
        break;
    case ESP_A2D_CONNECTION_STATE_EVT:
        if (p->conn_stat.state == ESP_A2D_CONNECTION_STATE_DISCONNECTED) {
            atomic_store(&streaming, false);
            atomic_store(&rate, 0);
            atomic_fetch_add(&generation, 1);
            esp_bt_gap_set_scan_mode(ESP_BT_CONNECTABLE, ESP_BT_GENERAL_DISCOVERABLE);
        } else if (p->conn_stat.state == ESP_A2D_CONNECTION_STATE_CONNECTED) {
            esp_bt_gap_set_scan_mode(ESP_BT_NON_CONNECTABLE, ESP_BT_NON_DISCOVERABLE);
        }
        break;
    default: break;
    }
}
static void gap_event(esp_bt_gap_cb_event_t event, esp_bt_gap_cb_param_t *p) {
    if (event == ESP_BT_GAP_CFM_REQ_EVT)
        esp_bt_gap_ssp_confirm_reply(p->cfm_req.bda, true);
}
void app_main(void) {
    esp_err_t r = nvs_flash_init();
    if (r == ESP_ERR_NVS_NO_FREE_PAGES || r == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        r = nvs_flash_init();
    }
    ESP_ERROR_CHECK(r);
    audio = xQueueCreate(QUEUE_SAMPLES, sizeof(frame_t));
    if (!audio) abort();
    quiet = SILENCE_SAMPLES;
    init_pwm();
    esp_timer_handle_t tick;
    const esp_timer_create_args_t args = {
        .callback = sample_tick, .dispatch_method = ESP_TIMER_TASK,
        .name = "pcm8k", .skip_unhandled_events = true
    };
    ESP_ERROR_CHECK(esp_timer_create(&args, &tick));
    ESP_ERROR_CHECK(esp_timer_start_periodic(tick, 125));
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_BLE));
    esp_bt_controller_config_t cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_bt_controller_init(&cfg));
    ESP_ERROR_CHECK(esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT));
    ESP_ERROR_CHECK(esp_bluedroid_init());
    ESP_ERROR_CHECK(esp_bluedroid_enable());
    ESP_ERROR_CHECK(esp_bt_gap_register_callback(gap_event));
    esp_bt_io_cap_t io = ESP_BT_IO_CAP_NONE;
    ESP_ERROR_CHECK(esp_bt_gap_set_security_param(ESP_BT_SP_IOCAP_MODE, &io, sizeof(io)));
    ESP_ERROR_CHECK(esp_bt_gap_set_device_name("Ultrasonic Rev A"));
    ESP_ERROR_CHECK(esp_a2d_register_callback(a2dp_event));
    ESP_ERROR_CHECK(esp_a2d_sink_init());
    ESP_ERROR_CHECK(esp_a2d_sink_register_data_callback(pcm_callback));
    ESP_ERROR_CHECK(esp_bt_gap_set_scan_mode(ESP_BT_CONNECTABLE, ESP_BT_GENERAL_DISCOVERABLE));
}
