
from pathlib2 import PurePath


blacklisted_files = {
    PurePath('/etc/shadow'): "Shadow File!",
    PurePath('/etc/passwd'): "Passwd File!"
}

blacklisted_directories = {
    # PurePath('/etc'),
    PurePath('/root'): "Root Directory"
}
