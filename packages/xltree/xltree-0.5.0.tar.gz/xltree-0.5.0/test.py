#
# python test.py all
#
# エクセルで樹形図を描こう
#

import traceback
import datetime
import sys

from tests.e_o1o0 import execute as execute_e_o1o0
from tests.e_o2o0 import execute as execute_e_o2o0
from tests.e_o3o0 import execute as execute_e_o3o0
from tests.e_o4o0 import execute as execute_e_o4o0

from tests.manual import execute as execute_manual
from tests.t_o1o0 import execute as execute_t_o1o0
from tests.t_o1o1o0_tree_model import execute as execute_t_o1o1o0
from tests.t_o2o0 import execute as execute_t_o2o0
from tests.t_o3o1o0 import execute as execute_t_o3o1o0
from tests.t_o3o2o0_do_not_merge_cells import execute as execute_t_o3o2o0
from tests.t_o4o0 import execute as execute_t_o4o0
from tests.t_o5o0 import execute as execute_t_o5o0
from tests.t_o6o0 import execute as execute_t_o6o0
from tests.t_o7o0 import execute as execute_t_o7o0


########################################
# コマンドから実行時
########################################
if __name__ == '__main__':
    """コマンドから実行時"""

    try:
        args = sys.argv

        if 1 < len(args):

            if args[1] == 'all':
                execute_e_o1o0()
                execute_e_o2o0()
                execute_e_o3o0()
                execute_e_o4o0()

                execute_t_o1o0()
                execute_t_o1o1o0()
                execute_t_o2o0()
                execute_t_o3o1o0()
                execute_t_o3o2o0()
                execute_t_o4o0()
                execute_t_o5o0()
                execute_t_o6o0()
                execute_t_o7o0()

            elif args[1] == 'e_o1o0':
                execute_e_o1o0()

            elif args[1] == 'e_o2o0':
                execute_e_o2o0()

            elif args[1] == 'e_o3o0':
                execute_e_o3o0()

            elif args[1] == 'e_o4o0':
                execute_e_o4o0()

            elif args[1] == 't_o1o0':
                execute_t_o1o0()

            elif args[1] == 't_o1o1o0':
                execute_t_o1o1o0()

            elif args[1] == 't_o2o0':
                execute_t_o2o0()

            elif args[1] == 't_o3o1o0':
                execute_t_o3o1o0()

            elif args[1] == 't_o3o2o0':
                execute_t_o3o2o0()

            elif args[1] == 't_o4o0':
                execute_t_o4o0()

            elif args[1] == 't_o5o0':
                execute_t_o5o0()

            elif args[1] == 't_o6o0':
                execute_t_o6o0()

            elif args[1] == 't_o7o0':
                execute_t_o7o0()

            else:
                raise ValueError(f'unsupported {args[1]=}')
        
        else:
            execute_manual()


    except Exception as err:
        print(f"""\
[{datetime.datetime.now()}] おお、残念！　例外が投げられてしまった！
{type(err)=}  {err=}

以下はスタックトレース表示じゃ。
{traceback.format_exc()}
""")
