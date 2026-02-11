from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "AAEjyWRYbleDzAfxHHI4SufJfzLt5kzq4b0"

questions = [
    {
        "question": "ما عاصمة اليمن؟",
        "options": ["عدن", "صنعاء", "تعز"],
        "answer": "صنعاء"
    },
    {
        "question": "كم عدد أركان الإسلام؟",
        "options": ["4", "5", "6"],
        "answer": "5"
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["score"] = 0
    context.user_data["q_index"] = 0
    await send_question(update, context)

async def send_question(update, context):
    index = context.user_data["q_index"]
    if index < len(questions):
        question = questions[index]
        keyboard = [[option] for option in question["options"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
        await update.message.reply_text(question["question"], reply_markup=reply_markup)
    else:
        score = context.user_data["score"]
        total = len(questions)
        percentage = (score / total) * 100
        await update.message.reply_text(f"انتهى الاختبار ✅\nدرجتك: {score}/{total}\nالنسبة: {percentage}%")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data["q_index"]
    if index < len(questions):
        user_answer = update.message.text
        correct_answer = questions[index]["answer"]

        if user_answer == correct_answer:
            context.user_data["score"] += 1

        context.user_data["q_index"] += 1
        await send_question(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))

app.run_polling()



