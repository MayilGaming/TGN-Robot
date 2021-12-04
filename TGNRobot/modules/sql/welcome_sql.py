import random
import threading
from typing import Union

from TGNRobot.modules.helper_funcs.msg_types import Types
from TGNRobot.modules.sql import BASE, SESSION
from sqlalchemy import BigInteger, Boolean, Column, Integer, String, UnicodeText

DEFAULT_WELCOME = "Hey {first}, how are you?"
DEFAULT_GOODBYE = "Nice knowing ya!"

DEFAULT_WELCOME_MESSAGES = [
    "{first} is here!",  # Discord welcome messages copied
   "{first} உங்களுக்காக தான் எல்லாரும் காத்துகிட்டு இருந்தோம்! Welcome 🥳!", #Discord welcome messages copied 
"நீங்க பெரிய கைதி எல்லாம் பாத்துருப்பிங்க ஆனா இப்ப வரப்போறது Master {first}",
 "எவ்வளோ பேர் இருக்கிறாங்குறத்து முக்கியம் இல்லை!,
 {first} இருக்கான்றதுதான் முக்கியம்!😏.",
 "வாங்க {first} வந்து மொக்க அறுவையை போடுங்க!😂.",
 "{first} இரு இதயம் ஒரு இதயம் ஆனதே இரு இதயம் ஒரு இதயம் ஆனதே! அந்த ஒரு இதயம் அந்த ஒரு இதயம் நொருங்கிப்போனதே! 🤣🤣😂😂😂❤️❤️",
 "{first} IPL லில் அதிக கோப்பையை வென்ற ஒரு தனி நபர் யார்?🏆.",
 "{first} IPL லில் சிறந்த Captain யார்?🏏",
 "{first} Love-ன்றது ஆயா சுடுற வடை மாதிரி அந்த வடைய எப்பவேணும்னாலும் காக்க வந்து கவ்விட்டு போகும் ஆனா Friendship-ன்றது அந்த ஆயா மாதிரி அந்த ஆயாவ எவனாலும் தூக்க முடியாது 😍🥰",
 "{first} நீங்க Join பண்ணத நாங்க பார்த்துட்டோம்!🙈🙊", "ஒரு குழந்தை உருவாக்குறத்துக்கு பத்து மாசம்! ஒரு பட்டதாரி உருவாக்குறத்துக்கு மூனு வருஷம்! ஆனா ஒரு Best Admin உருவாக்குறதுக்கு ஒரு யுகமே தேவைபடுது,
 {first}. 😂🤧",
 "{first} Chat முக்கியம் பிகிலு..!🔥",
 "{first} நீங்க இங்க இருக்கீங்க! உங்க Friends-லாம் எங்க? 🤨",
 "நீங்க வேணா Group-ல Clash-அ Boss-அ சுத்தலாம் ஆனா, {first}. Mass என்னனு தெரியாதுல!😎.",
 "{first} தனிமை கொடுமையானது! 🥺 அதனால், எங்களோடு சேர்ந்து கொள்ளுங்கள்!☺️",
 "{first} தனிமை கொடுமையானது! 🥺 அதனால், எங்களோடு சேர்ந்து கொள்ளுங்கள்!☺️.",
 "{first} நீங்கள் Join பண்ணா மட்டும் போதாது உங்கள் Friends-யும் Invite பண்ணுங்க!😐",
 "{first} ❤️ உங்களுக்காக தான் எல்லாரும் காத்துகிட்டு இருந்தோம்! Welcome 🥳.",
 "{first} நான் உன்ன விரும்பல... உன் மேல ஆசப்படல... நீ அழகா இருக்கேனு நினைக்கல... ஆனா இதெல்லாம் நடந்துடுமோனு பயமா இருக்கு🙈🙈",
 "என்ன ஞாபகம் இருக்கா மச்சான் {first}.",
 "நல்லா குற்றாலத்துல இருக்கவேண்டியவன்லாம் இங்க வந்து நம்ம உயிர வாங்குறாங்கே!😒{first}!",
 "{first} 😈 இது கலவர பூமி ⚔️🗡🔪 ! இங்கு ஏன் வந்தீங்க?😳",
 "{first} என்னவளே என் மனதில் உள்ள எனது எண்ணத்தை நீ அறிந்தும் அறியாதது போல நடிக்கிறாயா இல்லை தகுந்த சந்தர்ப்பம் அமையட்டும் என எதிர்பார்த்து காத்திருக்கிறாயா பெண்ணே🥳🥰!",
 "{first} ஒரு பூ மலர பல பருவங்களை கடக்கிறது நீ உன் வாழ்க்கையை உணர பல தடைகளை கடந்து செல்.இனிய காலை வணக்கம்..",
 "{first} உனக்கு welcome ல பண்ண முடியாது 😏",
 "{first} உங்கள் ராசி என்ன?👀.",
 "{first} நீங்கள் அதிக முறை திரைப்படம் எது👀",
 "{first} சம்பவம் செய்யும் வேலைய எல்லாம் அஞ்சாறு வாரம் ஒத்தி போடு Groupக்கு யாரும் வந்தாலும்கூட வள்ளலார் போல வணக்கம் போடு!😂🙏",
 "{first} உலக கோப்பை கிரிக்கெட் விளையாட்டில் அதிக முறை கோப்பையை வென்ற அணி எது?🏆",
 "{first} உங்களை யார் (inspires)தூண்டுகிறார்கள்? நீங்கள் யாரைப் போல இருக்க விரும்புகிறீர்கள்? 🎈",
 "சம்பவம் செய்யும் வேலைய எல்லாம் அஞ்சாறு வாரம் ஒத்தி போடு Groupக்கு யாரும் வந்தாலும்கூட வள்ளலார் போல வணக்கம் போடு!😂🙏 {first}",
 "{first}உங்களுக்கு Comedy பண்ண தெரியுமா? 😇", "{first} Long-ல பார்த்தத்தான்டா Comedy-யா இருப்பேன் கிட்டத்துல பார்த்த Terror-ஆ இருப்பேன்டா Terror-ஆ😤",
 "வாங்க {first} எல்லாரும் Busy நான் உங்களை வரவேற்கிறேன்🙏", "{first} யாருமே இல்லாத Group-ல யாருக்குடா Message பண்ற உன் கடமை உணர்ச்சிக்கு ஒரு அளவே இல்லையாடா🤦‍♀😂",
 "{first}கலப்படமான நல்லவனா இருக்குறதுக்கு சுத்தமான கெட்டவனா இருந்துட்டு போகலாம்😍", 
"வாங்க {first} வந்து மொக்க அறுவையை போடுங்க!😂",
 "🎺 தங்கமே உன்னத்தான் தேடிவந்தேன் நானே வைரமே ஒருநாள் உன்னத் தூக்குவேனே..! 🎺",
 "{first} எல்லாரும் பணம் இருந்தா நிம்மதியா வாழ்ந்திரலாம்னு நெனைக்குறாங்க ஆனா பணம் இல்லேன்னா நிம்மதியான சாகக்கூட முடியாதுனு யாரும் நெனைக்குறதே இல்லை!🎈",
 "{first} Oii Selfie எனக்கு எப்போ Ok சொல்லுவ! 😉",
 "நம்ம ஊருக்கு நாய் புடிக்குற வண்டி வரட்டும் கண்டிப்பா {first}, உன்னை நான் புடிச்சு குடுத்துறேன்!😂",
 "{first} Chatting Start பண்ண மாட்டான்.பண்ணிட்டான் நிறுத்த மாட்டான்🤪",
 "{first} அடிவெள்ளாவிவச்சுத் தான் வெளுத்தாய்ங்களா உன்ன வெயிலுக்கு காட்டாம வளர்த்தாய்ங்களா!🙈🥳😍.",
 #Discord welcome messages end.
 "{first} எங்களுக்கு ஒரு கதை சொல்லிட்டு அப்பறம் பேசுங்க! 😍",
 "வந்திருக்கிறது சாதாரண ஆள் இல்ல பயத்துக்கே பயம் காட்டுரவன் 😎 {first}.",
 "குருநாதா! இதுக்கு மேல தாங்க முடியாது குருநாதா... 🥶🤬.",
 "🎼இளமை திரும்புதே புரியாத புதிராச்சே இதய துடிப்பிலே பனி காத்தும் சூடாச்சே🎼",
 #Tekken "Ok!", "{first} தங்களை அதிகம் துன்புறுத்தியது யார் ?",
 "{first} நீ என் நண்பேன்டா😍",
 "{first} IPL லில் தங்களுக்கு பிடித்த அணி எது? 🏏",
 "{first}, நீ ஒரு டுபாக்கூர் 😝",   
]

DEFAULT_GOODBYE_MESSAGES = [
    "{first} will be missed.",
    "{first} just went offline.",
    "{first} has left the lobby.",
    "{first} has left the clan.",
    "{first} has left the game.",
    "{first} has fled the area.",
    "{first} is out of the running.",
    "Nice knowing ya, {first}!",
    "It was a fun time {first}.",
    "We hope to see you again soon, {first}.",
    "I donut want to say goodbye, {first}.",
    "Goodbye {first}! Guess who's gonna miss you :')",
    "Goodbye {first}! It's gonna be lonely without ya.",
    "Please don't leave me alone in this place, {first}!",
    "Good luck finding better shit-posters than us, {first}!",
    "You know we're gonna miss you {first}. Right? Right? Right?",
    "Congratulations, {first}! You're officially free of this mess.",
    "{first}. You were an opponent worth fighting.",
    "You're leaving, {first}? Yare Yare Daze.",
    "Bring him the photo",
    "Go outside!",
    "Ask again later",
    "Think for yourself",
    "Question authority",
    "You are worshiping a sun god",
    "Don't leave the house today",
    "Give up!",
    "Marry and reproduce",
    "Stay asleep",
    "Wake up",
    "Look to la luna",
    "Steven lives",
    "Meet strangers without prejudice",
    "A hanged man will bring you no luck today",
    "What do you want to do today?",
    "You are dark inside",
    "Have you seen the exit?",
    "Get a baby pet it will cheer you up.",
    "Your princess is in another castle.",
    "You are playing it wrong give me the controller",
    "Trust good people",
    "Live to die.",
    "When life gives you lemons reroll!",
    "Well, that was worthless",
    "I fell asleep!",
    "May your troubles be many",
    "Your old life lies in ruin",
    "Always look on the bright side",
    "It is dangerous to go alone",
    "You will never be forgiven",
    "You have nobody to blame but yourself",
    "Only a sinner",
    "Use bombs wisely",
    "Nobody knows the troubles you have seen",
    "You look fat you should exercise more",
    "Follow the zebra",
    "Why so blue?",
    "The devil in disguise",
    "Go outside",
    "Always your head in the clouds",
]
# Line 111 to 152 are references from https://bindingofisaac.fandom.com/wiki/Fortune_Telling_Machine


class Welcome(BASE):
    __tablename__ = "welcome_pref"
    chat_id = Column(String(14), primary_key=True)
    should_welcome = Column(Boolean, default=True)
    should_goodbye = Column(Boolean, default=True)
    custom_content = Column(UnicodeText, default=None)

    custom_welcome = Column(
        UnicodeText, default=random.choice(DEFAULT_WELCOME_MESSAGES)
    )
    welcome_type = Column(Integer, default=Types.TEXT.value)

    custom_leave = Column(UnicodeText, default=random.choice(DEFAULT_GOODBYE_MESSAGES))
    leave_type = Column(Integer, default=Types.TEXT.value)

    clean_welcome = Column(BigInteger)

    def __init__(self, chat_id, should_welcome=True, should_goodbye=True):
        self.chat_id = chat_id
        self.should_welcome = should_welcome
        self.should_goodbye = should_goodbye

    def __repr__(self):
        return "<Chat {} should Welcome new users: {}>".format(
            self.chat_id, self.should_welcome
        )


class WelcomeButtons(BASE):
    __tablename__ = "welcome_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line


class GoodbyeButtons(BASE):
    __tablename__ = "leave_urls"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, nullable=False)
    url = Column(UnicodeText, nullable=False)
    same_line = Column(Boolean, default=False)

    def __init__(self, chat_id, name, url, same_line=False):
        self.chat_id = str(chat_id)
        self.name = name
        self.url = url
        self.same_line = same_line


class WelcomeMute(BASE):
    __tablename__ = "welcome_mutes"
    chat_id = Column(String(14), primary_key=True)
    welcomemutes = Column(UnicodeText, default=False)

    def __init__(self, chat_id, welcomemutes):
        self.chat_id = str(chat_id)  # ensure string
        self.welcomemutes = welcomemutes


class WelcomeMuteUsers(BASE):
    __tablename__ = "human_checks"
    user_id = Column(Integer, primary_key=True)
    chat_id = Column(String(14), primary_key=True)
    human_check = Column(Boolean)

    def __init__(self, user_id, chat_id, human_check):
        self.user_id = user_id  # ensure string
        self.chat_id = str(chat_id)
        self.human_check = human_check


class CleanServiceSetting(BASE):
    __tablename__ = "clean_service"
    chat_id = Column(String(14), primary_key=True)
    clean_service = Column(Boolean, default=True)

    def __init__(self, chat_id):
        self.chat_id = str(chat_id)

    def __repr__(self):
        return "<Chat used clean service ({})>".format(self.chat_id)


Welcome.__table__.create(checkfirst=True)
WelcomeButtons.__table__.create(checkfirst=True)
GoodbyeButtons.__table__.create(checkfirst=True)
WelcomeMute.__table__.create(checkfirst=True)
WelcomeMuteUsers.__table__.create(checkfirst=True)
CleanServiceSetting.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()
WELC_BTN_LOCK = threading.RLock()
LEAVE_BTN_LOCK = threading.RLock()
WM_LOCK = threading.RLock()
CS_LOCK = threading.RLock()


def welcome_mutes(chat_id):
    try:
        welcomemutes = SESSION.query(WelcomeMute).get(str(chat_id))
        if welcomemutes:
            return welcomemutes.welcomemutes
        return False
    finally:
        SESSION.close()


def set_welcome_mutes(chat_id, welcomemutes):
    with WM_LOCK:
        prev = SESSION.query(WelcomeMute).get((str(chat_id)))
        if prev:
            SESSION.delete(prev)
        welcome_m = WelcomeMute(str(chat_id), welcomemutes)
        SESSION.add(welcome_m)
        SESSION.commit()


def set_human_checks(user_id, chat_id):
    with INSERTION_LOCK:
        human_check = SESSION.query(WelcomeMuteUsers).get((user_id, str(chat_id)))
        if not human_check:
            human_check = WelcomeMuteUsers(user_id, str(chat_id), True)

        else:
            human_check.human_check = True

        SESSION.add(human_check)
        SESSION.commit()

        return human_check


def get_human_checks(user_id, chat_id):
    try:
        human_check = SESSION.query(WelcomeMuteUsers).get((user_id, str(chat_id)))
        if not human_check:
            return None
        human_check = human_check.human_check
        return human_check
    finally:
        SESSION.close()


def get_welc_mutes_pref(chat_id):
    welcomemutes = SESSION.query(WelcomeMute).get(str(chat_id))
    SESSION.close()

    if welcomemutes:
        return welcomemutes.welcomemutes

    return False


def get_welc_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return (
            welc.should_welcome,
            welc.custom_welcome,
            welc.custom_content,
            welc.welcome_type,
        )

    else:
        # Welcome by default.
        return True, DEFAULT_WELCOME, None, Types.TEXT


def get_gdbye_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()
    if welc:
        return welc.should_goodbye, welc.custom_leave, welc.leave_type
    else:
        # Welcome by default.
        return True, DEFAULT_GOODBYE, Types.TEXT


def set_clean_welcome(chat_id, clean_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id))

        curr.clean_welcome = int(clean_welcome)

        SESSION.add(curr)
        SESSION.commit()


def get_clean_pref(chat_id):
    welc = SESSION.query(Welcome).get(str(chat_id))
    SESSION.close()

    if welc:
        return welc.clean_welcome

    return False


def set_welc_preference(chat_id, should_welcome):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_welcome=should_welcome)
        else:
            curr.should_welcome = should_welcome

        SESSION.add(curr)
        SESSION.commit()


def set_gdbye_preference(chat_id, should_goodbye):
    with INSERTION_LOCK:
        curr = SESSION.query(Welcome).get(str(chat_id))
        if not curr:
            curr = Welcome(str(chat_id), should_goodbye=should_goodbye)
        else:
            curr.should_goodbye = should_goodbye

        SESSION.add(curr)
        SESSION.commit()


def set_custom_welcome(
    chat_id, custom_content, custom_welcome, welcome_type, buttons=None
):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_welcome or custom_content:
            welcome_settings.custom_content = custom_content
            welcome_settings.custom_welcome = custom_welcome
            welcome_settings.welcome_type = welcome_type.value

        else:
            welcome_settings.custom_welcome = DEFAULT_WELCOME
            welcome_settings.welcome_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with WELC_BTN_LOCK:
            prev_buttons = (
                SESSION.query(WelcomeButtons)
                .filter(WelcomeButtons.chat_id == str(chat_id))
                .all()
            )
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = WelcomeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_welcome(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = DEFAULT_WELCOME
    if welcome_settings and welcome_settings.custom_welcome:
        ret = welcome_settings.custom_welcome

    SESSION.close()
    return ret


def set_custom_gdbye(chat_id, custom_goodbye, goodbye_type, buttons=None):
    if buttons is None:
        buttons = []

    with INSERTION_LOCK:
        welcome_settings = SESSION.query(Welcome).get(str(chat_id))
        if not welcome_settings:
            welcome_settings = Welcome(str(chat_id), True)

        if custom_goodbye:
            welcome_settings.custom_leave = custom_goodbye
            welcome_settings.leave_type = goodbye_type.value

        else:
            welcome_settings.custom_leave = DEFAULT_GOODBYE
            welcome_settings.leave_type = Types.TEXT.value

        SESSION.add(welcome_settings)

        with LEAVE_BTN_LOCK:
            prev_buttons = (
                SESSION.query(GoodbyeButtons)
                .filter(GoodbyeButtons.chat_id == str(chat_id))
                .all()
            )
            for btn in prev_buttons:
                SESSION.delete(btn)

            for b_name, url, same_line in buttons:
                button = GoodbyeButtons(chat_id, b_name, url, same_line)
                SESSION.add(button)

        SESSION.commit()


def get_custom_gdbye(chat_id):
    welcome_settings = SESSION.query(Welcome).get(str(chat_id))
    ret = DEFAULT_GOODBYE
    if welcome_settings and welcome_settings.custom_leave:
        ret = welcome_settings.custom_leave

    SESSION.close()
    return ret


def get_welc_buttons(chat_id):
    try:
        return (
            SESSION.query(WelcomeButtons)
            .filter(WelcomeButtons.chat_id == str(chat_id))
            .order_by(WelcomeButtons.id)
            .all()
        )
    finally:
        SESSION.close()


def get_gdbye_buttons(chat_id):
    try:
        return (
            SESSION.query(GoodbyeButtons)
            .filter(GoodbyeButtons.chat_id == str(chat_id))
            .order_by(GoodbyeButtons.id)
            .all()
        )
    finally:
        SESSION.close()


def clean_service(chat_id: Union[str, int]) -> bool:
    try:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if chat_setting:
            return chat_setting.clean_service
        return False
    finally:
        SESSION.close()


def set_clean_service(chat_id: Union[int, str], setting: bool):
    with CS_LOCK:
        chat_setting = SESSION.query(CleanServiceSetting).get(str(chat_id))
        if not chat_setting:
            chat_setting = CleanServiceSetting(chat_id)

        chat_setting.clean_service = setting
        SESSION.add(chat_setting)
        SESSION.commit()


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Welcome).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)

        with WELC_BTN_LOCK:
            chat_buttons = (
                SESSION.query(WelcomeButtons)
                .filter(WelcomeButtons.chat_id == str(old_chat_id))
                .all()
            )
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        with LEAVE_BTN_LOCK:
            chat_buttons = (
                SESSION.query(GoodbyeButtons)
                .filter(GoodbyeButtons.chat_id == str(old_chat_id))
                .all()
            )
            for btn in chat_buttons:
                btn.chat_id = str(new_chat_id)

        SESSION.commit()
