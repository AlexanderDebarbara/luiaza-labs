create-super-user:
	docker compose run api python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('magalu', 'magalu@magalu.com', 'magalu')"
	echo "Super user criado (username: magalu, password: magalu)"

test:
	docker compose run api pytest
