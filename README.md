# e7homework
sudo docker-compose build

sudo docker-compose up


Добавить сообщение:
curl -d "text=3rd message" -X POST http://89.208.211.24:8080/addmessag

Добавить к сообщению теги (через запятую, message_id - будет выведен при предыдущем действии):
curl -d "message_id=5e9857c9295a6e8a6339d45e&tag=three,four" -X POST http://89.208.211.24:8080/addtag

Добавить к сообщению комментарии:
curl -d 'message_id=5e9857c9295a6e8a6339d45e&name=John&text=sdfsfsdf ds s sd' -X POST http://89.208.211.24:8080/addcomment

Просмотр сообщения:
curl -d "message_id=5e9857c9295a6e8a6339d45e" -X GET http://89.208.211.24:8080/message

Просмотр статистики по сообщению:
curl -d "message_id=5e9857c9295a6e8a6339d45e" -X GET http://89.208.211.24:8080/message-stats
