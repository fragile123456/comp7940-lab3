'''
本程序依赖以下模块：
- python-telegram-bot==22.5
- urllib3==2.6.2
- requests
'''
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import configparser
import logging
from ChatGPT_HKBU import ChatGPT
gpt = None

# ========== 新增：导入ChatGPT类并定义全局变量 ==========
from ChatGPT_HKBU import ChatGPT
gpt = None

def main():
    # 配置日志（查看运行状态/错误）
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # 加载配置文件（Telegram Token + ChatGPT API Key）
    logging.info('初始化：加载配置文件...')
    config = configparser.ConfigParser()
    config.read('config.ini')

    # ========== 新增：初始化ChatGPT客户端 ==========
    global gpt
    gpt = ChatGPT(config)

    # 创建Telegram Bot应用实例
    logging.info('初始化：连接Telegram机器人...')
    app = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    # 注册消息处理器
    logging.info('初始化：注册消息处理器...')
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, callback))

    # 启动机器人
    logging.info('初始化：完成！')
    app.run_polling()

# ========== 替换：原回声逻辑→调用ChatGPT的智能回复逻辑 ==========
async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("UPDATE: " + str(update))
    # 先发送“思考中”提示
    loading_message = await update.message.reply_text('Thinking...')

    # 调用ChatGPT获取智能回复
    response = gpt.submit(update.message.text)

    # 替换加载提示为AI回复
    await loading_message.edit_text(response)

if __name__ == '__main__':
    main()