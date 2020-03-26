import os
import sys
def create_desktop_launcher():
    path = sys.argv[1]
    directory = os.path.join(os.environ['HOME'], 'Desktop')
    f = open(directory+'/OC-Manager.desktop','w+')
    f.write(f.'[Desktop Entry]\n \
            Keywords=Chromatography\n \
            Name=OC-Manager\n \
            Comment=Chromatography-Manager Software\n \
            Exec=cd {} %F\n \
            Terminal=true\n \
            Type=Application\n \
            MimeType=text/plain\n \
            Categories=Education;Chromatography;\n')
    f.close()

if __name__ == '__main__':
    create_desktop_launcher()
