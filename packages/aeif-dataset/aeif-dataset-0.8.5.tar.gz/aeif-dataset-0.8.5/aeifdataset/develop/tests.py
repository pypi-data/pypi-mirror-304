import multiprocessing as mp
from aeifdataset import Dataloader
import aeifdataset as ad
from tqdm import tqdm


# Funktion, die in jedem Prozess ausgeführt wird
def save_datarecord_images(datarecord, save_dir):
    for frame in datarecord:
        ad.save_all_images_in_frame(frame, save_dir, create_subdir=True)


def save_dataset_images_multithreaded(dataset, save_dir):
    # Anzahl der Prozessoren festlegen
    num_workers = 6

    # Pool erstellen
    with mp.Pool(processes=num_workers) as pool:
        # Erstellen der Aufgaben für jeden datarecord
        for datarecord in tqdm(dataset, desc="Submitting tasks for datarecords"):
            pool.apply_async(save_datarecord_images, args=(datarecord, save_dir))

        # Warten, bis alle Prozesse abgeschlossen sind
        pool.close()
        pool.join()


if __name__ == '__main__':
    save_dir = '/mnt/dataset/anonymisation/validation/27_09_seq_1/png'
    dataset = Dataloader("/mnt/hot_data/dataset/seq_1_maille/packed")

    frame = dataset[0][0]
