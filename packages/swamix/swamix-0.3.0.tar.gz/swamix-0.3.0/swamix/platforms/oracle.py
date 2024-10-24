import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient, models
from oci import generative_ai
from typing import Literal


def list_models(compartment_id):
    config = oci.config.from_file()
    # possible regions
    regions = ["sa-saopaulo-1", "eu-frankfurt-1", "uk-london-1", "us-chicago-1"]

    generative_ai_client = generative_ai.GenerativeAiClient(config, service_endpoint="https://generativeai.eu-frankfurt-1.oci.oraclecloud.com")

    list_models_response = generative_ai_client.list_models(compartment_id=compartment_id, capability=["CHAT"], display_name="meta.llama-3.1-70b-instruct")

    return list_models_response.data


def chat(
    user_input,
    model_id: str | None = None,
    region: Literal['us-chicago-1', 'eu-frankfurt-1'] = "eu-frankfurt-1",
):
    # Configuration
    endpoint = f"https://inference.generativeai.{region}.oci.oraclecloud.com"
    # model_id = "ocid1.generativeaimodel.oc1.us-chicago-1.amaaaaaask7dceyarleil5jr7k2rykljkhapnvhrqvzx4cwuvtfedlfxet4q"
    if model_id is None:
        raise ValueError("model_id is required")
    if region not in model_id:
        raise ValueError("model_id must be in the same region as the endpoint, possible misconfiguration by user")

    # Create client
    config = oci.config.from_file()
    # print(config)
    compartment_id = config['tenancy']
    client = GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10, 240))
    # Create chat request
    chat_request = models.ChatDetails(
        serving_mode=models.OnDemandServingMode(model_id=model_id),
        compartment_id=compartment_id,
        chat_request=models.GenericChatRequest(
            api_format=models.BaseChatRequest.API_FORMAT_GENERIC,
            messages=[{"role": "USER", "content": [{"type": "TEXT", "text": user_input}]}],
            max_tokens=600,
            temperature=1,
            frequency_penalty=0,
            presence_penalty=0,
            # top_p=0.75,
            # top_k=-1,
        ),
    )

    # Get chat response
    chat_response = client.chat(chat_request).data.chat_response.choices[0].message.content[0].text

    return chat_response


llama_3170_germany = {
    "model_id": "ocid1.generativeaimodel.oc1.eu-frankfurt-1.amaaaaaask7dceyatobkuq6yg3lqeqhawaj3i7pckwaoeyf2liwnzvgtp6ba",
    "region": "eu-frankfurt-1",
}
# Usage example:
response = chat("biggest known planet in universe, and details", **llama_3170_germany)
print((response))

# list
# response = list_models("ocid1.tenancy.oc1..aaaaaaaacibzcstouxwteyvshebzb2zyw5atfqbaunyqikc46vjccogpjaha")
# print(response)
