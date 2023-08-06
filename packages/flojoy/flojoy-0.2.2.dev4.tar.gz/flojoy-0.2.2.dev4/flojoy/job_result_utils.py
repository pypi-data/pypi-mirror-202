from flojoy.flojoy_instruction import FLOJOY_INSTRUCTION
from flojoy.plotly_utils import data_container_to_plotly
from rq.job import Job
from redis import Redis
import os

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
redis_connection = Redis(host=REDIS_HOST, port=REDIS_PORT)

def is_flow_controled(result):
    if FLOJOY_INSTRUCTION.FLOW_TO_DIRECTIONS in result or FLOJOY_INSTRUCTION.FLOW_TO_NODES in result:
        return True


def get_next_directions(result):
    if result is None: return ['main']
    return result.get(FLOJOY_INSTRUCTION.FLOW_TO_DIRECTIONS, ['main'])


def get_next_nodes(result):
    if result is None: return []
    return result.get(FLOJOY_INSTRUCTION.FLOW_TO_NODES, [])

def get_data_container_output(result):
    if not result:
        return {}
    if result.get(FLOJOY_INSTRUCTION.DATACONTAINER_FIELD): # to_plot is used
        return result[result[FLOJOY_INSTRUCTION.DATACONTAINER_FIELD]]
    if result.get(FLOJOY_INSTRUCTION.RESULT_FIELD):
        return result[result[FLOJOY_INSTRUCTION.RESULT_FIELD]]
    return result

def get_job_result(job_id: str):
        job = Job.fetch(job_id, connection=Redis(
            host=REDIS_HOST, port=REDIS_PORT))
        result = get_data_container_output(job.result)
        return result
    



def get_data(result):
    if not result:
        return {
            'output': result,
            'result': result
        }
    if result.get(FLOJOY_INSTRUCTION.DATACONTAINER_FIELD): # to_plot is used
        data = result[result[FLOJOY_INSTRUCTION.RESULT_FIELD]] # already processed for plotly
        return {
            'output': result,
            'result': data
        }
    if result.get(FLOJOY_INSTRUCTION.RESULT_FIELD):
        data_container = result[result[FLOJOY_INSTRUCTION.RESULT_FIELD]]
        data = data_container_to_plotly(data=data_container, plot_type=None)
        return {
            'output':result,
            'result': data
        }
    data = data_container_to_plotly(data=result, plot_type=None)
    return {
        'output': result,
        'result': data
    }