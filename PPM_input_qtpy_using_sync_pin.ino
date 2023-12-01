// This code contains the instructions to receive a PPM pulse that encodes a message.
// To do this, the code first reads a synchronization pulse through a different pin whose end marks the beginning of the
// PPM transmission. After this, PPM pulse is transformed to ASCII, which is decoded into a readable character.
// This new caharcter is printed on the serial monitor. This process is repeated for however many iterations until
// the message has been fully received. 

const int PPM_PIN = 2; // A2
const int SYNC_PIN = 3; // A3
// define time parameters for PPM pulse, sync pulse and period durations
#define PPM_PULSE_WIDTH 1
#define SYNC_PULSE_WIDTH 100
#define PERIOD 256
// Define variables that will be used later
bool syncSignalReceived = false; // Control variable for whether the sync signal has been received
float start_time;
float pulse_time;
float time_difference;
int asciiValue;



void setup() {
  Serial.begin(9600);  // Start the serial communication with the computer

  pinMode(SYNC_PIN, INPUT); // Activate sync pin for input
  pinMode(PPM_PIN, INPUT); // Activate PPM pin for input
}

void loop() {
  receiveSyncSignal(); // Call function to send sync signal
  
  if (syncSignalReceived) { // Only call function to send PPM signal if sync signal has been sent
    readPPMSignal();

  }
}

void receiveSyncSignal() {
  if (digitalRead(SYNC_PIN) == HIGH) {
    while (digitalRead(SYNC_PIN) == HIGH) {} // Wait for the sync pin to turn off
    if (digitalRead(SYNC_PIN) == LOW) {
      syncSignalReceived = true; // Change control variable to true so that PPM signal can be sent
    }
  }
}


void readPPMSignal() {
  while (digitalRead(SYNC_PIN) == LOW) { 
    start_time = millis(); // Record time at which the PPM period starts
    while (digitalRead(PPM_PIN) == LOW) {} // Wait for PPM pin to turn on
    if (digitalRead(PPM_PIN) == HIGH) { 
      pulse_time = millis(); // Record time at which the PPM pulse is received
      time_difference = pulse_time - start_time; // Compute difference
      delay(PERIOD - time_difference); // Wait for the PPM period to end

      asciiValue = round(time_difference / PPM_PULSE_WIDTH); // Calculate ASCII corresponding to character
      char character = (char) asciiValue; // Transform ASCII to character
      Serial.print(character);     
    }
  }
  Serial.println(" ");
  Serial.println("===================");  
  syncSignalReceived = false; // Change value of control variable
}