from orchestra_logger import orcProcess

def run_example_process(correlation_id, creds):
    orcProcessInstance = orcProcess(correlation_id, creds)
    print('Starting complicated process')
    try:
        print('Trying something complicated')
        raise Exception
    except Exception as e:
        print('Failed to do something complicated')
        orcProcessInstance.sendFailure(message = str(e), data={'some':'arbitrary stuff'})
    finally:
        print('Completed')
        orcProcessInstance.sendCompletion(message = 'Completed')

creds = {'apikey':'my_api_key'}
run_example_process('hello', creds)
