# import boto3
# import json

# # Initialize the Bedrock Agent client
# client = boto3.client("bedrock-agent")

# # Your agent's ID
# agent_id = "KRSWKL2QPK"

# # response = client.get_agent(
# #     agentId=agent_id
# # )

# response = client.list_agent_action_groups(
#     agentId=agent_id,
#     agentVersion="DRAFT"  
# )

# # Print the response from the agent
# print(json.dumps(response, indent=2, default=str))

# import boto3
# import json

# # Initialize the Bedrock Agent management client
# client = boto3.client("bedrock-agent")

# agent_id = "KRSWKL2QPK"  # Your existing agent ID

# # Create an alias (if one doesn't already exist)
# alias_response = client.create_agent_alias(
#     agentAliasName="default",
#     agentId=agent_id
# )

# agent_alias_id = alias_response["agentAlias"]["agentAliasId"]
# print("Created agent alias:", agent_alias_id)

import boto3
import json
import uuid

# Initialize the Bedrock Agent Runtime client using the correct service name.
runtime_client = boto3.client("bedrock-agent-runtime")

# Your agent's details
agent_id = "KRSWKL2QPK"
agent_alias_id = "W3TFBX5DRP"
session_id = str(uuid.uuid4())

# Define the input text for the conversation
input_text = "Help me learn about the song 'Die Philosoffen'"

# Invoke the agent
response = runtime_client.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=session_id,
    inputText=input_text
)

print("Response metadata:")
print(json.dumps(response.get("ResponseMetadata", {}), indent=2, default=str))
print("Session ID:", response.get("sessionId"))

# The 'completion' field is an event stream.
print("\nAgent reply (event stream):")
completion_stream = response.get("completion")

# Iterate over the event stream and print out payloads
for event in completion_stream:
    # Check if the event is a dictionary and contains a 'Payload' key
    if isinstance(event, dict) and "Payload" in event:
        payload = event["Payload"]
        # The payload may be in bytes; decode it if necessary
        if isinstance(payload, bytes):
            payload = payload.decode("utf-8")
        try:
            # Try to parse the payload as JSON
            data = json.loads(payload)
            print(json.dumps(data, indent=2))
        except Exception:
            # Otherwise, print the raw payload
            print(payload)
    else:
        # If the event isn't structured as expected, print it directly
        print(event)

