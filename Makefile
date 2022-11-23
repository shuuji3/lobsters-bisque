deploy:
	gcloud functions deploy \
		--region=${LOBSTERS_BISQUE_REGION} \
		--allow-unauthenticated \
		--trigger-http \
		--runtime=python310 \
		--gen2 \
		--entry-point=main \
		${LOBSTERS_BISQUE_FUNCTION_NAME}