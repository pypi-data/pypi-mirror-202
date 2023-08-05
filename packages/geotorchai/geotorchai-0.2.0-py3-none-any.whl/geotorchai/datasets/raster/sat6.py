
import os
from typing import Optional, Callable, Dict
import torch
from torch.utils.data import Dataset
from geotorchai.datasets.raster.utility import textural_features as ttf
from geotorchai.datasets.raster.utility import spectral_indices as si
from geotorchai.utility.exceptions import InvalidParametersException
import pandas as pd
import numpy as np


class SAT6(Dataset):
	'''
    This is a multi-class classification dtaaset. Link: https://www.kaggle.com/datasets/crawford/deepsat-sat6
    Image Height and Width: 28 x 28, No of bands: 4, No of classes: 6

    Parameters
    ..........
    root (String) - Path to the dataset if it is already downloaded. If not downloaded, it will be downloaded in the given path.
    download (Boolean, Optional) - Set to True if dataset is not available in the given directory. Default: False
    is_train_data (Boolean, Optional) - True denotes training data, while False indicates testing data. Default: True
    bands (List, Optional) - List of all bands that need to be included in the dataset. Default: list of all bands in the EuroSAT images.
    include_additional_features (Boolean, Optional) - Set to True if you want to include extra image features. Default: False
    additional_features_list (List, Optional) - List of extra features if previous parameter is set to True. Default: None
    user_features_callback (Dict[str, Callable], Optional) - User-defined functions for extracting some or all of the features included in the additional feature list.
                                                             A key in the dictionary is the feature name (exactly similar to what included in the feature list) and value
                                                             is the function that returns corresponding feature. The function takes an image as input and returns the
                                                             feature value. Default: None
    transform (Callable, Optional) - Tranforms to apply to each image. Default: None
    target_transform (Callable, Optional) - Tranforms to apply to each label. Default: None
    '''


	SPECTRAL_BANDS = ["red", "green", "blue", "nir"]
	RGB_BANDS = ["red", "green", "blue"]
	ADDITIONAL_FEATURES = ["contrast", "dissimilarity", "homogeneity", "energy", "correlation", "ASM", "mean_NDWI", "mean_NDVI", "mean_RVI"]
	TEXTURAL_FEATURES = ["contrast", "dissimilarity", "homogeneity", "energy", "correlation", "ASM"]
	SPECTRAL_INDICES = ["mean_NDWI", "mean_NDVI", "mean_RVI"]
	SAT6_CLASSES = ["building", "barren_land", "trees", "grassland", "road", "water"]
	
	IMAGE_HEIGHT = 28
	IMAGE_WIDTH = 28
	BAND_GREEN_INDEX = 1
	BAND_RED_INDEX = 0
	BAND_NIR_INDEX = 3


	def __init__(self, root, is_train_data = True, bands = SPECTRAL_BANDS, include_additional_features = False, additional_features_list = ADDITIONAL_FEATURES, user_features_callback: Optional[Dict[str, Callable]] = None, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None):
		super().__init__()
		# first check if selected bands are valid. Trow exception otherwise
		if not self._is_valid_bands(bands):
			raise InvalidParametersException("Invalid band names")

		self._feature_callbacks = [ttf._get_GLCM_Contrast, ttf._get_GLCM_Dissimilarity, ttf._get_GLCM_Homogeneity, ttf._get_GLCM_Energy, ttf._get_GLCM_Correlation, ttf._get_GLCM_ASM]

		self.selected_band_indices = torch.tensor([self.SPECTRAL_BANDS.index(band) for band in bands])
		self.user_features_callback = user_features_callback
		self.transform = transform
		self.target_transform = target_transform

		self._idx_to_class = {i:j for i, j in enumerate(self.SAT6_CLASSES)}
		self._class_to_idx = {value:key for key, value in self._idx_to_class.items()}
		self._rgb_band_indices = torch.tensor([self.SPECTRAL_BANDS.index(band) for band in self.RGB_BANDS])

		data_dir = self._get_path(root)
		if is_train_data:
			df = pd.read_csv(data_dir + '/X_train_sat6.csv', header=None)
			self.x_data = torch.tensor(df.values.reshape((324000, 28, 28, 4)), dtype=torch.float)
			self.x_data = torch.moveaxis(self.x_data, -1, 1)

			df = pd.read_csv(data_dir + '/y_train_sat6.csv', header=None)
			self.y_data = torch.argmax(torch.tensor(df.values), axis=1)
		else:
			df = pd.read_csv(data_dir + '/X_test_sat6.csv', header=None)
			self.x_data = torch.tensor(df.values.reshape((81000, 28, 28, 4)), dtype=torch.float)
			self.x_data = torch.moveaxis(self.x_data, -1, 1)

			df = pd.read_csv(data_dir + '/y_test_sat6.csv', header=None)
			self.y_data = torch.argmax(torch.tensor(df.values), axis=1)

		if include_additional_features == True and additional_features_list != None:
			self.external_features = []

			len_textural_features = len(self.TEXTURAL_FEATURES)
			all_features = np.array(self.ADDITIONAL_FEATURES)
			for i in range(len(self.x_data)):
				full_img = self.x_data[i]
				rgb_img = torch.index_select(full_img, dim = 0, index = self._rgb_band_indices)
				rgb_norm_img = ttf._normalize(rgb_img)
				gray_img = ttf._rgb_to_grayscale(rgb_norm_img)
				digitized_image = ttf._get_digitized_image(gray_img)

				features_row = []
				for ad_feature in additional_features_list:
					if self.user_features_callback != None and ad_feature in self.user_features_callback:
						features_row.append(self.user_features_callback[ad_feature](digitized_image))
					else:
						feature_index = np.where(all_features == ad_feature)[0]
						if len(feature_index) > 0:
							feature_index = feature_index[0]
							if feature_index < len_textural_features:
								features_row.append(self._feature_callbacks[feature_index](digitized_image))
							else:
								features_row.append(self._get_mean_spectral_index(full_img, ad_feature))
						else:
							raise InvalidParametersException("Callback not found for some user-defined feature: " + ad_feature)

				self.external_features.append(features_row)
			self.external_features = torch.tensor(self.external_features)

		else:
			self.external_features = None

	## This method returns the class labels as a dictionary of key-value pairs. Key-> class name, value-> class index
	def get_class_labels(self):
		return self._class_to_idx


	def __len__(self) -> int:
		return len(self.x_data)


	def __getitem__(self, index: int):
		img = self.x_data[index]
		img = torch.index_select(img, dim = 0, index = self.selected_band_indices)
		label = self.y_data[index]

		if self.transform is not None:
			img = self.transform(img)
		if self.target_transform is not None:
			label = self.target_transform(label)

		if self.external_features != None:
			return img, label, self.external_features[index]
		else:
			return img, label


	def _get_path(self, root_dir):
		queue = [root_dir]
		while queue:
			data_dir = queue.pop(0)
			folders = os.listdir(data_dir)
			if "X_train_sat6.csv" in folders and "y_train_sat6.csv" in folders and "X_test_sat6.csv" in folders  and "y_test_sat6.csv" in folders and "sat6annotations.csv" in folders:
				return data_dir

			for folder in folders:
				if os.path.isdir(data_dir + "/" + folder):
					queue.append(data_dir + "/" + folder)

		return None


	def _is_valid_bands(self, bands):
		for band in bands:
			if band not in self.SPECTRAL_BANDS:
				return False
		return True


	def _get_mean_spectral_index(self, full_img, feature_name):
		if feature_name == "mean_NDWI":
			band1 = full_img[self.BAND_GREEN_INDEX]
			band2 = full_img[self.BAND_NIR_INDEX]
			return si.get_mean_index(si.get_NDWI(band1, band2), self.IMAGE_HEIGHT, self.IMAGE_WIDTH)
		elif feature_name == "mean_NDVI":
			band1 = full_img[self.BAND_NIR_INDEX]
			band2 = full_img[self.BAND_RED_INDEX]
			return si.get_mean_index(si.get_NDVI(band1, band2), self.IMAGE_HEIGHT, self.IMAGE_WIDTH)
		elif feature_name == "mean_RVI":
			band1 = full_img[self.BAND_NIR_INDEX]
			band2 = full_img[self.BAND_RED_INDEX]
			return si.get_mean_index(si.get_RVI(band1, band2), self.IMAGE_HEIGHT, self.IMAGE_WIDTH)






