from __future__ import division, print_function
import numpy as np
from voltage_imaging_analysis import voltage_imaging_analysis_fcts as voltage_imaging_fcts
import timeit
import tifffile
import scipy
import cv2
from matplotlib import pyplot as plt
import skimage
from numpy.lib.stride_tricks import as_strided

# # scipy ndimage convolve 26 s
# # cv2 convolve 14 s

# def compute_local_correlation_image(data, no_neighbours=48, to_whiten_data=True):

#     # if to_whiten_data is True:
#     #     whitened_data = whiten_data(data)
#     # else:
#     whitened_data = data

#     if no_neighbours==4:
#         sz = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]).astype(np.float32)

#     if no_neighbours==8:
#         sz = np.ones((3, 3)).astype(np.float32)
#         sz[1, 1] = 0

#     if no_neighbours==24:
#         sz = np.ones((5, 5)).astype(np.float32)
#         sz[2, 2] = 0

#     if no_neighbours==48:
#         sz = np.ones((7, 7)).astype(np.float32)
#         sz[3, 3] = 0
    
#     local_correlation_img = whitened_data.copy()

#     for idx, img in enumerate(local_correlation_img):
#         # local_correlation_img[idx] = scipy.ndimage.convolve(img,sz,origin=0)
#         local_correlation_img[idx] = cv2.filter2D(img,-1,sz)

#     #     # local_correlation_img[idx] = cv2.filter2D(img,-1,sz)
#     #     # local_correlation_img[idx] = scipy.signal.fftconvolve(img, sz, mode='same')
#     #     # local_correlation_img[idx] = np.fft.irfft2(np.fft.rfft2(img) * np.fft.rfft2(sz, img.shape))

#     # norm = scipy.ndimage.convolve(np.ones(whitened_data.shape[1:], dtype='float32'), sz, origin=0)
#     norm = cv2.filter2D(np.ones(whitened_data.shape[1:], dtype='float32'),-1,sz)

#     fig, ax = plt.subplots()
#     ax.imshow( np.divide(np.mean(local_correlation_img, axis=0), norm))
#     plt.show()


#     # # norm = scipy.signal.fftconvolve(np.ones(whitened_data.shape[1:], dtype='float32'), sz, mode='same')
#     # # norm =  np.fft.irfft2(np.fft.rfft2(np.ones(whitened_data.shape[1:], dtype='float32')) * np.fft.rfft2(sz, np.ones(whitened_data.shape[1:], dtype='float32').shape))

#     # local_correlation_img = np.divide(np.mean(local_correlation_img * whitened_data, axis=0), norm)

#     return #np.divide(local_correlation_img - np.min(local_correlation_img), np.max(local_correlation_img) - np.min(local_correlation_img))

# class R_pca:
#     """Class which implements R_pca to decompose matrix into low rank (L) and sparse (S) components.

#     Args:
#         D: array to be decomposed
#         mu: not sure
#         lmbda: not sure
    
#     Returns:
#         resized array a
    
#     Raises:

#     """

#     def __init__(self, D, mu=None, lmbda=None):
#         self.D = D
#         self.S = np.zeros(self.D.shape)
#         self.Y = np.zeros(self.D.shape)

#         if mu:
#             self.mu = mu
#         else:
#             self.mu = np.prod(self.D.shape) / (4 * np.linalg.norm(self.D, ord=1))

#         self.mu_inv = 1 / self.mu

#         if lmbda:
#             self.lmbda = lmbda
#         else:
#             self.lmbda = 1 / np.sqrt(np.max(self.D.shape))

#     @staticmethod
#     def frobenius_norm(M):
#         return np.linalg.norm(M, ord='fro')

#     @staticmethod
#     def shrink(M, tau):
#         return np.sign(M) * np.maximum((np.abs(M) - tau), np.zeros(M.shape))

#     def svd_threshold(self, M, tau):
#         U, S, V = np.linalg.svd(M, full_matrices=False)
#         return np.dot(U, np.dot(np.diag(self.shrink(S, tau)), V))

#     def fit(self, tol=None, max_iter=1000, iter_print=100):
#         iter = 0
#         err = np.Inf
#         Sk = self.S
#         Yk = self.Y
#         Lk = np.zeros(self.D.shape)

#         if tol:
#             _tol = tol
#         else:
#             _tol = 1E-7 * self.frobenius_norm(self.D)

#         #this loop implements the principal component pursuit (PCP) algorithm
#         #located in the table on page 29 of https://arxiv.org/pdf/0912.3599.pdf
#         while (err > _tol) and iter < max_iter:
#             Lk = self.svd_threshold(
#                 self.D - Sk + self.mu_inv * Yk, self.mu_inv)                            #this line implements step 3
#             Sk = self.shrink(
#                 self.D - Lk + (self.mu_inv * Yk), self.mu_inv * self.lmbda)             #this line implements step 4
#             Yk = Yk + self.mu * (self.D - Lk - Sk)                                      #this line implements step 5
#             err = self.frobenius_norm(self.D - Lk - Sk)
#             iter += 1
#             if (iter % iter_print) == 0 or iter == 1 or iter > max_iter or err <= _tol:
#                 print('iteration: {0}, error: {1}'.format(iter, err))

#         self.L = Lk
#         self.S = Sk
#         return Lk, Sk

def tile_array(a, b0, b1):
    """Resize array using nearest neighbour interpolation.

    Args:
        a: array to be resized
        b0: number of tiles in x1 direction
        b1: number of tiles in x2 direction
    
    Returns:
        resized array a
    
    Raises:

    """

    r, c = a.shape                                    
    rs, cs = a.strides                                
    x = as_strided(a, (r, b0, c, b1), (rs, 0, cs, 0)) 
    return x.reshape(r*b0, c*b1)                      

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
#     all_resized_S.append(tile_array(S[x, :, :], no_tiles[1], no_tiles[2]))

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
