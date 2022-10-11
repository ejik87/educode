#include "Arduino.h"
#include <EncButton.h>  // Библиотека кнопок
#include "GyverPWM.h"

#define PWM_PIN 9 // задаем имя для Pin9
#define LEDON_PIN 13
#define BTN1_PIN 10
#define BTN2_PIN 11
#define ADC1_PIN A3

EncButton<EB_TICK, BTN1_PIN> btn1;
EncButton<EB_TICK, BTN2_PIN> btn2;

int sensorValue = 150;  // Задача задержки цикла изменения скважности PWM
bool startAccident = false;
unsigned long currentTime;
unsigned long cloopTime;
// int DELAY_VAUE = 50;

// =========================  SETUP  ================================
void setup() {
    Serial.begin(9600);
    pinMode(PWM_PIN, OUTPUT);
    pinMode(LEDON_PIN, OUTPUT);
    pinMode(ADC1_PIN, INPUT);
    btn1.attach(CLICK_HANDLER, startClick);
    currentTime = millis();  // Переменные current time и cloopTime используются для измерения временного промежутка
    Serial.println("I'm Ready!");
}

//  ================== Переключение запускатора функции PWM ===========================
void startClick() {
    startAccident = !startAccident;
    Serial.println("Click");
}

void time_loop() {
    if (millis()-currentTime>=50){
        currentTime = millis();
        btn1.tick();
        if (btn1.click()) {
            startClick();
        }
        btn2.tick();
        if (btn2.click()) {
            startClick();
        }
    }
}

// ================== Основная функция волнообразного падения ===========================
    // ========================  плавное включение светодиода  ==============================
void accident_down() {
    Serial.println("Accident down START!");
    digitalWrite(LEDON_PIN, startAccident);
    // начальное значение на Pin6 i=0, если i<=255, то прибавляем к i единицу
    for(int i=520;i<=752;) {
        time_loop();
        if (!startAccident){
            break;}
        if (millis()-cloopTime>=sensorValue){  // ставим задержку для эффекта
            sensorValue = analogRead(ADC1_PIN);
            // Serial.print("ADC: ");
            // Serial.println(sensorValue);
            cloopTime = millis();
            i++;
            PWM_20KHZ_D9(i);
            Serial.print("PWM: ");
            Serial.println(i);
        }
   }
    Serial.println("End downing");
}

    //=========================  плавное затухание светодиода  =================================
void accident_up() {
    Serial.println("Accident up START!");
    digitalWrite(LEDON_PIN, startAccident);

    // начальное значение на Pin6 i=255, если i>=255, то вычитаем от i единицу
    for(int i=752;i>=520;) {
        time_loop();
        if (!startAccident){
            break;}
        if (millis()-cloopTime>=sensorValue){  // ставим задержку для эффекта
            sensorValue = analogRead(ADC1_PIN);
            // Serial.print("ADC: ");
            // Serial.println(sensorValue);
            cloopTime = millis();
            i--;
            PWM_20KHZ_D9(i);
            Serial.print("PWM: ");
            Serial.println(i);
        }
    }
    Serial.println("End upping");
}

// ========================= LOOP ===========================
void loop() {
    btn1.tick();
    btn2.tick();
    // ======================= BTN1 =========================
    if (btn1.click()) {
        startClick();
        if (startAccident)
        {
            accident_down();
            startAccident = false;
            digitalWrite(LEDON_PIN, startAccident);
        }
    }
    // ======================= BTN2 =========================
    if (btn2.click()) {
        startClick();
        if (startAccident)
        {
            accident_up();
            startAccident = false;
            digitalWrite(LEDON_PIN, startAccident);
        }
    }
}
