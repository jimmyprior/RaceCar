import math
import random 

from PIL import Image, ImageDraw, ImageFont


circumference = 1250
radius = circumference / (2 * math.pi)
diameter = radius * 2

im_width = int(diameter * 2.2)
im_height = int(diameter * 2.2)

im_center_x = im_width / 2
im_center_y = im_height / 2

track_center_x = im_width / 2
track_center_y = im_height / 2

tank_color = (255, 0, 0) #tank and gas number g%
track_color = (0, 0, 255) #dist and track d%


def get_random_percents(number):
    """
    retruns a list of n random percents that will sum to 100
    """
    tanks = []
    total = 0
    for _ in range(number):
        num = random.randint(1, 10)
        total += num
        tanks.append(num)
    
    percents = []
    for tank in tanks:
        percents.append(math.floor(100 * tank / total))
    
    dif = 100 - sum(percents)
    
    if dif != 0:
        percents[random.randint(0, len(percents)-1)] += dif
    
    return percents

    
def get_points(theta, hypotenuse):
    x = math.cos(theta) * hypotenuse
    y = math.sin(theta) * hypotenuse
    return (x, y)


def draw_gas_can(img, center_x, center_y, radius):
    img.ellipse(
        [(center_x - radius, center_y - radius), 
         (center_x + radius, center_y + radius)], 
        fill=(255, 0, 0)
    )
    
    
def generate_track(qty_tanks):
    """
    qty_tanks : the number of thanks to be put randomly on the track
    """
    image = Image.new("RGB", (im_width, im_height), (255, 255, 255))
    draw = ImageDraw.Draw(image, "RGB")
    draw.ellipse(
        [(im_center_x - radius, im_center_y - radius), (im_center_x + radius, im_center_y + radius)], 
        outline = (0, 0, 0), 
        width = 6
    )
    distances = get_random_percents(qty_tanks)
    gas_amounts = get_random_percents(qty_tanks)
    circ = 0

    font = ImageFont.truetype("arial.ttf", 30)
    for index, dist, gas in zip(range(1, qty_tanks+1), distances, gas_amounts):
        #hypotenuse = radius
        index = qty_tanks - index
        gas_angle = ((circ + dist) / 100) * (2 * math.pi)
        gas_x, gas_y = get_points(gas_angle, radius)
        gas_label_x, gas_label_y = get_points(gas_angle, radius + 50)
        
        dist_angle = ((circ + dist / 2) / 100) * (2 * math.pi)
        dist_x, dist_y = get_points(dist_angle, radius)
        dist_label_x, dist_label_y = get_points(dist_angle, radius + 100)
        
        draw_gas_can(draw, gas_x + track_center_x, gas_y + track_center_y, 6)
        
        gas_label = [gas_label_x + track_center_x, gas_label_y + track_center_y]
        gas_tank = (gas_x + track_center_x, gas_y + track_center_y)
        draw.line([gas_tank, tuple(gas_label)], fill=tank_color) #draw the tank line
        
        dist_label = [dist_label_x + track_center_x, dist_label_y + track_center_y]
        dist_start = (dist_x + track_center_x, dist_y + track_center_y)
        draw.line([dist_start, tuple(dist_label)], fill=track_color) #draw the dist line
        
        circ += dist
        
        if gas_label[0] < track_center_x:
            gas_label[0] -= font.getsize(f"g{index}={gas}%")[0]
        
        if dist_label[0] < track_center_x:
            dist_label[0] -= font.getsize(f"g{index}={dist}%")[0]
            
        draw.text(tuple(gas_label), f"g{index}={gas}%", fill=(100, 0, 0), font=font) #draw gas percentage

        draw.text(tuple(dist_label), f"d{index}={dist}%", fill=(0, 0, 100), font=font) #previous circ + dist / 2

    return image


largest = 12
smallest = 2

#generate_track(5).show()

for i in range(10):
    generate_track(random.randint(smallest, largest)).save(f"tracks/track-{i}.png")

