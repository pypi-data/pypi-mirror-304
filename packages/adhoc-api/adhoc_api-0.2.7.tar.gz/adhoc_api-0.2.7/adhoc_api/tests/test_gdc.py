from pathlib import Path
import pytest
from pytest import MonkeyPatch, FixtureRequest
from datetime import datetime
import os

from adhoc_api.tool import AdhocApi, PythonTool, view_filesystem
from adhoc_api.examples.gdc import get_gdc_api_spec
from archytas.react import ReActAgent

here = Path(__file__).resolve().parent

import pdb



# Fixture to create the base directory at the start of the test session
@pytest.fixture(scope="session")
def run_base_directory(request: FixtureRequest) -> Path:
    # Define the base directory relative to your project
    base_dir = (here / "runs" / datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(base_dir, exist_ok=True)

    def cleanup():
        # Remove the base directory after the test session if it is empty
        if not os.listdir(base_dir):
            os.rmdir(base_dir)
    request.addfinalizer(cleanup)

    return base_dir


# Fixture to ensure each test runs in a unique directory
@pytest.fixture(autouse=True)
def run_in_project_directory(request: FixtureRequest, run_base_directory, monkeypatch: MonkeyPatch):
    # Get the test function name
    test_name: str = request.node.name

    # Create a unique directory for this test
    test_dir = run_base_directory/test_name
    os.makedirs(test_dir, exist_ok=True)

    # Change to the test-specific directory
    monkeypatch.chdir(test_dir)

    # After the test completes, check if the directory is empty and remove it if so
    yield  # Test runs at this point

    # Clean up: remove the directory if it's empty
    if not os.listdir(test_dir):
        os.rmdir(test_dir)  # Remove only if the directory is empty



def get_cases(filename:str) -> list[str]:
    return (here/filename).read_text().strip().split('\n')


def truncate(s:str, n:int=20) -> str:
    if len(s) <= n + 3:
        return s
    return f'{s[:n]}...'

# collect test cases from the text files
# DEBUG: just the processed cases for now
raw_cases = []#get_cases('queries_(raw).txt')
processed_cases = get_cases('queries_(processed).txt')

# make IDs for each case
raw_cases_ids = [f'GDC_raw_{i}' for i in range(len(raw_cases))]
processed_cases_ids = [f'GDC_processed_{i}' for i in range(len(processed_cases))]


PROOFREAD_EXTRA_INSTRUCTIONS = '''\

Please ensure that any potentially long download processes (e.g. involving multiple files) display a progress bar via the `tqdm` library.
Also assume the user doesn't have any special logins, authorizations, or access tokens/keys/etc. If the code mentions any such, please rewrite it to not require them.
'''

@pytest.mark.skip(reason="Disabled in favor of just using an archytas agent")
@pytest.mark.parametrize('case', raw_cases + processed_cases, ids=raw_cases_ids + processed_cases_ids)
def test_case_simple(case:str):

    # add extra note about progress bars to the proofread instructions
    test_api_spec = get_gdc_api_spec()
    test_api_spec['proofread_instructions'] += PROOFREAD_EXTRA_INSTRUCTIONS

    run_python = PythonTool().run_python
    adhoc_api = AdhocApi(
        apis=[test_api_spec],
        drafter_config={'model': 'gemini-1.5-pro-001'},
        finalizer_config={'model': 'gpt-4-turbo'},
    )
    code = adhoc_api.use_api('Genomics Data Commons', case)

    # add the goal to the code as a comment
    code = f'"""\nGoal: {case}\n"""\n\n{code}'

    # save the generated code to a file for later inspection
    Path('code.py').write_text(code)

    # attempt to run the code
    res, err, code = run_python(code)
    if code != 0:
        # save the traceback to a file for later inspection
        print(f'code error:\n{err}')
        Path(f'traceback.txt').write_text(err)
        raise Exception(f'Error running code: {err}')

    # save the output to a file for later inspection
    print(f'code output:\n{res}')
    Path(f'output.txt').write_text(res)
        

    # TODO: even if code runs, need better way to automatically check results for if they did the right thing


# TODO: honestly with retrying and everything, might just wanna make an archytas agent at this point
@pytest.mark.parametrize('case', raw_cases + processed_cases, ids=raw_cases_ids + processed_cases_ids)
def test_case_archytas(case:str):
    # add extra note about progress bars to the proofread instructions
    test_api_spec = get_gdc_api_spec()
    test_api_spec['proofread_instructions'] += PROOFREAD_EXTRA_INSTRUCTIONS

    def save_code_on_run(code:str, stdout:str, stderr:str, returncode:int):
        """side effect function to save the code+outputs+tracebacks to files"""
        path = Path('code.py')
        i = 0
        while path.exists():
            i += 1
            path = Path(f'code({i}).py')
        path.write_text(code)

        if returncode != 0:
            path = Path(f'traceback({i}).txt') if i > 0 else Path('traceback.txt')
            path.write_text(stderr)
            raise Exception(f'Error running code: {stderr}')
        
        path = Path(f'output({i}).txt') if i > 0 else Path('output.txt')
        path.write_text(stdout)


    python = PythonTool(sideeffect=save_code_on_run)
    adhoc_api = AdhocApi(
        apis=[test_api_spec],
        drafter_config={'model': 'gemini-1.5-pro-001'},
        finalizer_config={'model': 'gpt-4-turbo'},
    )

    tools = [adhoc_api, python, view_filesystem]
    agent = ReActAgent(model='gpt-4o', tools=tools, verbose=True)

    res = agent.react(case)
    print(f'agent final response: {res}\n')