int RL1 = 8;
int RL2 = 9;
int RL3 = 10;
int RL4 = 11;

int a = 0;
int b = 0;
int c = 0;
int d = 0;
int e = 0;
int f = 0;
int g = 0;
int h = 0;
int value = 0;

void setup() {
  pinMode(RL1, OUTPUT);
  pinMode(RL2, OUTPUT);
  pinMode(RL3, OUTPUT);
  pinMode(RL4, OUTPUT);
  digitalWrite(RL1, HIGH);
  digitalWrite(RL2, HIGH);
  digitalWrite(RL3, HIGH);
  digitalWrite(RL4, HIGH);
  Serial.begin(9600);
  Serial.println("Connection established...");
}

void loop()
{ while (Serial.available())
  {
    value = Serial.read();
  }
  if (a < 1 and value == '1') {
    a = a + 1;
    digitalWrite(RL1, LOW);
    delay (100);
    digitalWrite(RL1, HIGH);
    b = c = d = e = f = g = h = 0;
  }

  if (e < 1 and value == '2') {
    e = e + 1;
    digitalWrite(RL1, LOW);
    delay (100);
    digitalWrite(RL1, HIGH);
    a = b = c = d = f = g = h = 0;
  }
  
  if (b < 1 and value == '3') {
    b = b + 1;
    digitalWrite(RL2, LOW);
    delay (100);
    digitalWrite(RL2, HIGH);
    a = c = d = e = f = g = h = 0;
  }
  
    if (f < 1 and value == '4') {
    f = f + 1;
    digitalWrite(RL2, LOW);
    delay (100);
    digitalWrite(RL2, HIGH);
    a = b = c = d = e = g = h = 0;  
  }
  {
  if (c < 1 and value == '5') {
    c = c + 1;
    digitalWrite(RL3, LOW);
    delay (100);
    digitalWrite(RL3, HIGH);
    a = b = d = e = f = g = h = 0;
  }
  if (g < 1 and value == '6') {
    g = g + 1;
    digitalWrite(RL3, LOW);
    delay (100);
    digitalWrite(RL3, HIGH);
    a = b = c = d = e = f = h = 0;
  }
  if (d < 1 and value == '7') {
    d = d + 1;
    digitalWrite(RL4, LOW);
    delay (100);
    digitalWrite(RL4, HIGH);
    a = b = c = e = f = g = h = 0;
  }
  if (h < 1 and value == '8') {
    h = h + 1;
    digitalWrite(RL4, LOW);
    delay (100);
    digitalWrite(RL4, HIGH);
    a = b = c = d = e = f = g = 0;
  }
}
}
