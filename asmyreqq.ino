#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

const int buzzer_Pin1 = 9; // First buzzer pin
const int buzzer_Pin2 = 10; // Second buzzer pin
const int button_1 = A0;
const int button_2 = A1;
const int button_3 = A2;
bool button_1_status = LOW;
bool button_2_status = LOW;
bool button_3_status = LOW;

static int party_1_count = 0;
static int party_2_count = 0;
static int party_3_count = 0;

String winner_name = "";

// Define debounce delay
const int debounceDelay = 50;

void setup() {
  pinMode(buzzer_Pin1, OUTPUT); // First buzzer pin
  pinMode(buzzer_Pin2, OUTPUT); // Second buzzer pin
  pinMode(button_1, INPUT);
  pinMode(button_2, INPUT);
  pinMode(button_3, INPUT);
  Serial.begin(9600);
  lcd.begin(16, 2); // Changed to 16 columns and 4 rows
  lcd.print("Electronic");
  lcd.setCursor(3, 1); // Set cursor to the second row
  lcd.print("Vote Machine");
  delay(3000);
}

void loop() {
  byte a;
  lcd.clear();
  delay(100);
  lcd.print("Scan Your Face");
  delay(1000);
  if (Serial.available()) {
    a = Serial.read();
    if (a == 'a') {
      lcd.clear();
      lcd.print("Give Your Vote");
      while (1) {
        button_1_status = digitalRead(button_1);
        delay(debounceDelay);
        button_2_status = digitalRead(button_2);
        delay(debounceDelay);
        button_3_status = digitalRead(button_3);
        delay(debounceDelay);

        if (button_1_status == HIGH) {
          party_1_count++;
          digitalWrite(buzzer_Pin1, HIGH); // First buzzer on
          digitalWrite(buzzer_Pin2, HIGH); // Second buzzer on
          delay(1000);
          digitalWrite(buzzer_Pin1, LOW);
          digitalWrite(buzzer_Pin2, LOW);
          delay(1000);
          lcd.clear();
          lcd.print("Vote Taken");
          delay(1000);
          Serial.println("Vote Taken"); // Send message over serial
          break; // Exit the loop after vote is taken
        } else if (button_2_status == HIGH) {
          party_2_count++;
          digitalWrite(buzzer_Pin1, HIGH); // First buzzer on
          digitalWrite(buzzer_Pin2, HIGH); // Second buzzer on
          delay(1000);
          digitalWrite(buzzer_Pin1, LOW);
          digitalWrite(buzzer_Pin2, LOW);
          delay(1000);
          lcd.clear();
          lcd.print("Vote Taken");
          delay(1000);
          Serial.println("Vote Taken"); // Send message over serial
          break; // Exit the loop after vote is taken
        } else if (button_3_status == HIGH) {
          party_3_count++;
          digitalWrite(buzzer_Pin1, HIGH); // First buzzer on
          digitalWrite(buzzer_Pin2, HIGH); // Second buzzer on
          delay(1000);
          digitalWrite(buzzer_Pin1, LOW);
          digitalWrite(buzzer_Pin2, LOW);
          delay(1000);
          lcd.clear();
          lcd.print("Vote Taken");
          delay(1000);
          Serial.println("Vote Taken"); // Send message over serial
          break; // Exit the loop after vote is taken
        }
      }
    } else if (a == 'c') {
      while (1) {
        if ((party_1_count > party_2_count) && (party_1_count > party_3_count)) {
          winner_name = "A";
        } else if ((party_2_count > party_1_count) && (party_2_count > party_3_count)) {
          winner_name = "B";
        } else if ((party_3_count > party_1_count) && (party_3_count > party_2_count)) {
          winner_name = "C";
        } else if ((party_3_count == party_1_count) && (party_3_count == party_2_count) && (party_1_count == party_2_count)) {
          lcd.print("Tie.");
          delay(1000);
        } else if ((party_3_count == party_1_count == party_2_count == 0)) {
          lcd.print("No vote detected.");
        } else {
        }
        lcd.clear();
        delay(100);
        lcd.print("Winner:" + String(winner_name));
        lcd.setCursor(3, 1); // Set cursor to the second row
        lcd.print(winner_name);
        lcd.setCursor(0, 1);
        lcd.print("A:" + String(party_1_count) + " B:" + String(party_2_count) + " C:" + String(party_3_count));
        delay(1000);
      }
    } else if (a == 'b') {
      lcd.clear();
      lcd.print("Invalid Person");
      delay(1000);
      digitalWrite(buzzer_Pin1, HIGH); // First buzzer on
      digitalWrite(buzzer_Pin2, HIGH); // Second buzzer on
      delay(1000);
      digitalWrite(buzzer_Pin1, LOW);
      digitalWrite(buzzer_Pin2, LOW);
      delay(1000);
    } else if (a == 'e') {
      lcd.clear();
      lcd.print("Already Voted");
      delay(1000);
      digitalWrite(buzzer_Pin1, HIGH); // First buzzer on
      digitalWrite(buzzer_Pin2, HIGH); // Second buzzer on
      delay(1000);
      digitalWrite(buzzer_Pin1, LOW);
      digitalWrite(buzzer_Pin2, LOW);
      delay(1000);
    } else if (a == 'f') {
      lcd.clear();
      lcd.print("Face Not Recognized");
      delay(1000);
      digitalWrite(buzzer_Pin1, HIGH); // First buzzer on
      digitalWrite(buzzer_Pin2, HIGH); // Second buzzer on
      delay(1000);
      digitalWrite(buzzer_Pin1, LOW);
      digitalWrite(buzzer_Pin2, LOW);
      delay(1000);
    } else {
      // Do nothing
    }
  }
}
