"""
Student name: Yago Carballo Barroso
Module description: Audio signal handling, stereo and mono converter, signal encoding based on FM radio.
"""

def getData(file):
    # Leer archivo 'file'
    f = open(file,'rb')
    f.read(44) # Selecciono solo los bytes de datos (A partir del 44 según: http://soundfile.sapp.org/doc/WaveFormat/)
    
    data = []
    while True:
        muestra = f.read(1) 

        if not muestra:
            break

        data += muestra

    return data

def setHeader(original_file, data, mono=1):
    
    f = open(original_file,'rb')
    headerData = list(f.read(44))
    if mono:
        headerData[22] = 1 # NumChannels ([22:24] pero al ser little endian con modificar el primero podemos alternar mono/stereo)
        
        # SampleRate * 2
        # fs_str = ''.join(format(num, '02x') for num in headerData[27:23:-1])
        # fs = int(fs_str, 16) * 2
        # fs_doble_hex = format(fs, '08x')

        # fs_doble = [int(fs_doble_hex[i:i+2],16) for i in range(len(fs_doble_hex)-2, -1, -2)]

        # headerData[24:28] = fs_doble

    else:
        headerData[22] = 2 # stereo
    

    headerData += data

    return headerData


def estereo2mono(ficEste, ficMono, canal=2):
    data = getData(ficEste)

    if canal == 0:
        data_ficMono = []
        [data_ficMono.extend(data[i:i+2]) for i in range(0,len(data), 4)]
    # elif canal == 1:
    #     data_ficMono = [muestra[2:4] for muestra in data]
    # elif canal == 2:
    #     data_ficMono = [((muestra[0] + muestra[2]) / 2, (muestra[1] + muestra[3]) / 2) for muestra in data]
    # elif canal == 3:
    #     data_ficMono = [((muestra[0] - muestra[2]) / 2, (muestra[1] - muestra[3]) / 2) for muestra in data]
    else:
        print("Debe introduir un canal válido.")
    audio_mono = setHeader(ficEste, data_ficMono, mono=1)
    
    audio_bytes = bytes(audio_mono)

    with open(ficMono, 'wb') as archivo:
        archivo.write(audio_bytes)




def mono2estereo(ficIzq, ficDer, ficEste):

    data_izq = getData(ficIzq)
    data_der = getData(ficDer)
    
    data = [sum(muestra, ()) for muestra in zip(data_izq, data_der)]

    ficEste = setHeader(ficIzq, data, mono=0)


def codEstereo(ficEste, ficCod):
    dataSuma, dataResta = []
    estereo2mono(ficEste, dataSuma, canal=2)
    estereo2mono(ficEste, dataResta, canal=3)
    
    dataCod = [sum(muestra, ()) for muestra in zip(dataSuma, dataResta)]

    setHeader(ficEste, ficCod, mono=0)


# def decEstereo(ficCod, ficEste)



estereo2mono('wav/komm.wav', 'test.wav', canal=0)

