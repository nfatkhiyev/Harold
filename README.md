# Harold
CSH Harold Music RPi Script

HAROLD or Heralding Arrival by a Really Obnoxiously Loud Device is a device that plays music from Audiophiler https://github.com/sgreene570/audiophiler
, a music storage service for Computer Science House, whenever an iButton is scanned.

It uses a Raspberry Pi to make API calls to Audiophiler to get the song from an s3 bucket and then plays the first 30 sec. 

Currently it is working on the service branch. An update is coming soon where a light bar will react to the music played by Harold.
