class configMINIO:

    def __init__(self):
        self.storage_options = {
            'AWS_ENDPOINT_URL': 'http://31.97.241.212:9002',
            'AWS_ACCESS_KEY_ID': 'facundocoria',
            'AWS_SECRET_ACCESS_KEY': 'facundocoria',
            'AWS_ALLOW_HTTP': 'true',
            'AWS_CONDITIONAL_PUT': 'etag',
            'AWS_S3_ALLOW_UNSAFE_RENAME': 'true',
        }
        self.bkt_name = "facundocoria-bucket"

    def pasar_stgopt(self):
        return self.storage_options
    
    def pasar_bkt(self):
        return self.bkt_name