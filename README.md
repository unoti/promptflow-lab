# Azure Prompt Flow Lab
Experimenting with Azure Prompt Flow

In this project we'll start by following this [Azure Prompt Flow guide](https://microsoft.github.io/promptflow/how-to-guides/quick-start.html).  After that we'll look at doing some basic application work with it.

## Setup
I used Python 3.11, but other versions may work.  The above doc suggests 3.9+.

1. Clone this repo
2. Create virtual environment

    ```
    python -m venv venv
    venv\scripts\activate
    ```

3. Install things
    ```
    pip install -r requirements.txt
    ```

4. Verify installation
    ```
    pf -v
    ```
    This should print the version of promptflow, in my case 1.4.1.

# Basics
In this section we'll begin working through the quick start and making notes along the way.

* A flow is a series of functions and subfunctions (a [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph))
* The flow is represented in a YAML file
* Each node may be connected to others and input/output dependencies
* The *prompt flow executor* [executes the flow](https://microsoft.github.io/promptflow/concepts/concept-flows.html).


There's a sample repo at https://github.com/microsoft/promptflow.git.  I'm going to bring in one example from there here, to `examples/flows/web-classification`.

In this example we'll make a flow which categorizes URLs from the web into one of several predefined classes.

## Anatomy of a Flow
A *flow directory* contains all the contents of a flow.  Let's look at one in `examples/flows/web-classification`.  The contents are:

* `flow.dag.yaml`. This is all the nodes in the flow with their inputs and outputs, tools, and other info.
Looking in here we can see several node types. Some reference Python code, others invoke the LLM.
* `.promptflow/flow.tools.json` Defines the tools which we referred to in the yaml.
* Source files `.py`, `.jinja2` Are the source code files for the tools in the flow.
* `requirements.txt` are the packages needed for this flow.

Let's zoom in and look at two nodes in `flow.dag.yaml`:
```yaml
- name: classify_with_llm
  type: llm
  source:
    type: code
    path: classify_with_llm.jinja2
  inputs:
    deployment_name: gpt-35-turbo
    model: gpt-3.5-turbo
    max_tokens: 128
    temperature: 0.2
    url: ${inputs.url}
    text_content: ${summarize_text_content.output}
    examples: ${prepare_examples.output}
  connection: open_ai_connection
  api: chat
- name: convert_to_dict
  type: python
  source:
    type: code
    path: convert_to_dict.py
  inputs:
    input_str: ${classify_with_llm.output}
```

It looks like the first node, `classify_with_llm` invokes the LLM using a jinja2 template.  Let's take a peek at that template, `classify_with_llm.jinja2`:
```jinja
system:
Your task is to classify a given url into one of the following categories:
Movie, App, Academic, Channel, Profile, PDF or None based on the text content information.
The classification will be based on the url, the webpage text content summary, or both.

user:
The selection range of the value of "category" must be within "Movie", "App", "Academic", "Channel", "Profile", "PDF" and "None".
The selection range of the value of "evidence" must be within "Url", "Text content", and "Both".
Here are a few examples:
{% for ex in examples %}
URL: {{ex.url}}
Text content: {{ex.text_content}}
OUTPUT:
{"category": "{{ex.category}}", "evidence": "{{ex.evidence}}"}

{% endfor %}

For a given URL and text content, classify the url to complete the category and indicate evidence:
URL: {{url}}
Text content: {{text_content}}.
OUTPUT:
```

We can see it's going through a loop on the variable `examples`.  By looking further up in the flow YAML, we can see that the examples come from `prepare_examples.py`:
```python
@tool
def prepare_examples():
    return [
        {
            "url": "https://play.google.com/store/apps/details?id=com.spotify.music",
            "text_content": "Spotify is a free music and podcast streaming app with millions of songs, albums, and "
            "original podcasts. It also offers audiobooks, so users can enjoy thousands of stories. "
            "It has a variety of features such as creating and sharing music playlists, discovering "
            "new music, and listening to popular and exclusive podcasts. It also has a Premium "
            "subscription option which allows users to download and listen offline, and access "
            "ad-free music. It is available on all devices and has a variety of genres and artists "
            "to choose from.",
            "category": "App",
            "evidence": "Both",
        },
        ...
    ]
```
But it's not immediately clear how the output from `prepare_examples()` becomes the variable `examples` later on in the template.  There's nothing in the YAML flow that tells it to name the output from this function as `examples`.

However, we can see the `@tool` marker on this function, and there's something in `.promptflow/flow.tools.json` that seems like it could be the missing link. 
* But looking in there, too, I don't see how the output of `prepare_examples.py` becomes the input names `examples` in `classify_with_llm.jinjia2`. Perhaps this will become more clear later.

Let's prepare to run this flow by installing the requirements in requirements.txt.  I looked at those, and it's the 2 requirements we already installed for promptflow, plus Beautiful Soup 4 (an HTML parser).

Run this:
```
```