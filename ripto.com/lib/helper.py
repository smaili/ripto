import smtplib
import email.utils
import re
from email.mime.text import MIMEText


"""
Determines whether or not the user agent is from a mobile device
http://detectmobilebrowsers.com/
Regex updated: 9 September 2013
"""
# NOTE - put reg_b,reg_v as static so we don't need to recompile the regex's on each request
# NOTE - by default just detects phones. To add tablet support see here -> http://detectmobilebrowsers.com/about
# TODO - separate out into is_phone, is_tablet, is_device functions
reg_b = re.compile(r"(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino|android|ipad|playbook|silk", re.I|re.M)
reg_v = re.compile(r"1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|sk\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-", re.I|re.M)
def is_mobile(user_agent):
    return True if reg_b.search(user_agent) or reg_v.search(user_agent[0:4]) else False


def minify(html):
    html = html.replace("\r\n", "\n")
    html = html.replace("\n", "")
    html = re.sub(r"<p>\s+", "<p>", html)
    html = re.sub(r"\s+</p>", "</p>", html)
    html = re.sub(r">\s{2,}<", "><", html)
    html = re.sub(r"(>)\s{2,}(.)", r"\1 \2", html)

    # Original Version
    """
    html = html.replace("\r\n", "\n")
    html = html.replace("\r", "\n")
    html = html.replace("\n", " ")
    html = html.replace("  ", "")
    html = re.sub(r'>\s*<', '><', html)
    """

    return html


"""
Generates URL-friendly string with the Hashids library
http://hashids.org
"""
def gen_url(num):
    # TODO - add these chars to hash alphabet when the time is right: _-
    # TODO - port hasher.php to python
    import subprocess
    p = subprocess.Popen(['php', 'lib/hasher.php', str(num) ], stdout=subprocess.PIPE)
    result = p.communicate()[0]

    return result


"""
Greps post for all variables starting with wildcard and then sort it
"""
def grep_post(form, wildcard, exclude=''):
    arr = []
    for name in form:
        if name.startswith(wildcard) and name != wildcard and name != wildcard + exclude:
            arr.append(name)

    return sorted(arr)


def get_arg(request, name, type=None, default=None):
    return request.args.get(name, type=type) or request.form.get(name, type=type) or default
