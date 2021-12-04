from PIL import Image, ImageDraw, ImageFont

''' category = [['Team 1', 100, 200, 300, 400],
     ['Тема 2', 100, 200, 300, 400],
     ['Team 3', 100, '', 300, 400],
     ['Team 4', 100, 200, '', 400],
     ['Team 5', '', 200, 300, 400]] '''

def get_table_board(category):
    h, k = 300, 7
    step = int(h / 5)
    w = step * k
    im = Image.new('RGB', (w, h), (49, 140, 231))
    draw = ImageDraw.Draw(im)

    for i in range(0, 6):
        draw.line((0, step * i, w, step * i), fill='white', width=1)
        for i in range(3, k + 1):
            draw.line((step * i - 1, 0, step * i - 1, h), fill='white', width=1)
            draw.line((0, 0, 0, h), fill='white', width=1)

    for cat, i in zip(category, range(0, k)):
        draw.text((10, step * i + int(step / 2) - 5), str(cat[0]), font=None, fill=(255, 255, 255, 0))
        for question, n in zip(cat[1:], range(3, k + 1)):
            draw.text((step * n + int(step / 2) - 5, step * i + int(step / 2) - 5), str(question), font=None,
                      fill=(243, 244, 175, 0))

    return im

