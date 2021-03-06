import sys
from .models import Error
from .extensions import Senpy
from . import api


def argv_to_dict(argv):
    '''Turns parameters in the form of '--key value' into a dict {'key': 'value'}
    '''
    cli_dict = {}

    for i in range(len(argv)):
        if argv[i][0] == '-':
            key = argv[i].strip('-')
            value = argv[i + 1] if len(argv) > i + 1 else None
            if not value or value[0] == '-':
                cli_dict[key] = True
            else:
                cli_dict[key] = value
    return cli_dict


def main_function(argv):
    '''This is the method for unit testing
    '''
    params = api.parse_params(argv_to_dict(argv),
                              api.CLI_PARAMS,
                              api.API_PARAMS,
                              api.NIF_PARAMS)
    plugin_folder = params['plugin_folder']
    sp = Senpy(default_plugins=False, plugin_folder=plugin_folder)
    request = api.parse_call(params)
    algos = request.parameters.get('algorithm', sp.plugins.keys())
    for algo in algos:
        sp.activate_plugin(algo)
    res = sp.analyse(request)
    return res


def main():
    '''This method is the entrypoint for the CLI (as configured un setup.py)
    '''
    try:
        res = main_function(sys.argv[1:])
        print(res.to_JSON())
    except Error as err:
        print(err.to_JSON())
        sys.exit(2)


if __name__ == '__main__':
    main()
