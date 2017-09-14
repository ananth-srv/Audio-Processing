import wave
import pandas as pd

srtfile = open("D:/Docs/Audio/Movies/Autograph/Autograph-srt.txt",'r')
start_count = 0
data = srtfile.readlines()
print(data[0])
count = 0
text = []
file = []
next_data = 'count'
for i in data:
    i = i.rstrip('\n')
    print(i)
    if i == str(count+1):
        file_count = start_count + int(i)
        outfile = "D:/Docs/Audio/Movies/Autograph/" + str(file_count) + ".wav"
        wout = wave.open(outfile, 'wb')
        next_data = 'time'
        print('out', outfile)
        file.append(str(file_count))
        text_sub = count
        count = count + 1
    elif next_data == 'time':
        print('get time in seconds - hour', i[0:2], 'minute', i[3:5], 'seconds', i[6:8])
        win = wave.open('D:/Docs/Audio/Movies/Autograph/out.wav', 'rb')
        framrt = win.getframerate()
        start_seconds = int(i[0:2]) * 3600 + int(i[3:5]) * 60 + int(i[6:8]) + int(i[9:12]) * 0.001
        end_seconds = int(i[17:19]) * 3600 + int(i[20:22]) * 60 + int(i[23:25]) + int(i[26:29]) * 0.001 + 0.40
        print('start', start_seconds)
        print('end', end_seconds)
        next_data = 'text'
        s0, s1 = round(int(start_seconds * framrt)), round(int(end_seconds * framrt))
        win.readframes(s0)  # discard
        print('s1', s1)
        frames = win.readframes(s1 - s0)
        wout.setparams(win.getparams())
        wout.writeframes(frames)
        win.close()
        wout.close()
        print('write out complete')
    elif next_data == 'text':
        text.append(i)
        next_data = 'moretext'

    elif next_data == 'moretext':
        text[text_sub] = text[text_sub] + ' ' + i

final_data = pd.DataFrame({'file': file, 'text': text})
final_data.to_csv('D:/Docs/Audio/Movies/Autograph/data1.csv',index=False)