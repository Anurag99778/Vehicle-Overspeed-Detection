#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "your-SSID";
const char* password = "your-PASSWORD";
const char* server = "http://your-server-ip:8080";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    String url = server;
    url += "/parent-alert/?lat=28.6139&lon=77.2090&vehicle_number=DL5SAB9876";
    
    http.begin(url);
    int httpCode = http.GET();
    
    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.println("Error in sending GET request");
    }
    
    http.end();
  }
  delay(60000);  // Send data every minute
}
