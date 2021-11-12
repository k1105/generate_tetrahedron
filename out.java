import nervoussystem.obj.*;
import processing.opengl.*;

float a;
int NUM = 8;     
float offset = PI/NUM;
color[] colors = new color[NUM];
boolean record = false;

void setup() { 
  fullScreen(P3D);
  noStroke();
  colorMode(HSB,90,100,10,100);
   frameRate(30);
  for(int i=0;  i < NUM;  i++) {
    colors[i] = color(i*8+100,60,100,90);
  }
}

void draw() {     
  background(0);
  ambientLight(63, 90, 31);
  directionalLight(255,5,255,-1,0,0);
  pointLight(63, 127, 255, mouseX, mouseY, 200);
  spotLight(100, 100, 100, mouseX, mouseY, 200, 0, 0, -1, PI, 2);
  
   if (record) {
    beginRecord("nervoussystem.obj.OBJExport", "PATH TO DIRECTORY"+millis()+".obj");
  }
 
  
  translate(width/2, height/2, -50);
  rotateX(mouseY / 100.0);
  rotateY(mouseX / 100.0);
  for(int i=0;  i < NUM;  i++) {
    pushMatrix();
    fill(colors[i]);

    /* paste code here */

    popMatrix();
  }
  
  if (record) {
    endRecord();
    record = false;
  }
  
  a+=0.01;  
}

void mousePressed() {
  record = true;
}
