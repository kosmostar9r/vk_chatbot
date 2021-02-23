from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

AVATARS = ['avatars/avataaars.png', 'avatars/avataaars1.png', 'avatars/avataaars2.png', 'avatars/avataaars3.png',
           'avatars/avataaars4.png', 'avatars/avataaars5.png', 'avatars/avataaars6.png', 'avatars/avataaars7.png',
           'avatars/avataaars8.png', 'avatars/avataaars9.png', ]

DEPARTURE_OFFSET = (30, 237)
ARRIVAL_OFFSET = (30, 303)
DATE_ONLY_OFFSET = (259, 237)
TIME_ONLY_OFFSET = (259, 303)
EMAIL_OFFSET = (259, 171)
FONT = 'files/Roboto-Regular.ttf'
FONT_SIZE = 18
BLACK = (0, 0, 0, 255)
AVATAR_SIZE = (100, 100)
AVATAR_OFFSET = (30, 110)


def generate_ticket(departure, arrival, date, email):
    base = Image.open('files/ticket_sample.png').convert('RGBA')
    font = ImageFont.truetype(FONT, size=FONT_SIZE)

    date = date.split(' ')
    date_only = date[0]
    time_only = date[1]

    draw = ImageDraw.Draw(base)

    draw.text(DEPARTURE_OFFSET, departure, font=font, fill=BLACK)
    draw.text(ARRIVAL_OFFSET, arrival, font=font, fill=BLACK)
    draw.text(DATE_ONLY_OFFSET, date_only, font=font, fill=BLACK)
    draw.text(TIME_ONLY_OFFSET, time_only, font=font, fill=BLACK)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK)

    id_list = []
    for char in date_only:
        if len(id_list) >= 2:
            break
        id_list.append(int(char))

    avatar_id = id_list[-1]

    avatar = Image.open(AVATARS[avatar_id])
    avatar = avatar.resize(AVATAR_SIZE, Image.ANTIALIAS)

    base.paste(avatar, AVATAR_OFFSET)

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file


if __name__ == '__main__':
    print(generate_ticket('departure', 'arrival', '23-02-2021 18:00', 'email@email.com'))
