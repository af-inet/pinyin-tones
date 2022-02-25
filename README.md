# pinyin-tones (MacOS only)

Easily type pinyin with tone marks on MacOS.

For example, replaces "ni3" with "nǐ".

## installation

1. Download the [PinyinTones.plist](./PinyinTones.plist) file to your computer.

2. Open [System Preferences](https://www.howtogeek.com/683480/how-to-quickly-find-specific-system-preferences-on-a-mac/#:~:text=To%20launch%20it%2C%20click%20the,the%20window%20and%20click%20it)

3. In System Preferences, open **Keyboard**

4. Under Keyboard, navigate to **Text**

5. Click and drag the PinyinTones.plist file into the Text pane (where it says "Replace" "With")

6. Wait a moment, then you should see all the replacements loaded in, you're done!

## uninstall

Under System Preferences>Keyboard>Text, simply select all the pinyin substitutions and press the "-" button to delete them.

## how it works

The [main.py](./main.py) script generates a [Text Substitutions.plist](https://support.apple.com/en-mn/guide/mac-help/mchl2a7bd795/12.0/mac/12.0) using a complete list of pinyin from http://www.quickmandarin.com/chinesepinyintable/.

## run

requires python 3

```sh
python3 main.py > PinyinTones.plist
```
