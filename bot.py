import os
import random
import uuid
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# ============================================================
# QUESTION BANK
# 200 Truths + 200 Dares. Questions are mixed in tone:
# flirty, adult, funny, awkward, unexpected and savage.
# All players must be adults and all dares must be consensual.
# ============================================================

TRUTHS = [
    "Have you ever imagined kissing someone in this chat?",
    "What was your first impression of the other player?",
    "What is the most attractive thing about a man or woman?",
    "Have you ever had a crush on someone you were supposed to avoid?",
    "Have you ever flirted with two people at the same time?",
    "What is your biggest romantic fantasy?",
    "Have you ever kissed someone on the first date?",
    "Have you ever wanted to kiss a close friend?",
    "What is your biggest turn-on?",
    "Have you ever been jealous of someone you were not dating?",
    "Have you ever sent a risky late-night message?",
    "Have you ever hidden a relationship from your friends?",
    "Who in this chat would you choose for a romantic date?",
    "Who in this chat would make you the most nervous on a date?",
    "Have you ever kissed someone and immediately regretted it?",
    "Have you ever wanted someone who was already taken?",
    "What is the boldest move you have made on someone?",
    "Have you ever stalked a crush's social media?",
    "Have you ever lied about your relationship status?",
    "Have you ever gone back to an ex?",
    "What is your biggest dating red flag?",
    "What is your biggest relationship green flag?",
    "Have you ever fallen for someone at first sight?",
    "Have you ever kissed more than one person in one night?",
    "Have you ever had a friends-with-benefits situation?",
    "Have you ever been caught flirting?",
    "What makes someone instantly irresistible to you?",
    "Have you ever received a message that made your heart race?",
    "Have you ever imagined marrying someone you just met?",
    "Have you ever lied about your romantic experience?",
    "Have you ever had a secret admirer?",
    "Have you ever kissed someone to make another person jealous?",
    "Have you ever had a crush on a coworker?",
    "What is your favorite kind of kiss?",
    "Have you ever had a romantic dream about someone you know?",
    "What is your biggest turn-off?",
    "Have you ever flirted with someone just to get attention?",
    "Would you rather make the first move or be approached?",
    "What is the most embarrassing thing you have done for love?",
    "Have you ever wanted to confess your feelings but stayed quiet?",
    "Would you date someone your friends disliked?",
    "Would you forgive your partner for flirting with someone else?",
    "Have you ever been tempted to cheat?",
    "What would you never tolerate in a relationship?",
    "Have you ever cried over someone you were not dating?",
    "Who was your most unforgettable kiss?",
    "Would you kiss the other player if they asked?",
    "What is your ideal first date?",
    "What is the most romantic thing someone has done for you?",
    "Have you ever had a crush on two people at once?",
    "Would you date someone who is very jealous?",
    "Have you ever deleted romantic messages to hide them?",
    "What is one thing you have always wanted to try with a partner?",
    "Have you ever been attracted to someone just because of their voice?",
    "What is the boldest romantic message you have ever sent?",
    "Have you ever wanted to kiss someone but lost your courage?",
    "What is one thing that instantly makes you lose interest?",
    "Would you choose love or money?",
    "Would you marry someone you met online?",
    "Have you ever been caught staring at someone attractive?",
    "What is the longest you have had a crush on someone?",
    "Have you ever pretended to be busy to avoid a date?",
    "What is the weirdest thing you have ever found attractive?",
    "Have you ever imagined a whole relationship after one conversation?",
    "Have you ever dressed up hoping to run into someone?",
    "Have you ever sent a flirty message to the wrong person?",
    "Have you ever laughed at the worst possible romantic moment?",
    "What is the stupidest reason you have rejected someone?",
    "Have you ever practiced a kiss on your hand or a pillow?",
    "Have you ever forgotten someone's name during a date?",
    "Have you ever pretended to understand a romantic movie?",
    "Have you ever liked an old photo while deep-diving someone's profile?",
    "Have you ever rehearsed a phone call before making it?",
    "Have you ever been rejected so badly you changed your route?",
    "Have you ever made up an excuse to escape a date?",
    "Have you ever had a crush on someone because they smelled good?",
    "Have you ever sent a screenshot to the person in the screenshot?",
    "Have you ever pretended to be asleep to avoid a conversation?",
    "Have you ever imagined what your wedding would look like with a crush?",
    "What is the funniest thing you have done to impress someone?",
    "If your search history became public, how embarrassed would you be?",
    "Would you let your crush read your WhatsApp chats?",
    "If you could read the other player's mind for ten seconds, would you?",
    "If you were the last two people on Earth, would you date the other player?",
    "If your ex wrote your biography, what would the most embarrassing chapter be?",
    "Would you rather your parents read your diary or your romantic messages?",
    "If you had to marry one person you know, who would it be?",
    "What is something you would never admit on a first date?",
    "If you woke up married tomorrow, what would your first reaction be?",
    "Would you kiss the other player for a million dollars?",
    "What is the strangest thing that has ever made you blush?",
    "If your phone exposed one secret, what would it reveal?",
    "What is one thing people assume about you that is completely wrong?",
    "Have you ever pretended to like a gift you absolutely hated?",
    "Have you ever had a crush on a friend's sibling?",
    "Have you ever been attracted to someone much older than you?",
    "Have you ever had a secret hookup?",
    "Have you ever wanted to repeat a kiss immediately?",
    "Have you ever had a crush on someone you met online?",
    "Have you ever had feelings for someone who only saw you as a friend?",
    "Have you ever secretly checked who your crush follows?",
    "Have you ever posted something hoping one specific person would see it?",
    "Have you ever ignored a message because you wanted someone to chase you?",
    "Have you ever been caught checking someone out?",
    "Have you ever pretended not to notice someone flirting with you?",
    "Have you ever had a date so awkward you wanted to disappear?",
    "Have you ever lied about being busy while doing absolutely nothing?",
    "Have you ever fallen for someone after saying you never would?",
    "Have you ever missed an ex but refused to contact them?",
    "Have you ever kept an old romantic message because you could not delete it?",
    "Have you ever gone somewhere mainly because your crush would be there?",
    "Have you ever changed your appearance because of a crush?",
    "Have you ever compared two people you dated?",
    "Have you ever wished an ex would come back?",
    "Have you ever had chemistry with someone you should not want?",
    "Have you ever had a crush on someone in this chat?",
    "What is the first physical feature you notice in someone?",
    "What is the sexiest thing someone has ever whispered to you?",
    "Do you prefer slow romantic intimacy or spontaneous passion?",
    "Have you ever sent a suggestive photo?",
    "What is one fantasy you feel comfortable sharing?",
    "Have you ever had a sexual dream about someone you know?",
    "Would you rather be kissed unexpectedly or asked first?",
    "What kind of flirting works on you every time?",
    "Have you ever been attracted to someone you disliked?",
    "What is the most daring place you have kissed someone?",
    "Have you ever had a secret relationship?",
    "Have you ever been tempted to text an ex late at night?",
    "Would you give someone a second chance after they broke your heart?",
    "What is your most embarrassing dating story?",
    "What is one question you hope the other player does not ask?",
    "What is the most ridiculous lie you have told to impress a date?",
    "Have you ever pretended to be more experienced than you are?",
    "Have you ever had a crush on a teacher or professor when you were an adult?",
    "Have you ever flirted with someone in front of your partner?",
    "Have you ever been caught making out?",
    "What is the most unexpected thing you find attractive?",
    "What is your most irrational jealousy trigger?",
    "Would you date someone who earns less than you?",
    "Would you date someone who lives far away?",
    "Would you date someone with a completely opposite personality?",
    "What is the worst date excuse you have ever heard?",
    "Have you ever pretended to enjoy a date just to be polite?",
    "What is the most awkward thing that has happened during a kiss?",
    "Have you ever called someone by an ex's name?",
    "Have you ever sent a message and immediately thrown your phone away?",
    "What is the funniest nickname an ex gave you?",
    "Have you ever had a crush on someone because of their laugh?",
    "Have you ever fallen for a friend after seeing them dressed up?",
    "What would make you instantly say yes to a second date?",
    "What would make you leave a date immediately?",
    "Have you ever been attracted to two people in the same friend group?",
    "What is one romantic rule you secretly disagree with?",
    "Would you rather have amazing chemistry or complete trust?",
    "Would you rather be someone's first love or their last love?",
    "Have you ever stayed in a relationship longer than you should have?",
    "Have you ever broken someone's heart?",
    "Have you ever had your heart broken and pretended you were fine?",
    "Have you ever wanted someone to make the first move?",
    "What is one thing you are too shy to ask a potential partner?",
    "If the other player asked you on a date right now, what would you say?",
    "What is one thing about the other player you are curious about?",
    "What is the most spontaneous romantic decision you have made?",
    "Have you ever had a crush that lasted for years?",
    "Have you ever kissed someone you barely knew?",
    "Have you ever secretly wished a friendship would become romantic?",
    "What is your biggest secret attraction?",
    "What is one thing that makes you feel desired?",
    "What is the boldest compliment you have wanted to give someone?",
    "If you could relive one romantic moment, which would it be?",
    "What is your most unforgettable late-night conversation?",
    "Have you ever had a date that ended with an unexpected kiss?",
    "What is one harmless secret you are keeping from everyone?",
    "If the other player chose your next date outfit, would you wear it?",
    "What is the funniest thing you have done after being left on read?",
    "Have you ever pretended not to care when you cared a lot?",
    "What is your most controversial dating opinion?",
    "Would you rather date someone hilarious or someone incredibly attractive?",
    "What is one thing you wish people understood about you in relationships?",
    "Have you ever fallen for someone because they made you laugh?",
    "What is the most ridiculous thing you have done while jealous?",
    "Have you ever been attracted to a friend's ex?",
    "What is the most awkward compliment you have ever received?",
    "If your crush saw your camera roll, what would you worry about?",
    "Have you ever accidentally revealed a crush to the wrong person?",
    "What is one thing you would change about your last relationship?",
    "Have you ever wanted to kiss someone during an argument?",
    "What is your most unexpected guilty pleasure?",
    "Would you rather have your crush see your browser history or your drafts?",
    "What is one thing you find attractive that most people overlook?",
    "Have you ever made a playlist for someone and never sent it?",
    "Have you ever imagined a future with someone after one date?",
    "What is the most awkward silence you have experienced on a date?",
    "Have you ever pretended to know a song just to impress someone?",
    "If you had to describe your flirting style as an animal, what would it be?",
    "What is one thing you would only do for someone you really like?",
    "Have you ever been caught smiling at your phone?",
    "What is the most unexpected place you have met someone attractive?",
    "Would you rather confess your feelings by text or face to face?",
    "Have you ever been attracted to someone because of their confidence?",
    "What is the biggest romantic risk you would take?",
    "What is one thing that makes a person unforgettable to you?",
    "Have you ever wanted to ask someone out but asked for advice instead?",
    "What is the funniest misunderstanding you have had with a crush?",
    "If you had to give the other player a rating for flirting, what would it be and why?",
    "What is one secret you would reveal only after midnight?",
    "Have you ever had a crush on someone you first met in a group chat?",
    "Would you rather have a passionate romance or a peaceful relationship?",
    "What is one thing you would never share on a first date?",
    "Have you ever been attracted to someone just because they were kind to you?",
    "What is your most dramatic reaction to a breakup?",
    "If your love life were a movie, what would its title be?",
    "What is one thing you would ask the other player if there were no consequences?",
]

DARES = [
    "Look into the other player's eyes for 20 seconds without laughing.",
    "Give the other player your smoothest pickup line.",
    "Describe your ideal kiss in three sentences.",
    "Tell the other player what you first noticed about them.",
    "Give the other player a sincere compliment.",
    "Send a flirty emoji to someone who would welcome it.",
    "Give your best romantic movie-star wink.",
    "Describe your perfect midnight date.",
    "Say something that would make the other player blush.",
    "Send a voice note saying 'I miss you' dramatically.",
    "Give the other player a romantic nickname.",
    "Give your best flirting impression for 20 seconds.",
    "Tell the other player one thing you find attractive about them.",
    "Make up a romantic story involving you and the other player.",
    "Say your smoothest pickup line without laughing.",
    "Describe your first kiss in a dramatic way.",
    "Tell the other player your biggest romantic weakness.",
    "Send a harmless flirty message to someone who would welcome it.",
    "Give the other player three genuine compliments.",
    "Act like you are proposing marriage for 20 seconds.",
    "Sing 15 seconds of a romantic song.",
    "Describe your dream partner in exactly five words.",
    "Send a selfie with your most confident expression.",
    "Say three things you find attractive in a partner.",
    "Pretend you are on a first date with the other player.",
    "Give the other player a ridiculous romantic nickname.",
    "Tell your most embarrassing crush story.",
    "Act jealous for 15 seconds without using words.",
    "Say 'I think I'm falling for you' like a dramatic actor.",
    "Send a romantic song recommendation to the other player.",
    "Tell the other player your biggest turn-on.",
    "Do your best dramatic soap-opera seduction scene.",
    "Say the cheesiest pickup line you know.",
    "Tell the other player your first impression of them.",
    "Make the other player laugh in 20 seconds.",
    "Send a voice note with your best flirting line.",
    "Pretend you are meeting your celebrity crush.",
    "Give the other player a playful wink.",
    "Tell the other player what makes someone irresistible.",
    "Act out how you behave when you have a crush.",
    "Tell the other player one harmless secret.",
    "Make a funny marriage proposal.",
    "Give the other player a 15-second romantic speech.",
    "Compliment the other player without using 'beautiful' or 'handsome'.",
    "Pretend you are a contestant on a dating show and introduce yourself.",
    "Flirt with an imaginary person for 20 seconds.",
    "Recreate your most embarrassing rejection.",
    "Act like a dramatic movie lover who has been left on read.",
    "Give a fake apology for breaking someone's heart.",
    "Say 'I love you' in three different dramatic emotions.",
    "Pretend you are meeting your future in-laws.",
    "Describe yourself as a product someone should buy.",
    "Act jealous of the other player's pillow.",
    "Create a ridiculous wedding vow.",
    "Whisper your best romantic line toward the microphone.",
    "Give the other player a 10-second red-carpet introduction.",
    "Make up a seductive nickname for yourself.",
    "Describe the perfect date without using the word 'romantic'.",
    "Tell the other player what outfit you would wear on a date with them.",
    "Say something sweet in your most serious voice.",
    "Do your best impression of someone trying not to blush.",
    "Pretend to be a jealous partner whose food was stolen.",
    "Give the other player a compliment in a fake newsreader voice.",
    "Make up a ridiculous excuse for being late to a date.",
    "Act like you just saw your crush unexpectedly.",
    "Say a pickup line as if you are delivering a weather forecast.",
    "Describe your ideal partner like you are advertising a car.",
    "Send a voice note laughing like a cartoon villain.",
    "Give the other player a playful one-word review.",
    "Pretend you are accepting an award for best flirt.",
    "Tell the other player a joke that is so bad it becomes funny.",
    "Speak in a dramatic accent for the next two messages.",
    "Make up a fake dating profile headline for yourself.",
    "Describe your love life using only a movie title.",
    "Act like you are trying to impress a very judgmental cat.",
    "Give a dramatic reading of your last sent message, if comfortable.",
    "Invent a ridiculous reason someone should date you.",
    "Say the alphabet as if you are flirting with every letter.",
    "Pretend you are on a cooking show explaining how to make a perfect date.",
    "Make a 10-second commercial for your best quality.",
    "Do your best impression of someone seeing their crush online.",
    "Give the other player a compliment using a silly metaphor.",
    "Say 'you look good' in the most overdramatic way possible.",
    "Pretend to be a detective investigating who has a crush on you.",
    "Act out a breakup with your favourite snack.",
    "Describe your dream date like a football commentator.",
    "Make up a romantic poem with the words 'banana' and 'midnight'.",
    "Try to make the other player blush without mentioning appearance.",
    "Give a fake acceptance speech for winning a flirting competition.",
    "Pretend you are sending a voice note to your secret admirer.",
    "Make a heart with your hands and dedicate it to the other player.",
    "Tell the other player what kind of kiss you prefer.",
    "Describe your perfect romantic getaway.",
    "Give your best seductive movie-trailer voice.",
    "Finish this sentence: 'The most dangerous thing about you is...'",
    "Give the other player a playful compliment in exactly seven words.",
    "Act like you are trying to win back an ex in a soap opera.",
    "Send a goodnight message as if you are deeply in love.",
    "Tell the other player a harmless confession.",
    "Do your best impression of someone who just got a crush.",
    "Pretend to be a relationship expert for 30 seconds.",
    "Describe your ideal partner using only emojis, then explain.",
    "Give the other player a funny award title.",
    "Say your best pickup line in a whisper.",
    "Act out how you look when someone attractive walks past.",
    "Make up a fake scandalous headline about your love life.",
    "Tell the other player what makes a first date unforgettable.",
    "Give a dramatic reading of a fictional love letter.",
    "Pretend to be a celebrity being interviewed about your love life.",
    "Make up a new romantic holiday and explain how to celebrate it.",
    "Send a voice note saying 'I have a confession' in a dramatic tone.",
    "Describe the other player's vibe using three movie genres.",
    "Pretend you are asking the other player out in the year 1920.",
    "Do a 15-second dance like you just got a date.",
    "Give the other player a compliment as if you are a sports commentator.",
    "Say something romantic, then ruin it with a ridiculous ending.",
    "Act like you are trying to flirt while extremely nervous.",
    "Invent a secret handshake with the other player using words only.",
    "Tell the other player your most confident dating advice.",
    "Give your best impression of a person trying to hide a crush.",
    "Pretend you are proposing with an imaginary ring.",
    "Make up a two-line love song about the other player.",
    "Say 'I missed you' in the most unexpected voice you can.",
    "Give the other player a funny but affectionate nickname.",
    "Describe a perfect kiss like a sports replay.",
    "Act out a first date where everything goes hilariously wrong.",
    "Tell the other player one thing you would like to learn about them.",
    "Make a 10-second speech about why you are a catch.",
    "Give the other player a compliment without smiling.",
    "Pretend you are leaving a voicemail for your future spouse.",
    "Make up a romantic excuse to borrow someone's hoodie.",
    "Act like you are jealous of a fictional celebrity.",
    "Tell the other player what song should play during your entrance.",
    "Give a dramatic weather report about your current love life.",
    "Pretend to be a matchmaker and pair the two of you.",
    "Say your best line for asking someone on a second date.",
    "Do your best impression of someone getting caught staring.",
    "Describe your ideal date as if you are pitching a TV show.",
    "Tell the other player one quality that makes them interesting.",
    "Make up a ridiculous love potion recipe using three foods.",
    "Act like you just received a text from your secret crush.",
    "Give the other player a 10-second flirt lesson.",
    "Say a romantic line with a completely straight face.",
    "Pretend to be a nervous person asking for a first kiss.",
    "Make up a funny name for a couple consisting of you two.",
    "Tell the other player a compliment you would usually be too shy to say.",
    "Describe how you would plan a surprise date on a tiny budget.",
    "Act like you are auditioning to be the other player's favourite person.",
    "Give the other player a playful red-carpet interview.",
    "Say one sentence that sounds romantic but is actually about food.",
    "Pretend you are writing a dramatic breakup song about bad Wi-Fi.",
    "Do your best impression of someone trying to look cool.",
    "Make up a ridiculous dating rule that everyone must follow.",
    "Tell the other player what your ideal late-night conversation is about.",
    "Give the other player a compliment using a food comparison.",
    "Pretend you are a love doctor prescribing three dates.",
    "Act out your reaction to getting a 'we need to talk' text.",
    "Say a pickup line as if you are a robot.",
    "Invent a romantic holiday destination in your own bedroom or living room.",
    "Give a 10-second speech explaining why your smile deserves an award.",
    "Pretend you are introducing the other player as your celebrity guest.",
    "Make up a short, funny wedding toast for the two of you.",
    "Tell the other player what makes someone unforgettable.",
    "Act like you are trying to flirt while ordering food.",
    "Send a voice note with a dramatic 'good morning, sunshine'.",
    "Give the other player a playful compliment in a villain voice.",
    "Describe your perfect date using only sound effects.",
    "Pretend you are a news reporter covering your latest crush.",
    "Say something charming in the most awkward way possible.",
    "Make up a two-sentence story about how you met the other player.",
    "Give the other player a funny title such as 'Minister of Making Me Smile'.",
    "Act out a person trying to hide that they are blushing.",
    "Tell the other player one harmless dare you would give them.",
    "Pretend you are recording a dating-app introduction video.",
    "Make up a romantic slogan for yourself.",
    "Say 'you are trouble' in five different moods.",
    "Describe the other player as a fictional character archetype.",
    "Give your best impression of someone trying to recover after an awkward flirt.",
    "Invent a silly reason the two of you would become famous as a couple.",
    "Tell the other player one thing that would make a date instantly better.",
    "Give a dramatic speech about the heartbreak of an empty snack cupboard.",
    "Pretend you are proposing with a spoon as the ring.",
    "Say one sweet thing and one ridiculous thing about the other player.",
    "Act like you are on a reality dating show finale.",
    "Give the other player a playful compliment in a whisper.",
    "Describe your ideal partner as if you are ordering at a restaurant.",
    "Make up a funny excuse for why you are still single.",
    "Do your best impression of a person receiving a surprise kiss in a movie.",
    "Give the other player a 15-second confidence boost.",
    "Pretend to write a love poem about their favourite food.",
    "Say your most confident introduction as if entering a boxing ring.",
    "Make up a ridiculous couple nickname and explain it.",
    "Tell the other player what would make you say yes to a date.",
    "Give a dramatic speech about being left on read for five minutes.",
    "Act like you are trying to impress the other player's pet.",
    "Invent a funny anniversary tradition for the two of you.",
    "Say a romantic sentence as if you are extremely annoyed.",
    "Give the other player a compliment that starts with 'I wasn't expecting to notice...'.",
    "Pretend you are hosting a dating advice podcast.",
    "Make up a fictional story about your most chaotic date.",
    "Give your best impression of someone sending a risky text and panicking.",
    "Tell the other player what you would name a couple's group chat.",
    "Describe your dream date like you are selling tickets to it.",
    "Say one flirty sentence without using the words 'love', 'kiss' or 'beautiful'.",
    "Pretend to be a dramatic narrator describing the other player's entrance.",
    "Make up a funny award for the other player's personality.",
    "Tell the other player one question you would ask on a midnight date.",
    "Give a 10-second speech about why you deserve a second date.",
]

# Keep the question bank concise: exactly 200 original Truths and 200 original Dares.
TRUTHS = TRUTHS[:200]
DARES = DARES[:200]

# ============================================================
# IN-MEMORY GAME STATE
# Note: games reset if the hosting process restarts.
# ============================================================

games = {}


def create_game(user_id, name):
    return {
        "p1_id": user_id,
        "p1_name": name,
        "p2_id": None,
        "p2_name": None,
        "started": False,
        "turn": 1,
        "challenge_id": None,
        "challenge_type": None,
        "used_truths": set(),
        "used_dares": set(),
    }


def get_player(game, user_id):
    if user_id == game["p1_id"]:
        return 1
    if user_id == game["p2_id"]:
        return 2
    return None


def get_name(game, player):
    return game["p1_name"] if player == 1 else game["p2_name"]


def other_player(player):
    return 2 if player == 1 else 1


def get_question(game, category):
    pool = TRUTHS if category == "truth" else DARES
    used = game["used_truths"] if category == "truth" else game["used_dares"]
    available = [question for question in pool if question not in used]

    if not available:
        return None

    question = random.choice(available)
    used.add(question)
    return question


def choice_buttons(code, challenge_id):
    token = challenge_id or ""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔥 TRUTH",
                switch_inline_query_current_chat=f"truth {code} {token}",
            ),
            InlineKeyboardButton(
                "😈 DARE",
                switch_inline_query_current_chat=f"dare {code} {token}",
            ),
            InlineKeyboardButton(
                "🎲 RANDOM",
                switch_inline_query_current_chat=f"random {code} {token}",
            ),
        ],
    ])


def join_button(code):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🎮 JOIN GAME", callback_data=f"join:{code}")
    ]])


def start_button(code):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("▶️ START GAME", callback_data=f"start:{code}")
    ]])


def ready_message(game):
    return (
        f"{game['p1_name']} vs {game['p2_name']}\n"
        f"Next turn: {get_name(game, game['turn'])}"
    )


# ============================================================
# COMMANDS
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 <b>TRUTH OR DARE BABY</b>\n\n"
        "Create a game by typing @TRUTHORDAREBABYBOT in a chat "
        "and selecting START 1-ON-1 GAME.\n\n"
        "Both players must join before Player 1 starts.\\n"
        "Turns switch automatically after each question is selected.",
        parse_mode="HTML",
    )


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query
    user = query.from_user
    text = query.query.strip()

    # Create a new game when inline mode is opened with no query.
    if not text:
        code = uuid.uuid4().hex[:8]
        games[code] = create_game(user.id, user.first_name or "Player 1")
        game = games[code]

        result = InlineQueryResultArticle(
            id=f"game_{code}",
            title="🎮 START 1-ON-1 GAME",
            description="Create a two-player Truth or Dare game",
            input_message_content=InputTextMessageContent(
                "🎮 <b>TRUTH OR DARE BABY</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                "👤 Player 2: <b>Waiting...</b>\n\n"
                "Send this panel to the chat. Player 2 can tap JOIN GAME.",
                parse_mode="HTML",
            ),
            reply_markup=join_button(code),
        )
        await query.answer([result], cache_time=0, is_personal=True)
        return

    parts = text.split()
    if len(parts) < 2:
        await query.answer([], cache_time=0, is_personal=True)
        return

    action = parts[0].lower()
    code = parts[1]
    requested_challenge_id = parts[2] if len(parts) > 2 else ""

    game = games.get(code)
    if not game:
        await query.answer([], cache_time=0, is_personal=True)
        return

    player = get_player(game, user.id)
    if player is None:
        await query.answer(
            [],
            cache_time=0,
            is_personal=True,
        )
        return

    if not game["started"]:
        await query.answer([], cache_time=0, is_personal=True)
        return

    current_token = game["challenge_id"] or ""
    if requested_challenge_id != current_token:
        await query.answer([], cache_time=0, is_personal=True)
        return

    if player != game["turn"]:
        await query.answer([], cache_time=0, is_personal=True)
        return

    if action not in ("truth", "dare", "random"):
        await query.answer([], cache_time=0, is_personal=True)
        return

    # Truth and Dare buttons select from their own pools.
    # RANDOM chooses a fresh question from both pools.
    if action == "truth":
        category = "truth"
        question = get_question(game, category)
    elif action == "dare":
        category = "dare"
        question = get_question(game, category)
    else:
        categories = ["truth", "dare"]
        random.shuffle(categories)
        category = None
        question = None
        for candidate in categories:
            question = get_question(game, candidate)
            if question is not None:
                category = candidate
                break

    if question is None:
        await query.answer([], cache_time=0, is_personal=True)
        return

    # Switch immediately after a question is selected.
    game["turn"] = other_player(player)

    challenge_id = uuid.uuid4().hex[:10]
    game["challenge_id"] = challenge_id
    game["challenge_type"] = category

    next_player_name = get_name(game, game["turn"])
    message = (
        f"{category.title()}\n"
        f"{question}\n\n"
        f"Next turn: {next_player_name}"
    )

    result = InlineQueryResultArticle(
        id=f"challenge_{challenge_id}",
        title=category.title(),
        description=question[:100],
        input_message_content=InputTextMessageContent(
            message,
            parse_mode="HTML",
        ),
        reply_markup=choice_buttons(code, challenge_id),
    )

    # Every selected result is sent as a NEW message.
    # Previous challenge panels are not edited or deleted.
    await query.answer([result], cache_time=0, is_personal=True)


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data or ""
    user = query.from_user

    # JOIN GAME
    if data.startswith("join:"):
        code = data.split(":", 1)[1]
        game = games.get(code)

        if not game:
            await query.answer("This game no longer exists.", show_alert=True)
            return

        if user.id == game["p1_id"]:
            await query.answer("You are already Player 1.", show_alert=True)
            return

        if game["p2_id"] is None:
            game["p2_id"] = user.id
            game["p2_name"] = user.first_name or "Player 2"

            await query.answer("You joined the game!")
            await query.edit_message_text(
                "🎮 <b>TRUTH OR DARE BABY</b>\n\n"
                f"👤 Player 1: <b>{game['p1_name']}</b>\n"
                f"👤 Player 2: <b>{game['p2_name']}</b>\n\n"
                "✅ <b>Both players joined!</b>\n"
                "Player 1 can start the game.",
                parse_mode="HTML",
                reply_markup=start_button(code),
            )
            return

        if user.id == game["p2_id"]:
            await query.answer("You have already joined.", show_alert=True)
            return

        await query.answer("This game already has two players.", show_alert=True)
        return

    # START GAME
    if data.startswith("start:"):
        code = data.split(":", 1)[1]
        game = games.get(code)

        if not game:
            await query.answer("This game no longer exists.", show_alert=True)
            return

        if user.id != game["p1_id"]:
            await query.answer("Only Player 1 can start the game.", show_alert=True)
            return

        if game["p2_id"] is None:
            await query.answer("Waiting for Player 2.", show_alert=True)
            return

        game["started"] = True
        game["turn"] = 1
        game["challenge_id"] = None
        game["challenge_type"] = None
        game["used_truths"].clear()
        game["used_dares"].clear()

        await query.answer("Game started!")
        await query.edit_message_text(
            ready_message(game),
            parse_mode="HTML",
            reply_markup=choice_buttons(code, ""),
        )
        return

    await query.answer("Unknown action.", show_alert=True)


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing from environment variables.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_handler(CallbackQueryHandler(callbacks))

    log.info(
        "Bot starting. Truth bank: %s | Dare bank: %s",
        len(TRUTHS),
        len(DARES),
    )
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
