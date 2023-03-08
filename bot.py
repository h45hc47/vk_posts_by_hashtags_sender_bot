import ast
import codecs
import random
import configparser
import vk_api
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def get_posts_id_by_hashtags(wall, hashtag_list):
    posts_id = set()
    counter = 0
    
    for i in range(wall['count']):
        post_hashtags = wall['items'][i]['text'].split(' ')
        for hashtags in hashtag_list:
            for hashtag in hashtags:
                if hashtag in post_hashtags:
                    counter += 1
            if counter == len(hashtags):
                posts_id.add(wall['items'][i]['id'])
            counter = 0
    posts_id = list(posts_id)
    
    return posts_id

def main():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    login = config['authentication']['login']
    password = config['authentication']['password']
    access_token = config['authentication']['access_token']
    owner_id = int(config['authentication']['owner_id'])
    
    hashtag_list = ast.literal_eval(config['bot.configuration']['hashtag_list'])
    quantity = int(config['bot.configuration']['quantity'])
    
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('/send', color=VkKeyboardColor.POSITIVE)
    
    vk_user_session = vk_api.VkApi(login, password)
    vk_user_class_handling = vk_user_session.get_api()
    vk_group_session = vk_api.VkApi(token=access_token)
    vk_group_class_handling = vk_group_session.get_api()
    try:
        vk_user_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    
    longpoll = VkBotLongPoll(vk_group_session, abs(owner_id))
    longpoll_server_data = vk_group_class_handling.groups.getLongPollServer(group_id=abs(owner_id))
    longpoll_key = str(longpoll_server_data['key'])
    longpoll_server = str(longpoll_server_data['key'])
    longpoll_ts = str(longpoll_server_data['key'])
    
    tools = vk_api.VkTools(vk_user_session)
    
    vk_group_class_handling.messages.send(peer_id = 230933173, keyboard = keyboard.get_keyboard(), message = 'a', random_id = get_random_id())
    
    for event in longpoll.listen():
        print(event.type)
        if event.type == VkBotEventType.MESSAGE_NEW:
            text = event.object['message']['text'].split(' ')
            if '/help' == text[0]:
                vk_group_class_handling.messages.send(
                        key = longpoll_key,          
                        server = longpoll_server,
                        ts = longpoll_ts,
                        peer_id = event.object['message']['peer_id'],
                        random_id = get_random_id(),
                  	    message = '/help - помощь\n/add хештеги - добавление хештегов\n/remove хештеги - удаление хештегов\n/list - показать список хештегов\n/send - отправить мемы\n/quantity - показать текущее количество мемов для отправки\n&#12288;&#12288;&#12288;set число - установить кол-во мемов для отправки',
                	    chat_id = event.chat_id
                        )
            elif '/add' == text[0]:
                try:
                    if text[1]:
                        error_counter = 0
                        add_hashtag_list = set()
                        for i in range(1, len(text)):
                            if text[i][0] != '#':
                                error_counter += 1
                        if error_counter != 0:
                            vk_group_class_handling.messages.send(
                                key = longpoll_key,          
                                server = longpoll_server,
                                ts = longpoll_ts,
                                peer_id = event.object['message']['peer_id'],
                                random_id = get_random_id(),
                          	    message = 'Один или несколько хештегов введены неверно.',
                        	    chat_id = event.chat_id
                                )
                        else:
                            for i in range(1, len(text)):
                                add_hashtag_list.add(text[i])
                            add_hashtag_list = list(add_hashtag_list)
                            add_hashtag_list.sort()
                            if add_hashtag_list in hashtag_list:
                                vk_group_class_handling.messages.send(
                                    key = longpoll_key,          
                                    server = longpoll_server,
                                    ts = longpoll_ts,
                                    peer_id = event.object['message']['peer_id'],
                                    random_id = get_random_id(),
                          	        message = 'Текущая комбинация хештегов уже существует!',
                        	        chat_id = event.chat_id
                                    )
                            else:
                                hashtag_list.append(add_hashtag_list)
                                config['bot.configuration']['hashtag_list'] = str(hashtag_list)
                                with codecs.open('config.ini', 'w', 'utf-8') as configfile:
                                    config.write(configfile)
                                hashtag_list = ast.literal_eval(config['bot.configuration']['hashtag_list'])
                                vk_group_class_handling.messages.send(
                                    key = longpoll_key,          
                                    server = longpoll_server,
                                    ts = longpoll_ts,
                                    peer_id = event.object['message']['peer_id'],
                                    random_id = get_random_id(),
                          	        message = f'Хештеги добавлены: {add_hashtag_list}',
                        	        chat_id = event.chat_id
                                    )
                except:
                    vk_group_class_handling.messages.send(
                        key = longpoll_key,          
                        server = longpoll_server,
                        ts = longpoll_ts,
                        peer_id = event.object['message']['peer_id'],
                        random_id = get_random_id(),
                  	    message = '/add хештеги - добавление хештегов',
                	    chat_id = event.chat_id
                        )
            elif '/remove' == text[0]:
                try:
                    if text[1]:
                        error_counter = 0
                        remove_hashtag_list = set()
                        for i in range(1, len(text)):
                            if text[i][0] != '#':
                                error_counter += 1
                        if error_counter != 0:
                            vk_group_class_handling.messages.send(
                                key = longpoll_key,          
                                server = longpoll_server,
                                ts = longpoll_ts,
                                peer_id = event.object['message']['peer_id'],
                                random_id = get_random_id(),
                          	    message = 'Один или несколько хештегов введены неверно.',
                        	    chat_id = event.chat_id
                                )
                        else:
                            for i in range(1, len(text)):
                                remove_hashtag_list.add(text[i])
                            remove_hashtag_list = list(remove_hashtag_list)
                            if remove_hashtag_list in hashtag_list:
                                hashtag_list.remove(remove_hashtag_list)
                                config['bot.configuration']['hashtag_list'] = str(hashtag_list)
                                with codecs.open('config.ini', 'w', 'utf-8') as configfile:
                                    config.write(configfile)
                                hashtag_list = ast.literal_eval(config['bot.configuration']['hashtag_list'])
                                vk_group_class_handling.messages.send(
                                    key = longpoll_key,          
                                    server = longpoll_server,
                                    ts = longpoll_ts,
                                    peer_id = event.object['message']['peer_id'],
                                    random_id = get_random_id(),
                          	        message = f'Хештеги удалены: {add_hashtag_list}',
                        	        chat_id = event.chat_id
                                    )
                            else:
                                vk_group_class_handling.messages.send(
                                    key = longpoll_key,          
                                    server = longpoll_server,
                                    ts = longpoll_ts,
                                    peer_id = event.object['message']['peer_id'],
                                    random_id = get_random_id(),
                          	        message = 'Нет такой комбинации хештегов!',
                        	        chat_id = event.chat_id
                                    )
                except:
                    vk_group_class_handling.messages.send(
                        key = longpoll_key,          
                        server = longpoll_server,
                        ts = longpoll_ts,
                        peer_id = event.object['message']['peer_id'],
                        random_id = get_random_id(),
                  	    message = '/remove хештеги - удаление хештегов',
                	    chat_id = event.chat_id
                        )
            elif '/list' == text[0]:
                if len(hashtag_list) == 0:
                    vk_group_class_handling.messages.send(
                        key = longpoll_key,          
                        server = longpoll_server,
                        ts = longpoll_ts,
                        peer_id = event.object['message']['peer_id'],
                        random_id = get_random_id(),
                  	    message = 'Нет добавленных хештегов!',
                	    chat_id = event.chat_id
                        )
                else:
                    vk_group_class_handling.messages.send(
                            key = longpoll_key,          
                            server = longpoll_server,
                            ts = longpoll_ts,
                            peer_id = event.object['message']['peer_id'],
                            random_id = get_random_id(),
                      	    message = hashtag_list,
                    	    chat_id = event.chat_id
                            )
            elif '/send' == text[0]:
                wall = tools.get_all('wall.get', 100, {'owner_id': owner_id})
                posts_id_by_hashtag = get_posts_id_by_hashtags(wall, hashtag_list)
                if len(posts_id_by_hashtag) > quantity:
                    rand_posts_id = random.sample(posts_id_by_hashtag, quantity)
                else:
                    rand_posts_id = random.sample(posts_id_by_hashtag, len(posts_id_by_hashtag))
                if len(rand_posts_id) == 0:
                    vk_group_class_handling.messages.send(
                            key = longpoll_key,          
                            server = longpoll_server,
                            ts = longpoll_ts,
                            peer_id = event.object['message']['peer_id'],
                            random_id = get_random_id(),
                      	    message = 'Не найдено постов по данному списку хештегов.',
                    	    chat_id = event.chat_id
                            )
                else:
                    for id in rand_posts_id:
                        wall_post = f'wall{owner_id}_{id}'
                        vk_group_class_handling.messages.send(peer_id=event.object['message']['peer_id'], attachment=wall_post, random_id=get_random_id())
            elif '/quantity' == text[0]:
                try:
                    if text[1]:
                        if 'set' == text[1]:
                            try:
                                if text[2]:
                                    if int(text[2]) > 0:
                                        config['bot.configuration']['quantity'] = text[2]
                                        with codecs.open('config.ini', 'w', 'utf-8') as configfile:
                                            config.write(configfile)
                                        quantity = int(config['bot.configuration']['quantity'])
                                        vk_group_class_handling.messages.send(
                                            key = longpoll_key,          
                                            server = longpoll_server,
                                            ts = longpoll_ts,
                                            peer_id = event.object['message']['peer_id'],
                                            random_id = get_random_id(),
                  	                        message = f'Кол-во мемов для отправки установлено на {quantity}.',
                	                        chat_id = event.chat_id
                                            )
                                    elif int(text[2]) <= 0:
                                        vk_group_class_handling.messages.send(
                                            key = longpoll_key,          
                                            server = longpoll_server,
                                            ts = longpoll_ts,
                                            peer_id = event.object['message']['peer_id'],
                                            random_id = get_random_id(),
                  	                        message = 'Значение должно быть больше нуля!',
                	                        chat_id = event.chat_id
                                            )
                            except:
                                vk_group_class_handling.messages.send(
                                    key = longpoll_key,          
                                    server = longpoll_server,
                                    ts = longpoll_ts,
                                    peer_id = event.object['message']['peer_id'],
                                    random_id = get_random_id(),
                      	            message = 'set число - установить кол-во мемов для отправки.',
                    	            chat_id = event.chat_id
                                    )
                        else:
                            vk_group_class_handling.messages.send(
                                key = longpoll_key,          
                                server = longpoll_server,
                                ts = longpoll_ts,
                                peer_id = event.object['message']['peer_id'],
                                random_id = get_random_id(),
                      	        message = 'show - показать текущее кол-во мемов для отправки\nset число - установить кол-во мемов для отправки',
                    	        chat_id = event.chat_id
                                )
                except:
                    vk_group_class_handling.messages.send(
                            key = longpoll_key,          
                            server = longpoll_server,
                            ts = longpoll_ts,
                            peer_id = event.object['message']['peer_id'],
                            random_id = get_random_id(),
                      	    message = f'Текущее количество мемом для отправки - {quantity}.',
                    	    chat_id = event.chat_id
                            ) 
        elif event.type == VkBotEventType.WALL_POST_NEW:
            new_post = vk_user_class_handling.wall.get(owner_id=owner_id, count=1)


if __name__ == '__main__':
    main()