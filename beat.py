import logging

import serial
import pygame
from pygame.locals import *
import numpy
from numpy.fft import fft
from scipy.fftpack import fft as scipy_fft

logging.basicConfig(filename='beat_debug.log',level=logging.DEBUG)


# pygame stuff
WINX = 800
WINY = 600
screen = None
background = None
surf = None
thickness = 800/8
clock = None
fon = None
#pygame.init()

def setup_pygame():
    global screen, background, surf, clock, fon
    pygame.init()
    screen = pygame.display.set_mode((WINX, WINY))
    pygame.display.set_caption('Spect graph')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    surf = pygame.Surface((WINX, WINY))
    surf.blit(background, (0, 0))
    clock = pygame.time.Clock()
    fon = pygame.font.SysFont("",16)

#pygame.display.flip()



samples = []
ser = None	# serial port object. 
biggest = 0     # largest sample we have found (in a run)
scale_size = 1 # samples get divided by this
fft_axis = 1
def open_serial():
    global ser
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200)#19200)
    except Exception as e:
        logging.warning(e, "unable to open /dev/ttyUSB0")
        try:
            ser = serial.Serial('/dev/ttyUSB0', 115200) #19200)
        except Exception as ee:
            print "err"
            logging.warning(ee,"unable to open /dev/ttyUSB0 OR /dev/ttyUSB1")
NO_FFT = True
def getSamples(num):
    global biggest
    biggest = 0
    global samples
    line = ser.readline()
    num = num*4
    try:
        logging.debug(("raw serial(type(",type(line),") ",line))
    except:
        pass
    str_samples = line.split()
    num = len(str_samples)
    try:
        logging.debug(("str length", num))
        str_samples = str_samples[1:num]
        logging.debug(str_samples[1])
    except:
        getSamples(num)
    
    ser.flush()
    logging.debug("flushed serial - ser.flush()")
    #print str_samples
    numpy_samples = []
    for s in str_samples:
        
        #if int(s) < 5:
        #    s = 0
        numpy_samples.append(int(s))
    if not NO_FFT:
        numpy_samples = numpy.fft.fft(numpy_samples,fft_axis)

    samples = []
    i = 0
    while i < len(numpy_samples):
        k = numpy_samples[i]
        #k = int(s)
        try:
            k = int(k)
        except Exception as e:
            print "ERROR:" ,e
        k = scale(k)
        samples.append(k)
        i+=1
        #i+=2
    #print samples

        



def scale(inp):
    global biggest
    if inp*-1 > biggest:
        biggest = inp*-1
    if inp > biggest:
    	biggest = inp
    if inp < 0:
        inp = inp+biggest
    if not NO_FFT:
        inp = inp/scale_size
    else:
        inp = inp*scale_size
    return inp
    
  #  print samples

font_text = "asdfasdf"
def background_ren():
    # render the background
    font_text = "Largest Value:" + str(biggest) + "    Scale Size: "+ str(scale_size) + "    FFT:"+ str(not NO_FFT)
    surf.blit(background, (0, 0))
    font_color = (255,0,0,0)
 
    fonsurf = fon.render(font_text,3, font_color)
    fonsurf = fonsurf.convert_alpha()
    fonsurf.set_alpha(150)
#    fonsurf = fonsurf.convert()
    fonsurf.set_alpha(150)
    surf.blit(fonsurf,((0,0)))

#bar graph
def bar_graph():
   # print "GRAPHING..."
    color = (255,0,0)
    color = pygame.Color(0,0,0,0)

    background_ren()
   # print samples
    k = 0
    c = 1
    numSamples = len(samples)
    try:
        numSamples = WINX/numSamples
    except Exception as e:
        print e
    numSamples *= 1
 
    if len(samples) != 0:
        inc = 255/len(samples)
    else:
        inc = 255/1
    inc *= 1
    inc = int(inc)

    for s in samples:
        s = int(s)
        if c == 1:
            if (color.r + inc) < 255:
                color.r = color.r + inc
                
            else:
                color.r = 255
#            color = (255,0,0)
        elif c==2:
            if (color.b + inc) < 255:
                color.b = color.b + inc #(0,255,0)
            else:
                color.b == 0
        else:
            if (color.g + inc) < 255:
                color.g = color.g + inc
            else:
                color.g = 0
                c = 0
            
        c+=1
#	print color
	greatest = biggest/10
#        print greatest, greatest/8, greatest/9, greatest/10, "\t", s
        color.r = 255
        i = k*numSamples
        if s < 300:
            color.r = 255
            color.g = 0
            color.b = 0
        if s < 2000:
            color.r = 100
            color.g = 255
            color.b = 0
        if s < 150:
            color.r = 100
            color.g = 255
            color.b = 200

        if s < 100:
            color.r = 0
            color.g = 255
            color.b = 0
        if s < 30:
            color.r = 0
            color.g = 0
            color.b = 255
        if s < 10:
            color.r = 255
            color.g = 100
            color.b = 50
            

        pygame.draw.line(surf, color,(i,600),(i,600-s),1*numSamples)
        
        k +=1
    screen.blit(surf,(0,0))
    pygame.display.flip()


color_count = 0
def poly_graph():
    #if color_count == 0:
    background_ren()
#    surf.blit(background, (0, 0))
    x = 0
    poly = []
    inc = 800/(len(samples)/2)

    poly.append([-1000,-1000])
    for s in samples[:len(samples)/2]:
        poly.append([x,800-s])
#        poly.append([x+inc,s])
        x += inc
    poly.append([1000,-1000])
    thickness = 1
    global color_count
    #color_count +=1
    if(color_count == 1):
        pygame.draw.polygon(surf,(255,0,0),poly,thickness)
        
    elif(color_count == 2):
        pygame.draw.polygon(surf,(0,255,0),poly,thickness)
    else:
        color_count = 0
        pygame.draw.polygon(surf,(0,0,255),poly,thickness)
    screen.blit(surf,(0,0))
    pygame.display.flip()

# line graph
def line_graph():
    surf.blit(background, (0, 0))
    background_ren()
    poly = []
    # 16px spacing - 800/48 = ~16.6
    rate = 16
    x = 0
    samp = samples
    for s in samp:
        p = [x,WINY-s]
        x+=rate
        poly.append(p)

    c = (255,0,0)
    thickness = 1
    i = 0
    while(i < len(poly)-1):
        pygame.draw.line(surf,c,poly[i],poly[i+1],thickness)
        i+=1
    screen.blit(surf,(0,0))
    pygame.display.flip()

def main():
    end = False
    setup_pygame()
    open_serial()
    graph_type = 1
    pause = False
    while not end:
        getSamples(48)
        if not pause:

            if graph_type == 1:
                bar_graph()
            if graph_type == 2:
                poly_graph()
            if graph_type == 3:
                line_graph()

        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
#                global end
                SystemExit
                end = True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
#                global end
                end = True
            if event.type == KEYDOWN and event.key == K_1:
                graph_type = 1
            if event.type == KEYDOWN and event.key == K_2:
                graph_type = 2
            if event.type == KEYDOWN and event.key == K_3:
                graph_type = 3

            if event.type == KEYDOWN and event.key == K_q:
                global scale_size
                scale_size += 2

            if event.type == KEYDOWN and event.key == K_a:
                #global scale_size
                if scale_size-2 > 0:
                    scale_size -= 2
                else:
                    scale_size = 1

            if event.type == KEYDOWN and event.key == K_w:
                global fft_axis
                fft_axis += 1

            if event.type == KEYDOWN and event.key == K_s:
                #global scale_size
                if fft_axis-1 > 0:
                    fft_axis -= 1
                else:
                    fft_axis = 0

            if event.type == KEYDOWN and event.key == K_z:
                global NO_FFT
                if NO_FFT == True:
                    NO_FFT = False
                else:
                    NO_FFT = True
                    
            if event.type == MOUSEBUTTONDOWN:
                pause = True

            if event.type == MOUSEBUTTONUP:
                pause = False
            



if __name__ == "__main__":
    logging.debug("starting program...")
    main()


"""

def test1():
    
    line = ser.readline()
    
    line = line.split()
    if len(line) > 7:
        screen.blit(background, (0, 0))
        pygame.draw.line(screen,(255,0,0),(0,WINY),(0,WINY-int(line[0])),thickness)
        pygame.draw.line(screen,(0,255,0),(100,WINY),(100,WINY-int(line[1])),thickness)
        pygame.draw.line(screen,(0,0,255),(200,WINY),(200,WINY-int(line[2])),thickness)
        pygame.draw.line(screen,(255,255,0),(300,WINY),(300,WINY-int(line[3])),thickness)
        pygame.draw.line(screen,(255,0,255),(400,WINY),(400,WINY-int(line[4])),thickness)
        pygame.draw.line(screen,(0,255,0),(500,WINY),(500,WINY-int(line[5])),thickness)
        pygame.draw.line(screen,(255,100,0),(600,WINY),(600,WINY-int(line[6])),thickness)
        pygame.draw.line(screen,(255,0,100),(700,WINY),(700,WINY-int(line[7])),thickness)
        pygame.display.flip()
        print line
"""
