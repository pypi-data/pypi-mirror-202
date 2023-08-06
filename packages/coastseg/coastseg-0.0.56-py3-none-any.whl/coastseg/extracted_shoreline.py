# Standard library imports
import logging
from glob import glob1
import os
import json
from glob import glob
from typing import Optional, Union

# Internal dependencies imports
from coastseg import exceptions
from coastseg import common

# External dependencies imports
import geopandas as gpd
import numpy as np
from ipyleaflet import GeoJSON
from matplotlib.pyplot import get_cmap
from matplotlib.colors import rgb2hex
from tqdm.auto import tqdm
import pickle
import matplotlib.pyplot as plt

from coastsat import SDS_shoreline
from coastsat import SDS_preprocess
from coastsat.SDS_download import get_metadata
from coastsat.SDS_shoreline import extract_shorelines
from coastsat.SDS_tools import (
    remove_duplicates,
    remove_inaccurate_georef,
    output_to_gdf,
    get_filepath,
    get_filenames,
    merge_output,
)

logger = logging.getLogger(__name__)

__all__ = ["Extracted_Shoreline"]


def get_npz_tile(filename: str, session_path: str, satname: str) -> str:
    """
    Find the npz file that matches the given filename and satellite name in the specified session directory.

    Args:
        filename (str): The filename of the input file, which may contain the satellite name.
        session_path (str): The path of the session directory where the npz files are located.
        satname (str): The name of the satellite, which is used to match the npz file.

    Returns:
        str: The path of the matching npz file, or None if no match is found.

    Raises:
        None

    Example:
        If filename='path/to/somefile_satname_something.tif', session_path='path/to/session', and satname='satname',
        get_npz_tile(filename, session_path, satname) returns 'path/to/session/somefile_satname.npz'.

    """
    new_filename = filename.split(satname)[0] + satname
    for npz in glob1(session_path, "*.npz"):
        new_npz = npz.replace("_RGB", "")
        if new_filename in new_npz:
            return os.path.join(session_path, npz)
    return None


def load_image_labels(npz_file: str, class_indices: list = [2, 1, 0]) -> np.ndarray:
    """
    Load and process image labels from a .npz file.

    Parameters:
    npz_file (str): The path to the .npz file containing the image labels.
    class_indices (list): A list of indices corresponding to the classes to extract from the labels. Default is [2, 1, 0]
                          for sand , whitewater, and water classes.
                          2 - sand index
                          1 - whitewater index
                          0 - water index

    Returns:
    np.ndarray: A 3D numpy array of binary masks, where each mask corresponds to one of the specified classes.
    Must be in the order [sand,whitewater,water]
    """
    if not os.path.isfile(npz_file) or not npz_file.endswith(".npz"):
        raise ValueError(f"{npz_file} is not a valid .npz file.")

    data = np.load(npz_file)
    im_labels = np.zeros(
        shape=(
            data["grey_label"].shape[0],
            data["grey_label"].shape[1],
            len(class_indices),
        ),
        dtype=bool,
    )

    for i, idx in enumerate(class_indices):
        im_labels[..., i] = data["grey_label"] == idx

    return im_labels


def extract_shorelines_for_session(
    session_path: str, metadata: dict, settings: dict
) -> dict:
    """
    Main function to extract shorelines from satellite images
    original version: KV WRL 2018
    Arguments:
    -----------
    metadata: dict
        contains all the information about the satellite images that were downloaded
    settings: dict with the following keys
        'inputs': dict
            input parameters (sitename, filepath, polygon, dates, sat_list)
        'cloud_thresh': float
            value between 0 and 1 indicating the maximum cloud fraction in
            the cropped image that is accepted
        'cloud_mask_issue': boolean
            True if there is an issue with the cloud mask and sand pixels
            are erroneously being masked on the image
        'min_beach_area': int
            minimum allowable object area (in metres^2) for the class 'sand',
            the area is converted to number of connected pixels
        'min_length_sl': int
            minimum length (in metres) of shoreline contour to be valid
        'sand_color': str
            default', 'dark' (for grey/black sand beaches) or 'bright' (for white sand beaches)
        'output_epsg': int
            output spatial reference system as EPSG code
        'check_detection': bool
            if True, lets user manually accept/reject the mapped shorelines
        'save_figure': bool
            if True, saves a -jpg file for each mapped shoreline
        'adjust_detection': bool
            if True, allows user to manually adjust the detected shoreline
        'pan_off': bool
            if True, no pan-sharpening is performed on Landsat 7,8 and 9 imagery

    Returns:
    -----------
    output: dict
        contains the extracted shorelines and corresponding dates + metadata

    """
    sitename = settings["inputs"]["sitename"]
    filepath_data = settings["inputs"]["filepath"]
    collection = settings["inputs"]["landsat_collection"]
    default_min_length_sl = settings["min_length_sl"]

    # initialise output structure
    output = dict([])
    # create a subfolder to store the .jpg images showing the detection
    filepath_jpg = os.path.join(filepath_data, sitename, "jpg_files", "detection")
    if not os.path.exists(filepath_jpg):
        os.makedirs(filepath_jpg)

    # loop through satellite list
    for satname in metadata.keys():
        # get images
        filepath = get_filepath(settings["inputs"], satname)
        filenames = metadata[satname]["filenames"]

        # initialise the output variables
        output_timestamp = []  # datetime at which the image was acquired (UTC time)
        output_shoreline = []  # vector of shoreline points
        output_filename = (
            []
        )  # filename of the images from which the shorelines where derived
        output_cloudcover = []  # cloud cover of the images
        output_geoaccuracy = []  # georeferencing accuracy of the images
        output_idxkeep = (
            []
        )  # index that were kept during the analysis (cloudy images are skipped)
        output_t_mndwi = []  # MNDWI threshold used to map the shoreline

        if satname in ["L5", "L7", "L8", "L9"]:
            pixel_size = 15
        elif satname == "S2":
            pixel_size = 10

        # reduce min shoreline length for L7 because of the diagonal bands
        if satname == "L7":
            settings["min_length_sl"] = 200
        else:
            settings["min_length_sl"] = default_min_length_sl

        # loop through the images
        for i in tqdm(
            range(len(filenames)), desc="Mapping Shorelines", leave=True, position=0
        ):

            # print('\r%s:   %d%%' % (satname,int(((i+1)/len(filenames))*100)), end='')

            # get image filename
            fn = get_filenames(filenames[i], filepath, satname)
            # preprocess image (cloud mask + pansharpening/downsampling)
            (
                im_ms,
                georef,
                cloud_mask,
                im_extra,
                im_QA,
                im_nodata,
            ) = SDS_preprocess.preprocess_single(
                fn,
                satname,
                settings["cloud_mask_issue"],
                settings["pan_off"],
                collection,
            )
            # get image spatial reference system (epsg code) from metadata dict
            image_epsg = metadata[satname]["epsg"][i]

            # compute cloud_cover percentage (with no data pixels)
            cloud_cover_combined = np.divide(
                sum(sum(cloud_mask.astype(int))),
                (cloud_mask.shape[0] * cloud_mask.shape[1]),
            )
            if cloud_cover_combined > 0.99:  # if 99% of cloudy pixels in image skip
                continue
            # remove no data pixels from the cloud mask
            # (for example L7 bands of no data should not be accounted for)
            cloud_mask_adv = np.logical_xor(cloud_mask, im_nodata)
            # compute updated cloud cover percentage (without no data pixels)
            cloud_cover = np.divide(
                sum(sum(cloud_mask_adv.astype(int))),
                (sum(sum((~im_nodata).astype(int)))),
            )
            # skip image if cloud cover is above user-defined threshold
            if cloud_cover > settings["cloud_thresh"]:
                continue

            # calculate a buffer around the reference shoreline (if any has been digitised)
            im_ref_buffer = SDS_shoreline.create_shoreline_buffer(
                cloud_mask.shape, georef, image_epsg, pixel_size, settings
            )

            npz_file = get_npz_tile(filenames[i], session_path, satname)
            logger.info(f"npz_file: {npz_file}")
            # indexes of [0,1,2] in the npz file represent water, whitewater, and sand classes.
            # @todo derive the order of the classes from the modelcard
            # class_indices=[sand, whitewater, water] indexes in segmentation
            im_labels = load_image_labels(npz_file, class_indices=[2, 1, 0])

            # otherwise map the contours automatically with one of the two following functions:
            # if there are pixels in the 'sand' class --> use find_wl_contours2 (enhanced)
            # otherwise use find_wl_contours1 (traditional)
            try:  # use try/except structure for long runs
                if (
                    sum(im_labels[im_ref_buffer, 0]) < 50
                ):  # minimum number of sand pixels
                    print(
                        f"{fn} Not enough sand pixels within the beach buffer to detect shoreline"
                    )
                    continue
                else:
                    # use classification to refine threshold and extract the sand/water interface
                    contours_mwi, t_mndwi = SDS_shoreline.find_wl_contours2(
                        im_ms, im_labels, cloud_mask, im_ref_buffer
                    )
            except Exception as e:
                print(e)
                print("\nCould not map shoreline for this image: " + filenames[i])
                continue

            # process the water contours into a shoreline
            shoreline = SDS_shoreline.process_shoreline(
                contours_mwi, cloud_mask_adv, im_nodata, georef, image_epsg, settings
            )

            # visualise the mapped shorelines, there are two options:
            # if settings['check_detection'] = True, shows the detection to the user for accept/reject
            # if settings['save_figure'] = True, saves a figure for each mapped shoreline
            if settings["check_detection"] or settings["save_figure"]:
                date = filenames[i][:19]
                if not settings["check_detection"]:
                    plt.ioff()  # turning interactive plotting off
                skip_image = SDS_shoreline.show_detection(
                    im_ms,
                    cloud_mask,
                    im_labels,
                    shoreline,
                    image_epsg,
                    georef,
                    settings,
                    date,
                    satname,
                )

            # append to output variables
            output_timestamp.append(metadata[satname]["dates"][i])
            output_shoreline.append(shoreline)
            output_filename.append(filenames[i])
            output_cloudcover.append(cloud_cover)
            output_geoaccuracy.append(metadata[satname]["acc_georef"][i])
            output_idxkeep.append(i)
            output_t_mndwi.append(t_mndwi)

        # create dictionnary of output
        output[satname] = {
            "dates": output_timestamp,
            "shorelines": output_shoreline,
            "filename": output_filename,
            "cloud_cover": output_cloudcover,
            "geoaccuracy": output_geoaccuracy,
            "idx": output_idxkeep,
            "MNDWI_threshold": output_t_mndwi,
        }

    # change the format to have one list sorted by date with all the shorelines (easier to use)
    output = merge_output(output)

    # @todo replace this with save json
    # save outputput structure as output.pkl
    filepath = os.path.join(filepath_data, sitename)

    with open(os.path.join(filepath, sitename + "_output.pkl"), "wb") as f:
        pickle.dump(output, f)

    return output


def load_extracted_shoreline_from_files(
    dir_path: str,
) -> Optional["Extracted_Shoreline"]:
    """
    Load the extracted shoreline from the given directory.

    The function searches the directory for the extracted shoreline GeoJSON file, the shoreline settings JSON file,
    and the extracted shoreline dictionary JSON file. If any of these files are missing, the function returns None.

    Args:
        dir_path: The path to the directory containing the extracted shoreline files.

    Returns:
        An instance of the Extracted_Shoreline class containing the extracted shoreline data, or None if any of the
        required files are missing.
    """
    required_files = {
        "geojson": "*shoreline*.geojson",
        "settings": "*shoreline*settings*.json",
        "dict": "*shoreline*dict*.json",
    }

    extracted_files = {}

    for file_type, file_pattern in required_files.items():
        file_paths = glob(os.path.join(dir_path, file_pattern))
        if not file_paths:
            logger.warning(f"No {file_type} file could be loaded from {dir_path}")
            return None

        file_path = file_paths[0]  # Use the first file if there are multiple matches
        if file_type == "geojson":
            extracted_files[file_type] = common.read_gpd_file(file_path)
        else:
            extracted_files[file_type] = common.from_file(file_path)

    extracted_shorelines = Extracted_Shoreline()
    extracted_shorelines = extracted_shorelines.load_extracted_shorelines(
        extracted_files["dict"], extracted_files["settings"], extracted_files["geojson"]
    )

    logger.info(f"Loaded extracted shorelines from: {dir_path}")
    return extracted_shorelines


class Extracted_Shoreline:
    """Extracted_Shoreline: contains the extracted shorelines within a Region of Interest (ROI)"""

    LAYER_NAME = "extracted_shoreline"
    FILE_NAME = "extracted_shorelines.geojson"

    def __init__(
        self,
    ):
        # gdf: geodataframe containing extracted shoreline for ROI_id
        self.gdf = gpd.GeoDataFrame()
        # Use roi id to identify which ROI extracted shorelines derive from
        self.roi_id = ""
        # dictionary : dictionary of extracted shorelines
        # contains keys 'dates', 'shorelines', 'filename', 'cloud_cover', 'geoaccuracy', 'idx', 'MNDWI_threshold', 'satname'
        self.dictionary = {}
        # shoreline_settings: dictionary of settings used to extract shoreline
        self.shoreline_settings = {}

    def __str__(self):
        return f"Extracted Shoreline: ROI ID: {self.roi_id}\n geodataframe {self.gdf.head(5)}\nshoreline_settings{self.shoreline_settings}"

    def __repr__(self):
        return f"Extracted Shoreline:  ROI ID: {self.roi_id}\n geodataframe {self.gdf.head(5)}\nshoreline_settings{self.shoreline_settings}\ndictionary{self.dictionary}"

    def get_roi_id(self) -> Optional[str]:
        """
        Extracts the region of interest (ROI) ID from the shoreline settings.

        The method retrieves the sitename field from the shoreline settings inputs dictionary and extracts the
        ROI ID from it, if present. The sitename field is expected to be in the format "ID_XXXX_datetime03-22-23__07_29_15",
        where XXXX is the id of the ROI. If the sitename field is not present or is not in the
        expected format, the method returns None.

        shoreline_settings:
        {
            'inputs' {
                "sitename": 'ID_0_datetime03-22-23__07_29_15',
                }
        }

        Returns:
            The ROI ID as a string, or None if the sitename field is not present or is not in the expected format.
        """
        inputs = self.shoreline_settings.get("inputs", {})
        sitename = inputs.get("sitename", "")
        # checks if the ROI ID is present in the 'sitename' saved in the shoreline settings
        roi_id = sitename.split("_")[1] if sitename else None
        return roi_id

    def load_extracted_shorelines(
        self,
        extracted_shoreline_dict: dict = None,
        shoreline_settings: dict = None,
        extracted_shorelines_gdf: gpd.GeoDataFrame = None,
    ):
        """Loads extracted shorelines into the Extracted_Shoreline class.
        Intializes the class with the extracted shorelines dictionary, shoreline settings, and the extracted shorelines geodataframe

        Args:
            extracted_shoreline_dict (dict, optional): A dictionary containing the extracted shorelines. Defaults to None.
            shoreline_settings (dict, optional): A dictionary containing the shoreline settings. Defaults to None.
            extracted_shorelines_gdf (GeoDataFrame, optional): The extracted shorelines in a GeoDataFrame. Defaults to None.

        Returns:
            object: The Extracted_Shoreline class with the extracted shorelines loaded.

        Raises:
            ValueError: If the input arguments are invalid.
        """

        if not isinstance(extracted_shoreline_dict, dict):
            raise ValueError(
                f"extracted_shoreline_dict must be dict. not {type(extracted_shoreline_dict)}"
            )
        if extracted_shoreline_dict == {}:
            raise ValueError("extracted_shoreline_dict cannot be empty.")

        if extracted_shorelines_gdf is not None:
            if not isinstance(extracted_shorelines_gdf, gpd.GeoDataFrame):
                raise ValueError(
                    f"extracted_shorelines_gdf must be valid geodataframe. not {type(extracted_shorelines_gdf)}"
                )
            if extracted_shorelines_gdf.empty:
                raise ValueError("extracted_shorelines_gdf cannot be empty.")
            self.gdf = extracted_shorelines_gdf

        if not isinstance(shoreline_settings, dict):
            raise ValueError(
                f"shoreline_settings must be dict. not {type(shoreline_settings)}"
            )
        if shoreline_settings == {}:
            raise ValueError("shoreline_settings cannot be empty.")

        # dictionary : dictionary of extracted shorelines
        self.dictionary = extracted_shoreline_dict
        # shoreline_settings: dictionary of settings used to extract shoreline
        self.shoreline_settings = shoreline_settings
        # Use roi id to identify which ROI extracted shorelines derive from
        self.roi_id = shoreline_settings["inputs"]["roi_id"]
        return self

    def create_extracted_shorlines(
        self,
        roi_id: str = None,
        shoreline: gpd.GeoDataFrame = None,
        roi_settings: dict = None,
        settings: dict = None,
    ) -> "Extracted_Shoreline":
        """
        Extracts shorelines for a specified region of interest (ROI) and returns an Extracted_Shoreline class instance.

        Args:
        - self: The object instance.
        - roi_id (str): The ID of the region of interest for which shorelines need to be extracted.
        - shoreline (GeoDataFrame): A GeoDataFrame of shoreline features.
        - roi_settings (dict): A dictionary of region of interest settings.
        - settings (dict): A dictionary of extraction settings.

        Returns:
        - object: The Extracted_Shoreline class instance.
        """
        # validate input parameters are not empty and are of the correct type
        self._validate_input_params(roi_id, shoreline, roi_settings, settings)

        logger.info(f"Extracting shorelines for ROI id{roi_id}")
        self.dictionary = self.extract_shorelines(
            shoreline,
            roi_settings,
            settings,
        )

        if is_list_empty(self.dictionary["shorelines"]):
            logger.warning(f"No extracted shorelines for ROI {roi_id}")
            raise exceptions.No_Extracted_Shoreline(roi_id)

        map_crs = "EPSG:4326"
        # extracted shorelines have map crs so they can be displayed on the map
        self.gdf = self.create_geodataframe(
            self.shoreline_settings["output_epsg"], output_crs=map_crs
        )
        return self

    def create_extracted_shorlines_from_session(
        self,
        roi_id: str = None,
        shoreline: gpd.GeoDataFrame = None,
        roi_settings: dict = None,
        settings: dict = None,
        session_path: str = None,
    ) -> "Extracted_Shoreline":
        """
        Extracts shorelines for a specified region of interest (ROI) from a saved session and returns an Extracted_Shoreline class instance.

        Args:
        - self: The object instance.
        - roi_id (str): The ID of the region of interest for which shorelines need to be extracted.
        - shoreline (GeoDataFrame): A GeoDataFrame of shoreline features.
        - roi_settings (dict): A dictionary of region of interest settings.
        - settings (dict): A dictionary of extraction settings.
        - session_path (str): The path of the saved session from which the shoreline extraction needs to be resumed.

        Returns:
        - object: The Extracted_Shoreline class instance.
        """
        # validate input parameters are not empty and are of the correct type
        self._validate_input_params(roi_id, shoreline, roi_settings, settings)

        logger.info(f"Extracting shorelines for ROI id{roi_id}")
        self.dictionary = self.extract_shorelines(
            shoreline, roi_settings, settings, session_path=session_path
        )

        if is_list_empty(self.dictionary["shorelines"]):
            logger.warning(f"No extracted shorelines for ROI {roi_id}")
            raise exceptions.No_Extracted_Shoreline(roi_id)

        map_crs = "EPSG:4326"
        # extracted shorelines have map crs so they can be displayed on the map
        self.gdf = self.create_geodataframe(
            self.shoreline_settings["output_epsg"], output_crs=map_crs
        )
        return self

    def _validate_input_params(
        self,
        roi_id: str,
        shoreline: gpd.GeoDataFrame,
        roi_settings: dict,
        settings: dict,
    ) -> None:
        """
        Validates that the input parameters for shoreline extraction are not empty and are of the correct type.

        Args:
        - self: The object instance.
        - roi_id (str): The ID of the region of interest for which shorelines need to be extracted.
        - shoreline (GeoDataFrame): A GeoDataFrame of shoreline features.
        - roi_settings (dict): A dictionary of region of interest settings.
        - settings (dict): A dictionary of extraction settings.

        Raises:
        - ValueError: If any of the input parameters are empty or not of the correct type.
        """
        if not isinstance(roi_id, str):
            raise ValueError(f"ROI id must be string. not {type(roi_id)}")

        if not isinstance(shoreline, gpd.GeoDataFrame):
            raise ValueError(
                f"shoreline must be valid geodataframe. not {type(shoreline)}"
            )
        if shoreline.empty:
            raise ValueError("shoreline cannot be empty.")

        if not isinstance(roi_settings, dict):
            raise ValueError(f"roi_settings must be dict. not {type(roi_settings)}")
        if roi_settings == {}:
            raise ValueError("roi_settings cannot be empty.")

        if not isinstance(settings, dict):
            raise ValueError(f"settings must be dict. not {type(settings)}")
        if settings == {}:
            raise ValueError("settings cannot be empty.")

    def extract_shorelines(
        self,
        shoreline_gdf: gpd.geodataframe,
        roi_settings: dict,
        settings: dict,
        session_path: str = None,
    ) -> dict:
        """Returns a dictionary containing the extracted shorelines for roi specified by rois_gdf"""
        # project shorelines's crs from map's crs to output crs given in settings
        map_crs = 4326
        reference_shoreline = get_reference_shoreline(
            shoreline_gdf, settings["output_epsg"]
        )
        # Add reference shoreline to shoreline_settings
        self.shoreline_settings = self.create_shoreline_settings(
            settings, roi_settings, reference_shoreline
        )
        # gets metadata used to extract shorelines
        metadata = get_metadata(self.shoreline_settings["inputs"])
        logger.info(f"metadata: {metadata}")
        # extract shorelines from ROI
        if session_path is None:
            # extract shorelines with coastsat's models
            extracted_shorelines = extract_shorelines(metadata, self.shoreline_settings)
        elif session_path is not None:
             # extract shorelines with our models
            extracted_shorelines = extract_shorelines_for_session(
                session_path, metadata, self.shoreline_settings
            )
        logger.info(f"extracted_shoreline_dict: {extracted_shorelines}")
        # postprocessing by removing duplicates and removing in inaccurate georeferencing (set threshold to 10 m)
        extracted_shorelines = remove_duplicates(
            extracted_shorelines
        )  # removes duplicates (images taken on the same date by the same satellite)
        extracted_shorelines = remove_inaccurate_georef(
            extracted_shorelines, 10
        )  # remove inaccurate georeferencing (set threshold to 10 m)
        logger.info(
            f"after remove_inaccurate_georef : extracted_shoreline_dict: {extracted_shorelines}"
        )
        return extracted_shorelines

    def create_shoreline_settings(
        self,
        settings: dict,
        roi_settings: dict,
        reference_shoreline: dict,
    ) -> None:
        """sets self.shoreline_settings to dictionary containing settings, reference_shoreline
        and roi_settings

        shoreline_settings=
        {
            "reference_shoreline":reference_shoreline,
            "inputs": roi_settings,
            "adjust_detection": False,
            "check_detection": False,
            ...
            rest of items from settings
        }

        Args:
            settings (dict): map settings
            roi_settings (dict): settings of the roi. Must include 'dates'
            reference_shoreline (dict): reference shoreline
        """
        # deepcopy settings to shoreline_settings so it can be modified
        # shoreline_settings = copy.deepcopy(settings)
        shoreline_keys = [
            "cloud_thresh",
            "cloud_mask_issue",
            "min_beach_area",
            "min_length_sl",
            "output_epsg",
            "sand_color",
            "pan_off",
            "max_dist_ref",
            "dist_clouds",
        ]
        logger.info(f"settings used to create shoreline settings: {settings}")
        shoreline_settings = common.filter_dict_by_keys(settings, keys=shoreline_keys)
        logger.info(f"Loading shoreline_settings: {shoreline_settings}")
        # Add reference shoreline and shoreline buffer distance for this specific ROI
        shoreline_settings["reference_shoreline"] = reference_shoreline
        # disable adjusting shorelines manually in shoreline_settings
        shoreline_settings["adjust_detection"] = False
        # disable adjusting shorelines manually in shoreline_settings
        shoreline_settings["check_detection"] = False
        shoreline_settings["save_figure"] = True
        # copy roi_setting for this specific roi
        shoreline_settings["inputs"] = roi_settings
        logger.info(f"shoreline_settings: {shoreline_settings}")
        return shoreline_settings

    def create_geodataframe(
        self, input_crs: str, output_crs: str = None
    ) -> gpd.GeoDataFrame:
        """Creates a geodataframe with the crs specified by input_crs. Converts geodataframe crs
        to output_crs if provided.
        Args:
            input_crs (str ): coordinate reference system string. Format 'EPSG:4326'.
            output_crs (str, optional): coordinate reference system string. Defaults to None.
        Returns:
            gpd.GeoDataFrame: geodataframe with columns = ['geometery','date','satname','geoaccuracy','cloud_cover']
            converted to output_crs if provided otherwise geodataframe's crs will be
            input_crs
        """
        extract_shoreline_gdf = output_to_gdf(self.dictionary, "lines")
        extract_shoreline_gdf.crs = input_crs
        if output_crs is not None:
            extract_shoreline_gdf = extract_shoreline_gdf.to_crs(output_crs)
        return extract_shoreline_gdf

    def save_to_file(
        self,
        sitename: str,
        filepath: str,
    ):
        """save_to_file Save geodataframe to location specified by filepath into directory
        specified by sitename

        Args:
            sitename (str): directory of roi shoreline was extracted from
            filepath (str): full path to directory containing ROIs
        """
        savepath = os.path.join(filepath, sitename, Extracted_Shoreline.FILE_NAME)
        logger.info(
            f"Saving shoreline to file: {savepath}.\n Extracted Shoreline: {self.gdf}"
        )
        print(f"Saving shoreline to file: {savepath}")
        self.gdf.to_file(
            savepath,
            driver="GeoJSON",
            encoding="utf-8",
        )

    def to_file(
        self, filepath: str, filename: str, data: Union[gpd.GeoDataFrame, dict]
    ):
        """Save geopandas dataframe to file, or save data to file with to_file().

        Args:
            filepath (str): The directory where the file should be saved.
            filename (str): The name of the file to be saved.
            data (Any): The data to be saved to file.

        Raises:
            ValueError: Raised when data is not a geopandas dataframe and cannot be saved with tofile()
        """
        file_location = os.path.abspath(os.path.join(filepath, filename))

        if isinstance(data, gpd.GeoDataFrame):
            data.to_file(
                file_location,
                driver="GeoJSON",
                encoding="utf-8",
            )
        elif isinstance(data, dict):
            if data != {}:
                common.to_file(data, file_location)

    def style_layer(self, geojson: dict, layer_name: str, color: str) -> GeoJSON:
        """Return styled GeoJson object with layer name

        Args:
            geojson (dict): geojson dictionary to be styled
            layer_name(str): name of the GeoJSON layer
            color(str): hex code or name of color render shorelines

        Returns:
            "ipyleaflet.GeoJSON": shoreline as GeoJSON layer styled with color
        """
        assert geojson != {}, "ERROR.\n Empty geojson cannot be drawn onto  map"
        return GeoJSON(
            data=geojson,
            name=layer_name,
            style={
                "color": color,
                "opacity": 1,
                "weight": 3,
            },
        )

    def get_layer_name(self) -> list:
        """returns name of extracted shoreline layer"""
        layer_name = "extracted_shoreline"
        return layer_name

    def get_styled_layer(self, row_number: int = 0) -> GeoJSON:
        """
        Returns a single shoreline feature as a GeoJSON object with a specified style.

        Args:
        - row_number (int): The index of the shoreline feature to select from the GeoDataFrame.

        Returns:
        - GeoJSON: A single shoreline feature as a GeoJSON object with a specified style.
        """
        # load extracted shorelines onto map
        map_crs = 4326
        layers = []
        if self.gdf.empty:
            return layers
        # convert to map crs and turn in json dict
        projected_gdf = self.gdf.to_crs(map_crs)
        # select a single shoreline and convert it to json
        single_shoreline = projected_gdf.iloc[[row_number]]
        single_shoreline = common.stringify_datetime_columns(single_shoreline)
        logger.info(f"single_shoreline.columns: {single_shoreline.columns}")
        logger.info(f"single_shoreline: {single_shoreline}")
        # convert geodataframe to json
        features_json = json.loads(single_shoreline.to_json())
        logger.info(f"single_shoreline features_json: {features_json}")
        layer_name = self.get_layer_name()
        logger.info(f"layer_name: {layer_name}")
        logger.info(f"features_json['features']: {features_json['features']}")
        # create a single layer
        feature = features_json["features"][0]
        new_layer = self.style_layer(feature, layer_name, "red")
        logger.info(f"new_layer: {new_layer}")
        return new_layer


def get_reference_shoreline(
    shoreline_gdf: gpd.geodataframe, output_crs: str
) -> np.ndarray:
    """
    Converts a GeoDataFrame of shoreline features into a numpy array of latitudes, longitudes, and zeroes representing the mean sea level.

    Args:
    - shoreline_gdf (GeoDataFrame): A GeoDataFrame of shoreline features.
    - output_crs (str): The output CRS to which the shoreline features need to be projected.

    Returns:
    - np.ndarray: A numpy array of latitudes, longitudes, and zeroes representing the mean sea level.
    """
    # project shorelines's espg from map's espg to output espg given in settings
    reprojected_shorlines = shoreline_gdf.to_crs(output_crs)
    logger.info(f"reprojected_shorlines.crs: {reprojected_shorlines.crs}")
    logger.info(f"reprojected_shorlines: {reprojected_shorlines}")
    # convert shoreline_in_roi gdf to coastsat compatible format np.array([[lat,lon,0],[lat,lon,0]...])
    shorelines = make_coastsat_compatible(reprojected_shorlines)
    # shorelines = [([lat,lon],[lat,lon],[lat,lon]),([lat,lon],[lat,lon],[lat,lon])...]
    # Stack all the tuples into a single list of n rows X 2 columns
    shorelines = np.vstack(shorelines)
    # Add third column of 0s to represent mean sea level
    shorelines = np.insert(shorelines, 2, np.zeros(len(shorelines)), axis=1)
    return shorelines


def get_colors(length: int) -> list:
    # returns a list of color hex codes as long as length
    cmap = get_cmap("plasma", length)
    cmap_list = [rgb2hex(i) for i in cmap.colors]
    return cmap_list


def make_coastsat_compatible(feature: gpd.geodataframe) -> list:
    """Return the feature as an np.array in the form:
        [([lat,lon],[lat,lon],[lat,lon]),([lat,lon],[lat,lon],[lat,lon])...])
    Args:
        feature (gpd.geodataframe): clipped portion of shoreline within a roi
    Returns:
        list: shorelines in form:
            [([lat,lon],[lat,lon],[lat,lon]),([lat,lon],[lat,lon],[lat,lon])...])
    """
    features = []
    # Use explode to break multilinestrings in linestrings
    feature_exploded = feature.explode()
    # For each linestring portion of feature convert to lat,lon tuples
    lat_lng = feature_exploded.apply(
        lambda row: tuple(np.array(row.geometry.coords).tolist()), axis=1
    )
    features = list(lat_lng)
    return features


def is_list_empty(main_list: list) -> bool:
    all_empty = True
    for np_array in main_list:
        if len(np_array) != 0:
            all_empty = False
    return all_empty
