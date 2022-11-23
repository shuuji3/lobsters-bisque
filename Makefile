deploy:
	gcloud functions deploy \
		--region=${LOBSTERS_BISQUE_REGION} \
		--allow-unauthenticated \
		--trigger-topic=${LOBSTERS_BISQUE_PUBSUB_TOPIC_NAME} \
		--runtime=python310 \
		--gen2 \
		--entry-point=main \
		${LOBSTERS_BISQUE_FUNCTION_NAME}
