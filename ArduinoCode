#include "OneWire.h"
#include <DallasTemperature.h>
#include "DHT.h"
#include <DS1307RTC.h>
#include <Time.h>
#include <Wire.h> 
//#include <ESP8266WiFi.h>   

uint8_t pump_pin = 2;
uint8_t fitoLenta_pin = 3;
uint8_t light1_pin = 4;
uint8_t light2_pin = 5;
uint8_t light3_pin = 6;
uint8_t DHT11_pin = 7;
uint8_t water_level_pin = 8;
uint8_t plantStrip = 9;
uint8_t Twater_pin = 10;

 //эти две строчки не удалять и не менять
  const char* dwHost = "rapidfarm.club";
  int dwPort = 80;
// а это разкомментить только если работаешь с ESP8266 + разкоменнить include
 /* const char* ssid = "5G_DONSTU_M";
  const char* password = "{@univer2019donstu}";
  WiFiClient client; */



DHT dht(DHT11_pin, DHT11);  // Reading temperature or humidity takes about 250 milliseconds!

OneWire water_temp(Twater_pin);
DallasTemperature water_sensor(&water_temp);


String inSer = "";
boolean strFull = false;
tmElements_t datetime;

int pause = 1000;

float currentTemperatureDHT11=0;
float lastTemperatureDHT11=0;

float currentHumidity=0;
float lastHumidity=0;

byte LightStatement = NULL;
byte PumpStatement = NULL;

float currentTemperatureDS18B20=0;
float lastTemperatureDS18B20=0;
float water_temperature=0;

void setup() 
{
  Serial.begin(115200);
  dht.begin();
  water_sensor.begin();
  pinMode(fitoLenta_pin,OUTPUT);
  pinMode(water_level_pin,INPUT);
  pinMode(pump_pin,OUTPUT);


}

void loop()
{
                                                       // пришли данные времени по serial для времени

      if (strFull) 
      {
         datetime.Hour=(int(inSer[11])-48)*10+(int(inSer[12])-48);
         datetime.Minute=(int(inSer[14])-48)*10+(int(inSer[15])-48);
         datetime.Second=(int(inSer[17])-48)*10+(int(inSer[18])-48);
         datetime.Day=(int(inSer[0])-48)*10+(int(inSer[1])-48);
         datetime.Month=(int(inSer[3])-48)*10+(int(inSer[4])-48);
         datetime.Year=CalendarYrToTm((int(inSer[6])-48)*1000+(int(inSer[7])-48)*100+(int(inSer[8])-48)*10+(int(inSer[9])-48));


        RTC.write(datetime); // записать данные в DS3231
         // очистить строку
         inSer = "";
         strFull = false;
      }

      // получение данных из ds3231
      if (RTC.read(datetime)) 
      {
         print2(datetime.Hour, ":");
         print2(datetime.Minute, ":");
         print2(datetime.Second, " ");
         print2(datetime.Day, "/");
         print2(datetime.Month, "/");
         print2(tmYearToCalendar(datetime.Year) ,"");
         Serial.println();
      }

      else 
      {
           Serial.print("error");
            delay(5000);
      }

      delay(1000);//дальше датчики


  
 currentTemperatureDHT11 = dht.readTemperature();  //читаем температуру с dht11
   if(currentTemperatureDHT11 != lastTemperatureDHT11)
  {
   Serial.print(F(" Last_Air_Temperature: "));
   Serial.print(lastTemperatureDHT11 );      
   Serial.println(F("°C "));       
   lastTemperatureDHT11=currentTemperatureDHT11;
  }
  

   
 currentHumidity=dht.readHumidity();    //читаем влажность с dht11
  if(currentHumidity != lastHumidity)
  {
   Serial.print(F("Last_Humidity: "));   
   Serial.print(currentHumidity );
   Serial.println("%");    
   lastHumidity=currentHumidity;
  }



   currentTemperatureDS18B20 = water_sensor.getTempCByIndex(0);//читаем температуру воды
  if(currentTemperatureDS18B20 != lastTemperatureDS18B20)
  {   
   water_sensor.requestTemperatures();
   Serial.print(F("Last_Water_Temperature: "));   
   Serial.print(water_sensor.getTempCByIndex(0) );
   Serial.println("°C ");    
   lastTemperatureDS18B20=lastTemperatureDS18B20;
  }



   if(datetime.Hour>=10 and datetime.Hour<= 20)//свет
    {
      digitalWrite(fitoLenta_pin,HIGH);
    }    
    
   else{      digitalWrite(fitoLenta_pin,LOW);      }

   
   
   if(digitalRead(water_level_pin==HIGH))//насос
    {
      digitalWrite(pump_pin,LOW);
    }

   if(digitalRead(water_level_pin==LOW))
    {
      digitalWrite(pump_pin,HIGH);
    }

// delay(pause);
 SendDataSerial(LightStatement,
                  currentTemperatureDHT11,
                  currentTemperatureDS18B20,
                  PumpStatement,
                  currentHumidity,
                  String(RTC.read(datetime)),
                  String("NONE")
                 );
}

   void print2(int nn,String str)           //для времени
   {
      if (nn >= 0 && nn < 10)
         { Serial.print("0");}
      Serial.print(nn);
      Serial.print(str);
   }

   void serialEvent() 
   {
      while (Serial.available())
      {
         // получить очередной байт:
         char c = (char)Serial.read();
         // добавить в строку
         inSer += c;
         // /n - конец передачи
         if (c == '\n')
            { strFull = true;}
      }
   }
   //больше не для времени

void SendDataSerial(
              byte LightStatement,
              float AirTemp,
              float WaterTemp,
              byte PumpStatement,
              float Humidity,
              String ArduinoDateTime,
              String AdditInfo){
                Serial.print(String("POST /new_data?Humidity=") + String(Humidity) +
                                                String("&LightStatement=") + String(LightStatement)+
                                                String("&AirTemp=") + String(AirTemp)+
                                                String("&WaterTemp=") + String(WaterTemp)+
                                                String("&ArduinoDateTime=") + String(ArduinoDateTime)+
                                                String("&AdditInfo=") + String(AdditInfo)
                                                + String(" HTTP/1.1\r\n") +
                      String("Host: ") + String(dwHost) + String("\r\n") +
                      String("Connection: close\r\n\r\n"));
}

/*void SendDataESP(
              byte LightUpper,
              byte LightLower,
              byte AirTemp,
              byte WaterTemp,
              byte Humidity,
              String DateTime,
              String AdditInfo){


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  if (client.connect(dwHost, dwPort)) {
    String dweetStr = String("POST /new_data?Humidity=") + String(Humidity) + " HTTP/1.1\r\n" +
                      "Host: " + String(dwHost) + "\r\n" +
                      "Connection: close\r\n\r\n";
    client.print(dweetStr);
    Serial.println(dweetStr);
    }
  }*/
