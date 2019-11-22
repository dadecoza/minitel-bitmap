import sys

screen = []

# 80x72
filename = None

try:
    filename = sys.argv[1]
except Exception as e:
    print("Expected bmp filename.")
    sys.exit(0)

with open(filename, "rb") as f:
    count = 0
    f.seek(130)
    byte = f.read(1)
    line = []
    while byte:
        pixels = (list(reversed([not ((2**m) & ord(byte)) for m in range(8)])))
        for pixel in pixels:
            line.append(pixel)
        if not ((count+1) % 12):
            screen.append(line[:-16])
            line = []
        count += 1
        byte = f.read(1)

screen = list(reversed(screen))

byts = []
for row in range(24):
    for col in range(40):
        r = row*3
        c = col*2
        byte = 0

        if screen[r][c]:
            byte += 2**0

        if screen[r][c+1]:
            byte += 2**1

        if screen[r+1][c]:
            byte += 2**2

        if screen[r+1][c+1]:
            byte += 2**3

        if screen[r+2][c]:
            byte += 2**4

        if screen[r+2][c+1]:
            byte += 2**5

        byts.append(byte+32)

print("""
const PROGMEM byte bitmap[] = {%s};
byte buffer[960];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(2400);
  delay(100);
  Serial.write(12); //cls
  Serial.write(14); //graphic character mode
  memcpy_P(buffer, bitmap, 960);
  for (int i=0; i<960; i++) {
    Serial.write(buffer[i]);
  }
  Serial.write(15); // return to text mode
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(500);
}
""" % (",".join([str(i) for i in byts])))
