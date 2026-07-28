import os

from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from supabase import create_client

@deconstructible
class SupabaseStorage(Storage):

   
    def __init__(self):

        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

        self.bucket_name = "question-papers"

        # print("SUPABASE URL:", os.getenv("SUPABASE_URL"))
        # print("BUCKET:", self.bucket_name)

        try:
            buckets = self.supabase.storage.list_buckets()

            print("AVAILABLE BUCKETS:")

            for bucket in buckets:
                print(bucket.name)

        except Exception as e:
            print("BUCKET ERROR:", e)


    def _save(self, name, content):

        file_data = content.read()

        self.supabase.storage.from_(
            self.bucket_name
        ).upload(
            path=name,
            file=file_data,
            file_options={
                "content-type": "application/pdf",
                "upsert": True
            }
        )
        

        return name


    def exists(self, name):

        try:

            folder = os.path.dirname(name)
            filename = os.path.basename(name)

            files = self.supabase.storage.from_(
                self.bucket_name
            ).list(
                path=folder
            )

            for file in files:

                if file.get("name") == filename:
                    return True

            return False

        except Exception:

            return False


    def url(self, name):

        response = self.supabase.storage.from_(
            self.bucket_name
        ).create_signed_url(
            name,
            3600
        )

        return response["signedURL"]
    
    def download(self, name):

        return self.supabase.storage.from_(
            self.bucket_name
        ).download(name)