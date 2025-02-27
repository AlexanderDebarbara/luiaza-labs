create-super-user:
	sudo docker compose exec api python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('magalu', 'magalu@magalu.com', 'magalu')"
	echo "Super user criado"