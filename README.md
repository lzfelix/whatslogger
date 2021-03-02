# Whatslogger - Whatsapp Logger

_Whatsapp has a cap on the size of chats to be downloaded. This bot overcomes such a silly limitation.. I'm just leaving this here before I lose it._

## How to use
- This software is compatible with Firefox browser only, so it should be installed;
- Install `requirements.txt` as usual;
- Install the [GeckoDriver](https://github.com/mozilla/geckodriver/releases);
- Run `whatslogger.py contact-name [log-destination]`;
  - If `log-destination` is not provided, a file named `log_(contact-name).txt` will be created in the current directory.

## How it works
- Selenium will open a new Firefox tab and prompt for the QR-code authentication;
- Afterwards, it'll search for the desired contact, start logging messages, and scrolling the chat history;
- Messages are dumped in the text file as the process progresses. You can watch the logged messages in real time with `tail -f (log-destination.txt)`;
- It's possible to use the computer normally during the process;
- Notice you should not open web / desktop Whatsapp in any other tab or device meanwhile, as only one Whatsapp instance can be active at once;

## Functionalities
- Currently, only logs messages from a given chat;
- May or may not include new functionalities in the future.

## Limitations
- This code won't parse anything that is not text (ie: emojis, images, stickers, map locations, etc);
- There are no tests :unamused:

## Disclaimers
- Use it at your own risk, I'm not sure whether this violates WhatsApp terms of use :innocent:
- This is highly experimental and done for fun. The code can be improved in several ways;
- I'm just leaving this here before I lose it.

## Inner workings and curiosity
- The code interfaces with Whatsapp through Selenium, but as soon as messages are displayed on screen, the page HTML is downloaded and parsed by BeautifulSoup. This was done because the latter is much faster in parsing HTML due it's purpouse, whereas it cannot trigger Whatsapp's infinity scroll;
- Trivia: it seems Whatsapp generates a lot of div and class names randomly and these are changed from time to time. My guess is that this is to prevent scrapping messages, so I wouldn't be surprised if this code stops working in the near feature. A way that I found to overcome such an issue (at least for now) was relying on web accessibility tags.
