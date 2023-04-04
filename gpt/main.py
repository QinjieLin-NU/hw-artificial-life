import src.data_preprocessing.data_downloader as data_downloader
import src.data_preprocessing.data_transformer as data_transformer

if __name__=="__main__":
    data_dir = "../final/data"
    env_pattern = r"terrain\d+"
    seed_list = ["seed1234", "seed2345"] 
    brain_type = "ea"
    rawdata_dir = "./data/raw"
    proprocessdata_dir = "./data/preprocessed"
    
    downloader = data_downloader.DataDownloader()
    raw_file = downloader.download_file(data_dir, env_pattern, seed_list, brain_type, rawdata_dir)
    print("raw data file:",raw_file)

    data_tf = data_transformer.DataTransformer()
    prepcossed_file = data_tf.generate_sequence(raw_file, save_dir=proprocessdata_dir, subset=None)
    print("preprocessed data file:",prepcossed_file) 