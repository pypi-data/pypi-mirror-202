from __future__ import division, print_function
import numpy as np
from voltage_imaging_analysis import voltage_imaging_analysis_fcts as voltage_imaging_fcts
import timeit
import tifffile
import scipy
import cv2
from matplotlib import pyplot as plt
import skimage

blocksize_x1x2 = 10
blocksize_x3 = 10

fname = r"H:/1p_data_for_tests/1p_field_stim_no_stim_2/1p_field_stim_no_stim_2_MMStack_Pos0.ome.tif"

print("Loading " + fname + "...")

data = tifffile.imread(fname)

data_downsampled = skimage.measure.block_reduce(data, block_size=(blocksize_x3, blocksize_x1x2, blocksize_x1x2), func=np.mean, cval=0, func_kwargs=None)

no_tiles = np.ceil(np.divide(np.array(data.shape), np.array(data_downsampled.shape))).astype(int)

# use R_pca to estimate the degraded data as L + S, where L is low rank, and S is sparse
rpca = voltage_imaging_fcts.R_pca(data_downsampled.reshape(data_downsampled.shape[0], -1))
L, S = rpca.fit(max_iter=10000, iter_print=100)

S = S.reshape(data_downsampled.shape[0], data_downsampled.shape[1], data_downsampled.shape[2])

# S = skimage.measure.block_reduce(S, block_size=(5, 1, 1), func=np.mean, cval=0, func_kwargs=None)

# gaussian filter sparse components
S = scipy.ndimage.gaussian_filter(S, (3,1,1), order=0)

# JEDI = negative indicator --> multiply dataset by -1 and renormalize
S = -1*S
S = np.divide(S - np.min(S), np.max(S) - np.min(S))

# in each frame, identify "blobs"
for frame_idx in np.arange(S.shape[0]):
        if np.mod(frame_idx, 10) == 0:
            blobs = skimage.feature.blob_log(S[frame_idx, :, :], min_sigma=1, max_sigma=3, threshold=.05)

            fig, ax = plt.subplots()
            ax.imshow(S[frame_idx, :, :])
            for blob in blobs:
                y, x, r = blob
                c = plt.Circle((x, y), r, color="red", linewidth=2, fill=False)
                ax.add_patch(c)
            plt.show()

#     ax[idx].set_axis_off()

# generate masks for original dataset based on the blob position

# from skimage.feature

# S = (2**16 - 1)*np.divide(S - np.min(S), np.max(S) - np.min(S))

# print(np.min(S))
# print(np.max(S))

# tifffile.imsave(r"C:/Users/photonics-voltage/Desktop/lowrank_test.tif", S.astype(np.uint16))

# all_resized_S = []

# for x in np.arange(S.shape[0]):
#     all_resized_S.append(voltage_imaging_fcts.tile_array(S[x, :, :], no_tiles[1], no_tiles[2]))

# all_resized_S = np.array(all_resized_S)

# # get rid of artefacts from "block_reduce"
# pix_to_crop = np.array(all_resized_S.shape) - np.array(data.shape) 

# all_resized_S = all_resized_S[:, :-pix_to_crop[1], :-pix_to_crop[2]]

# fig, ax = plt.subplots()
# ax.imshow(np.std(all_resized_S, axis=0))
# plt.show()

# fig, axs = plt.subplots(nrows=1, ncols=3)
# ax1, ax2, ax3 = axs
# ax1.imshow(data_downsampled.reshape(data_downsampled.shape[0], -1))
# ax2.imshow(L)
# ax3.imshow(S)
# plt.show()



# print(data_downsampled.shape)
# ax.plot(np.mean(data_downsampled, axis=(1,2)))
# plt.show()

# fig, ax = plt.subplots()
# ax.imshow(np.mean(data_downsampled, axis=0))
# plt.show()


# initial_timeseries = np.mean(data, axis=(1,2))
# initial_timeseries = initial_timeseries - np.mean(initial_timeseries)
# initial_timeseries = initial_timeseries - np.mean(initial_timeseries)

# spatial_img = np.mean(data, 0)
# data = data - np.expand_dims(spatial_img, 0)

# simple_corr = np.mean(np.expand_dims(np.expand_dims(initial_timeseries, axis=-1), axis=-1)*data, 0)

# fig, ax = plt.subplots()
# ax.imshow(simple_corr)
# plt.show()



# % correlate the changes in intensity with the applied voltage
# [ysize, xsize] = size(avgimg);

# dV2 = reshape(dV, 1, 1, L);
# dVmat = repmat(dV2, [ysize xsize 1]);
# corrimg = mean(dVmat.*imgs,3);
# corrimg = corrimg/mean(dV.^2);

# % calculate a dV estimate at each pixel, based on the linear regression.
# imgs2 = zeros(size(imgs));
# corrmat = repmat(corrimg, [1 1 L]);
# imgs2 = imgs./corrmat;
# clear corrmat

# % Look at the residuals to get a noise at each pixel
# sigmaimg = mean((imgs2 - dVmat).^2,3);

# weightimg = (1./sigmaimg);
# weightimg = weightimg/mean(weightimg(:));

# dVout = squeeze(mean(mean(imgs2.*repmat(weightimg, [1 1 L]))));

# Vout = dVout + avgV;
# offsetimg = avgimg - avgV*corrimg;


# global_average = np.mean(data, axis=(1,2))
# global_average = np.divide(global_average - np.min(global_average), np.max(global_average) - np.min(global_average))

# data = np.divide(data - np.min(data, axis=0), np.max(data, axis=0) - np.min(data, axis=0))

# # data = np.divide(data, np.expand_dims(np.expand_dims(global_average, -1), -1))

# fig, ax = plt.subplots()
# ax.plot(np.mean(data, axis=(1,2)))
# data = np.subtract(data, np.expand_dims(np.expand_dims(global_average, -1), -1))
# ax.plot(np.mean(data, axis=(1,2)))
# plt.show()

# # data = np.lib.pad(data, ((200, 200), (0,0), (0,0)), mode="constant", constant_values=(0,0))

# start_time = timeit.default_timer()
# print("init timeseries:")
# init_timeseries = compute_local_correlation_image(data)
# print(timeit.default_timer() - start_time)
# print()


# fig, ax = plt.subplots()
# ax.imshow(init_timeseries)
# plt.show()


# start_time = timeit.default_timer()
# print("idxs laser on:")
# all_idxs_laser_on, _ = voltage_imaging_fcts.find_idxs_laser_on(init_timeseries, laser_on_off_border_pix=5)
# print(timeit.default_timer() - start_time)
# print()

# start_time = timeit.default_timer()
# print("segmentation mask:")
# segmentation_mask = voltage_imaging_fcts.update_segmentation_mask(data)
# print(timeit.default_timer() - start_time)
# print()

# start_time = timeit.default_timer()
# print("ridge coefficients:")
# ridge_coefficients = voltage_imaging_fcts.generate_pixel_weights(data, init_timeseries, segmentation_mask)
# print(timeit.default_timer() - start_time)
# print()

# start_time = timeit.default_timer()
# print("upd timeseries:")
# upd_timeseries = np.divide(np.matmul(data.reshape(data.shape[0], -1), ridge_coefficients[1:]), np.sum(ridge_coefficients[1:]))
# print(timeit.default_timer() - start_time)
# print()
