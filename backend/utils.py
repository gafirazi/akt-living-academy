import datetime

from .models import Murid

def get_new_nim(program_studi):
    nim_length = 5
    program_studi_mapping = {
        'Personal Branding': 'PB',
        'Public Speaking Beginner': 'PS',
        'Public Speaking Advance': 'PS',
        'Public Relations Beginner': 'PR',
        'Public Relations Advance': 'PR',
        'Event Organizer': 'EO'
    }

    today = datetime.datetime.now()
    year = today.year

    murids = Murid.objects.all()

    if len(murids) == 0:
        return program_studi_mapping[program_studi] + str(year) + '000001'
    else:
        list_nim = []

        for murid in murids:
            list_nim.append(murid.nim[-5:])
        
        list_nim.sort()
        list_nim.reverse()

        last_nim = int(list_nim[0])
        last_nim += 1
        last_nim_length = len(str(last_nim))

        new_nim = ''
        for i in range(nim_length - last_nim_length):
            new_nim += '0'
        
        new_nim += str(last_nim)
        return program_studi_mapping[program_studi] + str(year) + new_nim
