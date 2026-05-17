# Tinnitus Calibrator

### Why this repo

The idea of this repository comes from the observation that many people live with tinnitus (approximately half the people) including me. This simple app allows us to replicate our tinnitus using the frequency and volume metrics. We can also save the parameters we've entered to get a sound and thus, we can shared our different sounds (parameters). The goal is obviously not to compare each other's tinnitus and pain but to understand and see how annoying it is to live with tinnitus. I'm posting this because I never seen something like this before so it may be nice.

### The features

So, this is a simple app where you can play a sinusoidal sound and change its volume and frequency. So, you are able to match your tinnitus with a sound. Having done it myself, it requires some focus and a quiet as possible environment (headphones or a headset are recommended). Then, you can save the parameters you have entered, that match you tinnitus, as a formatted JSON file. It does withoout saying that you can also load back your own other people files.

As an example, I tried my best to replicate my own tinnitus and I dropped the parameters is this repo. If I got other examples I'll drop them here too.

### The main issue

One practical issue is that the output volume of the sound depends on many factors like your device volume level, the volume you selected on the app, your hearing sensitivity... So, one solution I've found is to calibrate the volume once before loading or saving sounds parameters. 
You start playing a sound and you decrease the volume progressively until you are no longer able to hear the sound. Now you can calibrate the volume and with that done, when you will save or load parameters, your hearing sensibility will be taken in account. 

With that said, I think the volume scale can be considered as linear (that is on what the entire calibration system is based) but there is, for sure, room to improve this system.

I think this is pretty straight forward, if I notice anything that I can explain here, I will do it. 
