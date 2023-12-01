// This code contains the instructions to receive a PPM pulse that encodes a message.
// In this case, unlike in raw PPM comms, the code does not decode the PPM pulses.
// Instead, it just recieves them and prints the timestamps of pulses on the serial monitor.
// An extra code is needed to decode the message, which can be found in the same folder and is written in Python.

const int PPM_PIN = 2; // A2
// define time parameters for PPM pulse and period durations
#define PPM_PULSE_WIDTH 1
#define PERIOD 256
#define LIMIT 150
// Define variables that will be used later
float pulse_time;
int counter = 0;


void setup() {
  Serial.begin(9600);  // Start the serial communication with the computer
  pinMode(PPM_PIN, INPUT); // Activate PPM pin for input
}

void loop() {
  readPPMSignal(); // Keep reading the PPm signal in loop
}

void readPPMSignal() {
  while (counter < LIMIT) { // Establish a limit on the number of timestamps the code records
    while (digitalRead(PPM_PIN) == LOW) {} // Wait for PPM pin to turn on
    if (digitalRead(PPM_PIN) == HIGH) { 
      pulse_time = millis(); // Record time at which each PPM pulse is received
      Serial.println(pulse_time); // Print each timestamp on the serial monitor

      // Serial.print(pulse_time); // Print each timestamp on the serial monitor
      // if (counter < LIMIT - 1){
      //   Serial.print(", "); // Print a comma after each timestamp except for the last one
      //}
      
      delay(PPM_PULSE_WIDTH); // Wait for the PPM pulse to end
      counter += 1;
    }
  }

}