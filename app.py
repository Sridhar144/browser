from flask import Flask, render_template, request

import webbrowser
import os
import platform

app = Flask(__name__)

recent_url = None  # To store the most recent URL


@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

#--------------------------------------------------Start - -------------------------------------------------------

@app.route('/start', methods=['GET'])
def start():
    global recent_url

    if 'browser' in request.args and 'url' in request.args:
        browser_name = str(request.args['browser'])
        url = str(request.args['url'])
        recent_url = url  # Update the most recent URL
        system_os = platform.system()

        if browser_name == "chrome":
            if system_os == "Windows":
                chrome_path = '"C:/Program Files/Google/Chrome/Application/chrome.exe" %s'
            else:
                chrome_path = '/usr/bin/google-chrome %s'
            
            webbrowser.get(chrome_path).open(url)  # Open the URL
            return f"Chrome started with the URL: {url}"

        elif browser_name == "mozilla":
            if system_os == "Windows":
                mozilla_path = '"C:/Program Files/Mozilla Firefox/firefox.exe" %s'
            else:
                mozilla_path = '/usr/bin/firefox %s'
            
            webbrowser.get(mozilla_path).open(url)  # Open the URL
            return f"Mozilla started with the URL: {url}"

        else:
            return "This browser isn't available"

    else:
        return "Error: Both 'browser' and 'url' parameters are required"


#-----------------------------------------------------------------Stop - -------------------------------------------------------------------

@app.route('/stop', methods=['GET'])
def stop():
    if 'browser' in request.args:
        browser_name = str(request.args['browser'])
        system_os = platform.system()

        if browser_name == "chrome":
            if system_os == "Windows":
                os.system("taskkill /im chrome.exe /f")
            else:
                os.system("pkill chrome")
            return "Chrome has been closed"

        elif browser_name == "mozilla":
            if system_os == "Windows":
                os.system("taskkill /im firefox.exe /f")
            else:
                os.system("pkill firefox")
            return "Mozilla Firefox has been closed"

        else:
            return "This browser isn't available"

    else:
        return "Error: 'browser' parameter is required"

#-----------------------------------------------------------Clear - ------------------------------------------------------------------------------------

@app.route('/cleanup', methods=['GET'])
def cleanup():
    if 'browser' in request.args:
        browser_name = str(request.args['browser'])

        if browser_name == "chrome":
            os.system("rm -rf ~/.cache/google-chrome/Default/Cache")
            os.system("rm -rf ~/.cache/google-chrome/Default/")
            os.system("rm -rf ~/.config/google-chrome/")
            os.system("rm -rf ~/.config/google-chrome/Default")
            return "Chrome data has been cleared"

        elif browser_name == "mozilla":
            os.system("rm -rf ~/.cache/mozilla/")
            os.system("rm -rf ~/.mozilla/")
            return "Mozilla data has been cleared"

    else:
        return "Error: 'browser' parameter is required"

#--------------------------------------------------------Get Recent URL and Open it ---------------------------------------------------------

@app.route('/getrecenturl', methods=['GET'])
def get_recent_url():
    global recent_url

    if recent_url:
        if 'browser' in request.args:
            browser_name = str(request.args['browser'])
            system_os = platform.system()

            if browser_name == "chrome":
                if system_os == "Windows":
                    chrome_path = '"C:/Program Files/Google/Chrome/Application/chrome.exe" %s'
                else:
                    chrome_path = '/usr/bin/google-chrome %s'

                webbrowser.get(chrome_path).open(recent_url)
                return f"The most recent URL is: {recent_url} and it has been opened in Chrome."

            elif browser_name == "mozilla":
                if system_os == "Windows":
                    mozilla_path = '"C:/Program Files/Mozilla Firefox/firefox.exe" %s'
                else:
                    mozilla_path = '/usr/bin/firefox %s'

                webbrowser.get(mozilla_path).open(recent_url)
                return f"The most recent URL is: {recent_url} and it has been opened in Mozilla Firefox."

            else:
                return "This browser isn't available"

        else:
            return f"The most recent URL is: {recent_url} but no browser was specified."
    else:
        return "No URL has been fetched yet."

#---------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=8000)
