import gc
import datetime
from ..models.database import Table
from ..models.tree_structure.converter import TreeStructureBasedOnTable
from ..settings import Settings
from .draw_tools import TreeDrawer, TreeEraser


class WorksheetHandle():
    """ワークシートへの対応"""


    @staticmethod
    def instantiate(target, based_on, ws, settings_obj, debug_write=False):
        """生成

        Parameters
        ----------
        target : str
            シート名
        based_on : str
            CSVファイルパス
        ws : Worksheet
            ワークシート
        settings_obj : Settings
            各種設定
        debug_write : bool
            デバッグライト
        """

        # CSV読込
        table = Table.from_csv(file_path=based_on)

        # table からツリー構造を作成
        #
        #   NOTE マルチ根にも対応していることに注意してください
        #
        forest = TreeStructureBasedOnTable.read_table_and_planting(table=table)

        return WorksheetHandle(target=target, based_on=based_on, ws=ws, settings_obj=settings_obj, table=table, forest=forest, debug_write=debug_write)


    def __init__(self, target, based_on, ws, settings_obj, table, forest, debug_write=False):
        """初期化

        Parameters
        ----------
        target : str
            シート名
        based_on : str
            CSVファイルパス
        ws : Worksheet
            ワークシート
        settings_obj : Settings
            各種設定
        table : .models.database.Table
            データテーブル
        forest : Forest
            森
        debug_write : bool
            デバッグライト
        """
        self._target = target
        self._based_on = based_on
        self._ws = ws
        self._settings_obj = settings_obj
        self._table = table
        self._forest = forest
        self._debug_write = debug_write


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        del self._target
        del self._based_on
        del self._ws
        del self._settings_obj
        del self._table
        del self._forest
        del self._debug_write

        # メモリ解放
        gc.collect()


    @property
    def forest(self):
        """森"""
        return self._forest


    def render_tree(self):
        """木の描画"""

        # ツリードロワーを用意、描画（都合上、要らない罫線が付いています）
        tree_drawer = TreeDrawer(table=self._table, ws=self._ws, settings_obj=self._settings_obj, debug_write=self._debug_write)
        tree_drawer.render()


        # 要らない罫線を消す
        # DEBUG_TIPS: このコードを不活性にして、必要な線は全部描かれていることを確認してください
        if True:
            tree_eraser = TreeEraser(table=self._table, ws=self._ws, settings_obj=self._settings_obj, debug_write=self._debug_write)
            tree_eraser.render()
        else:
            if self._debug_write:
                print(f"[{datetime.datetime.now()}] eraser disabled")
