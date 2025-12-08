from data import get_connection, User
from sqlalchemy import update
from datetime import datetime
import os
import random

session = get_connection()

class Model:
    @staticmethod
    def get_photo_list_shuffled():
        PHOTOS_DIR = 'photos'
        if not os.path.exists(PHOTOS_DIR):
            return [], {}, {}
        
        photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        photos = []
        names = {}
        tags = {}

        files = []
        for file in os.listdir(PHOTOS_DIR):
            for ext in photo_extensions:
                if file.lower().endswith(ext):
                    files.append(file)

        files.sort()
        
        for index, file in enumerate(files):
            photos.append(file)
            name_without_ext = file.split('.')[0]
            names[str(index)] = name_without_ext
            
            # Определение тэга по имени файла
            if '_m' in name_without_ext.lower():
                tags[str(index)] = 'Мужчина'
            elif '_f' in name_without_ext.lower():
                tags[str(index)] = 'Женщина'
            else:
                tags[str(index)] = None
        
        random.shuffle(photos)
        return photos, names, tags
    
    @staticmethod
    def get_five_shuffled(correct_answer, names, tags, correct_key):
        correct_tag = tags.get(correct_key)
        
        if correct_key is None:
            return []

        # Фильтруем варианты ответов по тэгу
        if correct_tag in ['Мужчина', 'Женщина']:
            wrong_keys = [key for key in names.keys() 
                         if key != correct_key and tags.get(key) == correct_tag]
        else:
            wrong_keys = [key for key in names.keys() if key != correct_key]

        if len(wrong_keys) >= 4:
            selected_wrong = random.sample(wrong_keys, 4)
        else:
            selected_wrong = wrong_keys

        all_options = [correct_key] + selected_wrong

        random.shuffle(all_options)
        
        return all_options

    @staticmethod
    def add_user(user_id, name):
        user = User(user_id=user_id, name=name, score=0)
        session.add(user)
        session.commit()
        session.close()

    @staticmethod
    def add_score(user_id, answer, right_answer):
        score = session.query(User).filter(User.user_id == user_id).first().score
        if answer == right_answer:
            new_score = score + 1
            stmt = update(User).where(User.user_id == user_id).values(score=new_score)
            session.execute(stmt)
            session.commit()
            session.close()

    @staticmethod
    def start_time(user_id):
        date_time_start = datetime.now()
        stmt = update(User).where(User.user_id == user_id).values(time_start=date_time_start)
        session.execute(stmt)
        session.commit()
        session.close()

    @staticmethod
    def end_time(user_id):
        date_time_end = datetime.now()
        stmt = update(User).where(User.user_id == user_id).values(time_end=date_time_end)
        session.execute(stmt)
        session.commit()
        session.close()

    @staticmethod
    def delta_time(user_id):
        user = session.query(User).filter(User.user_id == user_id).first()
        start = user.time_start
        end = user.time_end
        compl = end - start
        stmt = update(User).where(User.user_id == user_id).values(time_completion=str(compl))
        session.execute(stmt)
        session.commit()
        session.close()
        return compl
    
    @staticmethod
    def get_score(user_id):
        score = session.query(User).filter(User.user_id == user_id).first().score
        return score
    
    @staticmethod
    def get_user(user_id):
        user = session.query(User).filter(User.user_id == user_id).first()
        if user:
            return user.name
        else:
            return False
            
    @staticmethod
    def zero_score(user_id):
        stmt = update(User).where(User.user_id == user_id).values(score=0)
        session.execute(stmt)
        session.commit()
        session.close()