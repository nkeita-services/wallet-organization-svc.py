setup: ##@Install Dependencies
	python3 -m venv ~/.virtualenvs/wallet-account-svc.py
	source ~/.virtualenvs/wallet-account-svc.py/bin/activate
	pip3 install -r requirements.txt
up: ##@Run locally
	docker-compose up --build
down: ##@Stop containers
	docker-compose down
deploy: ##@Build and deploy to Cloud Run
	gcloud builds submit --tag gcr.io/wallet-test-256011/wallet-account-svc.py
	gcloud beta run deploy --image gcr.io/wallet-test-256011/wallet-account-svc.py --platform managed --allow-unauthenticated
