from archytas.react import ReActAgent, FailedTaskError
from archytas.tools import PythonTool
from easyrepl import REPL
from adhoc_api.tool import AdhocApi, APISpec, view_filesystem
from pathlib import Path
from yaml import safe_load


here = Path(__file__).parent




def main():
    python = PythonTool()
    gdc_api = get_gdc_api_spec()
    adhoc_api = AdhocApi(
        apis=[gdc_api],
        drafter_config={'model': 'gemini-1.5-pro-001'},
        finalizer_config={'model': 'gpt-4o'},
        # run_code=python.run  # don't include so top level agent will run the code itself
    )

    tools = [adhoc_api, python, view_filesystem]
    agent = ReActAgent(model='gpt-4o', tools=tools, verbose=True)
    print(agent.prompt)

    # REPL to interact with agent
    for query in REPL(history_file='.chat'):
        try:
            answer = agent.react(query)
            print(answer)
        except FailedTaskError as e:
            print(f"Error: {e}")



def get_gdc_api_spec() -> APISpec:
    documentation = (here/'api_documentation'/'gdc.md').read_text()
    facets = safe_load((here/'api_documentation'/'gdc_facets.yaml').read_text())['facets']
    gdc_api: APISpec = {
        'name': "Genomics Data Commons",
        'cache_key': 'api_assistant_gdc_david_testing',
        'description': GDC_DESCRIPTION,
        'documentation': documentation,
        'proofread_instructions': GDC_ADDITIONAL_INFO.format(facets=facets),
    }
    return gdc_api


GDC_DESCRIPTION = '''\
The NCI's Genomic Data Commons (GDC) provides the cancer research community with a repository and computational
platform for cancer researchers who need to understand cancer, its clinical progression, and response to therapy.
The GDC supports several cancer genome programs at the NCI Center for Cancer Genomics (CCG),
including The Cancer Genome Atlas (TCGA) and Therapeutically Applicable Research to Generate Effective Treatments (TARGET).'''

GDC_ADDITIONAL_INFO = '''
When querying the API, always use the JSON format, not TSV or anything else.
Do not use format="TSV".

Ensure any filters in the request align with the following list of facets provided.
Any filter not conforming to this list is an error and should be corrected.
The filters and their respective choices are as follows:
{facets}


Additionally, any data downloaded should be downloaded to the './data/' directory.
Please ensure the code makes sure this location exists, and all downloaded data is saved to this location.
'''





if __name__ == "__main__":
    main()

