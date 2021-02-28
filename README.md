# Whatslogger - Whatsapp Logger

_Whatsapp has a limit on the size of the logged chat history, so I wrote this bot to overcome such a silly limitation._

## How to use
- This software is compatible with Firefox browser only, so it should be installed;
- Install the `requirements.txt` as usual;
- Install the [GeckoDriver](https://github.com/mozilla/geckodriver/releases);
- Run `whatslogger.py contact-name [log-destination]`;
  - If `log-destination` is not provided, a file name `log_(contact-name).txt` will be created in the current directory.

## How it works
- Selenium will open a new Firefox tab and prompt for the QR-code authentication;
- Afterwards it'll search for the desired contact and start logging the messages and scrolling the chat history;
- Messages are dumped in the text file as the process progresses, meaning it's possible to watch the logged messages in real time with `tail -f (log-filename.txt);
- It's possible to use the computer normally during the process, except for whatsapp web / desktop app.

## Functionalities
- Currently only logs messages from a given chat;
- May or may not include new functionalities in the future.

## Limitations
- This code won't parse anything that is not text (ie: emojis, images, stickers, map locations, etc)
- There are no tests :unamused:

## Disclaimers
- Use it at your own risk, I'm not sure if this violates WhatsApp terms of use :innocent:
- This is highly experimental and done for fun. The code can be improved in several ways.

## Inner workings and curiosity
- Interface with whatsapp interface is done via Selenium, but as soon as the code touches the messages, the code is downloaded as HTML and parsed by BeautifulSoup. This is because the latter is much faster in parsing HTML due it's purpouse, whereas it cannot trigger Whatsapp's infinity scroll;
- Trivia: it seems Whatsapp generates a lot of div and class names randomly and changes these from time to time. My guess is that this is done to avoid exactly what this project does, so I won't be surprised if it stops working in the near feature. A way that I found to bypass that was relying on web accessibility tags.
