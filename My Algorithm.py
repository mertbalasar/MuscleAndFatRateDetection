import cv2
import os
import time

def load():
    imgPath = 'C:/Users/MERT/Desktop/Biokido/Bacak'
    imgList = os.listdir(imgPath)
    for i in range(len(imgList)):
        imgList[i] = imgPath + '/' + imgList[i]
    return imgList

def scanner(img, width, height, middler, middlec, f):
    last_whites = []
    
    lw = -1
    t = int(img[middler, middlec])
    a = t
    for u in range(middler - 1, -1, -1):
        t += int(img[u, middlec])
        a = t / (middler - u + 1)
        if a < 55 or f:
            if img[u, middlec] > (a * 1.15):
                lw = u
        else:
            if img[u, middlec] < (a / 1.15):
                lw = u
                break
    if lw != -1:
        last_whites.append(lw)

    lw = -1
    t = int(img[middler, middlec])
    a = t
    for d in range(middler + 1, height):
        t += int(img[d, middlec])
        a = t / (d - middler + 1)
        if a < 55 or f:
            if img[d, middlec] > (a * 1.15):
                lw = d
        else:
            if img[d, middlec] < (a / 1.15):
                lw = d
                break
    if lw != -1:
        last_whites.append(lw)

    lw = -1
    t = int(img[middler, middlec])
    a = t
    end = -1
    if middlec < int(width / 2):
        end = int(width/2)
    else:
        end = width
    for r in range(middlec + 1, end):
        t += int(img[middler, r])
        a = t / (r - middlec + 1)
        if a < 55 or f:
            if img[middler, r] > (a * 1.15):
                lw = r
        else:
            if img[middler, r] < (a / 1.15):
                lw = r
                break
    if lw != -1:
        last_whites.append(lw)

    lw = -1
    t = int(img[middler, middlec])
    a = t
    end = -1
    if middlec > int(width / 2):
        end = int(width/2)       
    for l in range(middlec - 1, end, -1):
        t += int(img[middler, l])
        a = t / (middlec - l + 1)
        if a < 55 or f:
            if img[middler, l] > (a * 1.15):
                lw = l
        else:
            if img[middler, l] < (a / 1.15):
                lw = l
                break
    if lw != -1:
        last_whites.append(lw)

    return last_whites

def alpha_sort(img, width, height, middler, middlec, lw):
    group13 = []
    group24 = []
    group13.append(int(img[lw[0], middlec]) + int(img[middler, lw[2]])) # 1. bölge
    group13.append(int(img[lw[1], middlec]) + int(img[middler, lw[3]])) # 3. bölge
    group24.append(int(img[lw[0], middlec]) + int(img[middler, lw[3]])) # 2. bölge
    group24.append(int(img[lw[1], middlec]) + int(img[middler, lw[2]])) # 4. bölge
    group13.append(group13.index(min(group13)))
    group13.append(group13.index(max(group13)))
    group24.append(group24.index(min(group24)))
    group24.append(group24.index(max(group24)))
    return group13, group24

def clear_pixels(img, img2, width, height, seperator):
    for r in range(height):
        for c in range(width):
            if img[r,c] > seperator:
                img2[r,c] = [255, 255, 255]
            else:
                img2[r,c] = [0, 0, 0]
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if img2[r,c][0] == 255 and img2[r+1,c][0] == 0 and img2[r+1,c+1][0] == 0 and img2[r,c+1][0] == 0 and img2[r-1,c][0] == 0 and img2[r-1,c-1][0] == 0 and img2[r,c-1][0] == 0 and img2[r-1,c+1][0] == 0 and img2[r+1,c-1][0] == 0:
                img2[r,c] = [0, 0, 0]

def draw_leg(img, img2, middler, middlec, row, column):
    height, width, alpha = img2.shape
    startr = row
    startc = column
    r = startr
    c = startc
    step = None
    step2 = None
    limitl = None
    limitr = None
    limitd = None
    limitu = None

    if startr < middler: # 1 VEYA 2. BÖLGE
        if startc > middlec: # 1. BÖLGE
            if column < int(width/2): # SOL BACAK
                limitl = middlec 
                limitr = int(width/2)
            else: # SAĞ BACAK
                limitl = int(width/2)
                limitr = width
            limitu = 0
            limitd = middler
        if startc < middlec: # 2. BÖLGE
            if column < int(width/2): # SOL BACAK
                limitl = 0
                limitr = middlec
            else: # SAĞ BACAK
                limitl = int(width/2)
                limitr = middlec
            limitu = 0
            limitd = middler
    else: # 3 VEYA 4. BÖLGE
        if startc > middlec: # 4. BÖLGE
            if column < int(width/2): # SOL BACAK
                limitl = middlec
                limitr = int(width/2)
            else: # SAĞ BACAK
                limitl = middlec
                limitr = width
            limitu = middler
            limitd = height
        if startc < middlec: # 3. BÖLGE
            if column < int(width/2): # SOL BACAK
                limitl = 0
                limitr = middlec
            else: # SAĞ BACAK
                limitl = int(width/2)
                limitr = middlec
            limitu = middler
            limitd = height

    #print('ROW: ' + str(row) + '\nCOLUMN: ' + str(column) + '\nLEFT LIMIT: ' + str(limitl) + '\nRIGHT LIMIT: ' + str(limitr) + '\nUP LIMIT: ' + str(limitu) + '\nDOWN LIMIT: ' + str(limitd) + '\n--------')
    
    if middler - r > 0:
        step2 = 1
    else:
        step2 = -1
    while True: # 1 YÖNE TARAMA YAPMAK İÇİN
        c = startc
        if step2 * (middler - r) >= 0:
            if img2[r, c][0] == 255: # 1. OLASILIK: BULUNULAN NOKTANIN BEYAZ OLMASI
                if middlec - startc > 0:
                    step = -1
                else:
                    step = 1
                while True:
                    if limitl < c + step < limitr:
                        if img2[r, c+step][0] == 255:
                            c += step
                        else:
                            img[r, c] = [0, 0, 255]
                            if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                                img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                            break
                    else:
                        img[r, c] = [0, 0, 255]
                        if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                            img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                        break
            else: # 2. OLASILIK: BULUNULAN NOKTANIN SİYAH OLMASI
                if middlec - startc > 0:
                    step = -1
                else:
                    step = 1
                counter = 0
                found = 0
                while True: # MERKEZİN DIŞINA ÇIKILARAK BEYAZ ELİPS SINIRI ARANIR
                    if limitl < c + step < limitr:
                        if img2[r, c+step][0] == 0:
                            if counter == 1:
                                found = 1
                                img[r, c] = [0, 0, 255]
                                if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                                    img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                                break
                            c += step
                        else:
                            counter = 1
                            c += step
                    else:
                        break
                if found == 0: # MERKEZİN DIŞINDA BEYAZ ELİPS SINIRI BULUNAMAZ MERKEZE YAKIN DEMEKTİR, MERKEZE YAKLAŞILARAK ARANIR                    
                    step *= -1                    
                    c = startc
                    while True:
                        if limitl < c + step < limitr:
                            if img2[r, c+step][0] == 255:
                                c += step
                                img[r, c] = [0, 0, 255]
                                if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                                    img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]                               
                                break                               
                            else:
                                c += step
                        else:
                            break
            r += step2
        else:
            break

    r = startr
    c = startc
    if middlec - c > 0:
        step2 = 1
    else:
        step2 = -1
    while True: # 1 YÖNE TARAMA YAPMAK İÇİN
        r = startr
        if step2 * (middlec - c) >= 0:
            if img2[r, c][0] == 255: # 1. OLASILIK: BULUNULAN NOKTANIN BEYAZ OLMASI
                if middler - startr > 0:
                    step = -1
                else:
                    step = 1
                while True:
                    if limitu < r + step < limitd:                                            
                        if img2[r+step, c][0] == 255:
                            r += step
                        else:
                            img[r, c] = [0, 0, 255]
                            if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                                img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                            break
                    else:
                        img[r, c] = [0, 0, 255]
                        if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                            img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                        break
            else: # 2. OLASILIK:: BULUNULAN NOKTANIN SİYAH OLMASI
                if middler - startr > 0:
                    step = -1
                else:
                    step = 1
                counter = 0
                found = 0
                while True: # MERKEZİN DIŞINA ÇIKILARAK BEYAZ ELİPS SINIRI ARANIR
                    if limitu < r + step < limitd:
                        if img2[r+step, c][0] == 0:
                            if counter == 1:
                                found = 1
                                img[r, c] = [0, 0, 255]
                                if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                                    img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                                break
                            r += step
                        else:
                            counter = 1
                            r += step
                    else:
                        break
                if found == 0: # MERKEZİN DIŞINDA BEYAZ ELİPS SINIRI BULUNAMAZ MERKEZE YAKIN DEMEKTİR, MERKEZE YAKLAŞILARAK ARANIR
                    step *= -1
                    r = startr
                    while True:
                        if limitu < r + step < limitd:
                            if img2[r+step, c][0] == 255:
                                r += step
                                img[r, c] = [0, 0, 255]
                                if -1 < (2 * middlec) - c < width and -1 < (2 * middler) - r < height:
                                    img[(2 * middler) - r, (2 * middlec) - c] = [0, 0, 255]
                                break
                            else:
                                r += step
                        else:
                            break
            c += step2
        else:
            break

def alpha_specifier(img, img2, group13, group24, middler, middlec, lw):
    if group13[3] == 0:
        draw_leg(img, img2, middler, middlec, lw[0], lw[2])
    if group13[3] == 1:
        draw_leg(img, img2, middler, middlec, lw[1], lw[3])
    if group24[3] == 0:
        draw_leg(img, img2, middler, middlec, lw[0], lw[3])
    if group24[3] == 1:
        draw_leg(img, img2, middler, middlec, lw[1], lw[2])
        
def multi_draw_ellipse(img, width, height, middler, middlec, middler2, middlec2, i):
    lw1 = scanner(img, width, height, middler, middlec, True) # left leg = [up row, down row, right column, left column]
    lw2 = scanner(img, width, height, middler2, middlec2, True) # right leg = [up row, down row, right column, left column]
    
    img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    sensitive = None
    if i >= 0 and i <= 7:
        sensitive = 80
    if i >= 8 and i <= 24:
        sensitive = 30
    if i == 25:
        sensitive = 55
    if i >= 26 and i <= 32:
        sensitive = 25
    clear_pixels(img, img2, width, height, sensitive)
    
    group_13, group_24 = alpha_sort(img, width, height, middler, middlec, lw1) # groupxy = [x. bölge ışığı, y. bölge ışığı, düşük ışıklı index, yüksek ışıklı index]
    group_13_2, group_24_2 = alpha_sort(img, width, height, middler2, middlec2, lw2)

    img3 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    sensitive = None
    if i >= 0 and i <= 1:
        sensitive = 60
    if i >= 2 and i <= 4:
        sensitive = 50
    if i >= 5 and i <= 7:
        sensitive = 40
    if i >= 8 and i <= 26:
        sensitive = 30
    if i >= 27 and i <= 32:
        sensitive = 20
    clear_pixels(img, img3, width, height, sensitive)

    alpha_specifier(img3, img2, group_13, group_24, middler, middlec, lw1)
    alpha_specifier(img3, img2, group_13_2, group_24_2, middler2, middlec2, lw2)

    total, muscle = calculate_leg(img3, middler, middlec, -1, int(width/2))
    total2, muscle2 = calculate_leg(img3, middler2, middlec2, int(width/2), width)

    return (total + total2), (muscle + muscle2)

def calculate_leg(img, middler, middlec, limitl, limitr):
    height, width, alpha = img.shape
    muscle = 0
    total = 0
    last_right = -1
    last_left = -1
    while last_right == -1 or last_left == -1:
        for r in range(middlec, limitr):
            if img[middler, r][0] == 0 and img[middler, r][1] == 0 and img[middler, r][2] == 255:
                last_right = r
                break
            else:
                if img[middler, r][0] == 255:
                    last_right = r
        for l in range(middlec, limitl, -1):
            if img[middler, l][0] == 0 and img[middler, l][1] == 0 and img[middler, l][2] == 255:
                last_left = l
                break
            else:
                if img[middler, l][0] == 255:
                    last_left = l
        if last_right == -1 or last_left == -1:
            middler += 1
    for c in range(last_left, last_right + 1):
        for u in range(middler, -1, -1):
            if img[u, c][0] == 0 and img[u, c][1] == 0 and img[u, c][2] == 255:
                break
            else:
                total += 1
                if img[u, c][2] == 0:
                    muscle += 1
        for d in range(middler, height):
            if img[d, c][0] == 0 and img[d, c][1] == 0 and img[d, c][2] == 255:
                break
            else:
                total += 1
                if img[d, c][2] == 0:
                    muscle += 1
    return total, muscle

def calculate_leg2(img, middler, middlec, i):
    height, width = img.shape
    img2 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    sensitive = None
    if i >= 33 and i <= 43:
        sensitive = 20
    if i >= 44 and i <= 53:
        sensitive = 25
    if i >= 54 and i <= 55:
        sensitive = 31
    if i >= 56 and i <= 57:
        sensitive = 35
    if i >= 58 and i <= 61:
        sensitive = 31
    if i >= 62 and i <= 63:
        sensitive = 35
    clear_pixels(img, img2, width, height, sensitive)
    
    muscle = 0
    total = 0
    last_right = -1
    last_left = -1
    last_up = -1
    last_down = -1
    while last_right == -1 or last_left == -1:
        for r in range(middlec, width):
            if img2[middler, r][0] == 255:
                last_right = r
        for l in range(middlec, -1, -1):
            if img2[middler, l][0] == 255:
                last_left = l
        if last_right == -1 or last_left == -1:
            middler += 1
    for c in range(last_left, last_right + 1):
        for u in range(middler, -1, -1):
            if img2[u, c][0] == 255:
                last_up = u
        for u in range(middler, last_up - 1, -1):
            total += 1
            if img2[u, c][0] == 0:
                muscle += 1
        for d in range(middler, height):
            if img2[d, c][0] == 255:
                last_down = d
        for d in range(middler, last_down):
            total += 1
            if img2[d, c][0] == 0:
                muscle += 1
    return total, muscle
    
def main():
    startsec = int(time.time())
    print('----------\nProgress Status: %0\n----------')
    imgList = load()
    middler = -1
    middlec = -1
    middler2 = -1
    middlec2 = -1
    total = 0
    muscle = 0
    for i in range(len(imgList)):
        startsec2 = time.time()
        img = cv2.imread(imgList[i], 0)
        height, width = img.shape
        if i < 11:
            middler = 113
            middlec = 80
            middler2 = 107
            middlec2 = 241
            t, m = multi_draw_ellipse(img, width, height, middler, middlec, middler2, middlec2, i)
            total += t
            muscle += m
        if i >= 11 and i < 24:
            middler = 119
            middlec = 84
            middler2 = 115
            middlec2 = 239
            t, m = multi_draw_ellipse(img, width, height, middler, middlec, middler2, middlec2, i)
            total += t
            muscle += m
        if i >= 24 and i < 33:
            middler = 119
            middlec = 84
            middler2 = 123
            middlec2 = 237
            t, m = multi_draw_ellipse(img, width, height, middler, middlec, middler2, middlec2, i)
            total += t
            muscle += m
        if i >= 33:
            middler = 134
            middlec = 155
            t, m = calculate_leg2(img, middler, middlec, i)
            total += t
            muscle += m
        endsec2 = time.time()
        print('Progress Status: %' + str(int((100*(i+1))/len(imgList))))
        timeremaining = (endsec2 - startsec2) * (len(imgList) - i - 1)
        if timeremaining >= 60:
            print('Time Remaining (min, sec): ' + str(int(timeremaining / 60)) + ' , ' + str(int(timeremaining - (int(timeremaining / 60) * 60))) + '\n----------')
        else:
            print('Time Remaining (sec): ' + str(int(timeremaining)) + '\n----------')
        #cv2.imshow('Name', img)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    print('Total Muscle: %' + str((100*muscle)/total))
    endsec = int(time.time())
    if endsec - startsec >= 60:
        print('Elapsed Time (min, sec): ' + str(int((endsec - startsec) / 60)) + ' , ' + str(endsec - (startsec + (int((endsec - startsec) / 60) * 60))))
    else:
        print('Elapsed Time (sec): ' + str(endsec - startsec))
main()
