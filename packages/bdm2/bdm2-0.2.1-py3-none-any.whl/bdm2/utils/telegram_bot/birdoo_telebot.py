import datetime
import time
from enum import Enum
from pathlib import Path

from bdm2.logger import build_logger
from bdm2.utils.dependency_checker import DependencyChecker

required_modules = [
    'telebot'
]

checker = DependencyChecker(required_modules)
checker.check_dependencies()
telebot = checker.get_module('telebot')

# import telebot
import yaml
from bdm2.constants.global_setup.env import MACHINE_ID, SESS_ID
from typing import Union
import os
import random
import warnings

_module_dir = os.path.dirname(os.path.abspath(__file__))

config_path = os.path.join(_module_dir, "sources", "config.yaml")
try:
    config = yaml.load(open(config_path, "r"), yaml.Loader)
except Exception as e:
    warnings.warn("No config file")
else:
    monitoring_chat_id = config["monitoring_chat_id"]
    results_chat_id = config["results_chat_id"]

    restore_chat_id = config["restore_chat_id"]
    engine_full_run_chat_id = config["engine_full_run_chat_id"]
    download_chat_id = config["download_chat_id"]
    aws_download_chat_id = config["aws_download_chat_id"]
    attention_chat_id = config["attention_chat_id"]
    zbage_experiments_chat_id = config["zbage_experiments_chat_id"]

    debug_chat_id = config["debug_chat_id"]

    _DEBUG = config["debug"]
    if _DEBUG:
        restore_chat_id = debug_chat_id
        engine_full_run_chat_id = debug_chat_id
        download_chat_id = debug_chat_id
        attention_chat_id = debug_chat_id

happy_gifs_dir = r"sources\happy_chicken"
sad_gifs_dir = r"sources\sad_chicken"
finish_gif_dir = r"sources\finish.gif"


def generate_info_msg(message: str) -> str:
    return f"{MACHINE_ID} #{SESS_ID} :\n{message}"


def generate_warning_msg(message: str) -> str:
    return f"⚠️WARNING\n{MACHINE_ID} #{SESS_ID} :\n{message}"


def generate_error_msg(message: str) -> str:
    return f"☠️ERROR\n{MACHINE_ID} #{SESS_ID} :\n{message}"


class MessageType(Enum):
    info = 1
    warning = 2
    error = 3
    raw = 4


bot_messages_frequancy = {}


class Bot(telebot.TeleBot):

    def __init__(self, token: str):
        telebot.TeleBot.__init__(self, token)

    def send_random_chicken(self, chat_id: int, mode: str):
        """
        Send predownloaded random gif to chat

        :param chat_id: chat id to send gif
        :type chat_id: int
        :param mode: gif style. "happy" or 'sad' or 'finish'
        :type mode: str
        :return: message object
        :rtype:
        """
        m = None
        while True:
            try:
                if mode == "happy":
                    path = _module_dir + "\\" + happy_gifs_dir
                    gif_list = [x for x in os.listdir(path) if x.endswith("gif")]
                    if len(gif_list) == 0:
                        return
                    gif_fname = path + "\\" + random.sample(gif_list, 1)[0]
                    gif = open(gif_fname, "rb")
                    m = self.send_animation(chat_id, gif)
                    gif.close()
                elif mode == "sad":
                    path = _module_dir + "\\" + sad_gifs_dir
                    gif_list = [x for x in os.listdir(path) if x.endswith("gif")]
                    if len(gif_list) == 0:
                        return
                    gif_fname = path + "\\" + random.sample(gif_list, 1)[0]
                    gif = open(gif_fname, "rb")
                    m = self.send_animation(chat_id, gif)
                    gif.close()
                elif mode == "finish":
                    gif_fname = _module_dir + "\\" + finish_gif_dir
                    gif = open(gif_fname, "rb")
                    m = self.send_animation(chat_id, gif)
                    gif.close()

                break
            except Exception as e:
                time.sleep(1)
        return m

    def make_action(self):

        global bot_messages_frequancy
        if self.token not in bot_messages_frequancy:
            bot_messages_frequancy[self.token] = 0
        bot_messages_frequancy[self.token] += 1

    def generate_msg(self, text: str, message_type: MessageType) -> str:
        """
        Generate str according to message type. Text will be wrapped into Message type stype

        .. todo::
            check message length according to telegram limits

        :param text: message text
        :type text: str
        :param message_type: type of message form header to the message
        :type message_type: MessageType
        :return: output message
        :rtype: str
        """
        if message_type == MessageType.info:
            msg = generate_info_msg(text)
        elif message_type == MessageType.warning:
            msg = generate_warning_msg(text)
        elif message_type == MessageType.error:
            msg = generate_error_msg(text)
        elif message_type == MessageType.raw:
            msg = text
        else:
            raise ValueError(f"Wrong MessageType {message_type}")
        return msg

    def edit_message_save(
            self,
            text: str,
            chat_id: int,
            message_id: int,
            message_type: MessageType = MessageType.info,
            n_max_atempts: int = 1,
            sleep_time: float = 1,
            verbose: bool = False,
    ) -> Union[telebot.types.Message, None]:
        """
        Save function to edit message.
        As telegram bot has limits of action in one chat per minute (20 actions per minute)
        it will try to sent message n_max_atempts with pauses = sleep_time

        :param text: message text
        :type text: str
        :param chat_id: chat id, where message is located
        :type chat_id: int
        :param message_id: message id to update
        :type message_id: int
        :param message_type: type of message to generate right message text
        :type message_type: MessageType
        :param n_max_atempts: max count of tries
        :type n_max_atempts: int
        :param sleep_time: pause between tries
        :type sleep_time: float
        :param verbose: if True, logger.info all try messages
        :type verbose: bool
        :return: if success returm message object
        :rtype:
        """
        logger = build_logger(Path(__file__), save_log=False)
        msg = self.generate_msg(text, message_type=message_type)
        n_attempts = 0
        while True:

            n_attempts += 1
            if n_attempts > n_max_atempts:
                break
            try:
                message = self.edit_message_text(msg, chat_id, message_id)
                self.make_action()
                return message
            except telebot.apihelper.ApiTelegramException as e:
                if "Too Many Requests" in str(e):
                    if verbose:
                        logger.info(
                            f"WAS sent {bot_messages_frequancy[self.token]} messanges before"
                        )
                        logger.info(
                            f"Trying to send status {e}: {n_attempts}/{n_max_atempts}"
                        )
                    time.sleep(sleep_time)
                else:
                    if verbose:
                        logger.info(f"Trying to send error status {e}")
                    return None
        return None

    def send_message_save(
            self,
            chat_id: int,
            text: str,
            message_type: MessageType = MessageType.raw,
            n_max_atempts: int = 1,
            sleep_time: float = 1,
            verbose: bool = False,
    ) -> Union[telebot.types.Message, None]:
        """
        Robust function to send message.
        As telegram bot has limits of action in one chat per minute (20 actions per minute)
        it will try to sent message n_max_atempts with pauses = sleep_time

        :param chat_id: chat id, where message is located
        :type chat_id: int
        :param text: message text
        :type text: str
        :param message_type: type of message to generate right message text
        :type message_type: MessageType
        :param n_max_atempts: max count of tries
        :type n_max_atempts: int
        :param sleep_time: pause between tries
        :type sleep_time: float
        :param verbose: if True, logger.info all try messages
        :type verbose: bool
        :return: if success returm message object
        :rtype:
        """
        logger = build_logger(Path(__file__), save_log=False)
        msg = self.generate_msg(text, message_type=message_type)

        n_attempts = 0
        while True:
            n_attempts += 1
            if n_attempts > n_max_atempts:
                break
            try:
                message = self.send_message(chat_id, msg)
                self.make_action()
                return message
            except telebot.apihelper.ApiTelegramException as e:
                time.sleep(sleep_time)
                if verbose:
                    logger.info(
                        f"WAS sent {bot_messages_frequancy[self.token]} messages before"
                    )
                    logger.info(
                        f"Trying to send status {e}: {n_attempts}/{n_max_atempts}"
                    )
        return None


try:
    if _DEBUG:
        bot = Bot(config["debug_bot_token"])
    else:
        bot = Bot(config["bot_token"])

    info_bot = Bot(config["info_bot_token"])
except Exception as ex:
    warnings.warn("No config file for bot creation")


def chech_throughput():
    logger = build_logger(Path(__file__), save_log=False)
    message = bot.send_message_save(
        attention_chat_id,
        f"{0}: {datetime.datetime.now()}\n\n\n\nsfsdfsfsfs",
        n_max_atempts=100,
        sleep_time=1,
        verbose=True,
    )
    for i in range(100):
        m = f"{i}: {datetime.datetime.now()}"
        logger.info(m)

        bot.edit_message_save(
            f"{i}: {datetime.datetime.now()}",
            attention_chat_id,
            message_id=message.message_id,
            n_max_atempts=100,
            sleep_time=1,
            verbose=True,
        )
