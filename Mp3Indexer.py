from os import listdir, getenv
from os.path import join
from dotenv import load_dotenv
from typing import Dict, Tuple

load_dotenv()
AUDIO_PATH = getenv('AUDIO_PATH')


def index_mp3_files() -> Tuple[Dict, Dict]:
    '''
    This function indexes all the mp3 files in the .env specified 'AUDIO_PATH'
    :return: a tuple containing a dictionary of numbers to mp3 files, and a dict of numbers to filenames (for the caller using the help option of the command)
    '''
    audio_files = listdir(AUDIO_PATH)
    audio_files.sort()
    mp3_ind_short = zip(range(1, len(audio_files)+1), [mp3.split('.')[0] for mp3 in [fi.lower() for fi in audio_files]])
    mp3_ind_long = zip(range(1, len(audio_files)+1), [join(AUDIO_PATH, file) for file in audio_files])

    return dict(mp3_ind_short), dict(mp3_ind_long)