// This code contains the instructions to emit a PPM pulse that encodes a message.
// To do this, the code first emits a synchronization pulse through a different pin whose end marks the beginning of the
// PPM transmission. After this, every character from the message is individually encoded to ASCII and the
// corresponding number is sent using PPM.

const int PPM_PIN = 28; // A2 in feather
const int SYNC_PIN = 29; // A3 in feather
// define time parameters for PPM pulse, sync pulse and period durations
#define PPM_PULSE_WIDTH 1
#define SYNC_PULSE_WIDTH 100
#define PERIOD 256
String message = "Hello World!"; // Create the message that we want to send in string form

void setup() {
  Serial.begin(9600);  // Start the serial communication with the computer

  pinMode(SYNC_PIN, OUTPUT); // Activate sync pin for output
  pinMode(PPM_PIN, OUTPUT); // Activate PPM pin for output
}

void loop() {
  // Call functions to send the sync and PPM signals one after the other for each iteration of the message
  generateSyncSignal();
  generatePPMSignal();
}

void generateSyncSignal() {
  // Turn sync pin on, then wait for the duration of the sync pulse, and then turn it off
  digitalWrite(SYNC_PIN, HIGH);
  delay(SYNC_PULSE_WIDTH);
  digitalWrite(SYNC_PIN, LOW);
}

void generatePPMSignal() {
  // Use 'for' loop to iterate over each character of the message string to send it individually 
  for (int i = 0; i < message.length(); i++) {
    int asciiValue = message.charAt(i); // Convert character to ASCII number
    delay(PPM_PULSE_WIDTH*asciiValue); // Wait until it is time to emit the PPM pulse corresponding to the character
    // Turn PPM pulse on for the corresponding duration and then turn it off 
    digitalWrite(PPM_PIN, HIGH);
    delay(PPM_PULSE_WIDTH);
    digitalWrite(PPM_PIN, LOW);
    delay(PERIOD - PPM_PULSE_WIDTH - PPM_PULSE_WIDTH*asciiValue); // Wait for the rest of the duration of the PPM period
  }
}