from google.cloud import firestore
from google.oauth2 import service_account
from datetime import datetime
import logging

class FirestoreManager:
    def __init__(self, credentials_file, set_):
        # 로깅 설정
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # 서비스 계정 자격 증명 로드
        self.credentials = service_account.Credentials.from_service_account_file(credentials_file)
        self.logger.info("Credentials loaded successfully.")
        
        # Firestore 클라이언트 초기화
        self.db = firestore.Client(credentials=self.credentials)
        self.logger.info("Firestore client initialized successfully.")

    def save_dataframe(self, dict_data: dict, collection_name):
        """데이터프레임의 내용을 Firestore에 저장합니다."""
        
        date_key = datetime.now().strftime("%Y-%m-%d")  # 예: "2024-10-19"
        collection_doc_ref = self.db.collection(collection_name)

        date_doc_ref = collection_doc_ref.document(date_key)

        for data_name, dataframe in dict_data.items():
            data_doc_ref = date_doc_ref.collection(data_name)
            for index, row in dataframe.iterrows():
                doc_key = f'doc_{index}'
                doc_ref = data_doc_ref.document(doc_key)
                doc_ref.set(row.to_dict())
                self.logger.info(f"Document {doc_key} added successfully under {collection_name}/{date_key}/{data_name}.")


    def read_data(self, collection_name):
        """Firestore에서 데이터를 읽어옵니다."""
        docs = self.db.collection(collection_name).stream()
        data = {}
        for doc in docs:
            data[doc.id] = doc.to_dict()
            self.logger.info(f"Document {doc.id} retrieved successfully from {collection_name}.")
        return data
