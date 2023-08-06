import cv2
from PIL import Image
import numpy as np
import os
from operator import itemgetter
import math


def standardize(img_path, export_dir, standard_img_dimension = 200):
    try:
        try:
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(img, (25, 23), 5)

        canny = cv2.Canny(blurred, 150, 300,apertureSize = 5, L2gradient = True)

        (cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        top_corner_list = []
        bottom_corner_list = []
        for cnt in cnts:
            x,y,w,h = cv2.boundingRect(cnt)
            top_corner_list.append((x,y))
            bottom_corner_list.append((x+w,y+h))

        top_corner = list((min(top_corner_list,key=itemgetter(0))[0], min(top_corner_list,key=itemgetter(1))[1]))
        bottom_corner = list((max(bottom_corner_list,key=itemgetter(0))[0], max(bottom_corner_list,key=itemgetter(1))[1]))

        img_with_alpha = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        frame_img_BGRA = img_with_alpha.copy()
        cv2.drawContours(frame_img_BGRA, cnts, -1, (123,21,231,42), -1)

        frame_img_RGBA = cv2.cvtColor(frame_img_BGRA, cv2.COLOR_BGRA2RGBA)
        cropped_img_BGRA = img_with_alpha[top_corner[1]:bottom_corner[1], top_corner[0]:bottom_corner[0]]
        cropped_img_RGBA = cv2.cvtColor(cropped_img_BGRA, cv2.COLOR_BGRA2RGBA)

        center = (round(frame_img_RGBA.shape[1]/2), round(frame_img_RGBA.shape[0]/2))
        radius = round(max(frame_img_RGBA.shape[0:2])/2)
        cv2.circle(frame_img_RGBA, center, radius, (123,21,231,42), -1)

        center = (round(cropped_img_RGBA.shape[1]/2), round(cropped_img_RGBA.shape[0]/2))
        radius = round(max(cropped_img_RGBA.shape[0:2])/2)
        cv2.circle(cropped_img_RGBA, center, radius, (123,21,231,42), -1)

        frame_img_RGBA_pil = Image.fromarray(frame_img_RGBA, mode='RGBA')
        cropped_img_pil = Image.fromarray(cropped_img_RGBA, mode='RGBA')

        img_dist = frame_img_RGBA_pil.getcolors(frame_img_RGBA_pil.size[0]*frame_img_RGBA_pil.size[1])
        cropped_dist = cropped_img_pil.getcolors(cropped_img_pil.size[0]*cropped_img_pil.size[1])

        cropped_dist = [x for x in cropped_dist if (x[1] != (123,21,231,42) and x != (231, 21, 123, 42))]
        img_dist = [x for x in img_dist if (x[1] != (123,21,231,42) and x != (231, 21, 123, 42))]
        cropped_dist = sorted(cropped_dist, key=lambda x: x[0], reverse=True)
        img_dist = sorted(img_dist, key=lambda x: x[0], reverse=True)
        archived_img_dist = img_dist.copy()
        freq, color = max(img_dist)
        freq1, color1 = max(cropped_dist)

        for cropped_color in cropped_dist:
            if cropped_color[1] == color:
                break
            else:
                img_dist.remove((freq, color))
                if len(img_dist) == 0:
                    freq, color = max(archived_img_dist)
                    break
                freq, color = max(img_dist)
        if color[3] == 0: 
            color = (255,255,255,255)


        final_img = Image.new('RGBA', (standard_img_dimension,standard_img_dimension), color)
        is_vertically_centered = (5*img.shape[0]/14) < (top_corner[1]+bottom_corner[1])/2 < (9*img.shape[0]/14)
        is_horizontally_centered = (5*img.shape[1]/14) < (top_corner[0]+bottom_corner[0])/2 < (9*img.shape[1]/14)
        is_square = .92 < img.shape[0]/img.shape[1] < 1.1


        is_valid = is_vertically_centered and is_horizontally_centered and is_square
        is_valid = is_valid and (abs(top_corner[1]-bottom_corner[1])/img.shape[0] >.5 or abs(top_corner[0]-bottom_corner[0])/img.shape[0] >.5)
        

        if is_valid:
            full_img = cv2.cvtColor(img_with_alpha, cv2.COLOR_BGRA2RGBA)
            full_img = Image.fromarray(full_img, mode='RGBA')
            full_img = full_img.resize((standard_img_dimension, standard_img_dimension), resample=Image.LANCZOS)

            try:
                final_img.paste(full_img, (round((final_img.size[0]-full_img.size[0])/2),round((final_img.size[1]-full_img.size[1])/2)), full_img)
            except:
                final_img.paste(full_img, (round((final_img.size[0]-full_img.size[0])/2),round((final_img.size[1]-full_img.size[1])/2)))

        else:
            crop_img = img_with_alpha[top_corner[1]:bottom_corner[1], top_corner[0]:bottom_corner[0]]
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGRA2RGBA)
            crop_img = Image.fromarray(crop_img, mode='RGBA') 
            width, height = crop_img.size
            new_width = 160*(width/max(list([width,height])))
            new_width = math.floor(new_width) if new_width>standard_img_dimension else math.ceil(new_width)
            new_height = 160*(height/max(list([width,height])))
            new_height = math.floor(new_height) if new_height>standard_img_dimension else math.ceil(new_height)
            crop_img = crop_img.resize((new_width,new_height), resample=Image.LANCZOS)

            try:
                final_img.paste(crop_img, (round((final_img.size[0]-crop_img.size[0])/2),round((final_img.size[1]-crop_img.size[1])/2)), crop_img)
            except:
                final_img.paste(crop_img, (round((final_img.size[0]-crop_img.size[0])/2),round((final_img.size[1]-crop_img.size[1])/2)))

        image_array = np.array(final_img)
        image_array = cv2.GaussianBlur(image_array, (25, 25), 7)
        mask = np.ones_like(image_array) * 255
        center = (round(image_array.shape[1]/2), round(image_array.shape[0]/2))
        radius = round(min(image_array.shape[0:2])/2)
        cv2.circle(mask, center, radius, 0, -1)
        circled_img = cv2.bitwise_and(image_array, mask)    
        circled_canny = cv2.Canny(circled_img, 150, 300,apertureSize = 5, L2gradient = True)
        (contours, _) = cv2.findContours(circled_canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        mask_canny = cv2.Canny(mask, 150, 300,apertureSize = 5, L2gradient = True)
        (contours1, _) = cv2.findContours(mask_canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(circled_canny, contours, -1, (255, 255, 255, 255), 2)
        cv2.drawContours(circled_canny, contours1, -1, (0, 0, 0, 255), 2)

        cropped_percentage = (len(circled_canny[circled_canny == 255])/(len(circled_canny[circled_canny == 255])+len(circled_canny[circled_canny == 0]))) * 100
        is_cropped = True if (cropped_percentage >= .22) else False

        if is_cropped:
            final_img = Image.new('RGBA', (standard_img_dimension,standard_img_dimension), color)
            crop_img = img_with_alpha[top_corner[1]:bottom_corner[1], top_corner[0]:bottom_corner[0]]
            crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGRA2RGBA)
            crop_img = Image.fromarray(crop_img, mode='RGBA')  
            crop_img.thumbnail((141,141), Image.ANTIALIAS)

            try:
                final_img.paste(crop_img, (round((final_img.size[0]-crop_img.size[0])/2),round((final_img.size[1]-crop_img.size[1])/2)), crop_img)
            except:
                final_img.paste(crop_img, (round((final_img.size[0]-crop_img.size[0])/2),round((final_img.size[1]-crop_img.size[1])/2)))

        img_name = img_path.split('/')[-1]
        img_name_segments = img_name.split('.')
        img_name = f'{".".join(img_name_segments[:-1])}.png'

        final_img.save(f"{export_dir}/{img_name}", format="png", quality=100, compress_level=0, optimize = False)

    except Exception as e:
        return e.msg
    
    return "image standardized successfully!"