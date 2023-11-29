from subprocess import call, run


class PcCommand():
    def __init__(self):
        pass
    
    def open_chrome(self, website):
        website = "" if website is None else website

        call("C:/Program Files/Google/Chrome/Application/chrome.exe " + website)

    def open_mail(recipient, subject, body):
        url = f'mailto:{recipient}?subject={subject}&body={body}'

        run(['start', 'outlook', url], shell=True)