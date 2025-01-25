import telebot
from telebot import types
import random
from nltk.corpus import words

token = '7917828499:AAECpr3kvb9dtmedVDY_pMRduQdu58NVJuE'
my_info = 'https://student.computing.dcu.ie/~artem.lytvyn2/portfolio/index.html'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def greeting(message):
    info = ('🎮 Welcome to GameBot! 🕹️\n'
            'Enjoy solo games like Wordle, Tic-Tac-Toe, and more—challenge '
            'yourself and have fun! 🚀')
    markup = types.ReplyKeyboardMarkup()
    b1 = types.KeyboardButton('Wordle')
    b2 = types.KeyboardButton('Rock Paper Scissors')
    b3 = types.KeyboardButton('Dice roller')
    b4 = types.KeyboardButton('Info about me')
    markup.row(b1, b2)
    markup.row(b3, b4)
    bot.send_message(message.chat.id, info, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


@bot.message_handler(commands=['stop'])
def stop_func(message):
    bot.send_message(message.chat.id, "GAME OVVVVVVER")


def on_click(message):
    if message.text == 'Wordle':
        text = ('🟩 Welcome to Wordle! 🟨\n'
                'Guess the 5-letter word in 6 attempts! \nEach guess will show colored clues '
                'to help you find the correct word. '
                'Green means correct letters, yellow means the letter is in the word but in the wrong position, '
                'and gray means the letter isn’t in the word at all. Ready to play?')
        bot.send_message(message.chat.id, text)

        i = 0
        word_list = words.words()
        five_letter_words = [word.lower() for word in word_list if len(word) == 5]
        word = random.choice(five_letter_words)
        left_attempts = 6
        bot.send_message(message.chat.id, f'Enter your guess')

        @bot.message_handler(func=lambda message: True)
        def inp(respond):
            nonlocal i
            value = 0
            if i < left_attempts:
                bot.send_message(message.chat.id, f'Attempts: {left_attempts - i}\tEnter your guess')
                g = respond.text.strip().lower()

                if g in five_letter_words:
                    guess = list(g)
                    j = 0
                    while j < len(guess):
                        if guess[j] == word[j]:
                            guess[j] = f'{guess[j]}🟩'
                            value += 1
                        elif guess[j] in word:
                            guess[j] = f'{guess[j]}🟨'
                        else:
                            guess[j] = f'{guess[j]}⬛'
                        j += 1

                    bot.send_message(message.chat.id, ' '.join(guess))
                    i += 1

                    if value == 5:
                        bot.send_message(message.chat.id, "🎉 YOU WON!!! 🎉\nTo play again, type /start.")
                        return

                else:
                    bot.send_message(message.chat.id, 'Invalid word or not 5 letters!')

                if i == left_attempts and value != 5:
                    bot.send_message(message.chat.id, f"You lost :(\nThe word was: {word}")
                    return
            else:
                return

    elif message.text == 'Rock Paper Scissors':
        info = ("Rock, Paper, Scissors Game! ✊✋✌️\nHey there! Ready to play Rock, Paper, Scissors?\nChoose "
                "your move and let's see if you can beat the bot! Good luck! 🎮")

        bot.send_message(message.chat.id, info)
        bot.send_message(message.chat.id, f'Pick rock, paper or scissors ✊✋✌️')

        def rps(respond):
            choices = ['rock', 'paper', 'scissors']
            robot = random.choice(choices)
            player = respond.text.strip().lower()
            if player not in choices:
                bot.send_message(respond.chat.id, "You can only choose from rock, paper, or scissors!")
            else:
                if (player == 'rock' and robot == 'scissors') or (player == 'paper' and robot == 'rock') or (
                        player == 'scissors' and robot == 'paper'):
                    bot.send_message(respond.chat.id, 'You won! 🎉')
                elif player == robot:
                    bot.send_message(respond.chat.id, 'It\'s a draw!')
                else:
                    bot.send_message(respond.chat.id, 'You lost 😢')
                bot.send_message(respond.chat.id, f'Robot picked {robot}.\nType /start to play again.')

            bot.clear_step_handler_by_chat_id(respond.chat.id)

        @bot.message_handler(func=lambda message: True)
        def game_handler(respond):
            rps(respond)

    elif message.text == 'Dice roller':
        bot.send_message(message.chat.id, "Dice 🎲🎲🎲")
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('1 dice', callback_data='1')
        btn2 = types.InlineKeyboardButton('2 dice', callback_data='2')
        btn3 = types.InlineKeyboardButton('3 dice', callback_data='3')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, "How many dices do you need?", reply_markup=markup)

        @bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3'])
        def dice_game(call):
            c = call.data
            d = [1, 2, 3, 4, 5, 6]
            results = [random.choice(d) for _ in range(int(c))]
            result_string = ' '.join([f'🎲 -> {r}' for r in results])
            bot.send_message(call.message.chat.id, result_string)
            bot.send_message(call.message.chat.id, "To play again, choose an option or type /start.")
            bot.register_next_step_handler(call.message, on_click)

    elif message.text == 'Info about me':
        bot.send_message(message.chat.id, f"Best of the best ≡ Artem Lytvyn (student "
                                          f"in DCU, Computer Science)\nPortfolio: {my_info}")


bot.polling(none_stop=True)
