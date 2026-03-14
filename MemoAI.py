import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer


class Memo:
   def __init__(self):
      self.model=SentenceTransformer('all-MiniLM-L6-v2')
      self.connect=psycopg2.connect(
                   database='MemoAI',
                   host='...',
                   user='...',
                   password='...',
                   port=0000,
                   )
      self.cur=self.connect.cursor()

   def get_embed(self,note):
      return self.model.encode(note)


   def add_note(self,note,title):
      try:
         self.cur.execute('INSERT INTO notes (note,note_title) VALUES (%s,%s)',(note,title))
         self.connect.commit()
         embed=self.get_embed(note)
         self.cur.execute('INSERT INTO note_embed (note_id,embed) VALUES(currval(\'notes_note_id_seq\'),%s)',(embed.tolist(),))
         self.connect.commit()
      except Exception as e:
         print(f"Error occurred: {e}")

   def show_notes(self):
      try:
         self.cur.execute('SELECT * FROM notes ORDER BY note_id DESC')
         return self.cur.fetchall()
      except Exception as e:
         print(f"Error occurred: {e}")  

   def calculate_similarity(self,note_embed1,note_embed2):
       dot_product=np.dot(note_embed1,note_embed2)
       norm_1 = np.linalg.norm(note_embed1)
       norm_2 = np.linalg.norm(note_embed2)
       return dot_product/(norm_1*norm_2)
   
   def fetch_embed(self,id):
      self.cur.execute('SELECT embed FROM note_embed WHERE note_id=%s',(id,))
      return np.fromstring(self.cur.fetchone()[0].strip('[]'), sep=',')
   
   def get_similarity_note(self,searchvalue,id):
       search_note_embed=self.get_embed(searchvalue)
       return self.calculate_similarity(search_note_embed,self.fetch_embed(id))

   def delete_note(self,id):
      try:
         self.cur.execute("Delete FROM notes WHERE note_id=%s",(id,)) 
         self.connect.commit()
      except Exception as e:
         print(f"Error occurred: {e}")
   
   def fetch_note(self,id):
      try:
         self.cur.execute('SELECT * FROM notes WHERE note_id=%s',(id,))
         return self.cur.fetchone()
      except Exception as e:
         print(f"Error occurred: {e}")
   def modify_note(self,id,title,note):
     try:
       self.cur.execute('UPDATE notes SET note=%s, note_title=%s WHERE note_id=%s',(note,title,id))
       self.connect.commit()
       embed=self.get_embed(note)
       self.cur.execute('UPDATE note_embed SET embed=%s WHERE note_id=%s',(embed.tolist(),id))
     except Exception as e:
       print(f"Error occurred: {e}")

