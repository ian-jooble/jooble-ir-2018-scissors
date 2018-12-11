from google_drive_downloader import GoogleDriveDownloader as gdd

import os
import config_global as config

if not exit(os.path.join(config.index_dir)):
    os.makedirs(os.path.join(config.index_dir))


gdd.download_file_from_google_drive(file_id='1fExvkfef61ADTZ8TVkdNIBlhAmznX_YK',
                                    dest_path=os.path.join(config.index_dir, "documents_id.json"),
                                    unzip=False)

gdd.download_file_from_google_drive(file_id='1Dws329i0tkGDj5FJq7xBrVDb8K0G_j-h',
                                    dest_path=os.path.join(config.index_dir, "inverted_index.json"),
                                    unzip=False)

gdd.download_file_from_google_drive(file_id='1Kwq_L4UnHs-hMQQU-I-KmF1ngSwZ43tM',
                                    dest_path=os.path.join(config.index_dir, "vectorizer_tfidf.dat"),
                                    unzip=False)

gdd.download_file_from_google_drive(file_id='1mzb24qwiKOOrs_H6gYX9QqTX5ZCzSKby',
                                    dest_path=os.path.join(config.index_dir, "forward_index.json"),
                                    unzip=False)
