# generate and save a .wav file from scratch
from random import randint, sample
from math import sin, pi

def generateRandom(duration, sampleRate, maxAmp):
    samples = []
    # loops and iterates through all samples 
    for _ in range(0, duration * sampleRate):
        # adds a random value to sample list between 0 and given maximum
        samples.append(randint(0,maxAmp))
    return samples


def generateSin(freq, duration, sampleRate, maxAmp):
    samples = []
    # iterates through all samples as defined by duration and samplerate
    for i in range(0, duration * sampleRate):
        # creates a loop of rising value and repeating after reaching top, whatever the freq is set to
        x = i % freq
        # this makes it on a scale of 0-1 instead of 0-frequency value
        x /= freq
        # changes range from a range of -1 to 1 to half of 255 to 255.
        y = int(sin((x)+1)*255/2)
        # appending the sin'ed looping value to the samples list
        samples.append(y)
    return samples

def generateSq(freq, duration, sampleRate, maxAmp):
    samples = []
    switcher = False
    counter = 0
    for i in range(0,duration * sampleRate):
        if switcher == False:
            x = 0
            if counter < freq:
                counter +=1
            elif counter >= freq:
                switcher = True
                counter = 0
        elif switcher == True:
            x = 255
            if counter < freq:
                counter +=1
            elif counter >= freq:
                switcher = False
                counter = 0
        samples.append(x)
    return samples

def generateTri(freq, duration, sampleRate, maxAmp):
    samples = []
    for i in range(0, duration * sampleRate):
        x = i % (sampleRate/freq)
        x /= (sampleRate/freq)
        if x < 0.5:
            y = int(2*x*maxAmp)
        else:
            y = 2*maxAmp-int(2*x*maxAmp)
        samples.append(y)
    return samples

def generateSaw(freq, duration, sampleRate, maxAmp):
    samples = []
    for i in range(0, duration * sampleRate):
        x = i % (sampleRate/freq)
        x/= (sampleRate/freq)
        y=int(x*255)
        samples.append(y)
    return samples


def save(fname, samples):
    sizeOfWavHeader = 16
    wavTypeFormat = 0x01
    channels = 1
    sampleFreq = 44100
    bitsPerSample = 8
    dataRate = sampleFreq * bitsPerSample // 8
    sizeOfData = len(samples)*bitsPerSample//8
    blockAlignment = dataRate * channels
    sizeOfFile = sizeOfData + sizeOfWavHeader
    f = open(fname,"wb")
    # writes the WAV magic number "RIFF" to signal the filetype. This is written in binary via .encode().
    # based on .WAV specifications from https://www.isip.piconepress.com/projects/speech/software/tutorials/production/fundamentals/v1.0/section_02/s02_01_p05.html
    f.write("RIFF".encode())   
    f.write(sizeOfFile.to_bytes(4,'little'))
    f.write("WAVE".encode())
    f.write("fmt ".encode())
    f.write(sizeOfWavHeader.to_bytes(4,'little'))
    f.write(wavTypeFormat.to_bytes(2,'little'))
    f.write(channels.to_bytes(2,'little'))
    f.write(sampleFreq.to_bytes(4,'little'))
    f.write(dataRate.to_bytes(4,'little'))
    f.write(blockAlignment.to_bytes(2,'little'))
    f.write(bitsPerSample.to_bytes(2,'little'))
    f.write("data".encode())
    f.write(sizeOfData.to_bytes(4,'little'))
    for sample in samples:
        f.write(sample.to_bytes(bitsPerSample//8,'little'))



save("test.wav",generateSq(440,5,44100,255))