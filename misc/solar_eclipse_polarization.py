import os # Operating System Library
import cv2 # OpenCV (Computer Vision) Library
import numpy as np # Numbers & Math Library
import polanalyser # Analysis of Polarized Images Library
from time import perf_counter # perf_counter() Function for Timing
from natsort import natsorted # natsorted() Function for Ordering
import matplotlib.pyplot as plt # For Image Visualizations
from matplotlib.colors import LinearSegmentedColormap # For the Difference Gradient
from scipy.ndimage import median_filter # Find the Median of the 8 Surrounding Pixels

VERBOSE = False
PI = np.pi
ANNULUS_CENTER = (1100, 1088) # (x, y)
ANNULUS_RADII = (620, 952) # (inner, outer)

ORIGINAL_DIR = "2024_04_08_eclipse" 
KEY, RAW_DERIVED, SHIFTED, DIFFERENCE = "keys", "raw_derived", "shifted", "difference"
DIFF_MEDIAN = os.path.join(DIFFERENCE, "_median")
AOLP, DOLP, INTENSITY = "aolp", "dolp", "intensity"
PNGS_AOLP, PNGS_DOLP, PNGS_INTENSITY = "aolp_pngs", "dolp_pngs", "intensity_pngs"


def main() -> None:
    start_time = perf_counter()
    get_color_keys()
    pngs_to_video(src_dir=ORIGINAL_DIR, output_path="2024_04_08_eclipse.mp4")
    
    get_raw_aolp_dolp_intensity(src_dir=ORIGINAL_DIR, output_dir=RAW_DERIVED)
    npys_to_pngs(src_dir=os.path.join(RAW_DERIVED, AOLP), output_dir=os.path.join(RAW_DERIVED, PNGS_AOLP), apply_aolp_color=True)
    npys_to_pngs(src_dir=os.path.join(RAW_DERIVED, DOLP), output_dir=os.path.join(RAW_DERIVED, PNGS_DOLP), apply_dolp_color=True)
    npys_to_pngs(src_dir=os.path.join(RAW_DERIVED, INTENSITY), output_dir=os.path.join(RAW_DERIVED, PNGS_INTENSITY))
    pngs_to_video(src_dir=os.path.join(RAW_DERIVED, PNGS_AOLP), output_path=os.path.join(RAW_DERIVED, "aolp_raw.mp4"))
    pngs_to_video(src_dir=os.path.join(RAW_DERIVED, PNGS_DOLP), output_path=os.path.join(RAW_DERIVED, "dolp_raw.mp4"))
    pngs_to_video(src_dir=os.path.join(RAW_DERIVED, PNGS_INTENSITY), output_path=os.path.join(RAW_DERIVED, "intensity_raw.mp4"))

    get_shifted_aolp_dolp_intensity(src_dir=RAW_DERIVED, output_dir=SHIFTED)
    npys_to_pngs(src_dir=os.path.join(SHIFTED, AOLP), output_dir=os.path.join(SHIFTED, PNGS_AOLP), apply_aolp_color=True)
    npys_to_pngs(src_dir=os.path.join(SHIFTED, DOLP), output_dir=os.path.join(SHIFTED, PNGS_DOLP), apply_dolp_color=True)
    npys_to_pngs(src_dir=os.path.join(SHIFTED, INTENSITY), output_dir=os.path.join(SHIFTED, PNGS_INTENSITY))
    pngs_to_video(src_dir=os.path.join(SHIFTED, PNGS_AOLP), output_path=os.path.join(SHIFTED, "aolp_shifted.mp4"))
    pngs_to_video(src_dir=os.path.join(SHIFTED, PNGS_DOLP), output_path=os.path.join(SHIFTED, "dolp_shifted.mp4"))
    pngs_to_video(src_dir=os.path.join(SHIFTED, PNGS_INTENSITY), output_path=os.path.join(SHIFTED, "intensity_shifted.mp4"))

    get_differences(src_dir=os.path.join(SHIFTED, AOLP), output_dir=os.path.join(DIFFERENCE, AOLP))
    get_differences(src_dir=os.path.join(SHIFTED, DOLP), output_dir=os.path.join(DIFFERENCE, DOLP))
    get_differences(src_dir=os.path.join(SHIFTED, INTENSITY), output_dir=os.path.join(DIFFERENCE, INTENSITY))
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFFERENCE, PNGS_AOLP), min_max=(-PI / 2, PI / 2), aolp=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFFERENCE, PNGS_DOLP), min_max=(-1.53, 1.53))
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFFERENCE, PNGS_INTENSITY), min_max=(-508.0, 508.0))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE, PNGS_AOLP), output_path=os.path.join(DIFFERENCE, "aolp_difference.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE, PNGS_DOLP), output_path=os.path.join(DIFFERENCE, "dolp_difference.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE, PNGS_INTENSITY), output_path=os.path.join(DIFFERENCE, "intensity_difference.mp4"))

    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFF_MEDIAN, PNGS_AOLP), min_max=(-PI / 2, PI / 2), aolp=True, median=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFF_MEDIAN, PNGS_DOLP), min_max=(-1.53, 1.53), median=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFF_MEDIAN, PNGS_INTENSITY), min_max=(-508.0, 508.0), median=True)  
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN, PNGS_AOLP), output_path=os.path.join(DIFF_MEDIAN, "aolp_diff_median.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN, PNGS_DOLP), output_path=os.path.join(DIFF_MEDIAN, "dolp_diff_median.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN, PNGS_INTENSITY), output_path=os.path.join(DIFF_MEDIAN, "intensity_diff_median.mp4"))

    DIFFERENCE_10X = os.path.join(DIFFERENCE, "_10x")
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFFERENCE_10X, PNGS_AOLP), min_max=(-PI / 2, PI / 2), scale=10, aolp=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFFERENCE_10X, PNGS_DOLP), min_max=(-1.53, 1.53), scale=10)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFFERENCE_10X, PNGS_INTENSITY), min_max=(-508.0, 508.0), scale=10)
    pngs_to_video(src_dir=os.path.join(DIFFERENCE_10X, PNGS_AOLP), output_path=os.path.join(DIFFERENCE_10X, "aolp_difference_10x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE_10X, PNGS_DOLP), output_path=os.path.join(DIFFERENCE_10X, "dolp_difference_10x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE_10X, PNGS_INTENSITY), output_path=os.path.join(DIFFERENCE_10X, "intensity_difference_10x.mp4"))

    DIFF_MEDIAN_10X = DIFF_MEDIAN + "10x"
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFF_MEDIAN_10X, PNGS_AOLP), min_max=(-PI / 2, PI / 2), scale=10, aolp=True, median=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFF_MEDIAN_10X, PNGS_DOLP), min_max=(-1.53, 1.53), scale=10, median=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFF_MEDIAN_10X, PNGS_INTENSITY), min_max=(-508.0, 508.0), scale=10, median=True)  
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_10X, PNGS_AOLP), output_path=os.path.join(DIFF_MEDIAN_10X, "aolp_diff_median10x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_10X, PNGS_DOLP), output_path=os.path.join(DIFF_MEDIAN_10X, "dolp_diff_median10x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_10X, PNGS_INTENSITY), output_path=os.path.join(DIFF_MEDIAN_10X, "intensity_diff_median10x.mp4"))

    # DIFFERENCE_25X = os.path.join(DIFFERENCE, "_25x")
    # diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFFERENCE_25X, PNGS_AOLP), min_max=(-PI / 2, PI / 2), scale=25, aolp=True)
    # diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFFERENCE_25X, PNGS_DOLP), min_max=(-1.53, 1.53), scale=25)
    # diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFFERENCE_25X, PNGS_INTENSITY), min_max=(-508.0, 508.0), scale=25)
    # pngs_to_video(src_dir=os.path.join(DIFFERENCE_25X, PNGS_AOLP), output_path=os.path.join(DIFFERENCE_25X, "aolp_difference_25x.mp4"))
    # pngs_to_video(src_dir=os.path.join(DIFFERENCE_25X, PNGS_DOLP), output_path=os.path.join(DIFFERENCE_25X, "dolp_difference_25x.mp4"))
    # pngs_to_video(src_dir=os.path.join(DIFFERENCE_25X, PNGS_INTENSITY), output_path=os.path.join(DIFFERENCE_25X, "intensity_difference_25x.mp4"))

    # DIFF_MEDIAN_25X = DIFF_MEDIAN + "25x"
    # diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFF_MEDIAN_25X, PNGS_AOLP), min_max=(-PI / 2, PI / 2), scale=25, aolp=True, median=True)
    # diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFF_MEDIAN_25X, PNGS_DOLP), min_max=(-1.53, 1.53), scale=25, median=True)
    # diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFF_MEDIAN_25X, PNGS_INTENSITY), min_max=(-508.0, 508.0), scale=25, median=True)  
    # pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_25X, PNGS_AOLP), output_path=os.path.join(DIFF_MEDIAN_25X, "aolp_diff_median25x.mp4"))
    # pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_25X, PNGS_DOLP), output_path=os.path.join(DIFF_MEDIAN_25X, "dolp_diff_median25x.mp4"))
    # pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_25X, PNGS_INTENSITY), output_path=os.path.join(DIFF_MEDIAN_25X, "intensity_diff_median25x.mp4"))

    DIFFERENCE_100X = os.path.join(DIFFERENCE, "_100x")
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFFERENCE_100X, PNGS_AOLP), min_max=(-PI / 2, PI / 2), scale=100, aolp=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFFERENCE_100X, PNGS_DOLP), min_max=(-1.53, 1.53), scale=100)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFFERENCE_100X, PNGS_INTENSITY), min_max=(-508.0, 508.0), scale=100)
    pngs_to_video(src_dir=os.path.join(DIFFERENCE_100X, PNGS_AOLP), output_path=os.path.join(DIFFERENCE_100X, "aolp_difference_100x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE_100X, PNGS_DOLP), output_path=os.path.join(DIFFERENCE_100X, "dolp_difference_100x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFFERENCE_100X, PNGS_INTENSITY), output_path=os.path.join(DIFFERENCE_100X, "intensity_difference_100x.mp4"))

    DIFF_MEDIAN_100X = DIFF_MEDIAN + "100x"
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, AOLP), output_path=os.path.join(DIFF_MEDIAN_100X, PNGS_AOLP), min_max=(-PI / 2, PI / 2), scale=100, aolp=True, median=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, DOLP), output_path=os.path.join(DIFF_MEDIAN_100X, PNGS_DOLP), min_max=(-1.53, 1.53), scale=100, median=True)
    diff_npys_to_pngs(src_dir=os.path.join(DIFFERENCE, INTENSITY), output_path=os.path.join(DIFF_MEDIAN_100X, PNGS_INTENSITY), min_max=(-508.0, 508.0), scale=100, median=True)  
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_100X, PNGS_AOLP), output_path=os.path.join(DIFF_MEDIAN_100X, "aolp_diff_median100x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_100X, PNGS_DOLP), output_path=os.path.join(DIFF_MEDIAN_100X, "dolp_diff_median100x.mp4"))
    pngs_to_video(src_dir=os.path.join(DIFF_MEDIAN_100X, PNGS_INTENSITY), output_path=os.path.join(DIFF_MEDIAN_100X, "intensity_diff_median100x.mp4"))

    print(f"Program Successfully Run in {(perf_counter() - start_time):.2f} Seconds")
    

def npys_to_pngs(src_dir: str, output_dir: str, apply_aolp_color: bool = False, apply_dolp_color: bool = False) -> None:
    start_time = perf_counter()
    print(f"Creating PNGs in '{output_dir}' from NPYs in '{src_dir}'...")
    os.makedirs(output_dir, exist_ok=True)
    for filename in natsorted(os.listdir(src_dir)):
        if filename.endswith(".npy"):
            input_filepath = os.path.join(src_dir, filename)
            npy = np.load(input_filepath)
            if apply_aolp_color: npy = polanalyser.applyColorToAoLP(npy)
            if apply_dolp_color: npy = polanalyser.applyColorToDoP(npy)
            output_filepath = os.path.join(output_dir, filename.replace(".npy", ".png"))
            cv2.imwrite(output_filepath, npy)
            if VERBOSE: print(f"Successfully Created '{output_filepath}' from '{input_filepath}'")
    print(f"Successfully Created All PNGs in {(perf_counter() - start_time):.2f} Seconds\n")


def diff_npys_to_pngs(src_dir: str, output_path: str, min_max: tuple, scale: int = 1, aolp: bool = False, median: bool = False):
    def get_difference_gradient() -> np.ndarray:
        gradient = np.zeros((256, 3), dtype=np.uint8)
        cyan = np.array([255, 255, 0], dtype=np.uint8)
        black = np.array([0, 0, 0], dtype=np.uint8)
        magenta = np.array([255, 0, 255], dtype=np.uint8)
        gradient[:128] = np.array([(1 - (i / 127)) * cyan + (i / 127) * black for i in range(128)], dtype=np.uint8) # Interpolate Between Cyan & Black (0 to 127)
        gradient[128:] = np.array([(1 - ((i - 128) / 127)) * black + ((i - 128) / 127) * magenta for i in range(128, 256)], dtype=np.uint8) # Interpolate Between Black & Magenta (128 to 255)
        return gradient
    

    start_time = perf_counter()
    print(f"Creating PNGs in '{output_path}' from NPYs in '{src_dir}'...")
    os.makedirs(output_path, exist_ok=True)
    for filename in natsorted(os.listdir(src_dir)):
        if filename.endswith(".npy"):
            input_filepath = os.path.join(src_dir, filename)
            npy = np.load(input_filepath)
            if median: npy = median_filter(npy, footprint=np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]))
            if aolp: npy = np.where(npy > PI / 2, PI - npy, np.where( npy < -PI / 2, -PI - npy, npy))
            npy = np.clip((((scale * npy) - min_max[0]) / (min_max[1] - min_max[0])) * 255, 0, 255).astype(np.uint8)
            npy = get_difference_gradient()[npy]
            output_filepath = os.path.join(output_path, filename.replace(".npy", ".png"))
            cv2.imwrite(output_filepath, npy)
            if VERBOSE: print(f"Successfully Created '{output_filepath}' from '{input_filepath}'")
    print(f"Successfully Created All PNGs in {(perf_counter() - start_time):.2f} Seconds\n")


def pngs_to_video(src_dir: str, output_path: str, FPS: int = 8) -> None:
    start_time = perf_counter()
    print(f"Creating MP4 Video ('{output_path}') from PNGs in '{src_dir}'...")
    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (2448, 2048))
    for filename in natsorted(os.listdir(src_dir)):
        if filename.endswith(".png"):
            input_filepath = os.path.join(src_dir, filename)
            png = cv2.imread(input_filepath)
            video.write(png)
            if VERBOSE: print(f"Successfully Added '{input_filepath}' to '{output_path}'")
    video.release()
    print(f"Successfully Created MP4 Video in {(perf_counter() - start_time):.2f} Seconds\n")


def get_raw_aolp_dolp_intensity(src_dir: str = ORIGINAL_DIR, output_dir: str = RAW_DERIVED) -> None:
    start_time = perf_counter()
    print(f"Creating AoLP, DoLP, & Intensity .npy Files in '{output_dir}' from '{src_dir}'...")
    os.makedirs(os.path.join(output_dir, AOLP), exist_ok=True)
    os.makedirs(os.path.join(output_dir, DOLP), exist_ok=True)
    os.makedirs(os.path.join(output_dir, INTENSITY), exist_ok=True)
    for filename in natsorted(os.listdir(src_dir)):
        if filename.startswith("eclipse1-") and filename.endswith(".png"):
            input_filepath = os.path.join(src_dir, filename)
            img_raw = cv2.imread(os.path.join(src_dir, filename), cv2.IMREAD_GRAYSCALE)
            img_000, img_045, img_090, img_135 = polanalyser.demosaicing(img_raw, polanalyser.COLOR_PolarMono)
            image_stokes_vectors = polanalyser.calcStokes([img_000, img_045, img_090, img_135], np.deg2rad([0, 45, 90, 135]))
            aolp, dolp, intensity = polanalyser.cvtStokesToAoLP(image_stokes_vectors), polanalyser.cvtStokesToDoLP(image_stokes_vectors), polanalyser.cvtStokesToIntensity(image_stokes_vectors) # Stokes Vector to AoLP, DoLP, and Intensity
            np.save(os.path.join(output_dir, AOLP, filename[24:].replace(".png", ".npy")), aolp)
            np.save(os.path.join(output_dir, DOLP, filename[24:].replace(".png", ".npy")), dolp)
            np.save(os.path.join(output_dir, INTENSITY, filename[24:].replace(".png", ".npy")), intensity)
            if VERBOSE: print(f"Successfully Created AoLP, DoLP, & Intensity NPYs in '{output_dir}' from '{input_filepath}'")
    print(f"Successfully Created All the AoLP, DoLP, & Intensity .npy Files in {(perf_counter() - start_time):.2f} Seconds\n")
   

def get_shifted_aolp_dolp_intensity(src_dir: str = RAW_DERIVED, output_dir: str = SHIFTED) -> None:
    def calculate_shifts(src_dir: str, reference: str = "3288.npy", shift_type: str = "base") -> list[tuple]:
        start_time = perf_counter()
        print(f"Calculating {shift_type.title()} Shifts from '{src_dir}' with Reference of '{reference}'...")
        npy_filenames = natsorted([filename for filename in os.listdir(src_dir) if filename.endswith(".npy")])
        shifts, ref_shift, prev_npy, annulus_mask = [(0, 0)], None, None, None
        for i, filename in enumerate(npy_filenames):
            input_filepath = os.path.join(src_dir, filename)
            if i > 0:
                curr_npy = np.load(input_filepath)
                if shift_type == "fine": curr_npy = cv2.bitwise_and(curr_npy, curr_npy, mask=annulus_mask)
                shift, _ = cv2.phaseCorrelate(prev_npy, curr_npy)
                shift = (shifts[-1][0] + shift[0], shifts[-1][1] + shift[1])
                shifts.append(shift)
                prev_npy = curr_npy
                if VERBOSE: print(f"Accumulated Shift from {npy_filenames[0]} to {filename}: {shift}")
                if filename == reference: 
                    if VERBOSE: print(f"   ^^^ '{reference}' is the Reference Shift: Every Other Accumulated Shift Will Be Subtracted from This One to Find the Calculated Shifts")
                    ref_shift = shift 
            elif i == 0:
                prev_npy = np.load(input_filepath)
                if shift_type == "fine":
                    annulus_mask = np.zeros(prev_npy.shape, dtype=np.uint8)
                    cv2.circle(annulus_mask, ANNULUS_CENTER, ANNULUS_RADII[1], (255), -1)
                    cv2.circle(annulus_mask, ANNULUS_CENTER, ANNULUS_RADII[0], (0), -1)
                    prev_npy = cv2.bitwise_and(prev_npy, prev_npy, mask=annulus_mask)
        for i, shift in enumerate(shifts):
            offset_shift = (ref_shift[0] - shift[0]), (ref_shift[1] - shift[1])
            shifts[i] = offset_shift
            if VERBOSE: print(f"The Calculated Shift of {npy_filenames[i]} from {reference}: {offset_shift}")
        if VERBOSE: print(f"\n{shift_type}_shifts = {shifts}\n")
        print(f"{shift_type.title()} Shifts Calculations Completed in {(perf_counter() - start_time):.2f} Seconds\n")
        return shifts


    def shift_images(src_dir: str, output_dir: str, shifts: list[tuple] = []) -> None:
        start_time = perf_counter()
        print(f"Creating Shifted NPYs in '{output_dir}' from '{src_dir}'...")
        os.makedirs(output_dir, exist_ok=True)
        for i, filename in enumerate(natsorted(os.listdir(src_dir))):
            input_filepath = os.path.join(src_dir, filename)
            npy = np.load(input_filepath)
            shift_matrix = np.float32([[1, 0, shifts[i][0]], [0, 1, shifts[i][1]]])
            shifted_npy = cv2.warpAffine(npy, shift_matrix, (npy.shape[1], npy.shape[0]), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
            output_filepath = os.path.join(output_dir, filename)
            np.save(output_filepath, shifted_npy)
            if VERBOSE: print(f"Successfully Created '{output_filepath}' from '{input_filepath}'")
        print(f"Successfully Created All the Shifted NPYs in {(perf_counter() - start_time):.2f} Seconds\n")
    
    
    os.makedirs(output_dir, exist_ok=True)
    base_shifts = calculate_shifts(src_dir=os.path.join(src_dir, INTENSITY), reference="3288.npy", shift_type="base")
    # base_shifts = [(497.4034708315485, 128.09313134039724), (498.69665090356375, 128.1846710864728), (499.59085854092746, 127.49207375703065), (500.25220352438373, 127.30425010629904), (501.0876895530005, 127.2114736759678), (501.98717991167405, 126.51292834789172), (503.2832926812973, 126.44109382736349), (504.23229279446514, 125.69142011444296), (505.10572328279454, 125.8487170975734), (506.2001145360307, 126.60028585354166), (507.2632103562769, 125.88345729313755), (508.23136980812615, 125.90003045649746), (508.8202579185354, 125.88037697790037), (509.7615633388002, 125.74732449699206), (510.98508448618713, 124.06531221906687), (511.7569827969521, 123.96399106741285), (512.9791282009244, 124.04858864303753), (514.1810068256068, 124.20197610633011), (515.7203848598942, 124.3979013290026), (516.7144593067703, 124.38026803985429), (517.3894987135031, 124.3615779990023), (518.9341852775724, 122.70008895500553), (519.7179503900502, 122.66420699383491), (520.7683378508314, 122.59320489870765), (522.080655188161, 122.66247432580508), (522.4536319263264, 122.49565236314618), (524.4158757556672, 116.77956293197508), (576.6406417698529, 110.74698392808978), (543.7754448278113, 114.47336703679093), (543.3438280159226, 114.42991924173134), (581.6187464642396, 94.23459242605009), (588.1972674100484, 75.66751955318011), (582.6077829991025, 60.36182853555397), (578.9487621459509, 71.15563218550756), (580.5110016356273, 70.23383771624822), (581.6871450034914, 70.18621299364918), (582.4458183043987, 70.59462083000221), (583.1381176697571, 70.2955373925081), (583.6620298228854, 69.61751674506684), (584.3488820886712, 68.7154741758535), (585.1453525669381, 67.86408317476275), (585.917963601903, 66.89622164896821), (586.7382792576864, 66.4053673423723), (587.0745760229356, 65.70368646696227), (588.4781858520355, 65.05720637845286), (581.6911928840741, 24.130233414522877), (546.1073380483829, 26.258040070873562), (344.5435354205367, 63.760621469906596), (128.76782056763614, 103.16793277892873), (75.28184950993318, 116.20426283559107), (78.74130090170797, 128.69969134036535), (139.68206722606965, 128.5549432397513), (1.9152057132025675, 154.72913372628773), (1.5942413548154946, 154.13134119809672), (-24.18474574117886, 13.218030937564208), (-23.343258262864083, 12.3505079238397), (-23.0153102886311, 10.506437978219992), (-22.311193370186174, 9.480778920946136), (-21.746142121536877, 8.888078702748658), (-20.809702247241376, 8.28367685714943), (-20.05153050771287, 8.010284483938335), (-19.053160842100397, 7.239078347172153), (-18.334674416623784, 6.547662991293123), (-17.861261736591132, 5.672771921241747), (-17.20804358191276, 5.3525906699735515), (-16.225946078714514, 4.376808199673064), (-15.06757683107935, 4.197967214324308), (-14.194928707681356, 3.4405216846896565), (-13.31632006027894, 3.151327171236403), (-12.214824437928883, 3.1933262113365117), (-11.55108684966308, 2.7875327923421764), (-10.925529576292547, 2.6176083538144894), (-9.903984697981286, 2.8798449830422896), (-9.016850322230766, 2.4771623171010333), (-8.364251083813542, 1.567006939077146), (-7.222390649763156, 1.432896324530816), (-6.3366372099203545, 1.2115331106811027), (-5.327380969190926, 0.7223573197049973), (-4.69225531931329, 0.6027377067565567), (-3.9879436226449343, -0.3157147648536238), (-2.8370764168075766, -0.5918476955598635), (-2.204836011324687, -0.7485532250492497), (-1.5540261997075504, -0.41524587206220076), (-0.3036744370569977, 0.20621608233011557), (0.0, 0.0), (0.4607965702405181, -0.7102018651902426), (1.3326157741630595, -1.6673315304284415), (2.294536509218915, -2.051767614544019), (3.0168352466921533, -2.8049820483970507), (3.567646647943093, -2.674728950686813), (4.696468718993174, -2.1849840902336837), (5.412307136437221, -2.5625624010182264), (6.098097875715439, -3.408206453389994), (7.0836106777644545, -4.374813743250343), (7.502143958241959, -5.402269544708474), (8.532087052284623, -5.7824176357264605), (9.173844344301187, -5.759646173942656), (10.002123440766809, -6.139798534802594), (10.783785250285064, -6.405236213370017), (11.50102430725201, -7.230800455029339), (12.422985202927293, -7.675511731314714), (13.421657283956392, -8.024619311365427), (14.095758571722172, -8.0567725029631), (14.961601769516164, -8.697655110161236), (15.748671224167992, -9.628393216081577), (16.823520013078905, -10.13945742737269), (17.762407654668095, -11.16099397617677), (18.679058910276353, -11.898626011212173), (19.835507126491848, -12.368900495446155), (20.432784267728266, -12.28641184767946), (20.97611952639113, -12.641101147060567), (21.73109842080612, -12.795970174514878), (22.166754481194403, -13.589433816354358), (22.978217953420653, -14.285306523673398), (23.82481654326466, -14.673504108994734), (24.599815602804938, -15.782520078076118), (25.366370328540143, -16.74061902778874), (26.124906403058958, -17.222786664962086), (26.670549072706308, -17.418573490007134), (27.515346600448083, -17.678255637329926), (28.66724122255573, -17.68383564573503), (29.123203018475124, -18.4297730741431), (29.56420103059986, -19.51808374560335), (30.59058897493128, -19.54725992535691), (31.316103005222885, -20.07994251311709), (32.26492219531315, -20.73557257613993), (32.95199944687306, -21.1806074755483), (33.839798376258614, -21.505077745492372), (34.32015422177619, -22.066824854284846), (35.00925236307444, -22.67671121477224), (35.883930770581856, -23.059707292287953), (36.748490675008725, -23.31020073300772), (37.460905954052805, -23.309729202164476), (38.061896291951825, -24.488326386155222), (38.57165116197916, -25.42219749187575), (39.21653722475753, -25.52405108277378), (40.08332580052502, -26.17063502291728), (40.77376669035198, -26.81411828533328), (41.9873687758643, -27.127917285587614), (42.73894405464216, -27.553855986833923), (43.186491584111536, -28.544078349046572), (44.02168851967599, -28.926376773202833), (44.96977646448909, -29.518728388848103), (45.67080360931732, -30.067879788137816), (46.12041241066913, -30.536864149800408), (46.66280388602718, -31.814821577254634), (47.397894073897305, -32.595288046183896), (48.32182447591731, -33.073933416697514), (48.925256824056305, -33.773795576164616), (49.61443613596907, -34.44458415686779), (50.68005065391753, -34.94913000986503), (51.09690999816553, -35.489293636452885), (51.812253958498786, -37.253491414567634), (52.66943006672591, -38.19798698513489), (53.0772265431292, -38.8763912742603), (53.82807979804011, -39.34399207123238), (54.59690932462263, -39.789763162402664), (55.1307982823148, -40.73740303434795), (55.5691411273142, -42.03174727859903), (56.21486574782648, -42.66226290601503), (56.94759433877471, -43.263855016017146), (57.78373242924158, -44.16965887217532), (58.72120471950939, -44.443254727824296), (59.37961037949867, -45.55911024077136), (60.355080637887795, -46.694416957500835), (61.13582116414227, -47.11561287522966), (61.864923466399205, -47.319892023923785), (62.61487500318049, -47.64897460291593), (63.509909312463606, -47.90830470444223), (64.13614300586664, -48.55908508607638), (64.98477788720197, -49.30164492128745), (65.45612597902164, -49.562002326267134), (66.20649723884685, -49.77753917970995), (66.94108476252904, -50.0002055570028), (67.58707125965884, -50.025851655699284), (68.62480123917157, -50.17148427246343), (69.34160076112926, -50.950153946056844), (70.01345243862647, -51.428012887508885), (70.92336239563542, -52.09260491763905), (71.17853817805303, -52.90205307907581), (72.34591113396868, -52.81182445429931), (72.78642222087205, -53.38550746767919), (73.5585281140684, -54.447827203617294), (74.18656293047388, -55.47494205918247), (74.91317442528134, -55.86267879072591), (75.4179935669365, -56.21208759714693), (76.33972100164397, -56.2775563739516), (76.7878215541914, -57.20307327303692), (77.26213490088662, -58.38271873978874), (77.8759535217132, -59.30494750359969), (78.89361551897468, -60.23782366538717), (79.69040486794029, -60.699618010498625), (80.31082992855681, -61.12767010734274), (81.33442712408032, -61.44714343720432), (82.02862569195577, -62.045855279281), (82.95745123802385, -63.97154497667066), (83.01115197666581, -63.17820865702697), (82.88344292210081, -63.200795947091024), (82.93016358320347, -63.7902931224138), (-259.5729012345705, 404.24187524853176), (-308.1263961972163, 496.15371817963967), (-286.9743016396974, 500.54201989857313), (-295.8436174766671, 501.78293861019245), (-287.11374420582615, 495.11265661674724), (-285.30479103140965, 495.17322782203905), (-285.133596842639, 495.03988420442397), (-283.237177979561, 494.4265033128472), (-282.5137843757386, 494.65340021910083)]
    np.save(os.path.join(output_dir, "base_shifts.npy"), np.array(base_shifts))
    shift_images(src_dir=os.path.join(src_dir, AOLP), output_dir=os.path.join(output_dir, "base_aolp"), shifts=base_shifts)
    
    fine_shifts = calculate_shifts(src_dir=os.path.join(output_dir, "base_aolp"), reference="3288.npy", shift_type="fine")
    # fine_shifts = [(1.3586557334094778, -0.09261378679650534), (1.2896656081939, -0.094719139269273), (1.2525841750386917, -0.08918175905455428), (1.2297267847243347, -0.08510800244948769), (1.1904813247208494, -0.08740062310255325), (1.1581003827245695, -0.07873600186519525), (1.0995263603779222, -0.07651370092128218), (1.056801889128792, -0.06355757428207198), (1.0256572332234555, -0.06850723788181767), (0.9802216661873899, -0.08556880329547312), (0.9346175101859444, -0.07105841228303689), (0.8921952596781466, -0.07194149179076703), (0.8720521287154952, -0.07233631555482134), (0.8249123713965218, -0.07294517230445763), (0.7673983652607603, -0.04973683733703638), (0.7366869980976389, -0.04625205826516776), (0.6772022698671663, -0.047982882658857307), (0.6346233841231879, -0.04597388170566319), (0.547632231610578, -0.05063216951384675), (0.5007456198416094, -0.053200833306959794), (0.4693493827510338, -0.05173709592565956), (0.399669972580341, -0.036028520929562546), (0.3682323963421368, -0.03835046445090029), (0.3216356067312063, -0.038539640680596676), (0.2651670415218632, -0.03959817887596273), (0.26058477055312324, -0.03759969933582852), (0.2048718948892656, -0.035749729207623204), (0.20069403535990205, -0.03240703919379939), (0.2095672548255152, -0.028600361496160076), (0.22343807426818785, -0.028095487164023325), (0.2515497485001106, -0.026953782680834593), (0.2516574751577991, -0.03501264761098355), (0.2453505193732326, -0.031161564215381077), (0.2333468303781956, -0.03377647394086125), (0.20093502285499198, -0.03227854006058806), (0.172387172616709, -0.03181611085324221), (0.15850573365264609, -0.033865910841200275), (0.14773071378135683, -0.03293566446166096), (0.14259385325999574, -0.031831341041311134), (0.12833393256528325, -0.032417980476338926), (0.11484757085759156, -0.031771971155649226), (0.10363958324978739, -0.029440976413525277), (0.08670006430429567, -0.0314473837688638), (0.08191796171968235, -0.032593159525504234), (0.04526387750729555, -0.029793446281701108), (0.04396375690203058, -0.02851386866836947), (0.0403642199096339, -0.027409320749711696), (0.04075393681182504, -0.0265497259492804), (0.04121515631413786, -0.026779721818343205), (0.04268102353330505, -0.02505591567035026), (0.0413050419499541, -0.026115412021226803), (0.04033624407543357, -0.02571672989779472), (0.04158417776557144, -0.024641299058430377), (0.0399907135858939, -0.027283818758519374), (0.040207354050608046, -0.025465834810461274), (0.03656581378731971, -0.025217609946025732), (0.03555113952052125, -0.02322232139283642), (0.03738543323606791, -0.02225557289318658), (0.03444352909787085, -0.02006730955565672), (0.03294200338655173, -0.022671056964554737), (0.030660320244805916, -0.019275063114946533), (0.028711924976732917, -0.017001896766714708), (0.029872796020981696, -0.01336618502091369), (0.026268609871294757, -0.014657707921060137), (0.0284524068410974, -0.01443943598178521), (0.025818744615889955, -0.01266884396363821), (0.026341137555846217, -0.01281025877221964), (0.022677213399447282, -0.010580859502056228), (0.022778911881459862, -0.011784744215219689), (0.021435085410757893, -0.010346598584646927), (0.020984858816291307, -0.011668460884379783), (0.020990927290768013, -0.011628315132270473), (0.019182178592927812, -0.014367385265131816), (0.015828760907197648, -0.009833519757194153), (0.015310971812596108, -0.0077470624335092), (0.014378424008327784, -0.009932153945328537), (0.010605384710743238, -0.008374196387649135), (0.010975590849284345, -0.008017926782486029), (0.011221882711879516, -0.006205781836342794), (0.007972210304160399, -0.005367968157997893), (0.004588040310864017, -0.0022678687198549596), (0.0006528589317440492, -0.0013706342328987375), (0.0019192963836758281, -0.001890417637241626), (-0.0007394187605314073, -0.0013169764213216695), (0.0, 0.0), (-0.003899579054404967, -0.00036055610939911276), (-0.0035215774753396545, 0.0022720109404872346), (-0.007556131427236323, 0.00350347663447792), (-0.00874241429482936, 0.005249894864164162), (-0.007398455872589693, 0.003319168924576843), (-0.011209924173044783, 0.00434250114869883), (-0.012905543617762305, 0.006085297114964305), (-0.014373009747941978, 0.006903616755494113), (-0.015280054318054681, 0.009367847121097839), (-0.02012183381975774, 0.00890788199274084), (-0.020895350881573904, 0.010825921908121927), (-0.023096557858025335, 0.012371533942200585), (-0.02502004256075452, 0.013363996397060873), (-0.025540957932207675, 0.012828199603859503), (-0.02754528684613433, 0.016276608315934027), (-0.027922845377361227, 0.015628430812625993), (-0.03191434981454222, 0.015861014827919462), (-0.0342883133516807, 0.01636745511711979), (-0.03384443790127989, 0.016558764312662788), (-0.0374088429891799, 0.018484848043385682), (-0.041182730408309, 0.018593195620383085), (-0.04085654886125667, 0.023121182267800577), (-0.04469617201857545, 0.022217988058059746), (-0.04829667176636576, 0.026296245521393757), (-0.04896845834082342, 0.02557805973935956), (-0.0473887344146533, 0.027466925559906485), (-0.05052231335048418, 0.027448173570633116), (-0.05224793437378139, 0.029766694744353117), (-0.05321276212839621, 0.030183406467926943), (-0.0542678142207933, 0.032209761918579716), (-0.05684725998048634, 0.03515034281974749), (-0.058671242537911894, 0.038576256500050476), (-0.05854246307671929, 0.03888205697342073), (-0.06050467197405851, 0.03800883349072137), (-0.0630852356662217, 0.039230387738371064), (-0.06376486359818045, 0.03919411835624942), (-0.06831613145823212, 0.04115700559157176), (-0.06611870308756806, 0.04381009921860368), (-0.06996467660269445, 0.04335926043393101), (-0.06950339563786656, 0.04575534159073413), (-0.0723505712549013, 0.04785570347291923), (-0.07275315036918073, 0.04842731091468977), (-0.07543883330072276, 0.049103022449912714), (-0.07646583736482171, 0.052221277135572564), (-0.07853590356103268, 0.053738239604740556), (-0.0803826145347557, 0.05343817889843194), (-0.08189540918101557, 0.05251341174709978), (-0.08098123406830382, 0.05402310211013628), (-0.08465333953881782, 0.057962938492551075), (-0.08358877251680497, 0.05933858234982381), (-0.08425459419731851, 0.058795828140773665), (-0.08572693463884207, 0.06055642146179707), (-0.08581077770236334, 0.06147430837859247), (-0.08684745663049398, 0.062190918005853746), (-0.08829352267161994, 0.06401551893645774), (-0.08923195028205555, 0.06558229558413586), (-0.09051789770364849, 0.06656447813838895), (-0.09020937694594977, 0.06832443733264881), (-0.09003813714480202, 0.0702810580789901), (-0.0919613929688694, 0.07023407055146436), (-0.09267854141398857, 0.07295469157304524), (-0.09155886050598383, 0.07687218409012075), (-0.09418308856879776, 0.07675830008213325), (-0.093746221244146, 0.07928953755424573), (-0.09458263098167663, 0.08101716294834205), (-0.0957613485713864, 0.08048924835838989), (-0.09624528023005041, 0.08175195204103147), (-0.09595511403881574, 0.08470861595014867), (-0.09691975159148569, 0.08950268811872775), (-0.09836693799093155, 0.0894978814536671), (-0.09641115221393193, 0.0905822112046053), (-0.09721700503905595, 0.09110955645326158), (-0.09957537739023792, 0.09271423811526347), (-0.09957396778554539, 0.09713403664920861), (-0.10017892931250572, 0.09913175978942945), (-0.10182094628612504, 0.09995130689196685), (-0.10188270996081883, 0.1027497768051262), (-0.10177167930032738, 0.10128582236745842), (-0.10264797775766965, 0.10468110433077982), (-0.10132889587976024, 0.10696847563929168), (-0.10054441404236059, 0.10768892072985636), (-0.10219044680752631, 0.10734677976631701), (-0.10155960972497269, 0.10827882143428269), (-0.10374366174778515, 0.10998199076709625), (-0.10280920008267458, 0.11163331170212132), (-0.10421648044302856, 0.11427777999404043), (-0.10401947336686135, 0.1144223549514436), (-0.10373513654371891, 0.11463757371518568), (-0.10422964917484023, 0.11500219960510094), (-0.10447411709105836, 0.1148021039429068), (-0.10480874982226851, 0.11482314933425641), (-0.10387202863557832, 0.11628613480672811), (-0.10654346364367484, 0.11624712970080964), (-0.10643900252716776, 0.11805915073057349), (-0.10655147635588946, 0.11931685847059725), (-0.10686212020573294, 0.11924539030860615), (-0.1050866475118255, 0.11921234723138241), (-0.10686284871985663, 0.12232727616617467), (-0.10805411133355847, 0.12580302010189826), (-0.10934051562230707, 0.126250705563848), (-0.10767058083729353, 0.12699172914074097), (-0.10964012691010794, 0.12745029056770818), (-0.11227987823531294, 0.12960882992240386), (-0.11157448433641548, 0.13034687028732606), (-0.11408305486907011, 0.13211594572851482), (-0.11714051721355645, 0.13456130874067185), (-0.11707233763786462, 0.1320198503165102), (-0.11685992729962891, 0.13666360081560924), (-0.11079418779331718, 0.1388563920463639), (-0.1084593554201092, 0.14314930520799862), (-0.10415138089547327, 0.15348418194525948), (-0.09758027455063711, 0.15404243653256344), (-0.14025920880999365, 0.12268073863003792), (-0.10079191860154424, 0.1540920142814457), (-0.1946443779127094, 0.1707675344554218), (-0.072870557722581, 0.1695675096685818), (-0.19369433109454803, 0.0737547194793251), (-0.2480825321508746, 0.04193568686866911), (-0.3866664762037999, -0.12033528303675212), (-0.40465044795860194, -0.09061939973446442), (-0.4714815636259573, -0.1948422004046506), (-0.5331122139784839, -0.14937438471167752), (-0.6328376379144629, -0.3074111379501119)]
    np.save(os.path.join(output_dir, "fine_shifts.npy"), np.array(fine_shifts))
    
    shifts = []
    for basic_shift, fine_shift in zip(base_shifts, fine_shifts):
        shifts.append((basic_shift[0] + fine_shift[0], basic_shift[1] + fine_shift[1]))
    np.save(os.path.join(output_dir, "shifts.npy"), np.array(shifts))

    shift_images(src_dir=os.path.join(src_dir, AOLP), output_dir=os.path.join(output_dir, AOLP), shifts=shifts)
    shift_images(src_dir=os.path.join(src_dir, DOLP), output_dir=os.path.join(output_dir, DOLP), shifts=shifts)
    shift_images(src_dir=os.path.join(src_dir, INTENSITY), output_dir=os.path.join(output_dir, INTENSITY), shifts=shifts)


def get_differences(src_dir: str = SHIFTED, output_dir: str = DIFFERENCE):
    start_time = perf_counter()
    print(f"Creating .npy Difference Files in '{output_dir}' from '{src_dir}'...")
    os.makedirs(output_dir, exist_ok=True)
    npy_names, prev_npy = natsorted([filename for filename in os.listdir(src_dir) if filename.endswith(".npy")]), None
    for i, filename in enumerate(npy_names):
        input_filepath = os.path.join(src_dir, filename)
        if i > 0:
            curr_npy = np.load(input_filepath)
            npys_difference = curr_npy - prev_npy
            output_filename = f"{npy_names[i-1].removesuffix('.npy')}to{filename}"
            output_filepath = os.path.join(output_dir, output_filename)
            np.save(output_filepath, npys_difference)
            prev_npy = curr_npy
            if VERBOSE: print(f"Successfully Derived Differences '{output_filename}'")
        else: prev_npy = np.load(input_filepath)
    print(f"Successfully Derived All the Difference NPYs in {(perf_counter() - start_time):.2f} Seconds\n")

    
def get_color_keys(output_dir: str = KEY) -> None:
    def aolp(output_path: str) -> None:
        start_time = perf_counter()
        radians = np.linspace(0, 3.1, 32)
        degrees = np.round(np.degrees(radians)).astype(int)
        colors = (polanalyser.applyColorToAoLP(radians) / 255.0)[..., ::-1]
        _, axes = plt.subplots(figsize=(15, 4))
        axes.bar(radians, [1] * len(radians), color=colors, width=0.1, edgecolor="none", align="center")
        axes.set_title("Angle of Linear Polarization Color Key", fontsize=16)
        axes.set_xlabel("Radians/Degrees", fontsize=12)
        axes.set_xticks(radians)
        axes.set_yticks([])
        axes.set_xticklabels([f"{rad:.1f}\n{deg}°" for rad, deg in zip(radians, degrees)], fontsize=10)
        axes.set_xlim([radians[0] - 0.05, radians[-1] + 0.05])
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.1)
        plt.clf()
        print(f"Successfully Created '{output_path}' in {(perf_counter() - start_time):.2f} Seconds\n")


    def aolp_difference(output_path: str) -> None:
        start_time = perf_counter()
        diffs_array = np.linspace(-PI, PI, 2000)
        wrapped_array = np.where(diffs_array > PI / 2, PI - diffs_array, np.where(diffs_array < -PI / 2, -PI - diffs_array, diffs_array))
        cmap = LinearSegmentedColormap.from_list("custom_gradient", ["cyan", "black", "magenta"], N=2000)
        gradient = np.repeat(np.linspace(-PI/2, PI/2, 100).reshape(-1, 1), 2000, axis=1)
        _, axes = plt.subplots(figsize=(15, 4))
        axes.imshow(gradient, aspect="auto", cmap=cmap, extent=[-PI, PI, -PI/2, PI/2], origin="lower")
        axes.plot(diffs_array, wrapped_array, label="Wrapped Difference", color="yellow", lw=1)
        axes.set_title("Angle of Linear Polarization - Difference Wrapping Key", fontsize=12)
        axes.set_xlabel("True AoLP Difference (Radians)", fontsize=7)
        axes.set_ylabel("Wrapped AoLP Difference (Radians)", fontsize=7)
        axes.set_xticks([-PI, -3*PI/4, -PI/2, -PI/4, 0, PI/4, PI/2, 3*PI/4, PI])
        axes.set_xticklabels(["-π", "-3π/4", "-π/2", "-π/4", "0", "π/4", "π/2", "3π/4", "π"], fontsize=5)
        axes.set_yticks([-PI/2, -PI/4, 0, PI/4, PI/2])
        axes.set_yticklabels(["-π/2", "-π/4", "0", "π/4", "π/2"], fontsize=5)
        axes.set_xlim(-PI, PI)
        axes.set_ylim(-PI / 2, PI / 2)
        axes.set_aspect("equal", adjustable="box")
        axes.grid(True)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.12)
        plt.clf()
        print(f"Successfully Created '{output_path}' in {(perf_counter() - start_time):.2f} Seconds\n")


    def difference(output_path: str) -> None:
        start_time = perf_counter()
        cmap = LinearSegmentedColormap.from_list("custom_gradient", ["cyan", "black", "magenta"], N=2000)
        gradient = np.linspace(-1, 1, 256).reshape(1, -1)
        gradient = np.vstack((gradient, gradient))
        _, axes = plt.subplots(figsize=(6, 2))
        axes.imshow(gradient, aspect="auto", cmap=cmap, extent=[-1, 1, 0, 1])
        axes.set_title("Difference Color Key", fontsize=14)
        axes.set_xticks([-1, 0, 1])
        axes.set_xticklabels(["Min (-)", "0", "Max (+)"])
        axes.set_yticks([])
        plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.1)
        plt.clf()
        print(f"Successfully Created '{output_path}' in {(perf_counter() - start_time):.2f} Seconds\n")


    def dolp_and_intensity(output_path: str) -> None:
        start_time = perf_counter()
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        _, axes = plt.subplots(figsize=(8, 2))
        axes.imshow(gradient, aspect="auto", cmap="gray", origin="lower")
        axes.set_title("Degree of Linear Polarization & Intensity Color Key")
        axes.set_yticks([])
        axes.set_xticks(np.linspace(0, 255, 11)) 
        axes.set_xticklabels([f"{x:.1f}" for x in np.linspace(0, 1, 11)])
        plt.savefig(output_path, dpi=300, bbox_inches="tight", pad_inches=0.1)
        plt.clf()
        print(f"Successfully Created '{output_path}' in {(perf_counter() - start_time):.2f} Seconds\n")


    os.makedirs(output_dir, exist_ok=True)
    aolp(output_path=os.path.join(output_dir, "AoLP.png"))
    aolp_difference(output_path=os.path.join(output_dir, "AoLP_Difference.png"))
    difference(output_path=os.path.join(output_dir, "Difference.png"))
    dolp_and_intensity(output_path=os.path.join(output_dir, "DoLP_And_Intensity.png"))


if __name__ == "__main__": 
    main() 
