# Paste into a watsonx.ai Studio notebook (runtime: "NLP + DO Runtime ... XS").
# Real IBM Watson NLP emotion model. Put your own messages in MESSAGES.
import watson_nlp, json
MESSAGES = ["Paste a message here"]
emo = watson_nlp.load('emotion_aggregated-workflow_en_stock')
out = {m: {"emotion": emo.run(m).to_dict()["emotion_predictions"][0]["emotion"]} for m in MESSAGES}
print(json.dumps(out))
# Copy the printed line, paste it into the app's "Add IBM Watson result" box.
