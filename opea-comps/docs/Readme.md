## Microservices

A MicroService instance does two things:
1. it contains API Gateway to an underlying service.  eg: LLM, Embedding, Reranker.
2. the instance itself is used within the [Orchestrator](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/orchestrator.py) to orchestrate a pipeline within the orchestrator's [directed acyclic graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph)


### Underlying FastAPI App

[MicroService](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/micro_service.py) inherits [HTTPService](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/http_service.py) which inturn inherits [BaseService](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/base_service.py)

BaseService provides some abstract functions you can override, the HTTPService creates a FastAPI app that serves the api via [Uvicorn](https://www.uvicorn.org/) Web server.

There are couple of endpoints defined by HTTPService for this app:
- /v1/health_check
- /v1/health (just points to /health_check)
- /v1/statistics

### Defining a MicroService vs MegaService Service

Here's an example of defining an LLM as a microservice.

```py
llm = MicroService(
    name="llm",
    host=LLM_SERVER_HOST_IP,
    port=LLM_SERVER_PORT,
    endpoint="/v1/chat/completions",
    use_remote_service=True,
    service_type=ServiceType.LLM,
    service_role=ServiceRoleType.MICROSERVICE,
)
```

By checking the [constants.py](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/constants.py) we can see the following `ServiceTypes` that we can be assigned to the microservice.

```
GATEWAY = 0
EMBEDDING = 1
RETRIEVER = 2
RERANK = 3
LLM = 4
ASR = 5
TTS = 6
GUARDRAIL = 7
VECTORSTORE = 8
DATAPREP = 9
UNDEFINED = 10
RAGAS = 11
LVM = 12
KNOWLEDGE_GRAPH = 13
WEB_RETRIEVER = 14
IMAGE2VIDEO = 15
TEXT2IMAGE = 16
ANIMATION = 17
IMAGE2IMAGE = 18
TEXT2SQL = 19
```

We also use `MicroService` class to define the MegaService MicroService by using `ServiceRoleType.MEGASERVICE` (also found in the [constants.py](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/constants.py)).

```py
self.endpoint = "/v1/example-service"
...
self.service = MicroService(
    self.__class__.__name__,
    service_role=ServiceRoleType.MEGASERVICE,
    host=self.host,
    port=self.port,
    endpoint=self.endpoint,
    input_datatype=ChatCompletionRequest,
    output_datatype=ChatCompletionResponse,
)
self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
self.service.start()
```

The MegaService MicroService is defining external endpoints to interact with the Megaservice

Note that `ServiceRoleType` has the following:
```py
MICROSERVICE = 0
MEGASERVICE = 1
```

## ServiceOrchestrator

The [ServiceOrchestrator](https://github.com/opea-project/GenAIComps/blob/main/comps/cores/mega/orchestrator.py) is the actual MegaService. 

```py
self.megaservice = ServiceOrchestrator()
```

ServiceOrchestrator allows you to define the workflow between your services and this flow is managed with a [directed acyclic graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph).


Here is an example of us creating a workflow with the ServiceOrchestrator from multiple MicroServices.

Notice we add the services to ServiceOrchestrator and then we define the flow.

```py
self.megaservice.add(guardrail_in).add(embedding).add(retriever).add(rerank).add(llm)
self.megaservice.flow_to(guardrail_in, embedding)
self.megaservice.flow_to(embedding, retriever)
self.megaservice.flow_to(retriever, rerank)
self.megaservice.flow_to(rerank, llm)
```

## Helper Utilities

There are three helper utilities:

```py
comps.cores.mega.utils
comps.cores.proto.api_protocol
comps.cores.proto.docarray
```

`comps.cores.mega.utils` has functions to check if ports are in use or get interal ip's of servics

`comps.cores.proto.api_protocol` defines machine of the data types for various intputs and outputs

`comps.cores.proto.docarray` defines data types for doc arrays

[DocArray](https://docs.docarray.org/) is a Python library expertly crafted for the representation, transmission, storage, and retrieval of multimodal data


```py
from comps.cores.mega.utils import handle_message
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo,
)
from comps.cores.proto.docarray import LLMParams, RerankerParms, RetrieverParms
```