import os
from google.cloud import datastore
from datetime import datetime, timezone # to_dictでタイムスタンプの扱いを確実にするため追加

# Datastore クライアントの初期化
# GAE環境ではプロジェクトIDは自動的に決定される
datastore_client = datastore.Client()

class PagespeedResult:
    """Pagespeed Insights の計測結果を保存するための Datastore モデル"""

    KIND = 'PagespeedResult' # Datastoreでのエンティティ種類名

    @staticmethod
    def get_key(url: str, strategy: str):
        """URLとstrategyからユニークなキーを生成"""
        # DatastoreのKeyオブジェクトを返す
        key_name = f"{url}-{strategy}"
        return datastore_client.key(PagespeedResult.KIND, key_name)

    @staticmethod
    def save_result(url: str, strategy: str, result_data: dict):
        """Pagespeed APIの結果をDatastoreに保存する"""
        key = PagespeedResult.get_key(url, strategy)
        entity = datastore.Entity(key=key)

        # 保存するプロパティを設定
        entity.update({
            'url': url,
            'strategy': strategy,
            'timestamp': datetime.now(timezone.utc), # datastore.datetime.datetime.now() の代わりに標準のdatetimeを使用
            'score': result_data.get('score'),
            'fcp': result_data.get('fcp'),
            'lcp': result_data.get('lcp'),
            'cls': result_data.get('cls'),
            'tbt': result_data.get('tbt'),
            'speed_index': result_data.get('speed_index'),
            'tti': result_data.get('tti'),
            'error': result_data.get('error') # エラーが発生した場合も保存
        })

        datastore_client.put(entity)
        return entity

    @staticmethod
    def get_latest_result(url: str, strategy: str):
        """最新の計測結果を取得する"""
        key = PagespeedResult.get_key(url, strategy)
        entity = datastore_client.get(key)
        return entity

    @staticmethod
    def to_dict(entity):
        """Datastore Entity を HTMLテンプレートで利用可能な辞書に変換する"""
        if not entity:
            return None

        # Datastore Entity のプロパティをコピー
        data = dict(entity)

        # タイムスタンプを文字列ではなく datetime オブジェクトとしてそのまま残す
        # survey.py の鮮度チェックで使用するため、datetimeオブジェクトである必要がある
        return data
