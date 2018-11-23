import argparse
import sys
from multiprocessing import Process
from statistics import mean

from algorithms.HillClimbing import HillClimbing
from algorithms.MinConflicts import MinConflicts
from algorithms.SimulatedAnnealing import SimulatedAnnealing

parser = argparse.ArgumentParser()
parser.add_argument(  # Allowed values: all,SA,HC,MC
    '--algo',
    type=str,
    default='*',
    help='Algorithm(s) to solve the N-Queens problem.'
)
parser.add_argument(
    '--start',
    type=int,
    default=8,
    help='Start experiments with this many queens (and end with --stop). If --start and --stop are the same just execute the experiments once.'
)
parser.add_argument(
    '--stop',
    type=int,
    default=8,
    help='Number of queens to stop experiments with.'
)
parser.add_argument(
    '--step',
    type=int,
    default=1,
    help='Increase number of queens between experiments by this much.'
)
parser.add_argument(
    '--repeat',
    type=int,
    default=1,
    help='Times to repeat each experiment.'
)
parser.add_argument(
    '--iter',
    type=int,
    default=5,
    help='Parameter of hill climbing algorithm.'
)
parser.add_argument(
    '--suppress',
    type=bool,
    default=False,
    help='Suppress std output of board statistics.'
)
parser.add_argument(
    '--min_cost',
    type=int,
    default=1e4,
    help='Minimum cost for hill climbing.'
)
parser.add_argument(
    '--t0',
    type=float,
    default=1.0,
    help='Starting temperature for SA.'
)
parser.add_argument(
    '--tmin',
    type=float,
    default=0.001,
    help='End temperature for SA.'
)
parser.add_argument(
    '--cool',
    type=float,
    default=0.99,
    help='Cooling factor for SA.'
)
parser.add_argument(
    '--eps',
    type=float,
    default=1e-5,
    help='Anything below this value is considered 0.'
)


# Routine that runs a specific algorithm a few times and then averages the results.
def run_experiments(_algo, _args):
    _algo.run(_args.start, _args.stop, _args.step, _args.repeat)
    print(_algo)
    for k, v in _algo.results.items():
        print("Average execution time for {0} is {1} with {2} moves on average, calculated by averaging the following times: {3}".format(k, mean(v), int(_algo.moves[k]), v))


if __name__ == '__main__':
    args, unparsed = parser.parse_known_args()  # Very convenient python parser
    print(args.__str__())
    ALGO = None
    if args.algo == 'HC':  # Hill climbing algorithm (BAD)
        ALGO = HillClimbing(args.iter, args.suppress, args.min_cost)
        run_experiments(ALGO, args)
    elif args.algo == 'SA':  # Simulated Annealing algorithm (GOOD)
        ALGO = SimulatedAnnealing(args.suppress, args.t0, args.tmin, args.cool, args.eps)
        run_experiments(ALGO, args)
    elif args.algo == "MC":  # Min conflicts algorithm (BEST)
        ALGO = MinConflicts(args.suppress)
        run_experiments(ALGO, args)
    elif args.algo == 'all' or args.algo == '*':  # Hail Marry mode, 1 process per algorithm, min 3 cores for good results.
        procs = [Process(target=run_experiments, args=(HillClimbing(args.iter, args.suppress, args.min_cost), args,)),
                 Process(target=run_experiments, args=(SimulatedAnnealing(args.suppress, args.t0, args.tmin, args.cool, args.eps), args,)),
                 Process(target=run_experiments, args=(MinConflicts(args.suppress), args,))]

        for proc in procs:
            proc.start()

        for proc in procs:
            proc.join()

    else:
        print('Invalid algorithm given, algorithm:{0}'.format(args.algo))
        sys.exit(-1)
