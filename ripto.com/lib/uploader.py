# System
import os

# Flask
from werkzeug import secure_filename

# RIP
from config import UPLOAD_FOLDER, MEDIA_FOLDER, MEDIA_EXTENSION, ALLOWED_EXTENSIONS, MEDIA_WIDTH, MEDIA_HEIGHT



def remove_memorial_photo(filename):
    if filename:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
        except:
            pass


def move_file(filename, dst):
    src = os.path.join(UPLOAD_FOLDER, filename)
    dst = os.path.join(dst, filename)
    try:
        os.rename(src, dst)
    except:
        pass


def move_memorial_media(media):
    if media.filename != 'nophoto.png':
        move_file(media.filename, MEDIA_FOLDER)


def process_media(media):
    valid = False

    if _verify_mime(media):
        try:
            filename = _save_file(media)
            full_filename = os.path.join(UPLOAD_FOLDER, filename)
            # make sure dev packages are installed and symlinked -> http://stackoverflow.com/questions/8915296/, http://jj.isgeek.net/2011/09/install-pil-with-jpeg-support-on-ubuntu-oneiric-64bits/
            from PIL import Image, ImageChops, ImageFile
            im = Image.open( os.path.join(UPLOAD_FOLDER, filename) )
            width, height = im.size
            if width > MEDIA_WIDTH and height > MEDIA_HEIGHT:
                # http://stackoverflow.com/questions/9103257/
                size = ( MEDIA_WIDTH, MEDIA_HEIGHT )
                im.thumbnail(size, Image.ANTIALIAS)
                #resized_size = im.size
                #cropped = im.crop( (0, 0, size[0], size[1]) )
                #offset_x = max( (size[0] - resized_size[0]) / 2, 0 )
                #offset_y = max( (size[1] - resized_size[1]) / 2, 0 )
                #im = ImageChops.offset(cropped, offset_x, offset_y)
            elif width < MEDIA_WIDTH or height < MEDIA_HEIGHT:
                raise Exception # raise so that it triggers remove photo
            else:
                pass # leave as is but make sure we resave so we can optimize/reduce filesize

            # TODO - figure out how to convert blackspace to transparent and save as gif instead of jpg
            ImageFile.MAXBLOCK = width * height * 4 # needed for optimiziation -> http://stackoverflow.com/questions/6788398/
            im.save(full_filename, quality=90, optimize=True)
            valid = True
        except:
            remove_memorial_photo(filename)


    return filename if valid else False


def _verify_mime(filestorage):
    ext = _get_ext(filestorage)
    return ext in ALLOWED_EXTENSIONS


def _get_ext(filestorage):
    # get ext from file headers rather than its filename
    import magic
    mime = magic.from_buffer(filestorage.read(1024), mime=True)
    filestorage.seek(0) # reset position!!!
    return mime.replace('image/','').lower()


def _save_file(filestorage):
    #TODO - add rescaling
    filename = secure_filename(filestorage.filename)
    filename = _gen_filename() + '.' + MEDIA_EXTENSION
    filestorage.save(os.path.join(UPLOAD_FOLDER, filename))
    return filename


def _gen_filename():
    import base64, uuid
    return base64.urlsafe_b64encode(uuid.uuid4().hex).replace('=', '')
