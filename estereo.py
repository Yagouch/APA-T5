"""
Student name: Yago Carballo Barroso
Module description: Audio signal handling, stereo and mono converter, signal encoding based on FM radio.
"""

def getData(file):
    # Leer archivo 'file'
    f = open(file,'rb')
    
    # Selecciono solo los bytes de datos (A partir del 44 según: http://soundfile.sapp.org/doc/WaveFormat/)
    f.read(44)
    data = list(f.read())

    return data

def setHeader(original_file, data, mono=1):
    
    f = open(original_file,'rb')
    headerData = list(f.read(44))
    if mono:
        headerData[22] = 1 # NumChannels ([22:24] pero al ser little endian con modificar el primero podemos alternar mono/stereo)
    else:
        headerData[22] = 2 # stereo
    
    headerData += data

    return headerData

def writeData(file, name):
    audio_bytes = bytes(file)

    with open(name, 'wb') as archivo:
        archivo.write(audio_bytes)

def estereo2mono(ficEste, ficMono, canal=2):
    data = getData(ficEste)

    if canal == 0:
        data_ficMono = []
        [data_ficMono.extend(data[i:i+2]) for i in range(0,len(data), 4)]

        audio_mono = setHeader(ficEste, data_ficMono, mono=1)
    elif canal == 1:
        data_ficMono = []
        [data_ficMono.extend(data[i:i+2]) for i in range(2,len(data), 4)]

        audio_mono = setHeader(ficEste, data_ficMono, mono=1)
    elif canal == 2:
        data_ficMono = []
        [data_ficMono.extend([int(data[i]/2+data[i+2]/2), int(data[i+1]/2+data[i+3]/2)]) for i in range(0,len(data), 4)]

        audio_mono = setHeader(ficEste, data_ficMono, mono=1)
    elif canal == 3:
        data_ficMono = []
        [data_ficMono.extend([abs(int(data[i]/2-data[i+2]/2)), abs(int(data[i+1]/2-data[i+3]/2))]) for i in range(0,len(data), 4)]

        audio_mono = setHeader(ficEste, data_ficMono, mono=1)

    else:
        print("Debe introduir un canal válido.")

    writeData(audio_mono, ficMono)


def mono2estereo(ficIzq, ficDer, ficEste):

    data_izq = getData(ficIzq)
    data_der = getData(ficDer)
    
    data_Este = []

    [data_Este.extend([data_izq[i], data_izq[i+1], data_der[i], data_der[i+1]]) for i in range(0, len(data_der), 2)]

    audio_Este = setHeader(ficIzq, data_Este, mono=0)

    writeData(audio_Este, ficEste)


def codEstereo(ficEste, ficCod):
    dataSuma, dataResta = []
    estereo2mono(ficEste, dataSuma, canal=2)
    estereo2mono(ficEste, dataResta, canal=3)
    
    dataCod = [sum(muestra, ()) for muestra in zip(dataSuma, dataResta)]

    setHeader(ficEste, ficCod, mono=0)


# def decEstereo(ficCod, ficEste)

if __name__ == '__main__':

    estereo2mono('wav/komm.wav', 'wav/komm_e2m0.wav', canal=0)
    estereo2mono('wav/komm.wav', 'wav/komm_e2m1.wav', canal=1)
    estereo2mono('wav/komm.wav', 'wav/komm_e2m2.wav', canal=2)
    estereo2mono('wav/komm.wav', 'wav/komm_e2m3.wav', canal=3)

    mono2estereo('wav/komm_e2m0.wav', 'wav/komm_e2m1.wav', 'wav/komm_m2e.wav')



