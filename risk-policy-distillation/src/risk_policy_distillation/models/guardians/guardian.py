import math
import random
import re

import numpy as np

from risk_policy_distillation.models.guardians.judge import Judge


class Guardian(Judge):

    def __init__(self, inference_engine, config):
        super().__init__(config)

        self.inference_engine = inference_engine

    def ask_guardian(self, message):
        if (isinstance(message, tuple) or isinstance(message, list)) and len(
            message
        ) == 2:
            prompt = message[0]
            response = message[1]
        else:
            prompt = message
            response = None

        messages = [{"role": "user", "content": prompt, "name": "test"}]
        if response is not None:
            messages.append({"role": "assistant", "content": response, "name": "test"})

        response = self.inference_engine.chat([messages])
        prediction = re.findall("<score>(.*?)</score>", response[0].prediction)[
            0
        ].strip()
        # output_id = self.output_labels.index(response[0].prediction.split("\n")[0])
        output_id = self.output_labels.index(prediction)

        return self.label_names[output_id]

    def predict_proba(self, inputs):
        messages = []
        for i in inputs:
            messages.append([{"role": "user", "content": i.strip()}])

        responses = self.inference_engine.chat(messages)
        probs = []
        for response in responses:
            prediction = re.findall("<score>(.*?)</score>", response.prediction)[
                0
            ].strip()
            if prediction == self.output_labels[0]:
                prob_no = response.logprobs[prediction]
                probs.append(
                    [
                        math.e**prob_no,
                        1 - math.e**prob_no,
                    ]
                )
            elif prediction == self.output_labels[1]:
                prob_yes = response.logprobs[prediction]
                probs.append(
                    [
                        1 - math.e**prob_yes,
                        math.e**prob_yes,
                    ]
                )

        return np.array(probs)
