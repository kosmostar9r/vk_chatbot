import datetime
from copy import deepcopy
from unittest import TestCase
from unittest.mock import patch, Mock

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent

import settings
from generate_ticket import generate_ticket
from vk_chatbot import Bot


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()

    return wrapper


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1607979076,
                            'from_id': 147786347,
                            'id': 56, 'out': 0,
                            'peer_id': 147786347,
                            'text': 'привет бот',
                            'conversation_message_id': 53,
                            'fwd_messages': [],
                            'important': False,
                            'random_id': 0,
                            'attachments': [],
                            'is_hidden': False},
                 'group_id': 200458364,
                 'event_id': 'fcefd492d42fc1bb130d5a4b7914e28fba5dee3f'}

    CONST_DATE = datetime.date.today()
    while CONST_DATE.day % 3 != 0:
        CONST_DATE += datetime.timedelta(days=1)
    EXPECTED_DATES = []
    EXPECTED_DATETIME = datetime.datetime.combine(CONST_DATE, time=datetime.time(hour=16, minute=25))
    DELTA = datetime.timedelta(days=1)
    while len(EXPECTED_DATES) < 5:
        if EXPECTED_DATETIME.day % 3 == 0:
            EXPECTED_DATES.append(EXPECTED_DATETIME)
        EXPECTED_DATETIME += DELTA

    INPUTS = [
        'asfd',
        'Привет',
        '/help',
        '/ticket',
        'москва',
        'рим',
        datetime.date.today().strftime('%d-%m-%Y'),
        '3',
        '2',
        '-',
        'да',
        '89123456789',
        'email@email.com'
    ]

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.INTENTS[0]['answer'],
        settings.INTENTS[0]['answer'],
        settings.SCENARIOS['ticket']['steps']['step1']['text'],
        settings.SCENARIOS['ticket']['steps']['step2']['text'],
        settings.SCENARIOS['ticket']['steps']['step3']['text'],
        settings.SCENARIOS['ticket']['steps']['step4']['text'].format(
            flies=f'1. {EXPECTED_DATES[0].strftime("%d-%m-%Y %H:%M")}'
                  f'\n2. {EXPECTED_DATES[1].strftime("%d-%m-%Y %H:%M")}'
                  f'\n3. {EXPECTED_DATES[2].strftime("%d-%m-%Y %H:%M")}'
                  f'\n4. {EXPECTED_DATES[3].strftime("%d-%m-%Y %H:%M")}'
                  f'\n5. {EXPECTED_DATES[4].strftime("%d-%m-%Y %H:%M")}'),
        settings.SCENARIOS['ticket']['steps']['step5']['text'],
        settings.SCENARIOS['ticket']['steps']['step6']['text'],
        settings.SCENARIOS['ticket']['steps']['step7']['text'].format(
            departure='Москва',
            arrival='Рим',
            chosen_date=(EXPECTED_DATES[2].strftime("%d-%m-%Y %H:%M")),
            places='2',
            comment='-'),
        settings.SCENARIOS['ticket']['steps']['step8']['text'],
        settings.SCENARIOS['ticket']['steps']['step9']['text'],
        settings.SCENARIOS['ticket']['steps']['step10']['text'],
    ]

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count  # [obj, obj, obj, ...]

        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('vk_chatbot.vk_api.VkApi'):
            with patch('vk_chatbot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.send_image = Mock()
                bot.run()

                bot.on_event.assert_called()
                # bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    @isolate_db
    def test_run_ok(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('vk_chatbot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_image = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_output = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_output.append(kwargs['message'])
        # for real, expec in zip(real_output, self.EXPECTED_OUTPUTS):
        #     print(real)
        #     print('-' * 50)
        #     print(expec)
        #     print('-' * 50)
        #     print(real == expec)
        #     print('_' * 50)

        assert real_output == self.EXPECTED_OUTPUTS

    def test_image_generation(self):
        ticket_file = generate_ticket('departure', 'arrival', '23-02-2021 18:00', 'email@email.com')

        with open('files/ticket_example.png', 'rb') as expected_file:
            expected_bytes = expected_file.read()
        assert ticket_file.read() == expected_bytes
