"""
Student name: Yago Carballo Barroso
Module description: Audio signal handling, stereo and mono converter, signal encoding based on FM radio.
"""

import struct

def getData(file):

    with open(file, 'rb') as f:
    
        header_raw = f.read(44)
        data_raw = f.read()


    header = [_ for _ in header_raw] 
    print(header[22])

    data = []
    [data.extend(struct.unpack('h', data_raw[i:i+2])) for i in range(0, len(data_raw), 2)]

    return data, header
  

def setData(header, data, name, mono=True, size=0):

    if mono:
        header[22] = 1
    else:
        header[22] = 2

    print(header[22])
    if size:
        size_hex = hex(size)[2:].zfill(8)
        size_hex_le = ''.join( [size_hex[i:i+2] for i in range(len(size_hex)-2,-1,-2)] )
        header[40:44] = [int(size_hex_le[i:i+2], 16) for i in range(0, len(size_hex_le), 2)]
        
    data_bytes = struct.pack('<'+ 'h' * len(data), *data)
    header_bytes = struct.pack('B' * len(header), *header)

    print(header_bytes)
    # audio = header_bytes + data_bytes

    with open(name, 'wb') as archivo:
        archivo.write(header_bytes)
        archivo.write(data_bytes)


def estereo2mono(ficEste, ficMono, canal=2):
    data, header = getData(ficEste)
    data_ficMono = []

    if canal == 0:
        [data_ficMono.append(data[i]) for i in range(0,len(data), 2)]

    elif canal == 1:
        [data_ficMono.append(data[i]) for i in range(1,len(data), 2)]

    elif canal == 2:
        [data_ficMono.extend([int(data[i]/2+data[i+2]/2), int(data[i+1]/2+data[i+3]/2)]) for i in range(0,len(data), 4)]
        print(data_ficMono)

    elif canal == 3:
        [data_ficMono.extend([abs(int(data[i]/2-data[i+2]/2)), abs(int(data[i+1]/2-data[i+3]/2))]) for i in range(0,len(data), 4)]

    else:
        print("Debe introduir un canal válido.")

    setData(header, data_ficMono, ficMono, mono=True)
    


# def mono2estereo(ficIzq, ficDer, ficEste):

#     data_izq = getData(ficIzq)
#     data_der = getData(ficDer)
    
#     data_Este = []
#     [data_Este.extend([data_izq[i], data_izq[i+1], data_der[i], data_der[i+1]]) for i in range(0, len(data_der), 2)]

#     audio_Este = setHeader(ficIzq, data_Este, mono=0)
#     writeData(audio_Este, ficEste)


# def codEstereo(ficEste, ficCod):
#     dataEste = getData(ficEste)

#     data_ficCod = []
#     [data_ficCod.extend([ int( (dataEste[i] + dataEste[i+2]) / 2 ), int( (dataEste[i+1] + dataEste[i+3]) / 2 ), int( (dataEste[i] - dataEste[i+2]) / 2 ), int( (dataEste[i+1] - dataEste[i+3]) / 2 ) ]) for i in range(0,len(dataEste), 4)]

#     audio_cod = setHeader(ficEste, data_ficCod, mono=1)
#     writeData(audio_cod, ficCod)


# def decEstereo(ficCod, ficEste):
#     dataCod = getData(ficCod)

#     dataEste = [] 
#     [dataEste.extend([int((dataCod[i] - dataCod[i+2]) / 2), int((dataCod[i+1] - dataCod[i+3]) / 2), int((dataCod[i] + dataCod[i+2]) / 2), int((dataCod[i+1] + dataCod[i+3]) / 2)]) for i in range(0, len(dataCod), 4)]

#     audioEste = setHeader(ficCod, dataEste, mono=0)
#     writeData(audioEste, ficEste)


if __name__ == '__main__':

    estereo2mono('wav/komm.wav', 'wav/komm_e2m0.wav', canal=0) 
    # estereo2mono('wav/komm.wav', 'wav/komm_e2m1.wav', canal=1)
    # estereo2mono('wav/komm.wav', 'wav/komm_e2m2.wav', canal=2)
    # estereo2mono('wav/komm.wav', 'wav/komm_e2m3.wav', canal=3)

    # mono2estereo('wav/komm_e2m0.wav', 'wav/komm_e2m1.wav', 'wav/komm_m2e.wav')

    # codEstereo('wav/komm.wav', 'wav/test.wav')
    # decEstereo('wav/test.wav', 'wav/testDECO.wav')



    # # Número entero negativo que queremos empaquetar
    # numero_negativo = -42

    # # Empaquetar el número usando complemento a dos (formato 'i' para enteros)
    # bytes_complemento_dos = struct.pack('i', numero_negativo)

    # print("Bytes con complemento a dos:", bytes_complemento_dos)

    # # Desempaquetar los bytes para obtener el número original
    # numero_desempaquetado = struct.unpack('i', bytes_complemento_dos)[0]

    # print("Número desempaquetado:", numero_desempaquetado)

    data, header = getData('wav/komm.wav')

    setData(header, data, 'wav/test.wav', mono=False)



